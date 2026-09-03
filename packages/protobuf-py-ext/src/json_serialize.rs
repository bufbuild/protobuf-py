//! `ProtoJSON` serialization.

use base64::{Engine as _, engine::general_purpose::STANDARD as BASE64_STANDARD};
use bytes::Bytes;
use pyo3::{
    Bound, Py, PyAny, PyErr, PyResult, Python,
    exceptions::{PyOverflowError, PyTypeError, PyValueError},
    types::{
        PyAnyMethods as _, PyBool, PyByteArray, PyByteArrayMethods as _, PyDict,
        PyDictMethods as _, PyInt, PyList, PyListMethods as _, PyString, PyStringMethods as _,
    },
};

use crate::{
    attribute_access::AttributeAccess,
    descriptor::{DescEnum, DescFieldValue, DescMessage, DescSingleValue, ScalarType},
    json_sink::{JsonSink, StringSink},
    marshaler::MessageMarshaler,
    nativemessage::NativeMessage,
    serializer::{
        FieldSerializer, FieldSerializerType, FieldSerializerValue, MessageSerializer,
        check_serialize_recursion_depth,
    },
};

const INT32_MIN: i64 = -(1 << 31);
const INT32_MAX: i64 = 1 << 31;
const UINT32_MAX: i64 = 1 << 32;
const FLOAT32_MAX: f64 = 3.402_823_466_385_288_6e38;
const FLOAT32_MIN: f64 = -3.402_823_466_385_288_6e38;

pub(crate) struct JsonOpts {
    pub(crate) always_emit_implicit: bool,
    pub(crate) print_enums_as_ints: bool,
    pub(crate) use_proto_field_name: bool,
    pub(crate) registry: Option<Py<PyAny>>,
}

impl MessageMarshaler {
    /// Serializes a message to a compact JSON string.
    pub(crate) fn to_json_string(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        opts: &JsonOpts,
    ) -> PyResult<Py<PyString>> {
        let mut sink = StringSink::new();
        self.write_json(py, message, &mut sink, opts, 0)?;
        Ok(PyString::new(py, &sink.finish()).unbind())
    }

    /// Writes a message as JSON.
    pub(crate) fn write_json<S: JsonSink>(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        check_serialize_recursion_depth(depth)?;
        match &self.wkt {
            Some(wkt) => wkt.write_json(self, py, message, sink, opts, depth),
            None => self.write_message_object(py, message, sink, opts, depth),
        }
    }

    /// Writes `{ ...fields... }` for a regular message.
    fn write_message_object<S: JsonSink>(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        sink.begin_object()?;
        self.write_message_fields(py, message, sink, opts, depth)?;
        sink.end_object()?;
        Ok(())
    }

    /// Writes a message's fields (and extensions) without the enclosing braces,
    /// so the Any inline form can append `@type` in the same object.
    pub(crate) fn write_message_fields<S: JsonSink>(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        self.serializer.validate_oneofs(py, message.as_any())?;
        for field in self.serializer.fields() {
            let Some(value) =
                MessageSerializer::get_field_value(message, field, opts.always_emit_implicit)?
            else {
                continue;
            };
            let key = if opts.use_proto_field_name {
                field.name.bind(py)
            } else {
                field.json_name.bind(py)
            };
            sink.py_key(key)?;
            field
                .serializer
                .write_json_value(py, &value, sink, opts, depth)?;
        }
        if let Some(registry) = &opts.registry {
            let registry = registry.bind(py);
            self.write_extensions(py, message, sink, opts, registry, depth)?;
        }
        Ok(())
    }

    fn write_extensions<S: JsonSink>(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        registry: &Bound<'_, PyAny>,
        depth: usize,
    ) -> PyResult<()> {
        let Some(unknown_fields) = message.get().unknown_fields(py) else {
            return Ok(());
        };
        let unknown_fields = unknown_fields.bind(py);
        if unknown_fields.is_empty() {
            return Ok(());
        }
        let msg_desc = message.as_any().getattr(&self.constants.desc)?;
        for field_number in unknown_fields.keys() {
            let ext_desc = registry.call_method1(
                self.constants.extension_for.bind(py),
                (&msg_desc, &field_number),
            )?;
            if ext_desc.is_none() {
                continue;
            }
            let ext_type = ext_desc.getattr(&self.constants.type_)?;
            let value = message.as_any().get_item(&ext_type)?;
            let ext_value_desc = ext_desc.getattr(&self.constants.value)?;
            let field_value = DescFieldValue::new(py, &ext_value_desc, &self.constants)?;
            let type_name = ext_desc.getattr(&self.constants.type_name)?;
            let type_name = type_name.extract::<&str>()?;
            sink.key(&format!("[{type_name}]"))?;
            write_desc_field_value(py, &field_value, &value, sink, opts, depth)?;
        }
        Ok(())
    }
}

impl FieldSerializer {
    /// Writes a field value as JSON, dispatching on the field's container kind.
    fn write_json_value<S: JsonSink>(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        match &self.type_ {
            FieldSerializerType::Singular => {
                self.write_single_json_value(py, value, sink, opts, depth)
            }
            FieldSerializerType::List { .. } => {
                let list = value.cast::<PyList>()?;
                sink.begin_array()?;
                for item in list {
                    self.write_single_json_value(py, &item, sink, opts, depth)?;
                }
                sink.end_array()?;
                Ok(())
            }
            FieldSerializerType::Map {
                key_serializer,
                value_serializer,
            } => {
                let FieldSerializerValue::Scalar(key_type) = &key_serializer.value else {
                    return Err(PyValueError::new_err("invalid map key type"));
                };
                let dict = value.cast::<PyDict>()?;
                sink.begin_object()?;
                for (key, val) in dict {
                    write_map_key(*key_type, &key, sink)?;
                    value_serializer.write_single_json_value(py, &val, sink, opts, depth)?;
                }
                sink.end_object()?;
                Ok(())
            }
        }
    }

    /// Writes a single (non-container) value, per this serializer's value kind.
    fn write_single_json_value<S: JsonSink>(
        &self,
        py: Python<'_>,
        value: &Bound<'_, PyAny>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        match &self.value {
            FieldSerializerValue::Scalar(scalar) => write_scalar_json(*scalar, value, sink),
            FieldSerializerValue::Enum(enum_) => write_enum_json(py, enum_, value, sink, opts),
            FieldSerializerValue::Message { message, .. } => {
                write_message_json(py, message, value, sink, opts, depth)
            }
        }
    }
}

/// Writes an extension value from its `DescFieldValue` (extensions are not part
/// of the marshaler's field tables).
fn write_desc_field_value<S: JsonSink>(
    py: Python<'_>,
    field_value: &DescFieldValue,
    value: &Bound<'_, PyAny>,
    sink: &mut S,
    opts: &JsonOpts,
    depth: usize,
) -> PyResult<()> {
    match field_value {
        DescFieldValue::Scalar { scalar_type, .. } => write_scalar_json(*scalar_type, value, sink),
        DescFieldValue::Enum { enum_, .. } => write_enum_json(py, enum_, value, sink, opts),
        DescFieldValue::Message { message, .. } => {
            write_message_json(py, message, value, sink, opts, depth)
        }
        DescFieldValue::List { element, .. } => {
            let list = value.cast::<PyList>()?;
            sink.begin_array()?;
            for item in list.iter() {
                write_single_desc_value(py, element, &item, sink, opts, depth)?;
            }
            sink.end_array()?;
            Ok(())
        }
        DescFieldValue::Map { .. } => {
            Err(PyValueError::new_err("map extensions are not supported"))
        }
    }
}

fn write_single_desc_value<S: JsonSink>(
    py: Python<'_>,
    element: &DescSingleValue,
    value: &Bound<'_, PyAny>,
    sink: &mut S,
    opts: &JsonOpts,
    depth: usize,
) -> PyResult<()> {
    match element {
        DescSingleValue::Scalar(scalar) => write_scalar_json(*scalar, value, sink),
        DescSingleValue::Enum(enum_) => write_enum_json(py, enum_, value, sink, opts),
        DescSingleValue::Message { message, .. } => {
            write_message_json(py, message, value, sink, opts, depth)
        }
    }
}

/// Reads a WKT int64 field with validation.
pub(crate) fn read_int64_attr(
    py: Python<'_>,
    message: &Bound<'_, NativeMessage>,
    attr: &AttributeAccess,
) -> PyResult<i64> {
    let value = attr.get(py, message.as_any())?;
    require_int(&value)?;
    value
        .extract::<i64>()
        .map_err(|_| overflow_value(&value, "int64"))
}

/// Reads a WKT int32 field with validation.
pub(crate) fn read_int32_attr(
    py: Python<'_>,
    message: &Bound<'_, NativeMessage>,
    attr: &AttributeAccess,
) -> PyResult<i32> {
    let value = attr.get(py, message.as_any())?;
    require_int(&value)?;
    #[allow(clippy::cast_possible_truncation, reason = "range-checked to i32")]
    Ok(extract_ranged(&value, INT32_MIN, INT32_MAX, "int32")? as i32)
}

pub(crate) fn write_message_json<S: JsonSink>(
    py: Python<'_>,
    message_desc: &DescMessage,
    value: &Bound<'_, PyAny>,
    sink: &mut S,
    opts: &JsonOpts,
    depth: usize,
) -> PyResult<()> {
    let expected_type = message_desc.get_python_type(py);
    if !value.is_instance(expected_type)? {
        return Err(PyTypeError::new_err(format!(
            "expected '{}', got {}",
            message_desc.get_marshaler(py)?.type_name,
            value.get_type()
        )));
    }
    let value = value.cast::<NativeMessage>()?;
    let marshaler = NativeMessage::get_marshaler(value)?;
    marshaler.write_json(py, value, sink, opts, depth + 1)
}

fn write_enum_json<S: JsonSink>(
    py: Python<'_>,
    enum_desc: &DescEnum,
    value: &Bound<'_, PyAny>,
    sink: &mut S,
    opts: &JsonOpts,
) -> PyResult<()> {
    if value.is_instance_of::<PyBool>() || !value.is_instance_of::<PyInt>() {
        return Err(PyTypeError::new_err(format!(
            "expected int for enum {}, got {}",
            enum_desc.type_name.bind(py).to_str()?,
            value.get_type()
        )));
    }
    if let Ok(number) = value.extract::<i32>() {
        let name = enum_desc.names_by_number.get(&number);
        if !enum_desc.open && name.is_none() {
            return Err(PyValueError::new_err(format!(
                "invalid enum value {number} for enum {}",
                enum_desc.type_name.bind(py).to_str()?
            )));
        }
        if enum_desc.is_null_value {
            return sink.null();
        }
        if opts.print_enums_as_ints {
            return sink.i64(i64::from(number));
        }
        if let Some(name) = name {
            return sink.py_str(name.bind(py));
        }
        // Open enum, unknown value: emit the bare integer.
        sink.i64(i64::from(number))
    } else {
        // An int outside i32 range: only valid for open enums (a closed
        // enum would reject the unknown value).
        if !enum_desc.open {
            return Err(PyValueError::new_err(format!(
                "invalid enum value {} for enum {}",
                value.str()?,
                enum_desc.type_name.bind(py).to_str()?
            )));
        }
        sink.py_number(value)
    }
}

pub(crate) fn write_scalar_json<S: JsonSink>(
    scalar: ScalarType,
    value: &Bound<'_, PyAny>,
    sink: &mut S,
) -> PyResult<()> {
    match scalar {
        ScalarType::Bool => {
            if !value.is_instance_of::<PyBool>() {
                return Err(type_got("expected bool", value));
            }
            sink.bool(value.extract::<bool>()?)
        }
        ScalarType::Int32 | ScalarType::Sint32 | ScalarType::Sfixed32 => {
            require_int(value)?;
            sink.i64(extract_ranged(value, INT32_MIN, INT32_MAX, "int32")?)
        }
        ScalarType::Uint32 | ScalarType::Fixed32 => {
            require_int(value)?;
            sink.i64(extract_ranged(value, 0, UINT32_MAX, "uint32")?)
        }
        ScalarType::Int64 | ScalarType::Sint64 | ScalarType::Sfixed64 => {
            require_int(value)?;
            let v = value
                .extract::<i64>()
                .map_err(|_| overflow_value(value, "int64"))?;
            let mut buf = itoa::Buffer::new();
            sink.str(buf.format(v))
        }
        ScalarType::Uint64 | ScalarType::Fixed64 => {
            require_int(value)?;
            let v = value
                .extract::<u64>()
                .map_err(|_| overflow_value(value, "uint64"))?;
            let mut buf = itoa::Buffer::new();
            sink.str(buf.format(v))
        }
        ScalarType::Float => {
            let f = require_float(value)?;
            if f.is_finite() && !(FLOAT32_MIN..=FLOAT32_MAX).contains(&f) {
                return Err(overflow_value(value, "float"));
            }
            write_double(value, f, sink)
        }
        ScalarType::Double => {
            let f = require_float(value)?;
            write_double(value, f, sink)
        }
        ScalarType::String => {
            let s = value
                .cast::<PyString>()
                .map_err(|_| type_got("expected str", value))?;
            sink.py_str(s)
        }
        ScalarType::Bytes => {
            let bytes = extract_bytes(value)?;
            sink.str(&BASE64_STANDARD.encode(&bytes))
        }
    }
}

/// Writes a double/float value: non-finite as `ProtoJSON` string literals, finite
/// via the Python object's `repr` (matching `json.dumps`, and preserving
/// int-valued doubles).
fn write_double<S: JsonSink>(value: &Bound<'_, PyAny>, f: f64, sink: &mut S) -> PyResult<()> {
    if f.is_nan() {
        sink.str("NaN")
    } else if f.is_infinite() {
        sink.str(if f > 0.0 { "Infinity" } else { "-Infinity" })
    } else {
        sink.py_number(value)
    }
}

fn write_map_key<S: JsonSink>(
    key_type: ScalarType,
    key: &Bound<'_, PyAny>,
    sink: &mut S,
) -> PyResult<()> {
    match key_type {
        ScalarType::String => sink.py_key(key.cast::<PyString>()?),
        ScalarType::Bool => sink.key(if key.extract::<bool>()? {
            "true"
        } else {
            "false"
        }),
        _ => sink.key(key.str()?.to_str()?),
    }
}

fn require_int(value: &Bound<'_, PyAny>) -> PyResult<()> {
    if value.is_instance_of::<PyBool>() || !value.is_instance_of::<PyInt>() {
        return Err(type_got("expected int", value));
    }
    Ok(())
}

fn require_float(value: &Bound<'_, PyAny>) -> PyResult<f64> {
    if value.is_instance_of::<PyBool>() {
        return Err(type_got("expected float", value));
    }
    value
        .extract::<f64>()
        .map_err(|_| type_got("expected float", value))
}

fn extract_ranged(value: &Bound<'_, PyAny>, min: i64, max: i64, ty: &str) -> PyResult<i64> {
    match value.extract::<i64>() {
        Ok(v) if v >= min && v < max => Ok(v),
        _ => Err(overflow_value(value, ty)),
    }
}

fn extract_bytes(value: &Bound<'_, PyAny>) -> PyResult<Bytes> {
    if let Ok(bytes) = value.extract::<Bytes>() {
        Ok(bytes)
    } else if let Ok(bytearray) = value.cast::<PyByteArray>() {
        Ok(Bytes::from(bytearray.to_vec()))
    } else {
        Err(type_got("expected bytes", value))
    }
}

fn type_got(prefix: &str, value: &Bound<'_, PyAny>) -> PyErr {
    PyTypeError::new_err(format!("{prefix}, got {}", value.get_type()))
}

fn overflow_value(value: &Bound<'_, PyAny>, ty: &str) -> PyErr {
    match value.str() {
        Ok(s) => PyOverflowError::new_err(format!("value {s} out of range for {ty}")),
        Err(err) => err,
    }
}
