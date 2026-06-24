use pyo3::{
    Bound, Py, PyAny, PyErr, PyResult, Python,
    exceptions::PyAttributeError,
    pyfunction,
    types::{PyAnyMethods as _, PyString, PyType},
};

/// Access to a Python attribute, to optimize access to slots.
///
/// Message types use slots to store field values which lays them out directly
/// in the storage of a `PyObject` at offsets fixed at class creation time.
/// This means, it's also wasteful for us to always resolve the offset via
/// `getattr` despite precomputing marshaler descriptors. This type extracts the
/// offset when it can, and reads attributes directly if so.
///
/// It uses standard getattr for attributes that aren't in slots (shouldn't happen
/// in practice except for uncommon cases like a user-defined Message subclass that
/// doesn't go through `Registry`), and on abi3, free-threaded, and `PyPy` wheels.
/// Notably, this means it is not used for unreleased Python versions that we may not
/// be running tests for yet. This ensures that our direct use of cpython's struct
/// internals should be verified by tests, or not done at all.
pub(crate) enum AttributeAccess {
    Offset(usize),
    Name(Py<PyString>),
}

impl AttributeAccess {
    /// Resolves `attr_name` on `py_type`. Uses a cached slot offset when
    /// possible (non-ABI3 + Python 3.11+), otherwise stores the name to retrieve with
    /// `getattr`.
    pub(crate) fn new(
        _py: Python<'_>,
        py_type: &Bound<'_, PyType>,
        attr_name: &Bound<'_, PyString>,
    ) -> Self {
        if let Ok(Some(offset)) = Self::try_compute_slot_offset(py_type, attr_name) {
            Self::Offset(offset)
        } else {
            Self::Name(attr_name.clone().unbind())
        }
    }

    /// Returns the attribute value from `obj`.
    pub(crate) fn get<'py>(
        &self,
        py: Python<'py>,
        obj: &Bound<'py, PyAny>,
    ) -> PyResult<Bound<'py, PyAny>> {
        match self {
            Self::Offset(offset) => {
                #[allow(
                    clippy::cast_ptr_alignment,
                    reason = "slot offsets point to PyObject* fields which CPython aligns correctly"
                )]
                let raw = unsafe {
                    *((obj.as_ptr() as *const u8)
                        .add(*offset)
                        .cast::<*mut pyo3::ffi::PyObject>())
                };
                if raw.is_null() {
                    // Can't happen in practiec.
                    return Err(PyAttributeError::new_err("uninitialized slot"));
                }
                Ok(unsafe { Bound::from_borrowed_ptr(py, raw) })
            }
            Self::Name(name) => obj.getattr(name),
        }
    }

    /// Sets the attribute on `obj` to `value`.
    pub(crate) fn set(&self, obj: &Bound<'_, PyAny>, value: &Bound<'_, PyAny>) -> PyResult<()> {
        match self {
            Self::Offset(offset) => {
                #[allow(
                    clippy::cast_ptr_alignment,
                    reason = "slot offsets point to PyObject* fields which CPython aligns correctly"
                )]
                unsafe {
                    let slot_ptr = obj
                        .as_ptr()
                        .cast::<u8>()
                        .add(*offset)
                        .cast::<*mut pyo3::ffi::PyObject>();
                    let new_raw = value.as_ptr();
                    pyo3::ffi::Py_INCREF(new_raw);
                    let old_raw = *slot_ptr;
                    *slot_ptr = new_raw;
                    pyo3::ffi::Py_XDECREF(old_raw);
                }
                Ok(())
            }
            Self::Name(name) => generic_setattr(obj, name.bind(obj.py()), value),
        }
    }

    pub(crate) fn clone_ref(&self, py: Python<'_>) -> Self {
        match self {
            Self::Offset(offset) => Self::Offset(*offset),
            Self::Name(name) => Self::Name(name.clone_ref(py)),
        }
    }

    /// Attempts to resolve a `__slots__` member offset for `attr_name` on
    /// `py_type`.
    #[cfg(all(not(Py_LIMITED_API), Py_3_11, not(Py_GIL_DISABLED)))]
    fn try_compute_slot_offset(
        py_type: &Bound<'_, PyType>,
        attr_name: &Bound<'_, PyString>,
    ) -> PyResult<Option<usize>> {
        use pyo3::{
            ffi::{PyMemberDef, PyMemberDescrObject},
            types::{PyStringMethods as _, PyTypeMethods as _},
        };

        let Some(descriptor) = py_type.getattr_opt(attr_name)? else {
            return Ok(None);
        };
        if descriptor.get_type().name()?.to_str()? != "member_descriptor" {
            return Ok(None);
        }
        let offset = unsafe {
            let ptr = descriptor.as_ptr() as *const PyMemberDescrObject;
            let member: *mut PyMemberDef = (*ptr).d_member;
            if member.is_null() {
                return Ok(None);
            }
            let Ok(offset) = usize::try_from((*member).offset) else {
                return Ok(None);
            };
            offset
        };
        Ok(Some(offset))
    }

    #[cfg(not(all(not(Py_LIMITED_API), Py_3_11, not(Py_GIL_DISABLED))))]
    #[allow(
        clippy::unnecessary_wraps,
        reason = "signature must match the Py_3_11 variant"
    )]
    fn try_compute_slot_offset(
        _py_type: &Bound<'_, PyType>,
        _attr_name: &Bound<'_, PyString>,
    ) -> PyResult<Option<usize>> {
        Ok(None)
    }
}

/// Wrapper around raw ffi for `PyObject_GenericSetAttr`. It is not exposed natively by `PyO3` for being a relatively
/// niche API. So is this file - we end up needing it after implementing __setattr__ in native since the standard
/// setattr would call into it leading to infinite recursion.
#[pyfunction]
pub(crate) fn generic_setattr(
    obj: &Bound<'_, PyAny>,
    name: &Bound<'_, PyString>,
    value: &Bound<'_, PyAny>,
) -> PyResult<()> {
    let ret =
        unsafe { pyo3::ffi::PyObject_GenericSetAttr(obj.as_ptr(), name.as_ptr(), value.as_ptr()) };
    if ret != 0 {
        Err(PyErr::fetch(obj.py()))
    } else {
        Ok(())
    }
}
