#![allow(clippy::cast_sign_loss, reason = "commonly needed for varint encoding")]
#![allow(
    clippy::cast_lossless,
    reason = "allows consistent code between signed and unsigned varint"
)]
#![allow(
    clippy::cast_possible_truncation,
    reason = "truncation is expected by protobuf spec"
)]

use std::{collections::HashMap, sync::Arc};

use buffa::encoding::{decode_varint, encode_varint, varint_len};
use bytes::{Buf as _, Bytes, BytesMut, TryGetError};
use pyo3::{
    Bound, IntoPyObjectExt as _, Py, PyAny, PyErr, PyResult, Python,
    exceptions::{PyRecursionError, PyValueError},
    types::{
        PyAnyMethods as _, PyBool, PyBytes, PyDict, PyFloat, PyInt, PyList, PyListMethods as _,
        PyString, PyType,
    },
};

use crate::{
    attribute_access::AttributeAccess,
    constants::Constants,
    descriptor::{
        DescEnum, DescField, DescFieldValue, DescMessage, DescSingleValue, FieldPresence,
        ScalarType, WireType,
    },
    nativemessage::NativeMessage,
    oneof::Oneof,
};

const DEPTH_LIMIT: usize = 100;

#[derive(Clone, Copy)]
pub(crate) struct FromBinaryOpts {
    /// Whether unknown fields/enum values should be dropped while parsing.
    pub(crate) ignore_unknown_fields: bool,
}

/// Parsed result for a single field value.
enum SingleValue<'py> {
    /// Parsed value that can be assigned to the message.
    Parsed(Bound<'py, PyAny>),
    /// Closed-enum numeric value that has no known enum variant.
    UnknownEnumValue(i32),
}

/// Parser-local value metadata needed for decoding field payloads.
enum FieldParserValue {
    /// Scalar value decoding info.
    Scalar(ScalarType),
    /// Nested message parser handle.
    Message {
        /// Message descriptor handle.
        message: DescMessage,
        /// Whether this value uses deprecated group wire encoding.
        delimited_encoding: bool,
    },
    /// Enum lookup/type info.
    Enum(DescEnum),
}

impl FieldParserValue {
    /// Converts descriptor single-value metadata into parser-local metadata.
    fn from_desc_single(value: &DescSingleValue) -> Self {
        match value {
            DescSingleValue::Scalar(scalar_type) => Self::Scalar(*scalar_type),
            DescSingleValue::Message {
                message,
                delimited_encoding,
            } => Self::Message {
                message: message.clone(),
                delimited_encoding: *delimited_encoding,
            },
            DescSingleValue::Enum(enum_) => Self::Enum(enum_.clone()),
        }
    }

    /// Returns the wire type expected for this value kind.
    fn wire_type(&self) -> WireType {
        match self {
            Self::Scalar(scalar_type) => scalar_type.wire_type(),
            Self::Message {
                delimited_encoding: false,
                ..
            } => WireType::LengthDelimited,
            Self::Message {
                delimited_encoding: true,
                ..
            } => WireType::StartGroup,
            Self::Enum(_) => WireType::Varint,
        }
    }
}

/// Per-field parsing mode and precomputed routing state.
enum ParserFieldType {
    Singular {
        /// Accessor for the oneof attribute on the message, if the field is in a oneof.
        oneof_attr: Option<AttributeAccess>,
        /// Whether the field requires explicit presence tracking.
        requires_presence: bool,
    },
    List {
        unpacked_wire_type: WireType,
        packable: bool,
    },
    Map {
        key_type: ScalarType,
        value_parser: Box<FieldParser>,
        key_default_value: Py<PyAny>,
        value_default_value: Py<PyAny>,
    },
}

impl ParserFieldType {
    /// Builds field parsing mode/state from descriptor metadata.
    fn new(
        py: Python<'_>,
        field: &DescField,
        python_type: &Bound<'_, PyType>,
        constants: &Constants,
    ) -> Self {
        match &field.value {
            DescFieldValue::Scalar { .. }
            | DescFieldValue::Message { .. }
            | DescFieldValue::Enum { .. } => {
                let oneof_attr = field
                    .value
                    .oneof_name()
                    .map(|name| AttributeAccess::new(py, python_type, name.bind(py)));
                let requires_presence =
                    oneof_attr.is_none() && !matches!(field.presence, FieldPresence::Implicit);
                ParserFieldType::Singular {
                    oneof_attr,
                    requires_presence,
                }
            }
            DescFieldValue::List { element, .. } => {
                let element_value = FieldParserValue::from_desc_single(element);
                let unpacked_wire_type = element_value.wire_type();
                let packable = !matches!(
                    element_value,
                    FieldParserValue::Message { .. }
                        | FieldParserValue::Scalar(ScalarType::Bytes | ScalarType::String)
                );
                ParserFieldType::List {
                    unpacked_wire_type,
                    packable,
                }
            }
            DescFieldValue::Map { key_type, value } => {
                let key_default_value = key_type.zero_value(py);
                let value_parser_value = FieldParserValue::from_desc_single(value);
                let value_wire_type = value_parser_value.wire_type();
                let value_default_value = match &value_parser_value {
                    FieldParserValue::Scalar(scalar_type) => scalar_type.zero_value(py),
                    FieldParserValue::Message { .. } => py.None(),
                    FieldParserValue::Enum(enum_) => enum_.zero_value.clone_ref(py),
                };
                let value_parser = Box::new(FieldParser {
                    type_: ParserFieldType::Singular {
                        oneof_attr: None,
                        requires_presence: false,
                    },
                    value: value_parser_value,
                    wire_type: value_wire_type,

                    // unused for map value parsing but being singletons, there isn't much overhead
                    // and it simplifies the logic for map value parsing a lot.
                    number: 2,
                    local_name_py: constants.value.clone_ref(py),
                    local_name: constants.value.extract::<String>(py).unwrap_or_default(),
                    attr: AttributeAccess::Name(constants.value.clone_ref(py)),
                });
                ParserFieldType::Map {
                    key_type: *key_type,
                    value_parser,
                    key_default_value,
                    value_default_value,
                }
            }
        }
    }
}

/// Parser for a single field in a message.
pub(crate) struct FieldParser {
    number: u32,
    local_name_py: Py<PyString>,
    local_name: String,
    attr: AttributeAccess,
    type_: ParserFieldType,
    /// Information for parsing the field value. For lists, this is the list element and for maps, the map value.
    value: FieldParserValue,
    wire_type: WireType,
}

impl FieldParser {
    /// Constructs a field parser from a normalized descriptor field.
    fn new(
        py: Python<'_>,
        field: &DescField,
        python_type: &Bound<'_, PyType>,
        constants: &Constants,
    ) -> Self {
        let field_element = match &field.value {
            DescFieldValue::Scalar { scalar_type, .. } => FieldParserValue::Scalar(*scalar_type),
            DescFieldValue::Message {
                message,
                delimited_encoding,
                ..
            } => FieldParserValue::Message {
                message: message.clone(),
                delimited_encoding: *delimited_encoding,
            },
            DescFieldValue::Enum { enum_, .. } => FieldParserValue::Enum(enum_.clone()),
            DescFieldValue::List { element, .. } => FieldParserValue::from_desc_single(element),
            DescFieldValue::Map { value, .. } => FieldParserValue::from_desc_single(value),
        };
        Self {
            number: field.number,
            local_name_py: field.local_name.clone_ref(py),
            local_name: field.local_name.extract::<String>(py).unwrap_or_default(),
            attr: AttributeAccess::new(py, python_type, field.local_name.bind(py)),
            type_: ParserFieldType::new(py, field, python_type, constants),
            value: field_element,
            wire_type: field.wire_type,
        }
    }

    /// Reads one field occurrence from the wire buffer into the target message.
    fn read_field<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
        tag: u32,
        wire_type: WireType,
        buffer: &mut Bytes,
        opts: FromBinaryOpts,
        depth: usize,
    ) -> PyResult<()> {
        match &self.type_ {
            ParserFieldType::Singular {
                oneof_attr,
                requires_presence,
            } => self.read_singular_field(
                py,
                message,
                tag,
                wire_type,
                buffer,
                opts,
                depth,
                oneof_attr.as_ref(),
                *requires_presence,
            )?,
            ParserFieldType::List {
                unpacked_wire_type,
                packable,
            } => self.read_list_field(
                py,
                message,
                tag,
                wire_type,
                buffer,
                opts,
                depth,
                *unpacked_wire_type,
                *packable,
            )?,
            ParserFieldType::Map {
                key_type,
                value_parser,
                key_default_value,
                value_default_value,
            } => self.read_map_field(
                py,
                message,
                tag,
                buffer,
                opts,
                depth,
                *key_type,
                value_parser,
                key_default_value,
                value_default_value,
            )?,
        }

        Ok(())
    }

    fn read_singular_field<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
        tag: u32,
        wire_type: WireType,
        buffer: &mut Bytes,
        opts: FromBinaryOpts,
        depth: usize,
        oneof_attr: Option<&AttributeAccess>,
        requires_presence: bool,
    ) -> PyResult<()> {
        let value =
            self.read_single_value(py, tag, wire_type, Some(message), buffer, opts, depth)?;
        match value {
            SingleValue::Parsed(value) => {
                if let Some(oneof_attr) = oneof_attr {
                    let oneof =
                        Oneof::new(self.local_name_py.bind(py), &value).into_bound_py_any(py)?;
                    oneof_attr.set(message, &oneof)?;
                } else {
                    self.attr.set(message, &value)?;
                    if requires_presence {
                        message.get().add_present_field(self.number);
                    }
                }
            }
            SingleValue::UnknownEnumValue(number) => {
                if !opts.ignore_unknown_fields {
                    let mut field = BytesMut::new();
                    encode_varint(tag as u64, &mut field);
                    encode_varint(number as u64, &mut field);
                    write_unknown_field(py, message, tag >> 3, &field)?;
                }
            }
        }
        Ok(())
    }

    fn read_list_field<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
        tag: u32,
        wire_type: WireType,
        buffer: &mut Bytes,
        opts: FromBinaryOpts,
        depth: usize,
        unpacked_wire_type: WireType,
        packable: bool,
    ) -> PyResult<()> {
        let python_list = self.attr.get(py, message)?;
        let list = python_list.cast::<PyList>()?;
        if wire_type == WireType::LengthDelimited && packable {
            let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
            check_buffer_remaining(buffer, len)?;
            let mut list_buffer = buffer.split_to(len);
            while list_buffer.has_remaining() {
                let value = self.read_single_value(
                    py,
                    tag,
                    wire_type,
                    None,
                    &mut list_buffer,
                    opts,
                    depth,
                )?;
                match value {
                    SingleValue::Parsed(value) => list.append(value)?,
                    SingleValue::UnknownEnumValue(number) => {
                        if !opts.ignore_unknown_fields {
                            // Always add unknown values as unpacked.
                            let mut field = BytesMut::new();
                            let tag = (tag & !0b111) | (unpacked_wire_type as u32);
                            encode_varint(tag as u64, &mut field);
                            encode_varint(number as u64, &mut field);
                            write_unknown_field(py, message, tag >> 3, &field)?;
                        }
                    }
                }
            }
        } else {
            let value = self.read_single_value(py, tag, wire_type, None, buffer, opts, depth)?;
            match value {
                SingleValue::Parsed(value) => list.append(value)?,
                SingleValue::UnknownEnumValue(number) => {
                    if !opts.ignore_unknown_fields {
                        let mut field = BytesMut::new();
                        encode_varint(tag as u64, &mut field);
                        encode_varint(number as u64, &mut field);
                        write_unknown_field(py, message, tag >> 3, &field)?;
                    }
                }
            }
        }
        Ok(())
    }

    fn read_map_field<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
        entry_tag: u32,
        buffer: &mut Bytes,
        opts: FromBinaryOpts,
        depth: usize,
        key_type: ScalarType,
        value_parser: &FieldParser,
        key_default_value: &Py<PyAny>,
        value_default_value: &Py<PyAny>,
    ) -> PyResult<()> {
        let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
        check_buffer_remaining(buffer, len)?;
        let mut entry_buffer = buffer.split_to(len);
        let entry_checkpoint = entry_buffer.clone();
        let mut key = None;
        let mut value = None;

        while entry_buffer.has_remaining() {
            let tag = decode_tag(&mut entry_buffer)?;
            let field_number = tag >> 3;
            let wire_type = WireType::from_tag(tag)?;
            match field_number {
                1 => {
                    if key_type.wire_type() != wire_type {
                        return Self::read_unknown_map_entry(
                            py,
                            message,
                            entry_tag,
                            &entry_checkpoint,
                            opts,
                        );
                    }
                    key = Some(read_scalar(py, key_type, &mut entry_buffer)?);
                }
                2 => {
                    if value_parser.wire_type != wire_type {
                        return Self::read_unknown_map_entry(
                            py,
                            message,
                            entry_tag,
                            &entry_checkpoint,
                            opts,
                        );
                    }
                    value = Some(value_parser.read_single_value(
                        py,
                        tag,
                        wire_type,
                        None,
                        &mut entry_buffer,
                        opts,
                        depth,
                    )?);
                }
                _ => {
                    skip_field(tag, &mut entry_buffer, depth + 1)?;
                }
            }
        }

        let key = key.unwrap_or_else(|| key_default_value.bind(py).clone());
        let value = if let Some(value) = value {
            value
        } else if let FieldParserValue::Message { message, .. } = &value_parser.value {
            // For message values, the default is a new instance of the message, not None.
            SingleValue::Parsed(message.get_python_type(py).call0()?)
        } else {
            SingleValue::Parsed(value_default_value.bind(py).clone())
        };
        let SingleValue::Parsed(value) = value else {
            // Unknown value (i.e., unknown closed enum value), whole entry is an unknown field.
            return Self::read_unknown_map_entry(py, message, entry_tag, &entry_checkpoint, opts);
        };
        let python_dict = self.attr.get(py, message)?;
        let dict = python_dict.cast::<PyDict>()?;
        dict.set_item(key, value)?;
        Ok(())
    }

    fn read_unknown_map_entry(
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        tag: u32,
        entry_bytes: &[u8],
        opts: FromBinaryOpts,
    ) -> PyResult<()> {
        if !opts.ignore_unknown_fields {
            let mut field_bytes = BytesMut::new();
            encode_varint(tag as u64, &mut field_bytes);
            encode_varint(entry_bytes.len() as u64, &mut field_bytes);
            field_bytes.extend_from_slice(entry_bytes);
            write_unknown_field(py, message, tag >> 3, &field_bytes)?;
        }
        Ok(())
    }

    /// Reads just the field value bytes for this field.
    fn read_single_value<'py>(
        &self,
        py: Python<'py>,
        tag: u32,
        wire_type: WireType,
        message: Option<&Bound<'py, NativeMessage>>,
        buffer: &mut Bytes,
        opts: FromBinaryOpts,
        depth: usize,
    ) -> PyResult<SingleValue<'py>> {
        let value = match &self.value {
            FieldParserValue::Scalar(scalar_type) => read_scalar(py, *scalar_type, buffer)?,
            FieldParserValue::Message {
                message: message_desc,
                ..
            } => {
                let mut message_buffer = if wire_type == WireType::LengthDelimited {
                    let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
                    check_buffer_remaining(buffer, len)?;
                    buffer.split_to(len)
                } else {
                    let mut checkpoint = buffer.clone();
                    consume_group(tag, buffer)?;
                    let end_tag = (tag & !0b111) | (WireType::EndGroup as u32);
                    let field_len = checkpoint.len() - buffer.len() - varint_len(end_tag as u64);
                    checkpoint.split_to(field_len)
                };
                let marshaler = message_desc.get_marshaler(py)?;
                let parser = &marshaler.parser;
                let existing = if let Some(message) = message {
                    self.get_field_value(py, message)?
                } else {
                    None
                };
                let message_instance = if let Some(existing) = existing
                    && !existing.is_none()
                {
                    existing.cast_into::<NativeMessage>()?
                } else {
                    marshaler.new_empty_message(py, parser.inner.python_type.bind(py))?
                };
                parser.merge_from_binary(
                    py,
                    &message_instance,
                    &mut message_buffer,
                    opts,
                    depth + 1,
                )?;
                message_instance.into_any()
            }
            FieldParserValue::Enum(enum_) => {
                let number = decode_varint(buffer).map_err(map_varint_err)? as i32;
                let value = enum_.values.get(&number);
                if let Some(value) = value {
                    value.bind(py).clone()
                } else if enum_.open {
                    enum_.py_type.bind(py).call1((number,))?
                } else {
                    return Ok(SingleValue::UnknownEnumValue(number));
                }
            }
        };
        Ok(SingleValue::Parsed(value))
    }

    fn wire_type_matches(&self, wire_type: WireType) -> bool {
        if self.wire_type == wire_type {
            return true;
        }
        if let ParserFieldType::List {
            unpacked_wire_type,
            packable,
        } = &self.type_
        {
            if *unpacked_wire_type == wire_type {
                return true;
            }
            if *packable && wire_type == WireType::LengthDelimited {
                return true;
            }
        }
        false
    }

    /// Returns the current value for a field, including oneof slot handling.
    fn get_field_value<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
    ) -> PyResult<Option<Bound<'py, PyAny>>> {
        if let ParserFieldType::Singular {
            oneof_attr: Some(oneof_access),
            requires_presence: _,
        } = &self.type_
        {
            let value = oneof_access.get(py, message)?;
            let Ok(oneof) = value.cast::<Oneof>() else {
                return Ok(None);
            };
            let oneof = oneof.get();

            return if oneof.field.bind(py).extract::<&str>()? == self.local_name {
                Ok(Some(oneof.value.bind(py).clone()))
            } else {
                Ok(None)
            };
        }

        Ok(Some(self.attr.get(py, message)?))
    }
}

/// Shared parser state reused across parser clones.
struct MessageParserInner {
    fields: ParserTable,
    python_type: Py<PyType>,
}

#[derive(Clone)]
/// Entry-point parser for a concrete Python message type.
pub(crate) struct MessageParser {
    inner: Arc<MessageParserInner>,
}

impl MessageParser {
    /// Creates a message parser from descriptor fields.
    pub(crate) fn new(
        py: Python<'_>,
        fields: &Vec<DescField>,
        python_type: &Bound<'_, PyType>,
        constants: &Constants,
    ) -> Self {
        MessageParser {
            inner: Arc::new(MessageParserInner {
                fields: ParserTable::new(py, fields, python_type, constants),
                python_type: python_type.clone().unbind(),
            }),
        }
    }

    /// Merges wire data into an existing Python message instance.
    pub(crate) fn merge_from_binary<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
        buffer: &mut Bytes,
        opts: FromBinaryOpts,
        depth: usize,
    ) -> PyResult<()> {
        check_parse_recursion_depth(depth)?;
        while buffer.has_remaining() {
            let checkpoint = buffer.clone();
            let tag = decode_tag(buffer)?;
            let field_number = tag >> 3;
            if field_number == 0 {
                return Err(PyValueError::new_err("invalid field number: 0"));
            }
            let wire_type = WireType::from_tag(tag)?;
            if let Some(field) = self.inner.fields.get(field_number)
                && field.wire_type_matches(wire_type)
            {
                field.read_field(py, message, tag, wire_type, buffer, opts, depth)?;
            } else {
                skip_field_with_wire_type(field_number, wire_type, buffer, depth + 1)?;
                if !opts.ignore_unknown_fields {
                    let field_len = checkpoint.len() - buffer.len();
                    write_unknown_field(py, message, field_number, &checkpoint[..field_len])?;
                }
            }
        }
        Ok(())
    }
}

/// Reads a scalar value from the wire buffer.
fn read_scalar<'py>(
    py: Python<'py>,
    s: ScalarType,
    buffer: &mut Bytes,
) -> PyResult<Bound<'py, PyAny>> {
    let res = match s {
        ScalarType::Double => {
            PyFloat::new(py, buffer.try_get_f64_le().map_err(map_try_get_err)?).into_any()
        }
        ScalarType::Float => PyFloat::new(
            py,
            f64::from(buffer.try_get_f32_le().map_err(map_try_get_err)?),
        )
        .into_any(),
        ScalarType::Int64 => {
            let value = decode_varint(buffer).map_err(map_varint_err)?;
            PyInt::new(py, value.cast_signed()).into_any()
        }
        ScalarType::Uint64 => {
            PyInt::new(py, decode_varint(buffer).map_err(map_varint_err)?).into_any()
        }
        ScalarType::Int32 => {
            let value = decode_varint(buffer).map_err(map_varint_err)?;
            PyInt::new(py, value as i32).into_any()
        }
        ScalarType::Fixed64 => {
            PyInt::new(py, buffer.try_get_u64_le().map_err(map_try_get_err)?).into_any()
        }
        ScalarType::Fixed32 => {
            PyInt::new(py, buffer.try_get_u32_le().map_err(map_try_get_err)?).into_any()
        }
        ScalarType::Bool => {
            let value = decode_varint(buffer).map_err(map_varint_err)?;
            PyBool::new(py, value > 0).into_bound_py_any(py)?
        }
        ScalarType::String => {
            let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
            check_buffer_remaining(buffer, len)?;
            let bytes = buffer.split_to(len);
            PyString::from_bytes(py, &bytes)?.into_any()
        }
        ScalarType::Bytes => {
            let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
            check_buffer_remaining(buffer, len)?;
            let bytes = buffer.split_to(len);
            PyBytes::new(py, &bytes).into_any()
        }
        ScalarType::Uint32 => {
            PyInt::new(py, decode_varint(buffer).map_err(map_varint_err)? as u32).into_any()
        }
        ScalarType::Sfixed32 => {
            PyInt::new(py, buffer.try_get_i32_le().map_err(map_try_get_err)?).into_any()
        }
        ScalarType::Sfixed64 => {
            PyInt::new(py, buffer.try_get_i64_le().map_err(map_try_get_err)?).into_any()
        }
        ScalarType::Sint32 => {
            let value = decode_varint(buffer).map_err(map_varint_err)? as u32;
            PyInt::new(py, decode_zigzag32(value)).into_any()
        }
        ScalarType::Sint64 => {
            let value = decode_varint(buffer).map_err(map_varint_err)? as u64;
            PyInt::new(py, decode_zigzag64(value)).into_any()
        }
    };
    Ok(res)
}

/// Converts invalid varint-like decode failures into Python errors.
fn map_varint_err<E>(_: E) -> PyErr {
    PyValueError::new_err("invalid varint")
}

/// Raises if parsing a nested message exceeds the shared recursion limit.
fn check_parse_recursion_depth(depth: usize) -> PyResult<()> {
    if depth > DEPTH_LIMIT {
        return Err(PyRecursionError::new_err(format!(
            "exceeded maximum recursion depth {DEPTH_LIMIT} while parsing message"
        )));
    }
    Ok(())
}

/// Raises if skipping a nested unknown field exceeds the shared recursion limit.
fn check_skip_recursion_depth(depth: usize, field_number: u32) -> PyResult<()> {
    if depth > DEPTH_LIMIT {
        return Err(PyRecursionError::new_err(format!(
            "exceeded maximum recursion depth {DEPTH_LIMIT} while skipping field {field_number}"
        )));
    }
    Ok(())
}

/// Converts buffer underflow errors into Python errors.
#[allow(clippy::needless_pass_by_value, reason = "makes caller code cleaner")]
fn map_try_get_err(err: TryGetError) -> PyErr {
    PyValueError::new_err(format!(
        "unexpected end of buffer: needed {} bytes but only {} available",
        err.requested, err.available
    ))
}

/// Ensures the buffer contains at least `needed` bytes.
fn check_buffer_remaining(buffer: &Bytes, needed: usize) -> PyResult<()> {
    if buffer.remaining() < needed {
        Err(PyValueError::new_err(format!(
            "unexpected end of buffer: needed {} bytes but only {} available",
            needed,
            buffer.remaining()
        )))
    } else {
        Ok(())
    }
}

/// Consumes a group field without recursion so its payload can be parsed as a nested message.
fn consume_group(tag: u32, buffer: &mut Bytes) -> PyResult<()> {
    let mut groups = vec![tag >> 3];
    while buffer.has_remaining() {
        let tag = decode_tag(buffer)?;
        let field_number = tag >> 3;
        let wire_type = WireType::from_tag(tag)?;
        match wire_type {
            WireType::StartGroup => groups.push(field_number),
            WireType::EndGroup => {
                let expected = groups.last().copied().ok_or_else(|| {
                    PyValueError::new_err(format!(
                        "unexpected end group tag outside of group for field {field_number}",
                    ))
                })?;
                if field_number != expected {
                    return Err(PyValueError::new_err(format!(
                        "mismatched group end tag: expected {expected}, got {field_number}",
                    )));
                }
                groups.pop();
                if groups.is_empty() {
                    return Ok(());
                }
            }
            WireType::Varint => {
                decode_varint(buffer).map_err(map_varint_err)?;
            }
            WireType::Bit64 => {
                check_buffer_remaining(buffer, 8)?;
                buffer.advance(8);
            }
            WireType::LengthDelimited => {
                let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
                check_buffer_remaining(buffer, len)?;
                buffer.advance(len);
            }
            WireType::Bit32 => {
                check_buffer_remaining(buffer, 4)?;
                buffer.advance(4);
            }
        }
    }
    Err(PyValueError::new_err("unterminated group"))
}

/// Writes raw field bytes to the message unknown-field store.
fn write_unknown_field(
    py: Python<'_>,
    message: &Bound<'_, NativeMessage>,
    field_number: u32,
    field_bytes: &[u8],
) -> PyResult<()> {
    let unknown_fields_unbound = message.get().get_or_init_unknown_fields(py);
    let unknown_fields = unknown_fields_unbound.bind(py);
    let field_list = if let Ok(list) = unknown_fields.get_item(field_number) {
        list.cast::<PyList>()?.clone()
    } else {
        let new_list = PyList::empty(py);
        unknown_fields.set_item(field_number, &new_list)?;
        new_list
    };
    field_list.append(PyBytes::new(py, field_bytes))?;
    Ok(())
}

/// Skips a wire field by decoding the wire type from its tag.
fn skip_field(tag: u32, buffer: &mut Bytes, depth: usize) -> PyResult<()> {
    let field_number = tag >> 3;
    let wire_type = WireType::from_tag(tag)?;
    skip_field_with_wire_type(field_number, wire_type, buffer, depth)
}

/// Skips one field payload for a known wire type.
fn skip_field_with_wire_type(
    field_number: u32,
    wire_type: WireType,
    buffer: &mut Bytes,
    depth: usize,
) -> PyResult<()> {
    check_skip_recursion_depth(depth, field_number)?;
    match wire_type {
        WireType::Varint => {
            decode_varint(buffer).map_err(map_varint_err)?;
        }
        WireType::Bit64 => {
            check_buffer_remaining(buffer, 8)?;
            buffer.advance(8);
        }
        WireType::LengthDelimited => {
            let len = decode_varint(buffer).map_err(map_varint_err)? as usize;
            check_buffer_remaining(buffer, len)?;
            buffer.advance(len);
        }
        WireType::StartGroup => {
            while buffer.has_remaining() {
                let tag = decode_tag(buffer)?;
                let inner_field_number = tag >> 3;
                let inner_wire_type = WireType::from_tag(tag)?;
                if inner_wire_type == WireType::EndGroup {
                    if inner_field_number == field_number {
                        return Ok(());
                    }
                    return Err(PyValueError::new_err(format!(
                        "mismatched group end tag: expected {inner_field_number}, got {field_number}",
                    )));
                }
                let nested_depth = if inner_wire_type == WireType::StartGroup {
                    depth + 1
                } else {
                    depth
                };
                skip_field(tag, buffer, nested_depth)?;
            }
            return Err(PyValueError::new_err("Unterminated group in unknown field"));
        }
        WireType::EndGroup => {
            return Err(PyValueError::new_err(format!(
                "Unexpected end group tag for field {field_number}",
            )));
        }
        WireType::Bit32 => {
            check_buffer_remaining(buffer, 4)?;
            buffer.advance(4);
        }
    }
    Ok(())
}

/// Decodes protobuf zig-zag 32-bit integer encoding.
const fn decode_zigzag32(value: u32) -> i32 {
    ((value >> 1).cast_signed()) ^ (-((value & 1).cast_signed()))
}

/// Decodes protobuf zig-zag 64-bit integer encoding.
const fn decode_zigzag64(value: u64) -> i64 {
    ((value >> 1).cast_signed()) ^ (-((value & 1).cast_signed()))
}

fn decode_tag(buffer: &mut Bytes) -> PyResult<u32> {
    let tag = decode_varint(&mut buffer.take(5)).map_err(map_varint_err)?;
    u32::try_from(tag).map_err(map_varint_err)
}

/// A lookup table for field parsers. Most messages are small or contiguous, and we can significantly
/// optimize lookup for them by specializing the table.
enum ParserTable {
    /// Dense table keyed by field number for compact/contiguous schemas.
    Array(Box<[Option<FieldParser>]>),
    /// Sparse map keyed by field number for non-contiguous schemas.
    HashMap(HashMap<u32, FieldParser>),
}

impl ParserTable {
    /// Builds the most efficient parser table representation for the schema.
    fn new(
        py: Python<'_>,
        fields: &Vec<DescField>,
        python_type: &Bound<'_, PyType>,
        constants: &Constants,
    ) -> Self {
        let mut field_numbers = fields.iter().map(|f| f.number).collect::<Vec<_>>();
        field_numbers.sort_unstable();
        let max_field_number = field_numbers.last().copied().unwrap_or(0);
        let use_array = if max_field_number <= 16 {
            true
        } else {
            let array_len = (max_field_number + 1) as usize;
            let used = fields.len();
            // Require at least 80% occupancy in the backing array.
            used * 5 >= array_len * 4
        };
        if use_array {
            let mut array = Vec::with_capacity((max_field_number + 1) as usize);
            array.resize_with((max_field_number + 1) as usize, || None);
            for field in fields {
                let number = field.number as usize;
                array[number] = Some(FieldParser::new(py, field, python_type, constants));
            }
            ParserTable::Array(array.into_boxed_slice())
        } else {
            let mut map = HashMap::with_capacity(fields.len());
            for field in fields {
                map.insert(
                    field.number,
                    FieldParser::new(py, field, python_type, constants),
                );
            }
            ParserTable::HashMap(map)
        }
    }

    /// Looks up a parser by field number.
    fn get(&self, field_number: u32) -> Option<&FieldParser> {
        match self {
            ParserTable::Array(array) => {
                let index = field_number as usize;
                if index >= array.len() {
                    None
                } else {
                    array[index].as_ref()
                }
            }
            ParserTable::HashMap(map) => map.get(&field_number),
        }
    }
}
