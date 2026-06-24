//! Native representation of subset of protobuf descriptors, read directly from
//! Python objects. Parser and Serializer then take the subset they each need with
//! precomputed information to keep cache lookups and Python interactions to a minimum.

use std::{collections::HashMap, ops::Deref, sync::Arc};

use pyo3::{
    Bound, Py, PyAny, PyResult, Python,
    exceptions::PyValueError,
    pyclass,
    sync::PyOnceLock,
    types::{
        PyAnyMethods as _, PyBool, PyBytes, PyFloat, PyInt, PyList, PyListMethods as _, PyString,
        PyType,
    },
};

use crate::{constants::Constants, marshaler::MessageMarshaler};

/// Presence semantics for a field, matching descriptor.proto values.
#[derive(Clone, Copy)]
pub(crate) enum FieldPresence {
    // Numbers from descriptor.proto
    /// Explicit presence bit (proto2/optional semantics).
    Explicit = 1,
    /// Implicit presence (zero/default means unset).
    Implicit = 2,
    /// Legacy required field semantics.
    LegacyRequired = 3,
}

impl FieldPresence {
    fn try_from_py(py_presence: &Bound<'_, PyAny>) -> PyResult<Self> {
        match py_presence.extract::<u32>()? {
            1 => Ok(FieldPresence::Explicit),
            2 => Ok(FieldPresence::Implicit),
            3 => Ok(FieldPresence::LegacyRequired),
            other => Err(PyValueError::new_err(format!("invalid presence: {other}"))),
        }
    }
}

/// Protobuf wire-format type tags.
#[derive(Clone, Copy, PartialEq)]
pub(crate) enum WireType {
    // Numbers from protobuf wire format.
    /// Variable-length integer encoding.
    Varint = 0,
    /// Fixed-width 64-bit encoding.
    Bit64 = 1,
    /// Length-prefixed bytes/messages.
    LengthDelimited = 2,
    /// Start of a deprecated group.
    StartGroup = 3,
    /// End of a deprecated group.
    EndGroup = 4,
    /// Fixed-width 32-bit encoding.
    Bit32 = 5,
}

impl WireType {
    pub(crate) fn from_tag(tag: u32) -> PyResult<Self> {
        let res = match tag & 0b111 {
            0 => WireType::Varint,
            1 => WireType::Bit64,
            2 => WireType::LengthDelimited,
            3 => WireType::StartGroup,
            4 => WireType::EndGroup,
            5 => WireType::Bit32,
            type_ => {
                return Err(PyValueError::new_err(format!("invalid wire type: {type_}")));
            }
        };
        Ok(res)
    }
}

/// Scalar protobuf value kinds from descriptor.proto.
#[derive(Clone, Copy)]
pub(crate) enum ScalarType {
    // Numbers from descriptor.proto
    /// 64-bit IEEE floating point.
    Double = 1,
    /// 32-bit IEEE floating point.
    Float = 2,
    /// Signed 64-bit varint.
    Int64 = 3,
    /// Unsigned 64-bit varint.
    Uint64 = 4,
    /// Signed 32-bit varint.
    Int32 = 5,
    /// Unsigned fixed-width 64-bit.
    Fixed64 = 6,
    /// Unsigned fixed-width 32-bit.
    Fixed32 = 7,
    /// Boolean.
    Bool = 8,
    /// UTF-8 string.
    String = 9,
    /// Raw bytes.
    Bytes = 12,
    /// Unsigned 32-bit varint.
    Uint32 = 13,
    /// Signed fixed-width 32-bit.
    Sfixed32 = 15,
    /// Signed fixed-width 64-bit.
    Sfixed64 = 16,
    /// Zig-zag encoded signed 32-bit varint.
    Sint32 = 17,
    /// Zig-zag encoded signed 64-bit varint.
    Sint64 = 18,
}

impl ScalarType {
    fn from_py(py_type: &Bound<'_, PyAny>) -> PyResult<Self> {
        let res = match py_type.extract::<u32>()? {
            1 => ScalarType::Double,
            2 => ScalarType::Float,
            3 => ScalarType::Int64,
            4 => ScalarType::Uint64,
            5 => ScalarType::Int32,
            6 => ScalarType::Fixed64,
            7 => ScalarType::Fixed32,
            8 => ScalarType::Bool,
            9 => ScalarType::String,
            12 => ScalarType::Bytes,
            13 => ScalarType::Uint32,
            15 => ScalarType::Sfixed32,
            16 => ScalarType::Sfixed64,
            17 => ScalarType::Sint32,
            18 => ScalarType::Sint64,
            other => {
                return Err(PyValueError::new_err(format!(
                    "invalid scalar type: {other}"
                )));
            }
        };
        Ok(res)
    }

    pub(crate) fn wire_type(self) -> WireType {
        match self {
            ScalarType::Uint32
            | ScalarType::Uint64
            | ScalarType::Int32
            | ScalarType::Int64
            | ScalarType::Bool
            | ScalarType::Sint32
            | ScalarType::Sint64 => WireType::Varint,
            ScalarType::Float | ScalarType::Fixed32 | ScalarType::Sfixed32 => WireType::Bit32,
            ScalarType::Double | ScalarType::Fixed64 | ScalarType::Sfixed64 => WireType::Bit64,
            ScalarType::String | ScalarType::Bytes => WireType::LengthDelimited,
        }
    }

    pub(crate) fn zero_value(self, py: Python<'_>) -> Py<PyAny> {
        match self {
            ScalarType::Double | ScalarType::Float => PyFloat::new(py, 0.0).into_any().unbind(),
            ScalarType::Int64
            | ScalarType::Uint64
            | ScalarType::Int32
            | ScalarType::Uint32
            | ScalarType::Fixed64
            | ScalarType::Sfixed64
            | ScalarType::Fixed32
            | ScalarType::Sfixed32
            | ScalarType::Sint32
            | ScalarType::Sint64 => PyInt::new(py, 0).into_any().unbind(),
            ScalarType::Bool => PyBool::new(py, false).to_owned().into_any().unbind(),
            ScalarType::String => PyString::new(py, "").into_any().unbind(),
            ScalarType::Bytes => PyBytes::new(py, &[]).into_any().unbind(),
        }
    }
}

struct DescMessageInner {
    /// Lazily-initialized marshaler for this message type.
    marshaler: PyOnceLock<MessageMarshaler>,
    /// Python class object for the message type.
    py_type: Py<PyType>,
    constants: Constants,
}

/// Handle to the marshaler for a message type to reduce Python access on the hot path.
/// Resolved lazily since recursive message types prevent marshalers from being ready before
/// the entire message graph has been initialized.
#[pyclass(from_py_object, frozen)]
#[derive(Clone)]
pub(crate) struct DescMessage {
    inner: Arc<DescMessageInner>,
}

impl DescMessage {
    fn new(py: Python<'_>, desc: &Bound<'_, PyAny>, constants: &Constants) -> PyResult<Self> {
        let py_type = desc.getattr(&constants.type_)?;
        if let Some(ext_desc) = py_type.getattr_opt(&constants.ext_value_type)? {
            return Ok(ext_desc.extract::<DescMessage>()?);
        }

        let res_py = Py::new(
            py,
            Self {
                inner: Arc::new(DescMessageInner {
                    marshaler: PyOnceLock::new(),
                    py_type: py_type.cast::<PyType>()?.clone().unbind(),
                    constants: constants.clone(),
                }),
            },
        )?;

        py_type.setattr(&constants.ext_value_type, res_py.clone_ref(py))?;
        Ok(res_py.get().clone())
    }

    pub(crate) fn get_python_type<'py>(&self, py: Python<'py>) -> &Bound<'py, PyType> {
        self.inner.py_type.bind(py)
    }

    pub(crate) fn get_marshaler(&self, py: Python<'_>) -> PyResult<&MessageMarshaler> {
        self.inner.marshaler.get_or_try_init(py, || {
            let message_type = self.inner.py_type.bind(py);
            let marshaler = message_type
                .getattr(&self.inner.constants.ext_marshaler)?
                .cast::<MessageMarshaler>()?
                .get()
                .clone();
            Ok(marshaler)
        })
    }
}

pub(crate) struct DescEnumInner {
    /// Whether unknown numeric values are accepted.
    pub(crate) open: bool,
    /// Numeric value -> Python enum object.
    pub(crate) values: HashMap<i32, Py<PyAny>>,
    /// Default enum value (first declared value).
    pub(crate) zero_value: Py<PyAny>,
    /// Python enum class object.
    pub(crate) py_type: Py<PyAny>,
    /// Fully-qualified enum type name.
    pub(crate) type_name: Py<PyString>,
}

#[pyclass(from_py_object, frozen)]
#[derive(Clone)]
pub(crate) struct DescEnum {
    /// Shared handle to immutable enum descriptor metadata.
    inner: Arc<DescEnumInner>,
}

impl Deref for DescEnum {
    type Target = DescEnumInner;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl DescEnum {
    fn new(py: Python<'_>, desc: &Bound<'_, PyAny>, constants: &Constants) -> PyResult<Self> {
        let py_type = desc.getattr(&constants.type_)?;
        if let Some(ext_desc) = py_type.getattr_opt(&constants.ext_value_type)? {
            let enum_ = ext_desc.extract::<DescEnum>()?;
            return Ok(enum_);
        }
        let type_name = desc
            .getattr(&constants.type_name)?
            .cast::<PyString>()?
            .clone()
            .unbind();
        let open = desc.getattr(&constants.open)?.extract::<bool>()?;
        let python_values_any = desc.getattr(&constants.values)?;
        let python_values = python_values_any.cast::<PyList>()?;
        if python_values.is_empty() {
            return Err(PyValueError::new_err("enum must have at least one value"));
        }
        let mut values = HashMap::new();
        let mut first_value = None;
        for enum_value in python_values.iter() {
            let number = enum_value.getattr(&constants.number)?.extract::<i32>()?;
            let local_name_any = enum_value.getattr(&constants.local_name)?;
            let local_name = local_name_any.cast::<PyString>()?;
            let value = py_type.getattr(local_name)?;
            if first_value.is_none() {
                first_value = Some(value.clone().unbind());
            }
            values.insert(number, value.unbind());
        }
        let zero_value = first_value.unwrap();

        let res_py = Py::new(
            py,
            Self {
                inner: Arc::new(DescEnumInner {
                    open,
                    values,
                    zero_value,
                    py_type: py_type.clone().unbind(),
                    type_name,
                }),
            },
        )?;

        py_type.setattr(&constants.ext_value_type, res_py.clone_ref(py))?;
        Ok(res_py.get().clone())
    }
}

/// Arc wrapper around the `PyString` for the oneof name to allow Clone.
#[derive(Clone)]
pub(crate) struct OneofName(Arc<Py<PyString>>);

impl Deref for OneofName {
    type Target = Py<PyString>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl OneofName {
    fn new(py_name: Py<PyString>) -> Self {
        Self(Arc::new(py_name))
    }
}

/// Singular value kinds used as list/map elements and shared parsing metadata.
#[derive(Clone)]
pub(crate) enum DescSingleValue {
    /// Scalar field element.
    Scalar(ScalarType),
    /// Message field element.
    Message {
        /// Message descriptor handle.
        message: DescMessage,
        /// Whether this message uses group encoding.
        delimited_encoding: bool,
    },
    /// Enum field element.
    Enum(DescEnum),
}

impl DescSingleValue {
    pub(crate) fn wire_type(&self) -> WireType {
        match self {
            DescSingleValue::Scalar(scalar_type) => scalar_type.wire_type(),
            DescSingleValue::Message {
                delimited_encoding, ..
            } => {
                if *delimited_encoding {
                    WireType::StartGroup
                } else {
                    WireType::LengthDelimited
                }
            }
            DescSingleValue::Enum(_) => WireType::Varint,
        }
    }
}

/// Full field value model for a descriptor field.
#[derive(Clone)]
pub(crate) enum DescFieldValue {
    /// Singular scalar field.
    Scalar {
        /// Scalar wire/value type.
        scalar_type: ScalarType,
        /// Oneof this field belongs to, if any.
        oneof_name: Option<OneofName>,
    },
    /// Singular message field.
    Message {
        /// Message descriptor handle.
        message: DescMessage,
        /// Whether this message uses group encoding.
        delimited_encoding: bool,
        /// Oneof this field belongs to, if any.
        oneof_name: Option<OneofName>,
    },
    /// Singular enum field.
    Enum {
        /// Enum descriptor handle.
        enum_: DescEnum,
        /// Oneof this field belongs to, if any.
        oneof_name: Option<OneofName>,
    },
    /// Repeated list field.
    List {
        /// Element value descriptor for each list item.
        element: DescSingleValue,
        /// Whether repeated values use packed wire encoding.
        packed: bool,
    },
    /// Map field encoded as repeated key/value entry messages.
    Map {
        /// Scalar key type (protobuf map keys are always scalar).
        key_type: ScalarType,
        /// Value descriptor for the map entry value.
        value: DescSingleValue,
    },
}

impl DescFieldValue {
    pub(crate) fn oneof_name(&self) -> Option<OneofName> {
        match self {
            DescFieldValue::Scalar { oneof_name, .. }
            | DescFieldValue::Message { oneof_name, .. }
            | DescFieldValue::Enum { oneof_name, .. } => oneof_name.clone(),
            DescFieldValue::List { .. } | DescFieldValue::Map { .. } => None,
        }
    }
}

/// Normalized field descriptor used by parser and serializer builders.
pub(crate) struct DescField {
    /// The field's value descriptor.
    pub(crate) value: DescFieldValue,
    /// The name of the Python attribute for this field.
    pub(crate) local_name: Py<PyString>,
    /// The field number.
    pub(crate) number: u32,
    /// The field presence.
    pub(crate) presence: FieldPresence,
    /// Whether the field requires explicit presence tracking.
    pub(crate) requires_presence: bool,
    /// The wire type.
    pub(crate) wire_type: WireType,
}

impl DescField {
    #[allow(clippy::too_many_lines, reason = "clearer with one function")]
    fn new(py: Python<'_>, field: &Bound<'_, PyAny>, constants: &Constants) -> PyResult<Self> {
        if !field.is_instance(constants.types.desc_field.bind(py))? {
            return Err(PyValueError::new_err("invalid field descriptor"));
        }

        let py_number_any = field.getattr(&constants.number)?;
        let py_number = py_number_any.cast::<PyInt>()?;
        let number = py_number.extract::<u32>()?;
        let local_name = field
            .getattr(&constants.local_name)?
            .cast::<PyString>()?
            .clone()
            .unbind();
        let presence = FieldPresence::try_from_py(&field.getattr(&constants.presence)?)?;
        let requires_presence = field
            .getattr(&constants.requires_presence)?
            .extract::<bool>()?;
        let desc_value = field.getattr(&constants.value)?;

        if desc_value.is_instance(constants.types.desc_field_value_scalar.bind(py))? {
            let oneof_name = oneof_local_name(&desc_value, constants)?;
            let scalar_type = ScalarType::from_py(&desc_value.getattr(&constants.scalar)?)?;
            Ok(Self {
                local_name,
                number,
                presence,
                requires_presence,
                wire_type: scalar_type.wire_type(),
                value: DescFieldValue::Scalar {
                    scalar_type,
                    oneof_name,
                },
            })
        } else if desc_value.is_instance(constants.types.desc_field_value_enum.bind(py))? {
            let oneof_name = oneof_local_name(&desc_value, constants)?;
            let py_desc_enum = desc_value.getattr(&constants.enum_)?;
            let desc_enum = DescEnum::new(py, &py_desc_enum, constants)?;
            Ok(Self {
                local_name,
                number,
                presence,
                requires_presence,
                wire_type: WireType::Varint,
                value: DescFieldValue::Enum {
                    enum_: desc_enum,
                    oneof_name,
                },
            })
        } else if desc_value.is_instance(constants.types.desc_field_value_message.bind(py))? {
            let oneof_name = oneof_local_name(&desc_value, constants)?;
            let py_desc_message = desc_value.getattr(&constants.message)?;
            let delimited_encoding = desc_value
                .getattr(&constants.delimited_encoding)?
                .extract::<bool>()?;
            let desc_message = DescMessage::new(py, &py_desc_message, constants)?;
            Ok(Self {
                local_name,
                number,
                presence,
                requires_presence,
                wire_type: if delimited_encoding {
                    WireType::StartGroup
                } else {
                    WireType::LengthDelimited
                },
                value: DescFieldValue::Message {
                    message: desc_message,
                    delimited_encoding,
                    oneof_name,
                },
            })
        } else if desc_value.is_instance(constants.types.desc_field_value_list.bind(py))? {
            let py_desc_element = desc_value.getattr(&constants.element)?;
            let desc_element =
                if py_desc_element.is_instance(constants.types.scalar_type.bind(py))? {
                    DescSingleValue::Scalar(ScalarType::from_py(&py_desc_element)?)
                } else if py_desc_element.is_instance(constants.types.desc_enum.bind(py))? {
                    DescSingleValue::Enum(DescEnum::new(py, &py_desc_element, constants)?)
                } else if py_desc_element.is_instance(constants.types.desc_message.bind(py))? {
                    let delimited_encoding = desc_value
                        .getattr(&constants.delimited_encoding)?
                        .extract::<bool>()?;
                    DescSingleValue::Message {
                        message: DescMessage::new(py, &py_desc_element, constants)?,
                        delimited_encoding,
                    }
                } else {
                    return Err(PyValueError::new_err("invalid list element type"));
                };
            let packed = desc_value.getattr(&constants.packed)?.extract::<bool>()?;
            let wire_type = if packed {
                WireType::LengthDelimited
            } else {
                desc_element.wire_type()
            };
            Ok(Self {
                local_name,
                number,
                presence,
                requires_presence,
                wire_type,
                value: DescFieldValue::List {
                    element: desc_element,
                    packed,
                },
            })
        } else if desc_value.is_instance(constants.types.desc_field_value_map.bind(py))? {
            let key_type = ScalarType::from_py(&desc_value.getattr(&constants.key)?)?;
            let py_desc_value = desc_value.getattr(&constants.value)?;
            let desc_value = if py_desc_value.is_instance(constants.types.scalar_type.bind(py))? {
                DescSingleValue::Scalar(ScalarType::from_py(&py_desc_value)?)
            } else if py_desc_value.is_instance(constants.types.desc_enum.bind(py))? {
                DescSingleValue::Enum(DescEnum::new(py, &py_desc_value, constants)?)
            } else if py_desc_value.is_instance(constants.types.desc_message.bind(py))? {
                DescSingleValue::Message {
                    message: DescMessage::new(py, &py_desc_value, constants)?,
                    // Map values are encoded as length-delimited in entry messages.
                    delimited_encoding: false,
                }
            } else {
                return Err(PyValueError::new_err("invalid map value type"));
            };
            let wire_type = WireType::LengthDelimited;
            Ok(Self {
                local_name,
                number,
                presence,
                requires_presence,
                wire_type,
                value: DescFieldValue::Map {
                    key_type,
                    value: desc_value,
                },
            })
        } else {
            Err(PyValueError::new_err("invalid field value type"))
        }
    }
}

pub(crate) fn message_fields(
    py: Python<'_>,
    message_desc: &Bound<'_, PyAny>,
    constants: &Constants,
) -> PyResult<Vec<DescField>> {
    let python_fields_any = message_desc.getattr(&constants.fields)?;
    let python_fields = python_fields_any.cast::<PyList>()?;
    let mut fields = Vec::with_capacity(python_fields.len());
    for field in python_fields.iter() {
        fields.push(DescField::new(py, &field, constants)?);
    }
    Ok(fields)
}

fn oneof_local_name(
    value_desc: &Bound<'_, PyAny>,
    constants: &Constants,
) -> PyResult<Option<OneofName>> {
    let oneof_desc = value_desc.getattr(&constants.oneof)?;
    if oneof_desc.is_none() {
        Ok(None)
    } else {
        Ok(Some(OneofName::new(
            oneof_desc
                .getattr(&constants.local_name)?
                .cast::<PyString>()?
                .clone()
                .unbind(),
        )))
    }
}
