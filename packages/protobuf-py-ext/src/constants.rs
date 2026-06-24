use std::{ops::Deref, sync::Arc};

use pyo3::{
    Py, PyResult, Python,
    sync::PyOnceLock,
    types::{PyAnyMethods as _, PyString, PyType},
};

/// References to Python types.
pub(crate) struct Types {
    /// The class `protobuf._descriptors.DescField`.
    pub(crate) desc_field: Py<PyType>,
    /// The class `protobuf._descriptors.DescFieldValueScalar`.
    pub(crate) desc_field_value_scalar: Py<PyType>,
    /// The class `protobuf._descriptors.DescFieldValueEnum`.
    pub(crate) desc_field_value_enum: Py<PyType>,
    /// The class `protobuf._descriptors.DescFieldValueMessage`.
    pub(crate) desc_field_value_message: Py<PyType>,
    /// The class `protobuf._descriptors.DescFieldValueList`.
    pub(crate) desc_field_value_list: Py<PyType>,
    /// The class `protobuf._descriptors.DescFieldValueMap`.
    pub(crate) desc_field_value_map: Py<PyType>,
    /// The class `protobuf._descriptors.ScalarType`.
    pub(crate) scalar_type: Py<PyType>,
    /// The class `protobuf._descriptors.DescMessage`.
    pub(crate) desc_message: Py<PyType>,
    /// The class `protobuf._descriptors.DescEnum`.
    pub(crate) desc_enum: Py<PyType>,
}

/// Constants used for Python access, such as for instance checks or
/// creating objects. We also use it for string lookups instead of the intern!
/// macro to make sure we share across all call sites.
pub(crate) struct ConstantsInner {
    /// The string `_defaults`.
    pub(crate) defaults: Py<PyString>,
    /// The string `delimited_encoding`.
    pub(crate) delimited_encoding: Py<PyString>,
    /// The string `_desc`.
    pub(crate) desc: Py<PyString>,
    /// The string `element`.
    pub(crate) element: Py<PyString>,
    /// The string `enum`.
    pub(crate) enum_: Py<PyString>,
    /// The string `_ext_marshaler`.
    pub(crate) ext_marshaler: Py<PyString>,
    /// The string `_ext_value_type`.
    pub(crate) ext_value_type: Py<PyString>,
    /// The string `fields`.
    pub(crate) fields: Py<PyString>,
    /// The string `_fields_by_name`.
    pub(crate) fields_by_name: Py<PyString>,
    /// The string `key`.
    pub(crate) key: Py<PyString>,
    /// The string `local_name`.
    pub(crate) local_name: Py<PyString>,
    /// The string `message`.
    pub(crate) message: Py<PyString>,
    /// The string `number`.
    pub(crate) number: Py<PyString>,
    /// The string `oneof`.
    pub(crate) oneof: Py<PyString>,
    /// The string `_oneofs_by_local_name`.
    pub(crate) oneofs_by_local_name: Py<PyString>,
    /// The string `open`.
    pub(crate) open: Py<PyString>,
    /// The string `packed`.
    pub(crate) packed: Py<PyString>,
    /// The string `presence`.
    pub(crate) presence: Py<PyString>,
    /// The string `_requires_presence`.
    pub(crate) requires_presence: Py<PyString>,
    /// The string `scalar`.
    pub(crate) scalar: Py<PyString>,
    /// The string `type_name`.
    pub(crate) type_name: Py<PyString>,
    /// The string `type`.
    pub(crate) type_: Py<PyString>,
    /// The string `value`.
    pub(crate) value: Py<PyString>,
    /// The string `values`.
    pub(crate) values: Py<PyString>,

    /// The string `__new__`.
    pub(crate) dunder_new: Py<PyString>,

    /// Python types.
    pub(crate) types: Types,
}

#[derive(Clone)]
pub(crate) struct Constants {
    inner: Arc<ConstantsInner>,
}

impl Constants {
    pub(crate) fn get(py: Python<'_>) -> PyResult<Self> {
        static INSTANCE: PyOnceLock<Constants> = PyOnceLock::new();

        Ok(INSTANCE.get_or_try_init(py, || Self::new(py))?.clone())
    }

    #[allow(clippy::too_many_lines)]
    fn new(py: Python<'_>) -> PyResult<Self> {
        let mod_descriptors = py.import("protobuf._descriptors")?;
        Ok(Self {
            inner: Arc::new(ConstantsInner {
                defaults: PyString::new(py, "_defaults").unbind(),
                delimited_encoding: PyString::new(py, "delimited_encoding").unbind(),
                desc: PyString::new(py, "_desc").unbind(),
                element: PyString::new(py, "element").unbind(),
                enum_: PyString::new(py, "enum").unbind(),
                ext_marshaler: PyString::new(py, "_ext_marshaler").unbind(),
                ext_value_type: PyString::new(py, "_ext_value_type").unbind(),
                fields: PyString::new(py, "fields").unbind(),
                fields_by_name: PyString::new(py, "_fields_by_name").unbind(),
                key: PyString::new(py, "key").unbind(),
                local_name: PyString::new(py, "local_name").unbind(),
                message: PyString::new(py, "message").unbind(),
                number: PyString::new(py, "number").unbind(),
                oneof: PyString::new(py, "oneof").unbind(),
                oneofs_by_local_name: PyString::new(py, "_oneofs_by_local_name").unbind(),
                open: PyString::new(py, "open").unbind(),
                packed: PyString::new(py, "packed").unbind(),
                presence: PyString::new(py, "presence").unbind(),
                requires_presence: PyString::new(py, "_requires_presence").unbind(),
                scalar: PyString::new(py, "scalar").unbind(),
                type_name: PyString::new(py, "type_name").unbind(),
                type_: PyString::new(py, "type").unbind(),
                value: PyString::new(py, "value").unbind(),
                values: PyString::new(py, "values").unbind(),

                dunder_new: PyString::new(py, "__new__").unbind(),

                types: Types {
                    desc_field: mod_descriptors
                        .getattr("DescField")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_field_value_scalar: mod_descriptors
                        .getattr("DescFieldValueScalar")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_field_value_enum: mod_descriptors
                        .getattr("DescFieldValueEnum")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_field_value_message: mod_descriptors
                        .getattr("DescFieldValueMessage")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_field_value_list: mod_descriptors
                        .getattr("DescFieldValueList")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_field_value_map: mod_descriptors
                        .getattr("DescFieldValueMap")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    scalar_type: mod_descriptors
                        .getattr("ScalarType")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_message: mod_descriptors
                        .getattr("DescMessage")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                    desc_enum: mod_descriptors
                        .getattr("DescEnum")?
                        .cast::<PyType>()?
                        .clone()
                        .unbind(),
                },
            }),
        })
    }
}

impl Deref for Constants {
    type Target = ConstantsInner;

    fn deref(&self) -> &Self::Target {
        &self.inner
    }
}
