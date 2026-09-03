use pyo3::{
    Bound, IntoPyObject as _, IntoPyObjectExt as _, Py, PyAny, PyResult, Python,
    exceptions::PyTypeError,
    pyclass, pyfunction, pymethods,
    sync::PyOnceLock,
    types::{
        PyAnyMethods as _, PyByteArray, PyByteArrayMethods as _, PyBytes, PyBytesMethods as _,
        PyDict, PyDictMethods as _, PyList, PyListMethods as _, PyString, PyStringMethods as _,
        PyTuple, PyType, PyTypeMethods as _,
    },
};

use crate::{
    attribute_access::generic_setattr,
    bitset::BitSet,
    buffer::Buffer,
    constants::Constants,
    json_parse::{FromJsonOpts, merge_from_json, read_message_from_tree},
    json_serialize::JsonOpts,
    json_sink::PyValueSink,
    marshaler::{Member, MessageMarshaler},
    oneof::Oneof,
};

/// Base class inserted into Python message types to provide accelerated functions.
///
/// Messages match definitions on the Python Message class. By having priority
/// in method resolution order, the accelerated definitions are used instead of
/// pure Python.
#[pyclass(subclass, frozen, weakref, module = "protobuf_ext")]
pub(super) struct NativeMessage {
    /// Pointer to the marshaler for this message type. Only missing for bootstraps protos.
    marshaler: Option<MessageMarshaler>,

    present: BitSet,
    unknown_fields: PyOnceLock<Py<PyDict>>,
}

#[pymethods]
impl NativeMessage {
    #[new]
    #[classmethod]
    #[pyo3(signature = (*_args, **_kwargs))]
    fn new(
        cls: &Bound<'_, PyType>,
        py: Python<'_>,
        _args: &Bound<'_, PyTuple>,
        _kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<Self> {
        let marshaler_any = cls.getattr_opt(&Constants::get(py)?.ext_marshaler)?;
        let marshaler = if let Some(marshaler_any) = &marshaler_any {
            Some(marshaler_any.cast::<MessageMarshaler>()?.get().clone())
        } else {
            None
        };
        let present = if let Some(marshaler_any) = &marshaler_any {
            let marshaler = marshaler_any.cast::<MessageMarshaler>()?;
            BitSet::new(marshaler.get().max_field_number)
        } else {
            // Don't know the maximum field number yet. This only happens for bootstrap protos.
            BitSet::new(u32::MAX)
        };
        Ok(Self {
            marshaler,
            present,
            unknown_fields: PyOnceLock::new(),
        })
    }

    #[pyo3(signature = (**kwargs))]
    fn __init__(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        kwargs: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<()> {
        let marshaler = NativeMessage::get_marshaler(slf)?;
        marshaler.fill_empty_message(py, slf)?;
        if let Some(kwargs) = kwargs {
            for (key, value) in kwargs {
                if value.is_none() {
                    continue;
                }
                if let Some(member_any) = marshaler.members_by_name.bind(py).get_item(&key)? {
                    // SAFETY - members is a private dict which we only insert Member into.
                    let member = unsafe { member_any.cast_unchecked::<Member>() }.get();
                    member.attr.set(slf, &value)?;
                    if let Some(field_number) = member.field_number {
                        slf.get().add_present_field(field_number);
                    }
                } else {
                    return Err(PyTypeError::new_err(format!(
                        "{}.__init__() got an unexpected keyword argument '{}'",
                        slf.get_type().qualname()?,
                        key
                    )));
                }
            }
        }
        Ok(())
    }

    #[classmethod]
    #[pyo3(signature = (data, *, ignore_unknown_fields = false))]
    fn from_binary<'py>(
        cls: &Bound<'py, PyType>,
        py: Python<'py>,
        data: Buffer,
        ignore_unknown_fields: bool,
    ) -> PyResult<Bound<'py, NativeMessage>> {
        let data = data.into_inner();
        let constants = Constants::get(py)?;
        let marshaler_any = cls.getattr(&constants.ext_marshaler)?;
        let marshaler = marshaler_any.cast::<MessageMarshaler>()?.get();
        let message = marshaler.new_empty_message(py, cls)?;
        let slf = message.cast::<NativeMessage>()?;
        marshaler.merge_from_binary(py, slf, data, ignore_unknown_fields)?;
        Ok(message)
    }

    #[pyo3(signature = (*, write_unknown_fields = true))]
    fn to_binary<'py>(
        slf: &Bound<'_, Self>,
        py: Python<'py>,
        write_unknown_fields: bool,
    ) -> PyResult<Bound<'py, PyBytes>> {
        NativeMessage::get_marshaler(slf)?.to_binary(py, slf, write_unknown_fields)
    }

    #[pyo3(signature = (*, registry = None, always_emit_implicit = false, print_enums_as_ints = false, use_proto_field_name = false))]
    fn to_json(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        registry: Option<Py<PyAny>>,
        always_emit_implicit: bool,
        print_enums_as_ints: bool,
        use_proto_field_name: bool,
    ) -> PyResult<Py<PyString>> {
        let marshaler = NativeMessage::get_marshaler(slf)?;
        let opts = JsonOpts {
            always_emit_implicit,
            print_enums_as_ints,
            use_proto_field_name,
            registry,
        };
        marshaler.to_json_string(py, slf, &opts)
    }

    #[classmethod]
    #[pyo3(signature = (json, *, ignore_unknown_fields = false, registry = None))]
    fn from_json<'py>(
        cls: &Bound<'py, PyType>,
        py: Python<'py>,
        json: &Bound<'py, PyAny>,
        ignore_unknown_fields: bool,
        registry: Option<Py<PyAny>>,
    ) -> PyResult<Bound<'py, NativeMessage>> {
        let constants = Constants::get(py)?;
        let marshaler_any = cls.getattr(&constants.ext_marshaler)?;
        let marshaler = marshaler_any.cast::<MessageMarshaler>()?.get().clone();
        let message = marshaler.new_empty_message(py, cls)?;
        parse_json_into(
            py,
            &marshaler,
            &message,
            json,
            ignore_unknown_fields,
            registry,
        )?;
        Ok(message)
    }

    #[pyo3(signature = (json, *, ignore_unknown_fields = false, registry = None))]
    fn _merge_from_json(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        json: &Bound<'_, PyAny>,
        ignore_unknown_fields: bool,
        registry: Option<Py<PyAny>>,
    ) -> PyResult<()> {
        let marshaler = NativeMessage::get_marshaler(slf)?;
        parse_json_into(py, &marshaler, slf, json, ignore_unknown_fields, registry)
    }

    #[pyo3(signature = (*, registry = None, always_emit_implicit = false, print_enums_as_ints = false, use_proto_field_name = false))]
    fn _to_json_value<'py>(
        slf: &Bound<'py, Self>,
        py: Python<'py>,
        registry: Option<Py<PyAny>>,
        always_emit_implicit: bool,
        print_enums_as_ints: bool,
        use_proto_field_name: bool,
    ) -> PyResult<Bound<'py, PyAny>> {
        let marshaler = NativeMessage::get_marshaler(slf)?;
        let opts = JsonOpts {
            always_emit_implicit,
            print_enums_as_ints,
            use_proto_field_name,
            registry,
        };
        let mut sink = PyValueSink::new(py);
        marshaler.write_json(py, slf, &mut sink, &opts, 0)?;
        sink.finish()
    }

    #[classmethod]
    #[pyo3(signature = (data, *, ignore_unknown_fields = false, registry = None))]
    fn _from_json_value<'py>(
        cls: &Bound<'py, PyType>,
        py: Python<'py>,
        data: Bound<'py, PyAny>,
        ignore_unknown_fields: bool,
        registry: Option<Py<PyAny>>,
    ) -> PyResult<Bound<'py, NativeMessage>> {
        let constants = Constants::get(py)?;
        let marshaler_any = cls.getattr(&constants.ext_marshaler)?;
        let marshaler = marshaler_any.cast::<MessageMarshaler>()?.get().clone();
        let message = marshaler.new_empty_message(py, cls)?;
        let opts = FromJsonOpts {
            ignore_unknown_fields,
            registry,
        };
        read_message_from_tree(py, &marshaler, &message, data, &opts)?;
        Ok(message)
    }

    fn __setattr__(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        name: &Bound<'_, PyString>,
        value: &Bound<'_, PyAny>,
    ) -> PyResult<()> {
        let marshaler = NativeMessage::get_marshaler(slf)?;

        if let Some(member_any) = marshaler.members_by_name.bind(py).get_item(name)? {
            // SAFETY - members is a private dict which we only insert Member into.
            let member = unsafe { member_any.cast_unchecked::<Member>() }.get();
            member.attr.set(slf, value)?;
            if let Some(field_number) = member.field_number {
                slf.get().add_present_field(field_number);
            }
        } else {
            // Not a known field. Delegate to Python for error message.
            generic_setattr(slf, name, value)?;
        }

        Ok(())
    }

    fn __copy__<'py>(
        slf: &Bound<'py, Self>,
        py: Python<'py>,
    ) -> PyResult<Bound<'py, NativeMessage>> {
        let marshaler = NativeMessage::get_marshaler(slf)?;

        let new = marshaler.new_unset_message(&slf.get_type())?;
        for member in &marshaler.members {
            let value = member.attr.get(py, slf)?;
            member.attr.set(&new, &value)?;
        }

        new.get().present.set_all(&slf.get().present);
        copy_unknown_fields(py, &new, slf)?;

        Ok(new)
    }

    fn _merge_from_binary(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        data: Buffer,
        ignore_unknown_fields: bool,
    ) -> PyResult<()> {
        let data = data.into_inner();
        NativeMessage::get_marshaler(slf)?.merge_from_binary(py, slf, data, ignore_unknown_fields)
    }

    fn __deepcopy__<'py>(
        slf: &Bound<'py, Self>,
        py: Python<'py>,
        _memo: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<Bound<'py, Self>> {
        let marshaler = NativeMessage::get_marshaler(slf)?;

        let new = marshaler.new_unset_message(&slf.get_type())?;
        for member in &marshaler.members {
            let value = member.attr.get(py, slf)?;
            let value = if let Ok(value_message) = value.cast::<NativeMessage>() {
                NativeMessage::__deepcopy__(value_message, py, None)?.into_any()
            } else if let Ok(value_list) = value.cast::<PyList>() {
                let list = PyList::empty(py);
                deepcopy_list(py, &list, value_list)?;
                list.into_any()
            } else if let Ok(value_dict) = value.cast::<PyDict>() {
                let dict = PyDict::new(py);
                deepcopy_dict(py, &dict, value_dict)?;
                dict.into_any()
            } else if let Ok(oneof) = value.cast::<Oneof>() {
                deepcopy_oneof(py, oneof)?
            } else {
                value
            };
            member.attr.set(&new, &value)?;
        }
        new.get().present.set_all(&slf.get().present);
        copy_unknown_fields(py, &new, slf)?;

        Ok(new)
    }

    fn __eq__(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        other: &Bound<'_, NativeMessage>,
    ) -> PyResult<bool> {
        if !other.is_instance(&slf.get_type())? {
            return Ok(false);
        }
        let marshaler = NativeMessage::get_marshaler(slf)?;

        for member in &marshaler.members {
            if let Some(field_number) = member.field_number {
                let slf_present = slf.get().has_present_field(field_number);
                let other_present = other.get().has_present_field(field_number);
                if slf_present != other_present {
                    return Ok(false);
                }
                if !slf_present {
                    continue;
                }
            }
            let slf_value = member.attr.get(py, slf)?;
            let other_value = member.attr.get(py, other)?;
            if !slf_value.is(&other_value) && !slf_value.eq(&other_value)? {
                return Ok(false);
            }
        }

        Ok(true)
    }

    fn _merge_from(
        slf: &Bound<'_, Self>,
        py: Python<'_>,
        source: &Bound<'_, Self>,
        ignore_unknown_fields: bool,
    ) -> PyResult<()> {
        let marshaler = NativeMessage::get_marshaler(slf)?;
        if !source.is_instance(marshaler.python_type.bind(py))? {
            return Err(PyTypeError::new_err(format!(
                "invalid source message type, expected {}, got {}",
                marshaler.python_type.bind(py).qualname()?,
                source.get_type().qualname()?
            )));
        }
        let source_present = &source.get().present;
        slf.get().present.set_all(source_present);

        for member in &marshaler.members {
            if let Some(field_number) = member.field_number
                && !source_present.get(field_number)
            {
                continue;
            }

            let source_value = member.attr.get(py, source)?;
            if source_value.is_none() {
                continue;
            }

            // Unlike in Python, we inspect value types directly without using descriptor information. While there
            // may be some performance benefit to not having to lookup marshalers on every message copy, especially
            // for containers, we don't know if the user gave a correct message and risk segfaults if doing that
            // instead of duck-typing errors.
            if let Ok(source_value_message) = source_value.cast::<NativeMessage>() {
                let target_value_any = member.attr.get(py, slf)?;
                let target_value_message = if target_value_any.is_none() {
                    let source_value_marshaler =
                        NativeMessage::get_marshaler(source_value_message)?;
                    let target_value = source_value_marshaler
                        .new_empty_message(py, &source_value_message.get_type())?;
                    member.attr.set(slf, &target_value)?;
                    target_value
                } else {
                    target_value_any.cast_into::<NativeMessage>()?
                };
                NativeMessage::_merge_from(
                    &target_value_message,
                    py,
                    source_value_message,
                    ignore_unknown_fields,
                )?;
            } else if let Ok(source_value_list) = source_value.cast::<PyList>() {
                let target_value_any = member.attr.get(py, slf)?;
                let target_value_list = target_value_any.cast::<PyList>()?;
                deepcopy_list(py, target_value_list, source_value_list)?;
            } else if let Ok(source_value_dict) = source_value.cast::<PyDict>() {
                let target_value_any = member.attr.get(py, slf)?;
                let target_value_dict = target_value_any.cast::<PyDict>()?;
                deepcopy_dict(py, target_value_dict, source_value_dict)?;
            } else if let Ok(oneof) = source_value.cast::<Oneof>() {
                let value = deepcopy_oneof(py, oneof)?;
                member.attr.set(slf, &value)?;
            } else {
                member.attr.set(slf, &source_value)?;
            }
        }

        if !ignore_unknown_fields
            && let Some(source_unknown_fields_unbound) = source.get().unknown_fields.get(py)
        {
            let source_unknown_fields = source_unknown_fields_unbound.bind(py);
            let self_unknown_fields_unbound = slf.get().get_or_init_unknown_fields(py);
            let self_unknown_fields = self_unknown_fields_unbound.bind(py);
            for (key, value) in source_unknown_fields {
                let list = if let Some(existing) = self_unknown_fields.get_item(&key)? {
                    existing.cast_into::<PyList>()?
                } else {
                    let new_list = PyList::empty(py);
                    self_unknown_fields.set_item(key, &new_list)?;
                    new_list
                };
                for item in value.cast::<PyList>()? {
                    list.append(item)?;
                }
            }
        }

        Ok(())
    }

    fn _get_field_number_present(&self, field_number: u32) -> bool {
        self.present.get(field_number)
    }

    fn _set_field_number_present(&self, field_number: u32) {
        self.present.set(field_number, true);
    }

    fn _clear_field_number_present(&self, field_number: u32) {
        self.present.set(field_number, false);
    }

    #[getter]
    fn _present<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        let list = PyList::empty(py);
        self.present.for_each(|i| list.append(i))?;
        Ok(list)
    }

    #[pyo3(name = "_get_or_init_unknown_fields")]
    pub(super) fn get_or_init_unknown_fields(&self, py: Python<'_>) -> Py<PyDict> {
        self.unknown_fields
            .get_or_init(py, || PyDict::new(py).unbind())
            .clone_ref(py)
    }

    #[getter(_unknown_fields)]
    pub(super) fn unknown_fields(&self, py: Python<'_>) -> Option<Py<PyDict>> {
        self.unknown_fields.get(py).map(|v| v.clone_ref(py))
    }
}

impl NativeMessage {
    pub(super) fn add_present_field(&self, field_number: u32) {
        self.present.set(field_number, true);
    }

    pub(crate) fn clear_present_field(&self, field_number: u32) {
        self.present.set(field_number, false);
    }

    pub(super) fn has_present_field(&self, field_number: u32) -> bool {
        self.present.get(field_number)
    }

    pub(crate) fn get_marshaler(slf: &Bound<'_, Self>) -> PyResult<MessageMarshaler> {
        if let Some(marshaler) = &slf.get().marshaler {
            Ok(marshaler.clone())
        } else {
            Ok(slf
                .getattr(&Constants::get(slf.py())?.ext_marshaler)?
                .cast::<MessageMarshaler>()?
                .get()
                .clone())
        }
    }
}

#[pyfunction]
pub(super) fn initialize_message_type(
    py: Python<'_>,
    message_type: &Bound<'_, PyType>,
) -> PyResult<()> {
    let constants = Constants::get(py)?;
    if message_type
        .getattr_opt(&constants.ext_marshaler)?
        .is_some()
    {
        return Ok(());
    }

    let constants = Constants::get(py)?;
    let message_desc = message_type.getattr(&constants.desc)?;
    let marshaler = MessageMarshaler::new(py, &message_desc, &constants)?.into_pyobject(py)?;
    message_type.setattr(&constants.ext_marshaler, marshaler)?;
    Ok(())
}

/// Parses JSON (`str`/`bytes`/`bytearray`) into `message`.
fn parse_json_into<'py>(
    py: Python<'py>,
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    json: &Bound<'py, PyAny>,
    ignore_unknown_fields: bool,
    registry: Option<Py<PyAny>>,
) -> PyResult<()> {
    let opts = FromJsonOpts {
        ignore_unknown_fields,
        registry,
    };
    if let Ok(text) = json.cast::<PyString>() {
        merge_from_json(py, marshaler, message, text.to_str()?.as_bytes(), &opts)
    } else if let Ok(bytes) = json.cast::<PyBytes>() {
        merge_from_json(py, marshaler, message, bytes.as_bytes(), &opts)
    } else if let Ok(bytearray) = json.cast::<PyByteArray>() {
        let owned = bytearray.to_vec();
        merge_from_json(py, marshaler, message, &owned, &opts)
    } else {
        Err(PyTypeError::new_err(format!(
            "json must be str, bytes, or bytearray, got {}",
            json.get_type()
        )))
    }
}

fn deepcopy_list(
    py: Python<'_>,
    target: &Bound<'_, PyList>,
    source: &Bound<'_, PyList>,
) -> PyResult<()> {
    for item in source {
        if let Ok(message) = item.cast::<NativeMessage>() {
            let copied = NativeMessage::__deepcopy__(message, py, None)?;
            target.append(copied)?;
        } else {
            target.append(item)?;
        }
    }
    Ok(())
}

fn deepcopy_dict(
    py: Python<'_>,
    target: &Bound<'_, PyDict>,
    source: &Bound<'_, PyDict>,
) -> PyResult<()> {
    for (key, value) in source {
        if let Ok(message) = value.cast::<NativeMessage>() {
            let copied = NativeMessage::__deepcopy__(message, py, None)?;
            target.set_item(key, copied)?;
        } else {
            target.set_item(key, value)?;
        }
    }
    Ok(())
}

fn deepcopy_oneof<'py>(
    py: Python<'py>,
    source_value: &Bound<'py, Oneof>,
) -> PyResult<Bound<'py, PyAny>> {
    let value = source_value.get().value.bind(py);
    if let Ok(value_message) = value.cast::<NativeMessage>() {
        let field = source_value.get().field.bind(py);
        let copied = NativeMessage::__deepcopy__(value_message, py, None)?;
        Oneof::new(field, &copied.into_any()).into_bound_py_any(py)
    } else {
        Ok(source_value.clone().into_any())
    }
}

fn copy_unknown_fields(
    py: Python<'_>,
    target: &Bound<'_, NativeMessage>,
    source: &Bound<'_, NativeMessage>,
) -> PyResult<()> {
    if let Some(source_unknown_fields) = source.get().unknown_fields.get(py) {
        let target_unknown_fields_unbound = target.get().get_or_init_unknown_fields(py);
        let target_unknown_fields = target_unknown_fields_unbound.bind(py);
        for (key, value) in source_unknown_fields.bind(py) {
            let list = value.cast::<PyList>()?;
            target_unknown_fields.set_item(key, PyList::new(py, list)?)?;
        }
    }
    Ok(())
}
