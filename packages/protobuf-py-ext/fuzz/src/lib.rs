//! What the fuzz targets share: an embedded interpreter running protobuf-py
//! with the instrumented extension, the message types to fuzz, and the checks
//! that the extension and protobuf-py's Python code marshal alike.
//!
//! The extension only works on Python message classes, so the targets cannot
//! call it without an interpreter. The interpreter itself is not instrumented,
//! so coverage only guides fuzzing of the extension.
//!
//! The generated message classes extend the extension's `NativeMessage`
//! before protobuf-py's `Message`, which the extension overrides the
//! marshaling methods of. Calling `Message`'s methods directly runs the
//! Python marshaling on the same messages.

use std::ffi::CString;
use std::path::{Path, PathBuf};
use std::sync::LazyLock;

use pyo3::exceptions::{PyEOFError, PyOverflowError, PyRecursionError, PyTypeError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyList, PyString, PyType};

/// The interpreter's home, from the interpreter the targets were built with.
const BUILD_PYTHONHOME: &str = env!("PROTOBUF_PY_FUZZ_PYTHONHOME");

/// The interpreter's site-packages, for `typing_extensions`.
const BUILD_SITE: &str = env!("PROTOBUF_PY_FUZZ_SITE");

/// The protobuf-py repository.
const REPO: &str = env!("PROTOBUF_PY_FUZZ_REPO");

/// Imports the message types and returns them sorted by name, with a registry
/// of all of them for `Any` and extensions.
const BOOTSTRAP: &str = r#"
from protobuf import Message, Registry
from protobuf._to_binary import ToBinaryOptions, write_message
from protobuf._wire import BinaryWriter
from protobuf.wkt.google.protobuf import (
    any_pb, api_pb, descriptor_pb, duration_pb, empty_pb, field_mask_pb,
    source_context_pb, struct_pb, timestamp_pb, type_pb, wrappers_pb,
)
from gen.conformance.messages import (
    test_messages_edition2023_pb, test_messages_edition_unstable_pb,
    test_messages_proto2_editions_pb, test_messages_proto2_pb,
    test_messages_proto3_editions_pb, test_messages_proto3_pb,
)
import protobuf_ext._protobuf_ext

if protobuf_ext._protobuf_ext.__spec__.origin != "built-in":
    raise RuntimeError("the uninstrumented extension was imported")

registry = Registry(
    any_pb.desc(), api_pb.desc(), descriptor_pb.desc(), duration_pb.desc(),
    empty_pb.desc(), field_mask_pb.desc(), source_context_pb.desc(),
    struct_pb.desc(), timestamp_pb.desc(), type_pb.desc(), wrappers_pb.desc(),
    test_messages_edition2023_pb.desc(),
    test_messages_edition_unstable_pb.desc(),
    test_messages_proto2_editions_pb.desc(), test_messages_proto2_pb.desc(),
    test_messages_proto3_editions_pb.desc(), test_messages_proto3_pb.desc(),
)
descs = sorted(
    (desc for desc in registry if hasattr(desc, "fields")),
    key=lambda desc: desc.type_name,
)
types = [desc.type for desc in descs]
type_names = [desc.type_name for desc in descs]

def contents(message):
    writer = BinaryWriter()
    write_message(message, writer, ToBinaryOptions(write_unknown_fields=True))
    return writer.finish()
"#;

/// The message types and the registry they are in.
pub struct Harness {
    /// Message classes, sorted by type name.
    pub types: Vec<Py<PyType>>,
    /// The full names of [`Harness::types`].
    pub type_names: Vec<String>,
    /// A `protobuf.Registry` with all of [`Harness::types`].
    pub registry: Py<PyAny>,
    /// `protobuf.Message`, whose methods run the Python marshaling.
    message: Py<PyType>,
    /// Serializes a message with Python's code without validating it, to
    /// compare messages.
    contents: Py<PyAny>,
}

/// Where to find the interpreter's home and the Python packages.
struct Paths {
    home: PathBuf,
    sys_path: Vec<PathBuf>,
}

/// OSS-Fuzz runs the targets without the source tree or the build's
/// interpreter, with both copied into `python/` beside them.
fn paths() -> Paths {
    let bundled = std::env::current_exe()
        .ok()
        .and_then(|exe| Some(exe.parent()?.join("python")))
        .filter(|dir| dir.is_dir());
    if let Some(bundled) = bundled {
        return Paths {
            home: bundled.join("home"),
            sys_path: vec![bundled.join("site")],
        };
    }
    let repo = Path::new(REPO);
    Paths {
        home: PathBuf::from(BUILD_PYTHONHOME),
        sys_path: vec![
            repo.join("src"),
            repo.join("packages/protobuf-py-ext"),
            repo.join("tests/conformance"),
            PathBuf::from(BUILD_SITE),
        ],
    }
}

static HARNESS: LazyLock<Harness> = LazyLock::new(|| {
    let paths = paths();
    // SAFETY: the fuzz targets are single-threaded while initializing.
    unsafe {
        std::env::set_var("PYTHONHOME", &paths.home);
        // Allocates Python objects with malloc so that AddressSanitizer sees
        // the extension's accesses to them.
        std::env::set_var("PYTHONMALLOC", "malloc");
        std::env::set_var("PYTHONDONTWRITEBYTECODE", "1");
        // Registers the extension that the targets link, instrumented,
        // as a built-in module to take precedence over any that is installed.
        pyo3::ffi::PyImport_AppendInittab(
            c"protobuf_ext._protobuf_ext".as_ptr(),
            Some(protobuf_ext::protobuf_python_ext::__pyo3_init),
        );
    }
    Python::initialize();
    Python::attach(|py| {
        let sys_path = py
            .import("sys")
            .and_then(|sys| sys.getattr("path"))
            .expect("sys.path exists");
        let sys_path = sys_path.cast::<PyList>().expect("sys.path is a list");
        for (index, dir) in paths.sys_path.iter().enumerate() {
            let dir = dir.to_str().expect("the path is UTF-8");
            sys_path.insert(index, dir).expect("sys.path is extended");
        }
        let globals = PyDict::new(py);
        let bootstrap = CString::new(BOOTSTRAP).expect("no nul in the bootstrap");
        if let Err(error) = py.run(&bootstrap, Some(&globals), None) {
            error.print(py);
            panic!("the bootstrap failed with sys.path {sys_path}");
        }
        let item = |name: &str| {
            globals
                .get_item(name)
                .expect("the bootstrap sets the item")
                .expect("the bootstrap sets the item")
        };
        let types = item("types")
            .cast::<PyList>()
            .expect("the types are a list")
            .iter()
            .map(|class| class.cast_into::<PyType>().expect("a type").unbind())
            .collect();
        let type_names: Vec<String> = item("type_names")
            .extract()
            .expect("the type names are strings");
        assert!(
            u16::try_from(type_names.len()).is_ok(),
            "two bytes select a type"
        );
        Harness {
            types,
            type_names,
            registry: item("registry").unbind(),
            message: item("Message")
                .cast_into::<PyType>()
                .expect("Message is a type")
                .unbind(),
            contents: item("contents").unbind(),
        }
    })
});

/// The harness, initializing the interpreter on first use.
#[must_use]
pub fn harness() -> &'static Harness {
    &HARNESS
}

/// The options of `to_json`, other than the registry.
#[derive(Clone, Copy, Debug, Default)]
#[allow(clippy::struct_field_names, reason = "named as the Python arguments")]
pub struct JsonOptions {
    pub always_emit_implicit: bool,
    pub print_enums_as_ints: bool,
    pub use_proto_field_name: bool,
}

/// An input for a target: the message type, the options, and the payload.
pub struct Input<'a> {
    /// Index into [`Harness::types`].
    pub type_index: usize,
    /// Whether to parse with `ignore_unknown_fields`.
    pub ignore_unknown_fields: bool,
    /// The options to serialize JSON with.
    pub json_options: JsonOptions,
    /// The payload to parse.
    pub payload: &'a [u8],
}

impl<'a> Input<'a> {
    /// Splits `data` into a little-endian `u16` type selector, a flags byte,
    /// and the payload. The flags' lowest bit is `ignore_unknown_fields` and
    /// the next three the [`JsonOptions`].
    #[must_use]
    pub fn new(data: &'a [u8]) -> Option<Self> {
        let (header, payload) = data.split_first_chunk::<3>()?;
        let selector = usize::from(u16::from_le_bytes([header[0], header[1]]));
        let flags = header[2];
        Some(Self {
            type_index: selector % harness().types.len(),
            ignore_unknown_fields: flags & 1 != 0,
            json_options: JsonOptions {
                always_emit_implicit: flags & 2 != 0,
                print_enums_as_ints: flags & 4 != 0,
                use_proto_field_name: flags & 8 != 0,
            },
            payload,
        })
    }

    /// The target input for `payload` as `type_name`, or `None` if the type
    /// is not one of [`Harness::types`].
    ///
    /// # Panics
    ///
    /// If the interpreter fails to initialize.
    #[must_use]
    pub fn encode(type_name: &str, ignore_unknown_fields: bool, payload: &[u8]) -> Option<Vec<u8>> {
        let index = harness()
            .type_names
            .iter()
            .position(|name| name == type_name)?;
        let selector = u16::try_from(index).expect("checked when listed");
        let flags = u8::from(ignore_unknown_fields);
        Some([&selector.to_le_bytes()[..], &[flags], payload].concat())
    }
}

/// Whether `error` is one that parsing invalid input raises.
fn is_parse_error(py: Python<'_>, error: &PyErr) -> bool {
    error.is_instance_of::<PyValueError>(py)
        || error.is_instance_of::<PyTypeError>(py)
        || error.is_instance_of::<PyEOFError>(py)
        || error.is_instance_of::<PyOverflowError>(py)
        || error.is_instance_of::<PyRecursionError>(py)
}

/// Panics unless `error` is one that parsing invalid input raises.
///
/// # Panics
///
/// If `error` is anything else, such as a `PanicException`.
pub fn expect_parse_error(py: Python<'_>, error: &PyErr, context: &str) {
    if !is_parse_error(py, error) {
        error.print(py);
        panic!("{context}: unexpected error {error}");
    }
}

/// Unwraps `result`, printing the Python traceback before panicking.
///
/// # Panics
///
/// If `result` is an error.
pub fn expect_ok<T>(py: Python<'_>, result: PyResult<T>, context: &str) -> T {
    result.unwrap_or_else(|error| {
        error.print(py);
        panic!("{context}: {error}")
    })
}

/// Which code marshals messages.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Implementation {
    /// The extension.
    Native,
    /// protobuf-py's Python code.
    Python,
}

/// Parses `binary` as `class`.
///
/// # Errors
///
/// If `binary` is not valid for `class`.
pub fn from_binary<'py>(
    implementation: Implementation,
    class: &Bound<'py, PyType>,
    binary: &[u8],
    ignore_unknown_fields: bool,
) -> PyResult<Bound<'py, PyAny>> {
    let py = class.py();
    let binary = PyBytes::new(py, binary);
    match implementation {
        Implementation::Native => {
            let kwargs = PyDict::new(py);
            kwargs.set_item("ignore_unknown_fields", ignore_unknown_fields)?;
            class.call_method("from_binary", (binary,), Some(&kwargs))
        }
        Implementation::Python => {
            let message = class.call0()?;
            harness().message.bind(py).call_method1(
                "_merge_from_binary",
                (&message, binary, ignore_unknown_fields),
            )?;
            Ok(message)
        }
    }
}

/// Parses `json` as `class`.
///
/// # Errors
///
/// If `json` is not valid for `class`.
pub fn from_json<'py>(
    implementation: Implementation,
    class: &Bound<'py, PyType>,
    json: &Bound<'py, PyAny>,
    ignore_unknown_fields: bool,
) -> PyResult<Bound<'py, PyAny>> {
    let py = class.py();
    let kwargs = PyDict::new(py);
    kwargs.set_item("registry", harness().registry.bind(py))?;
    kwargs.set_item("ignore_unknown_fields", ignore_unknown_fields)?;
    match implementation {
        Implementation::Native => class.call_method("from_json", (json,), Some(&kwargs)),
        Implementation::Python => {
            let message = class.call0()?;
            harness().message.bind(py).call_method(
                "_merge_from_json",
                (&message, json),
                Some(&kwargs),
            )?;
            Ok(message)
        }
    }
}

/// Serializes `message` to binary.
///
/// # Errors
///
/// If `message` is missing required fields.
pub fn to_binary(implementation: Implementation, message: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    let binary = match implementation {
        Implementation::Native => message.call_method0("to_binary")?,
        Implementation::Python => harness()
            .message
            .bind(message.py())
            .call_method1("to_binary", (message,))?,
    };
    Ok(binary.cast::<PyBytes>()?.as_bytes().to_vec())
}

/// Serializes `message` to JSON.
///
/// # Errors
///
/// If `message` cannot be represented in JSON, such as an out of range
/// `Timestamp`, or has an extension in its unknown fields that does not
/// parse.
pub fn to_json(
    implementation: Implementation,
    message: &Bound<'_, PyAny>,
    options: JsonOptions,
) -> PyResult<String> {
    let py = message.py();
    let kwargs = PyDict::new(py);
    kwargs.set_item("registry", harness().registry.bind(py))?;
    kwargs.set_item("always_emit_implicit", options.always_emit_implicit)?;
    kwargs.set_item("print_enums_as_ints", options.print_enums_as_ints)?;
    kwargs.set_item("use_proto_field_name", options.use_proto_field_name)?;
    let json = match implementation {
        Implementation::Native => message.call_method("to_json", (), Some(&kwargs))?,
        Implementation::Python => {
            harness()
                .message
                .bind(py)
                .call_method("to_json", (message,), Some(&kwargs))?
        }
    };
    Ok(json.cast::<PyString>()?.to_string())
}

/// Returns both results if both implementations succeeded, `None` if both
/// raised the same type of error that invalid input raises, and panics
/// otherwise.
///
/// # Panics
///
/// If only one implementation succeeded, they raised different types of
/// errors, or either raised an unexpected error.
pub fn agree<T>(
    py: Python<'_>,
    context: &str,
    native: PyResult<T>,
    python: PyResult<T>,
) -> Option<(T, T)> {
    match (native, python) {
        (Ok(native), Ok(python)) => Some((native, python)),
        (Err(native), Err(python)) => {
            expect_parse_error(py, &native, &format!("{context} (native)"));
            expect_parse_error(py, &python, &format!("{context} (Python)"));
            assert!(
                native.get_type(py).is(python.get_type(py)),
                "{context}: native raised {native} but Python {python}"
            );
            None
        }
        (Ok(_), Err(python)) => {
            python.print(py);
            panic!("{context}: Python raised {python} but native succeeded");
        }
        (Err(native), Ok(_)) => {
            native.print(py);
            panic!("{context}: native raised {native} but Python succeeded");
        }
    }
}

/// Checks that the messages that the implementations parsed are the same.
///
/// Compares what they serialize to, since `==` skips unknown fields and
/// extensions, and NaN fields never compare equal. Serializes without
/// validating, since a parsed message may be missing required fields.
///
/// # Panics
///
/// If they are not.
pub fn check_same_message(context: &str, native: &Bound<'_, PyAny>, python: &Bound<'_, PyAny>) {
    let py = native.py();
    let contents = harness().contents.bind(py);
    let native_contents = expect_ok(py, contents.call1((native,)), "serializing to compare");
    let python_contents = expect_ok(py, contents.call1((python,)), "serializing to compare");
    assert!(
        expect_ok(py, native_contents.eq(&python_contents), "comparing"),
        "{context}: native parsed {native:?} but Python {python:?}\n\
         native: {native_contents:?}\npython: {python_contents:?}"
    );
}

/// Parses `binary` with both implementations and checks that they agree,
/// returning the native message if they succeeded.
///
/// # Panics
///
/// If the implementations disagree.
#[must_use]
pub fn parse_binary<'py>(
    class: &Bound<'py, PyType>,
    binary: &[u8],
    ignore_unknown_fields: bool,
) -> Option<Bound<'py, PyAny>> {
    let (native, python) = agree(
        class.py(),
        "from_binary",
        from_binary(Implementation::Native, class, binary, ignore_unknown_fields),
        from_binary(Implementation::Python, class, binary, ignore_unknown_fields),
    )?;
    check_same_message("from_binary", &native, &python);
    Some(native)
}

/// Parses `json` with both implementations and checks that they agree,
/// returning the native message if they succeeded.
///
/// # Panics
///
/// If the implementations disagree.
#[must_use]
pub fn parse_json<'py>(
    class: &Bound<'py, PyType>,
    json: &Bound<'py, PyAny>,
    ignore_unknown_fields: bool,
) -> Option<Bound<'py, PyAny>> {
    let (native, python) = agree(
        class.py(),
        "from_json",
        from_json(Implementation::Native, class, json, ignore_unknown_fields),
        from_json(Implementation::Python, class, json, ignore_unknown_fields),
    )?;
    check_same_message("from_json", &native, &python);
    Some(native)
}

/// Serializes the message that `binary` parses to as `class` again.
fn binary_round_trip(class: &Bound<'_, PyType>, binary: &[u8]) -> Vec<u8> {
    let py = class.py();
    let parsed = expect_ok(
        py,
        from_binary(Implementation::Native, class, binary, false),
        "binary round trip",
    );
    expect_ok(
        py,
        to_binary(Implementation::Native, &parsed),
        "binary round trip",
    )
}

/// Checks that the implementations serialize `message` to the same binary,
/// and that it round-trips.
fn check_binary(message: &Bound<'_, PyAny>) {
    let py = message.py();
    let class = message.get_type();
    let Some((native, python)) = agree(
        py,
        "to_binary",
        to_binary(Implementation::Native, message),
        to_binary(Implementation::Python, message),
    ) else {
        return;
    };
    assert_eq!(native, python, "to_binary of {class}");
    // Parsing normalizes values that serialize lossily, such as a float
    // field parsed from JSON that underflows to zero as a float32.
    let binary = binary_round_trip(&class, &native);
    // Map entries are serialized last to first, so it takes two round trips
    // to get the same bytes back.
    let twice = binary_round_trip(&class, &binary_round_trip(&class, &binary));
    assert_eq!(twice, binary, "binary round trip of {class}");
}

/// Checks that the implementations serialize `message` to the same JSON, and
/// parse it alike, and that it round-trips.
fn check_json(message: &Bound<'_, PyAny>, options: JsonOptions) {
    let py = message.py();
    let class = message.get_type();
    let Some((native, python)) = agree(
        py,
        "to_json",
        to_json(Implementation::Native, message, options),
        to_json(Implementation::Python, message, options),
    ) else {
        return;
    };
    assert_eq!(native, python, "to_json of {class}");
    // Parsing normalizes values that serialize lossily, such as a NullValue
    // field set to a number other than zero, which serializes as null.
    let json = json_round_trip(&class, &native, options);
    let twice = json_round_trip(&class, &json, options);
    assert_eq!(twice, json, "JSON round trip of {class}");
}

/// Serializes the message that `json` parses to as `class` again, checking
/// that the implementations parse it alike.
fn json_round_trip(class: &Bound<'_, PyType>, json: &str, options: JsonOptions) -> String {
    let py = class.py();
    let parsed = parse_json(class, &PyString::new(py, json).into_any(), false)
        .unwrap_or_else(|| panic!("{class} serialized {json} but did not parse it"));
    expect_ok(
        py,
        to_json(Implementation::Native, &parsed, options),
        "JSON round trip",
    )
}

/// Checks that the implementations serialize a parsed `message` alike, and
/// that it round-trips through binary and JSON.
///
/// Compares serialized forms rather than messages, since NaN fields never
/// compare equal.
///
/// # Panics
///
/// If the implementations disagree or a round trip changes the message.
pub fn check_serialization(message: &Bound<'_, PyAny>, json_options: JsonOptions) {
    check_binary(message);
    check_json(message, json_options);
}
