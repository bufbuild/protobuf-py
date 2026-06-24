#![allow(clippy::cast_sign_loss, reason = "commonly needed for varint encoding")]
#![allow(
    clippy::cast_lossless,
    reason = "allows consistent code between signed and unsigned varint"
)]
#![allow(
    clippy::cast_possible_truncation,
    reason = "truncation is expected by protobuf spec"
)]

use std::sync::Arc;

use pyo3::{
    Bound, Py, PyAny, PyErr, PyResult, Python,
    exceptions::{PyOverflowError, PyTypeError, PyValueError},
    types::{
        PyAnyMethods as _, PyBool, PyBytes, PyBytesMethods as _, PyDict, PyDictMethods as _,
        PyFloat, PyInt, PyList, PyListMethods as _, PyString, PyStringMethods as _, PyType,
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
    reverse_buffer::ReverseBuffer,
};

#[derive(Clone, Copy)]
pub(crate) struct ToBinaryOpts {
    /// Whether to include unknown fields when writing wire bytes.
    pub(crate) write_unknown_fields: bool,
}

/// Per-field serialization mode and container-specific state.
enum FieldSerializerType {
    /// Singular scalar/message/enum field.
    Singular,
    /// Repeated list field.
    List {
        /// Whether repeated values are encoded using packed wire format.
        packed: bool,
    },
    /// Map field encoded as repeated entry messages.
    Map {
        /// Serializer for map-entry key (field number 1).
        key_serializer: Box<FieldSerializer>,
        /// Serializer for map-entry value (field number 2).
        value_serializer: Box<FieldSerializer>,
    },
}

impl FieldSerializerType {
    /// Builds serializer mode/state from descriptor field value metadata.
    fn new(value_type: &DescFieldValue) -> Self {
        match value_type {
            DescFieldValue::Scalar { .. }
            | DescFieldValue::Message { .. }
            | DescFieldValue::Enum { .. } => Self::Singular,
            DescFieldValue::List { packed, .. } => Self::List { packed: *packed },
            DescFieldValue::Map { key_type, value } => {
                // Key has field number 1
                let key_tag = (1 << 3) | (key_type.wire_type() as u32);
                let key_marshaler = FieldSerializer {
                    tag: key_tag,
                    type_: FieldSerializerType::Singular,
                    value: FieldSerializerValue::Scalar(*key_type),
                };

                let value_wire_type = match value {
                    DescSingleValue::Scalar(scalar_type) => scalar_type.wire_type(),
                    DescSingleValue::Message { .. } => WireType::LengthDelimited,
                    DescSingleValue::Enum(_) => WireType::Varint,
                };

                // Value has field number 2
                let value_tag = (2 << 3) | (value_wire_type as u32);
                let value_end_tag = if value_wire_type == WireType::StartGroup {
                    Some((2 << 3) | (WireType::EndGroup as u32))
                } else {
                    None
                };
                let value_marshaler = FieldSerializer {
                    tag: value_tag,
                    type_: FieldSerializerType::Singular,
                    value: FieldSerializerValue::from_desc_single(value, value_end_tag),
                };
                Self::Map {
                    key_serializer: Box::from(key_marshaler),
                    value_serializer: Box::from(value_marshaler),
                }
            }
        }
    }
}

/// Serializer-local value metadata needed to write field payloads.
enum FieldSerializerValue {
    /// Scalar encoding info.
    Scalar(ScalarType),
    /// Enum validation metadata.
    Enum(DescEnum),
    /// Nested message serializer and optional group end tag.
    Message {
        message: DescMessage,
        end_tag: Option<u32>,
    },
}

impl FieldSerializerValue {
    /// Converts descriptor single-value metadata into serializer-local metadata.
    fn from_desc_single(value: &DescSingleValue, end_tag: Option<u32>) -> Self {
        match value {
            DescSingleValue::Scalar(scalar_type) => Self::Scalar(*scalar_type),
            DescSingleValue::Message {
                message,
                delimited_encoding,
            } => Self::Message {
                message: message.clone(),
                end_tag: if *delimited_encoding { end_tag } else { None },
            },
            DescSingleValue::Enum(enum_) => Self::Enum(enum_.clone()),
        }
    }
}

/// Serializer for one field number.
struct FieldSerializer {
    /// The tag to output for the field.
    tag: u32,
    /// The type of the field.
    type_: FieldSerializerType,
    /// How to serialize the value of the field. For lists, it is the list element type and for maps, the map value.
    value: FieldSerializerValue,
}

impl FieldSerializer {
    /// Constructs a field serializer from a normalized descriptor field.
    fn new(field: &DescField) -> Self {
        let field_value = match &field.value {
            DescFieldValue::Scalar { scalar_type, .. } => {
                FieldSerializerValue::Scalar(*scalar_type)
            }
            DescFieldValue::Message {
                message,
                delimited_encoding,
                ..
            } => FieldSerializerValue::Message {
                message: message.clone(),
                end_tag: if *delimited_encoding {
                    Some((field.number << 3) | (WireType::EndGroup as u32))
                } else {
                    None
                },
            },
            DescFieldValue::Enum { enum_, .. } => FieldSerializerValue::Enum(enum_.clone()),
            DescFieldValue::List { element, .. } => {
                let list_end_tag = Some((field.number << 3) | (WireType::EndGroup as u32));
                FieldSerializerValue::from_desc_single(element, list_end_tag)
            }
            DescFieldValue::Map { value, .. } => {
                // Map values are encoded in entry field number 2.
                let map_value_end_tag = Some((2 << 3) | (WireType::EndGroup as u32));
                FieldSerializerValue::from_desc_single(value, map_value_end_tag)
            }
        };
        let tag = (field.number << 3) | (field.wire_type as u32);
        Self {
            tag,
            type_: FieldSerializerType::new(&field.value),
            value: field_value,
        }
    }

    /// Writes this field's wire bytes for the provided value.
    ///
    /// The buffer is filled back-to-front: each field's bytes are prepended so
    /// that, once a length-delimited payload is written, its length is known
    /// from how far the buffer grew and can be prepended without a sizing pass.
    fn write_binary(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        buffer: &mut ReverseBuffer,
        opts: ToBinaryOpts,
        constants: &Constants,
    ) -> PyResult<()> {
        match &self.type_ {
            FieldSerializerType::Singular => {
                self.write_singular_field(py, value, buffer, opts)?;
            }
            FieldSerializerType::List { packed } => {
                self.write_list_field(py, value, buffer, opts, *packed)?;
            }
            FieldSerializerType::Map {
                key_serializer: key_marshaler,
                value_serializer: value_marshaler,
            } => self.write_map_field(
                py,
                value,
                buffer,
                opts,
                constants,
                key_marshaler,
                value_marshaler,
            )?,
        }

        Ok(())
    }

    fn write_singular_field(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        buffer: &mut ReverseBuffer,
        opts: ToBinaryOpts,
    ) -> PyResult<()> {
        self.write_single_value(py, value, buffer, opts)?;
        buffer.prepend_varint(self.tag as u64);
        Ok(())
    }

    fn write_list_field(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        buffer: &mut ReverseBuffer,
        opts: ToBinaryOpts,
        packed: bool,
    ) -> PyResult<()> {
        let value_list = value.cast::<PyList>()?;
        let len = value_list.len();
        if len == 0 {
            return Ok(());
        }
        // As with message fields, prepend list values in reverse order to
        // have the correct order on the wire.
        if packed {
            let payload_end = buffer.len();
            for i in (0..len).rev() {
                self.write_single_value(py, &value_list.get_item(i)?, buffer, opts)?;
            }
            let payload_len = buffer.len() - payload_end;
            buffer.prepend_varint(payload_len as u64);
            buffer.prepend_varint(self.tag as u64);
        } else {
            for i in (0..len).rev() {
                self.write_singular_field(py, &value_list.get_item(i)?, buffer, opts)?;
            }
        }
        Ok(())
    }

    fn write_map_field(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        buffer: &mut ReverseBuffer,
        opts: ToBinaryOpts,
        constants: &Constants,
        key_marshaler: &FieldSerializer,
        value_marshaler: &FieldSerializer,
    ) -> PyResult<()> {
        let value_dict = value.cast::<PyDict>()?;
        // Protobuf maps are unordered, with many languages using hash maps for
        // their storage. This means we don't need to retain any order and
        // output map entries in forward order to avoid having to collect them
        // into a reversable list first.
        for (key, value) in value_dict {
            let entry_end = buffer.len();
            value_marshaler.write_binary(py, &value, buffer, opts, constants)?;
            key_marshaler.write_binary(py, &key, buffer, opts, constants)?;
            let entry_len = buffer.len() - entry_end;
            buffer.prepend_varint(entry_len as u64);
            buffer.prepend_varint(self.tag as u64);
        }
        Ok(())
    }

    /// Validates and writes only the field value payload (without outer tag).
    fn write_single_value(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        buffer: &mut ReverseBuffer,
        opts: ToBinaryOpts,
    ) -> PyResult<()> {
        match &self.value {
            FieldSerializerValue::Scalar(scalar_type) => {
                Self::write_single_scalar_value(*scalar_type, value, buffer)?;
            }
            FieldSerializerValue::Enum(e) => {
                let value = value.extract::<i32>()?;
                if !e.open && !e.values.contains_key(&value) {
                    return Err(PyValueError::new_err(format!(
                        "invalid enum value {value} for enum '{}'",
                        e.type_name
                    )));
                }
                buffer.prepend_varint(value as u64);
            }
            FieldSerializerValue::Message {
                message: message_desc,
                end_tag,
            } => {
                if let Some(end_tag) = end_tag {
                    // Group encoding: the end tag is the final byte and so is
                    // prepended first, ahead of the submessage payload.
                    buffer.prepend_varint(*end_tag as u64);
                    if !value.is_none() {
                        let message = value.cast::<NativeMessage>()?;
                        let serializer = &message_desc.get_marshaler(py)?.serializer;
                        serializer.write_binary(py, message, buffer, opts)?;
                    }
                } else if value.is_none() {
                    buffer.prepend_varint(0);
                } else {
                    let message = value.cast::<NativeMessage>()?;
                    let serializer = &message_desc.get_marshaler(py)?.serializer;
                    let payload_end = buffer.len();
                    serializer.write_binary(py, message, buffer, opts)?;
                    let payload_len = buffer.len() - payload_end;
                    buffer.prepend_varint(payload_len as u64);
                }
            }
        }
        Ok(())
    }

    #[allow(
        clippy::too_many_lines,
        reason = "flat match over every scalar type reads better than splitting"
    )]
    fn write_single_scalar_value(
        scalar_type: ScalarType,
        value: &Bound<'_, PyAny>,
        buffer: &mut ReverseBuffer,
    ) -> PyResult<()> {
        match scalar_type {
            ScalarType::Int32 => {
                validate_is_int(value)?;
                let value = value.extract::<i32>().map_err(|_| {
                    PyOverflowError::new_err(format!("value {value} out of range for int32"))
                })?;
                buffer.prepend_varint(value as u64);
            }
            ScalarType::Int64 => {
                validate_is_int(value)?;
                let value = value.extract::<i64>().map_err(|_| {
                    PyOverflowError::new_err(format!("value {value} out of range for int64"))
                })?;
                buffer.prepend_varint(value as u64);
            }
            ScalarType::Uint32 => {
                validate_is_int(value)?;
                let value = value.extract::<u32>().map_err(|_| {
                    PyOverflowError::new_err(format!("value {value} out of range for uint32"))
                })?;
                buffer.prepend_varint(value as u64);
            }
            ScalarType::Uint64 => {
                validate_is_int(value)?;
                let value = value.extract::<u64>().map_err(|_| {
                    PyOverflowError::new_err(format!("value {value} out of range for uint64"))
                })?;
                buffer.prepend_varint(value);
            }
            ScalarType::Sint32 => {
                validate_is_int(value)?;
                let value = value.extract::<i32>()?;
                buffer.prepend_varint(encode_zigzag32(value) as u64);
            }
            ScalarType::Sint64 => {
                validate_is_int(value)?;
                let value = value.extract::<i64>()?;
                buffer.prepend_varint(encode_zigzag64(value));
            }
            ScalarType::Fixed32 => {
                validate_is_int(value)?;
                let value = value.extract::<u32>()?;
                buffer.prepend_slice(&value.to_le_bytes());
            }
            ScalarType::Fixed64 => {
                validate_is_int(value)?;
                let value = value.extract::<u64>()?;
                buffer.prepend_slice(&value.to_le_bytes());
            }
            ScalarType::Sfixed32 => {
                validate_is_int(value)?;
                let value = value.extract::<i32>()?;
                buffer.prepend_slice(&value.to_le_bytes());
            }
            ScalarType::Sfixed64 => {
                validate_is_int(value)?;
                let value = value.extract::<i64>()?;
                buffer.prepend_slice(&value.to_le_bytes());
            }
            ScalarType::Bool => {
                if !value.is_instance_of::<PyBool>() {
                    return Err(PyTypeError::new_err(format!(
                        "expected bool, got {}",
                        value.get_type()
                    )));
                }
                let value = value.extract::<bool>()?;
                buffer.prepend_u8(u8::from(value));
            }
            ScalarType::Float => {
                validate_is_float(value)?;
                let value_f64 = value.extract::<f64>()?;
                let value_f32 = value_f64 as f32;
                if value_f32.is_infinite() && !value_f64.is_infinite() {
                    return Err(PyOverflowError::new_err(format!(
                        "value {value_f64} out of range for float32"
                    )));
                }
                buffer.prepend_slice(&value_f32.to_le_bytes());
            }
            ScalarType::Double => {
                validate_is_float(value)?;
                let value = value.extract::<f64>()?;
                buffer.prepend_slice(&value.to_le_bytes());
            }
            ScalarType::String => {
                let value = value.cast::<PyString>().map_err(|_| {
                    PyTypeError::new_err(format!("expected string, got {}", value.get_type()))
                })?;
                let bytes = value.to_str()?.as_bytes();
                buffer.prepend_slice(bytes);
                buffer.prepend_varint(bytes.len() as u64);
            }
            ScalarType::Bytes => {
                let value = value.cast::<PyBytes>().map_err(|_| {
                    PyTypeError::new_err(format!("expected bytes, got {}", value.get_type()))
                })?;
                let value_bytes = value.as_bytes();
                buffer.prepend_slice(value_bytes);
                buffer.prepend_varint(value_bytes.len() as u64);
            }
        }
        Ok(())
    }

    fn is_zero_value(&self, value: &Bound<'_, PyAny>) -> PyResult<bool> {
        if matches!(&self.type_, FieldSerializerType::Singular) {
            return match &self.value {
                FieldSerializerValue::Scalar(scalar_type) => match scalar_type {
                    ScalarType::Double | ScalarType::Float => {
                        let value = value.extract::<f64>()?;
                        Ok(value == 0.0 && value.is_sign_positive())
                    }
                    _ => Ok(!(value.is_truthy()?)),
                },
                FieldSerializerValue::Enum(e) => value.eq(&e.zero_value),
                FieldSerializerValue::Message { .. } => Ok(value.is_none()),
            };
        }
        Ok(!(value.is_truthy()?))
    }
}

/// Information on a field in the serializer. We separate out the state needed
/// to evaluate a field value from the state needed to serialize it to keep
/// the serialization logic simpler.
struct SerializerField {
    /// The Python attribute name for the field (used in error messages and oneof lookup).
    py_attr: String,
    /// The field number.
    number: u32,
    /// The presence of the field.
    presence: FieldPresence,
    /// Access for the oneof wrapper attribute, if this field is part of a oneof.
    oneof: Option<AttributeAccess>,
    /// Access for the field's own attribute on the message.
    attr: AttributeAccess,
    /// The serializer for the field.
    serializer: FieldSerializer,
}

/// Shared serializer state reused across serializer clones.
struct MessageSerializerInner {
    /// The Python type for this serializer.
    python_type: Py<PyType>,
    /// Per-field metadata and field serializers.
    fields: Box<[SerializerField]>,
    /// Oneof attribute accessors for oneof validation.
    oneofs: Box<[AttributeAccess]>,
    /// Descriptor map of fields keyed by local name.
    fields_by_name: Py<PyAny>,
    /// Cached constants/types used for Python interop.
    constants: Constants,
}

#[derive(Clone)]
/// Entry-point serializer for a concrete Python message type.
pub(crate) struct MessageSerializer {
    inner: Arc<MessageSerializerInner>,
}

impl MessageSerializer {
    /// Creates a message serializer from descriptor fields.
    pub(crate) fn new(
        py: Python<'_>,
        message_desc: &Bound<'_, PyAny>,
        python_type: &Bound<'_, PyType>,
        fields: &Vec<DescField>,
        constants: &Constants,
    ) -> PyResult<Self> {
        let fields_by_name = message_desc.getattr(&constants.fields_by_name)?;
        let mut marshaler_fields = Vec::with_capacity(fields.len());
        for field in fields {
            let serializer = FieldSerializer::new(field);
            let oneof_access = field
                .value
                .oneof_name()
                .map(|name| AttributeAccess::new(py, python_type, name.bind(py)));
            let attr_access = AttributeAccess::new(py, python_type, field.local_name.bind(py));
            marshaler_fields.push(SerializerField {
                py_attr: field.local_name.extract::<String>(py)?,
                number: field.number,
                presence: field.presence,
                oneof: oneof_access,
                attr: attr_access,
                serializer,
            });
        }
        let mut oneof_names = Vec::new();
        for key in message_desc
            .getattr(&constants.oneofs_by_local_name)?
            .cast::<PyDict>()?
            .keys()
            .iter()
        {
            oneof_names.push(AttributeAccess::new(
                py,
                python_type,
                key.cast::<PyString>()?,
            ));
        }
        Ok(Self {
            inner: Arc::new(MessageSerializerInner {
                python_type: python_type.clone().unbind(),
                fields: marshaler_fields.into_boxed_slice(),
                oneofs: oneof_names.into_boxed_slice(),
                fields_by_name: fields_by_name.clone().unbind(),
                constants: constants.clone(),
            }),
        })
    }
}

impl MessageSerializer {
    /// Validates a Python message and writes its wire bytes.
    ///
    /// Bytes are written back-to-front into `buffer`, so fields are emitted in
    /// reverse field order (and unknown fields first) to land in forward order
    /// on the wire without needint to presize length-prefixed fields.
    pub(crate) fn write_binary(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        buffer: &mut ReverseBuffer,
        opts: ToBinaryOpts,
    ) -> PyResult<()> {
        if !message.is_instance(self.inner.python_type.bind(py))? {
            return Err(PyTypeError::new_err(format!(
                "expected {}, got '{}'",
                self.inner.python_type,
                message.get_type()
            )));
        }

        self.validate_oneofs(py, message)?;

        // Unknown fields should be at the end so we write them first.
        if opts.write_unknown_fields {
            Self::write_unknown_fields(py, message, buffer)?;
        }

        for field in self.inner.fields.iter().rev() {
            let Some(value) = Self::get_field_value(message, field)? else {
                continue;
            };
            field
                .serializer
                .write_binary(py, &value, buffer, opts, &self.inner.constants)?;
        }

        Ok(())
    }

    /// Gets a field value if it should be serialized for this message.
    fn get_field_value<'py>(
        message: &Bound<'py, NativeMessage>,
        field: &SerializerField,
    ) -> PyResult<Option<Bound<'py, PyAny>>> {
        let py = message.py();

        if let Some(oneof_access) = &field.oneof {
            let value = oneof_access.get(py, message)?;
            let Ok(oneof) = value.cast::<Oneof>() else {
                return Ok(None);
            };
            let oneof = oneof.get();
            return if oneof.field.bind(py).extract::<&str>()? == field.py_attr {
                Ok(Some(oneof.value.bind(py).clone()))
            } else {
                Ok(None)
            };
        }

        let value = field.attr.get(py, message)?;

        if matches!(field.presence, FieldPresence::Implicit) {
            return if field.serializer.is_zero_value(&value)? {
                Ok(None)
            } else {
                Ok(Some(value))
            };
        }

        let present = if matches!(field.serializer.value, FieldSerializerValue::Message { .. }) {
            !value.is_none()
        } else {
            message.get().has_present_field(field.number)
        };

        if !present {
            return if matches!(field.presence, FieldPresence::LegacyRequired) {
                Err(PyErr::new::<PyValueError, _>(format!(
                    "cannot encode {} to binary: required field not set",
                    field.py_attr
                )))
            } else {
                Ok(None)
            };
        }

        Ok(Some(value))
    }

    /// Writes raw unknown field bytes from the message.
    fn write_unknown_fields(
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        buffer: &mut ReverseBuffer,
    ) -> PyResult<()> {
        let Some(unknown_fields_unbound) = message.get().unknown_fields(py) else {
            return Ok(());
        };
        let unknown_fields = unknown_fields_unbound.bind(py);
        // Gather chunks in forward order, then prepend in reverse so they land
        // in their original order.
        let mut chunks = Vec::new();
        for (_, field_list) in unknown_fields {
            let field_list = field_list.cast::<PyList>()?;
            for field_bytes in field_list.iter() {
                chunks.push(field_bytes);
            }
        }
        for field_bytes in chunks.iter().rev() {
            buffer.prepend_slice(field_bytes.extract::<&[u8]>()?);
        }
        Ok(())
    }

    /// Ensures oneof slots reference known fields.
    fn validate_oneofs(&self, py: Python<'_>, message: &Bound<'_, PyAny>) -> PyResult<()> {
        for oneof_access in &self.inner.oneofs {
            let oneof_any = oneof_access.get(py, message)?;
            if oneof_any.is_none() {
                continue;
            }
            let Ok(oneof) = oneof_any.cast::<Oneof>() else {
                return Err(PyTypeError::new_err(format!(
                    "expected Oneof, got '{}'",
                    oneof_any.get_type()
                )));
            };
            if !self
                .inner
                .fields_by_name
                .bind(py)
                .contains(&oneof.get().field)?
            {
                return Err(PyValueError::new_err(format!(
                    "unknown oneof field '{}'",
                    oneof.get().field
                )));
            }
        }
        Ok(())
    }
}

/// Encodes i32 using protobuf zig-zag encoding.
fn encode_zigzag32(v: i32) -> u32 {
    ((v << 1) ^ (v >> 31)) as u32
}

/// Encodes i64 using protobuf zig-zag encoding.
fn encode_zigzag64(v: i64) -> u64 {
    ((v << 1) ^ (v >> 63)) as u64
}

/// Validates that a Python value is an int (excluding bool).
fn validate_is_int(value: &Bound<'_, PyAny>) -> PyResult<()> {
    if value.is_instance_of::<PyBool>() {
        return Err(PyTypeError::new_err(format!(
            "expected int, got {}",
            value.get_type()
        )));
    }
    value
        .cast::<PyInt>()
        .map_err(|_| PyTypeError::new_err(format!("expected int, got {}", value.get_type())))?;
    Ok(())
}

/// Validates that a Python value is a float.
fn validate_is_float(value: &Bound<'_, PyAny>) -> PyResult<()> {
    value
        .cast::<PyFloat>()
        .map_err(|_| PyTypeError::new_err(format!("expected float, got {}", value.get_type())))?;
    Ok(())
}
