use pyo3::{Bound, Py, PyAny, PyResult, Python, pyclass, pymethods, types::PyAnyMethods as _};

#[pyclass(module = "protobuf._oneof", frozen, generic)]
pub(crate) struct Oneof {
    #[pyo3(get)]
    pub(crate) field: Py<PyAny>,
    #[pyo3(get)]
    pub(crate) value: Py<PyAny>,
}

#[pymethods]
impl Oneof {
    #[new]
    pub(crate) fn new(field: &Bound<'_, PyAny>, value: &Bound<'_, PyAny>) -> Self {
        Self {
            field: field.clone().unbind(),
            value: value.clone().unbind(),
        }
    }

    fn __eq__(&self, py: Python<'_>, other: &Bound<'_, PyAny>) -> PyResult<bool> {
        if let Ok(other) = other.cast::<Oneof>() {
            let other = other.get();
            Ok(self.field.bind(py).eq(other.field.bind(py))?
                && self.value.bind(py).eq(other.value.bind(py))?)
        } else {
            Ok(false)
        }
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        Ok(format!(
            "Oneof(field={field}, value={value})",
            field = self.field.bind(py).repr()?,
            value = self.value.bind(py).repr()?,
        ))
    }

    #[classattr]
    fn __match_args__() -> (&'static str, &'static str) {
        // Populated as a classattr once when creating type so no need to intern
        // PyString.
        ("field", "value")
    }
}
