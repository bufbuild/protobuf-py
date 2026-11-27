//! Input abstraction for JSON parsing, to read from either a string or Python object.

use jiter::{Jiter, JiterError, JiterErrorType, JsonErrorType, NumberAny, NumberInt, Peek};
use pyo3::{
    Bound, IntoPyObject as _, PyAny, PyErr, PyResult, Python,
    exceptions::{PyOverflowError, PyTypeError, PyValueError},
    types::{
        PyAnyMethods as _, PyBool, PyDict, PyFloat, PyInt, PyList, PyString, PyStringMethods as _,
    },
};

/// The kind of the next JSON value, as reported by `peek`.
#[derive(Clone, Copy, PartialEq, Eq)]
pub(crate) enum JsonKind {
    Null,
    Bool,
    Number,
    String,
    Array,
    Object,
}

/// A streaming source of JSON tokens producing Python values bound to `'py`.
pub(crate) trait JsonSource<'py> {
    /// The GIL token for values produced by this source.
    fn py(&self) -> Python<'py>;
    /// Reports the kind of the next value without consuming it.
    fn peek(&mut self) -> PyResult<JsonKind>;
    // Reads a JSON null.
    fn next_null(&mut self) -> PyResult<()>;
    // Reads a JSON boolean.
    fn next_bool(&mut self) -> PyResult<bool>;
    /// Reads a JSON number as a Python `int` or `float` object.
    fn next_number(&mut self) -> PyResult<Bound<'py, PyAny>>;
    // Reads a JSON number.
    fn next_float(&mut self) -> PyResult<f64>;
    /// Reads a JSON string as a Python string object.
    fn next_py_str(&mut self) -> PyResult<Bound<'py, PyString>>;

    /// Reads a JSON string as a Rust str, calling the function with it.
    fn with_next_str<R>(&mut self, f: impl FnOnce(&str) -> PyResult<R>) -> PyResult<R>;

    /// Consumes an array, calling the function for each element. The function must consume (read or skip) the element.
    fn for_each_array_item(&mut self, f: impl FnMut(&mut Self) -> PyResult<()>) -> PyResult<()>;

    /// Consumes an object, calling the function for each key. The function
    /// must consume (read or skip) the value for the key.
    fn for_each_object_key(
        &mut self,
        f: impl FnMut(&str, &mut Self) -> PyResult<()>,
    ) -> PyResult<()>;

    /// Skips the next value entirely.
    fn skip(&mut self) -> PyResult<()>;
}

/// A `JsonSource` backed by the `jiter` pull parser over raw JSON bytes.
pub(crate) struct JiterSource<'a> {
    jiter: Jiter<'a>,
    data: &'a [u8],
    py: Python<'a>,
    buf: String,
}

impl<'a> JiterSource<'a> {
    pub(crate) fn new(py: Python<'a>, data: &'a [u8]) -> Self {
        Self {
            jiter: Jiter::new(data),
            data,
            py,
            buf: String::new(),
        }
    }

    /// Consumes trailing whitespace and errors on trailing content, matching
    /// `json.loads`.
    pub(crate) fn finish(&mut self) -> PyResult<()> {
        let (py, data) = (self.py, self.data);
        self.jiter
            .finish()
            .map_err(|err| jiter_decode_error(py, data, &err))
    }
}

/// Checks that `data` is a single JSON document, raising the
/// `json.JSONDecodeError` that parsing it fails with.
pub(crate) fn check_syntax(py: Python<'_>, data: &[u8]) -> PyResult<()> {
    let mut jiter = Jiter::new(data);
    match jiter.next_skip().and_then(|()| jiter.finish()) {
        Ok(()) => Ok(()),
        // Python's parsing allows deeper nesting than jiter, so it checks
        // what is past jiter's limit.
        Err(JiterError {
            error_type: JiterErrorType::JsonError(JsonErrorType::RecursionLimitExceeded),
            ..
        }) => check_syntax_in_python(py, data),
        Err(err) => Err(jiter_decode_error(py, data, &err)),
    }
}

/// Parses `data` as protobuf-py's Python code does, raising the
/// `json.JSONDecodeError` that it fails with, if any.
fn check_syntax_in_python(py: Python<'_>, data: &[u8]) -> PyResult<()> {
    let Ok(text) = std::str::from_utf8(data) else {
        return Ok(());
    };
    let json_decode_error = py.import("json")?.getattr("JSONDecodeError")?;
    match py
        .import("protobuf._from_json")
        .and_then(|module| module.call_method1("parse_json_text", (text,)))
    {
        Err(err) if err.is_instance(py, &json_decode_error) => Err(err),
        _ => Ok(()),
    }
}

/// Converts a jiter error into a `json.JSONDecodeError` to preserve exception
/// hierarchy with Python.
fn jiter_decode_error(py: Python<'_>, data: &[u8], err: &JiterError) -> PyErr {
    let message = err.error_type.to_string();
    let doc = String::from_utf8_lossy(data);
    let build = || -> PyResult<PyErr> {
        let json_mod = py.import("json")?;
        let exc = json_mod.getattr("JSONDecodeError")?;
        let obj = exc.call1((message.as_str(), doc.as_ref(), err.index))?;
        Ok(PyErr::from_value(obj))
    };
    match build() {
        Ok(err) | Err(err) => err,
    }
}

fn peek_to_kind(peek: Peek) -> JsonKind {
    match peek {
        Peek::Null => JsonKind::Null,
        Peek::True | Peek::False => JsonKind::Bool,
        Peek::String => JsonKind::String,
        Peek::Array => JsonKind::Array,
        Peek::Object => JsonKind::Object,
        // Numbers (including the bare `Infinity`/`NaN` peeks, which error when
        // actually read since `allow_inf_nan` is off).
        _ => JsonKind::Number,
    }
}

fn number_any_to_py(py: Python<'_>, number: NumberAny) -> PyResult<Bound<'_, PyAny>> {
    match number {
        NumberAny::Int(NumberInt::Int(value)) => Ok(PyInt::new(py, value).into_any()),
        NumberAny::Int(NumberInt::BigInt(value)) => Ok(value.into_pyobject(py)?.into_any()),
        NumberAny::Float(value) => Ok(PyFloat::new(py, value).into_any()),
    }
}

impl<'py> JsonSource<'py> for JiterSource<'py> {
    fn py(&self) -> Python<'py> {
        self.py
    }

    fn peek(&mut self) -> PyResult<JsonKind> {
        let (py, data) = (self.py, self.data);
        let peek = self
            .jiter
            .peek()
            .map_err(|err| jiter_decode_error(py, data, &err))?;
        Ok(peek_to_kind(peek))
    }

    fn next_null(&mut self) -> PyResult<()> {
        let (py, data) = (self.py, self.data);
        self.jiter
            .next_null()
            .map_err(|err| jiter_decode_error(py, data, &err))
    }

    fn next_bool(&mut self) -> PyResult<bool> {
        let (py, data) = (self.py, self.data);
        self.jiter
            .next_bool()
            .map_err(|err| jiter_decode_error(py, data, &err))
    }

    fn next_number(&mut self) -> PyResult<Bound<'py, PyAny>> {
        let (py, data) = (self.py, self.data);
        let number = self
            .jiter
            .next_number()
            .map_err(|err| jiter_decode_error(py, data, &err))?;
        number_any_to_py(py, number)
    }

    fn next_float(&mut self) -> PyResult<f64> {
        let (py, data) = (self.py, self.data);
        let start = self.jiter.current_index();
        let value = self
            .jiter
            .next_float()
            .map_err(|err| jiter_decode_error(py, data, &err))?;
        // Python converts an integer with float(), which raises for one too
        // large for a double instead of returning infinity.
        if value.is_infinite()
            && !self
                .jiter
                .slice_to_current(start)
                .iter()
                .any(|b| matches!(b, b'.' | b'e' | b'E'))
        {
            return Err(PyOverflowError::new_err(
                "int too large to convert to float",
            ));
        }
        Ok(value)
    }

    fn next_py_str(&mut self) -> PyResult<Bound<'py, PyString>> {
        let py = self.py;
        self.with_next_str(|s| Ok(PyString::new(py, s)))
    }

    fn with_next_str<R>(&mut self, f: impl FnOnce(&str) -> PyResult<R>) -> PyResult<R> {
        let (py, data) = (self.py, self.data);
        let value = self
            .jiter
            .next_str()
            .map_err(|err| jiter_decode_error(py, data, &err))?;
        f(value)
    }

    fn for_each_array_item(
        &mut self,
        mut f: impl FnMut(&mut Self) -> PyResult<()>,
    ) -> PyResult<()> {
        let (py, data) = (self.py, self.data);
        let mut not_done = self
            .jiter
            .next_array()
            .map_err(|err| jiter_decode_error(py, data, &err))?
            .is_some();
        while not_done {
            f(self)?;
            not_done = self
                .jiter
                .array_step()
                .map_err(|err| jiter_decode_error(py, data, &err))?
                .is_some();
        }
        Ok(())
    }

    fn for_each_object_key(
        &mut self,
        mut f: impl FnMut(&str, &mut Self) -> PyResult<()>,
    ) -> PyResult<()> {
        let (py, data) = (self.py, self.data);
        // Jiter unescapes the key into temporary storage, which is also used
        // when reading a value which would clobber it. So to present the key
        // and allow value reading, a copy of some sort is required. We use
        // a reused buffer to reduce allocations for it.
        let mut key_buf = std::mem::take(&mut self.buf);
        let mut maybe_key = self
            .jiter
            .next_object()
            .map_err(|err| jiter_decode_error(py, data, &err))?;
        while let Some(key) = maybe_key {
            key_buf.clear();
            key_buf.push_str(key);
            f(&key_buf, self)?;
            maybe_key = self
                .jiter
                .next_key()
                .map_err(|err| jiter_decode_error(py, data, &err))?;
        }
        self.buf = key_buf;
        Ok(())
    }

    fn skip(&mut self) -> PyResult<()> {
        let (py, data) = (self.py, self.data);
        self.jiter
            .next_skip()
            .map_err(|err| jiter_decode_error(py, data, &err))
    }
}

/// Raised for a JSON structural type that a field cannot accept.
pub(crate) fn unexpected_json_type() -> PyErr {
    PyValueError::new_err("unexpected json type")
}

/// A `JsonSource` that walks an already-materialized Python tree.
pub(crate) struct PyTreeSource<'py> {
    py: Python<'py>,
    /// The value positioned to be read next, if any.
    current: Option<Bound<'py, PyAny>>,
}

impl<'py> PyTreeSource<'py> {
    pub(crate) fn new(py: Python<'py>, root: Bound<'py, PyAny>) -> Self {
        Self {
            py,
            current: Some(root),
        }
    }

    fn take_current(&mut self) -> PyResult<Bound<'py, PyAny>> {
        self.current
            .take()
            .ok_or_else(|| PyValueError::new_err("unexpected end of JSON tree"))
    }
}

impl<'py> JsonSource<'py> for PyTreeSource<'py> {
    fn py(&self) -> Python<'py> {
        self.py
    }

    fn peek(&mut self) -> PyResult<JsonKind> {
        let value = self
            .current
            .as_ref()
            .ok_or_else(|| PyValueError::new_err("unexpected end of JSON tree"))?;
        if value.is_none() {
            Ok(JsonKind::Null)
        } else if value.is_instance_of::<PyBool>() {
            Ok(JsonKind::Bool)
        } else if value.is_instance_of::<PyInt>() || value.is_instance_of::<PyFloat>() {
            Ok(JsonKind::Number)
        } else if value.is_instance_of::<PyString>() {
            Ok(JsonKind::String)
        } else if value.is_instance_of::<PyList>() {
            Ok(JsonKind::Array)
        } else if value.is_instance_of::<PyDict>() {
            Ok(JsonKind::Object)
        } else {
            Err(PyTypeError::new_err(format!(
                "unexpected type in JSON tree: {}",
                value.get_type()
            )))
        }
    }

    fn next_null(&mut self) -> PyResult<()> {
        let value = self.take_current()?;
        if value.is_none() {
            Ok(())
        } else {
            Err(unexpected_json_type())
        }
    }

    fn next_bool(&mut self) -> PyResult<bool> {
        self.take_current()?.extract::<bool>()
    }

    fn next_number(&mut self) -> PyResult<Bound<'py, PyAny>> {
        self.take_current()
    }

    fn next_float(&mut self) -> PyResult<f64> {
        self.take_current()?.extract::<f64>()
    }

    fn next_py_str(&mut self) -> PyResult<Bound<'py, PyString>> {
        let value = self.take_current()?;
        Ok(value.cast_into::<PyString>()?)
    }

    fn with_next_str<R>(&mut self, f: impl FnOnce(&str) -> PyResult<R>) -> PyResult<R> {
        let value = self.next_py_str()?;
        let s = value.to_str()?;
        f(s)
    }

    fn for_each_array_item(
        &mut self,
        mut f: impl FnMut(&mut Self) -> PyResult<()>,
    ) -> PyResult<()> {
        let list = self.take_current()?.cast_into::<PyList>()?;
        for item in list {
            self.current = Some(item);
            f(self)?;
            self.current = None;
        }
        Ok(())
    }

    fn for_each_object_key(
        &mut self,
        mut f: impl FnMut(&str, &mut Self) -> PyResult<()>,
    ) -> PyResult<()> {
        let dict = self.take_current()?.cast_into::<PyDict>()?;
        for (key, value) in dict {
            let key = key
                .extract::<&str>()
                .map_err(|_| PyTypeError::new_err("JSON object keys must be strings"))?;
            self.current = Some(value);
            f(key, self)?;
            self.current = None;
        }
        Ok(())
    }

    fn skip(&mut self) -> PyResult<()> {
        self.current = None;
        Ok(())
    }
}
