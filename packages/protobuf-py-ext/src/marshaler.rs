use std::{ops::Deref, sync::Arc};

use bytes::Bytes;
use pyo3::{
    Bound, Py, PyAny, PyResult, Python,
    exceptions::PyKeyError,
    pyclass,
    types::{
        PyAnyMethods as _, PyBytes, PyDict, PyDictMethods as _, PyList, PyStringMethods as _,
        PyType,
    },
};

use crate::{
    attribute_access::AttributeAccess,
    constants::Constants,
    descriptor::{DescFieldValue, message_fields},
    nativemessage::NativeMessage,
    parser::{FromBinaryOpts, MessageParser},
    reverse_buffer::ReverseBuffer,
    serializer::{MessageSerializer, ToBinaryOpts},
};

#[pyclass(frozen)]
pub(crate) struct Member {
    pub(crate) attr: AttributeAccess,
    /// The field number of the member. Only populated if it needs
    /// presence tracking.
    pub(crate) field_number: Option<u32>,
}

impl Member {
    fn clone_ref(&self, py: Python<'_>) -> Self {
        Self {
            attr: self.attr.clone_ref(py),
            field_number: self.field_number,
        }
    }
}

/// Pre-computed defaults for initializing a new message.
struct MessageDefaults {
    /// Scalar field attribute accessors and their default values.
    scalars: Vec<(AttributeAccess, Py<PyAny>)>,
    /// List field attribute accessors.
    lists: Vec<AttributeAccess>,
    /// Dict field attribute accessors.
    dicts: Vec<AttributeAccess>,
}

pub(crate) struct MessageMarshalerInner {
    /// Reusable parser for this message type.
    pub(crate) parser: MessageParser,
    /// Reusable serializer for this message type.
    pub(crate) serializer: MessageSerializer,
    pub(crate) members_by_name: Py<PyDict>,
    pub(crate) members: Vec<Member>,

    /// The maximum field number of the message.
    pub(crate) max_field_number: u32,

    /// The Python type of the message.
    pub(crate) python_type: Py<PyType>,

    /// The default values for each member.
    defaults: MessageDefaults,

    /// Shared constants.
    pub(crate) constants: Constants,
}

/// Entrypoint to native marshaling code.
#[pyclass(from_py_object, frozen)]
#[derive(Clone)]
pub(super) struct MessageMarshaler {
    /// Shared parser/serializer state for this message type.
    inner: Arc<MessageMarshalerInner>,
}

impl Deref for MessageMarshaler {
    type Target = MessageMarshalerInner;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}

impl MessageMarshaler {
    /// Builds parser/serializer state from a Python message descriptor.
    pub(super) fn new(
        py: Python<'_>,
        message_desc: &Bound<'_, PyAny>,
        constants: &Constants,
    ) -> PyResult<Self> {
        let python_type_any = message_desc.getattr(&constants.type_)?;
        let python_type = python_type_any.cast::<PyType>()?;
        let fields = message_fields(py, message_desc, constants)?;
        let parser = MessageParser::new(py, &fields, python_type, constants);
        let serializer = MessageSerializer::new(py, message_desc, python_type, &fields, constants)?;
        let max_field_number = fields.iter().map(|f| f.number).max().unwrap_or(0);
        let members_by_name = PyDict::new(py);
        for field in &fields {
            match &field.value {
                DescFieldValue::Scalar {
                    oneof_name: Some(oneof_name),
                    ..
                }
                | DescFieldValue::Message {
                    oneof_name: Some(oneof_name),
                    ..
                }
                | DescFieldValue::Enum {
                    oneof_name: Some(oneof_name),
                    ..
                } => {
                    // We go ahead and let the last-field of the oneof win to keep accumulating the
                    // members here simplest.
                    let oneof_name = oneof_name.bind(py);
                    members_by_name.set_item(
                        oneof_name.to_str()?.to_string(),
                        Member {
                            attr: AttributeAccess::new(py, python_type, oneof_name),
                            field_number: None,
                        },
                    )?;
                }
                _ => members_by_name.set_item(
                    field.local_name.to_str(py)?.to_string(),
                    Member {
                        attr: AttributeAccess::new(py, python_type, field.local_name.bind(py)),
                        field_number: field.requires_presence.then_some(field.number),
                    },
                )?,
            }
        }
        let members = members_by_name
            .iter()
            .map(|(_, v)| {
                let member = v.cast::<Member>()?;
                Ok(member.get().clone_ref(py))
            })
            .collect::<PyResult<Vec<_>>>()?;

        let mut defaults = MessageDefaults {
            scalars: Vec::new(),
            lists: Vec::new(),
            dicts: Vec::new(),
        };
        for item in message_desc
            .getattr(&constants.defaults)?
            .cast::<PyList>()?
        {
            let name = item.get_item(0)?;
            let default = item.get_item(1)?;
            let member_any = members_by_name.get_item(&name)?.ok_or_else(|| {
                PyKeyError::new_err(format!("default value specified for unknown field {name}"))
            })?;
            // SAFETY - members is a private dict which we only insert Member into.
            let member = unsafe { member_any.cast_unchecked::<Member>() }.get();
            if default.is_instance_of::<PyList>() {
                defaults.lists.push(member.attr.clone_ref(py));
            } else if default.is_instance_of::<PyDict>() {
                defaults.dicts.push(member.attr.clone_ref(py));
            } else {
                defaults
                    .scalars
                    .push((member.attr.clone_ref(py), default.unbind()));
            }
        }
        Ok(Self {
            inner: Arc::new(MessageMarshalerInner {
                parser,
                serializer,
                members_by_name: members_by_name.unbind(),
                members,
                max_field_number,
                python_type: python_type.clone().unbind(),
                defaults,
                constants: constants.clone(),
            }),
        })
    }

    /// Merges wire bytes into an existing Python message instance.
    pub(super) fn merge_from_binary(
        &self,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        mut data: Bytes,
        ignore_unknown_fields: bool,
    ) -> PyResult<()> {
        self.inner.parser.merge_from_binary(
            py,
            message,
            &mut data,
            FromBinaryOpts {
                ignore_unknown_fields,
            },
            0,
        )
    }

    /// Serializes a Python message instance into protobuf wire bytes.
    pub(super) fn to_binary<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'_, NativeMessage>,
        write_unknown_fields: bool,
    ) -> PyResult<Bound<'py, PyBytes>> {
        let mut buffer = ReverseBuffer::new();
        self.inner.serializer.write_binary(
            py,
            message,
            &mut buffer,
            ToBinaryOpts {
                write_unknown_fields,
            },
        )?;
        Ok(buffer.into_py_bytes(py))
    }

    pub(super) fn new_unset_message<'py>(
        &self,
        python_type: &Bound<'py, PyType>,
    ) -> PyResult<Bound<'py, NativeMessage>> {
        let message = python_type
            .call_method1(&self.constants.dunder_new, (python_type,))?
            .cast_into::<NativeMessage>()?;
        Ok(message)
    }

    pub(super) fn new_empty_message<'py>(
        &self,
        py: Python<'py>,
        python_type: &Bound<'py, PyType>,
    ) -> PyResult<Bound<'py, NativeMessage>> {
        let message = self.new_unset_message(python_type)?;
        self.fill_empty_message(py, &message)?;
        Ok(message)
    }

    pub(super) fn fill_empty_message<'py>(
        &self,
        py: Python<'py>,
        message: &Bound<'py, NativeMessage>,
    ) -> PyResult<()> {
        for (attr, value) in &self.defaults.scalars {
            attr.set(message, value.bind(py))?;
        }
        for attr in &self.defaults.lists {
            attr.set(message, &PyList::empty(py))?;
        }
        for attr in &self.defaults.dicts {
            attr.set(message, &PyDict::new(py))?;
        }
        Ok(())
    }
}
