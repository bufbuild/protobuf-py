//! Generates payloads to use with fuzzing.
//! Automatically run by `uv run poe fuzz` before fuzzing.
//!
//! - `binary/`: each binary input of the protobuf conformance suite.
//! - `json/`: each JSON input of the protobuf conformance suite.
//!
//! The conformance runner runs this example again as its testee, which writes
//! each input it is sent as a seed and skips the test.

use std::ffi::CString;
use std::hash::{DefaultHasher, Hash as _, Hasher as _};
use std::io::Write as _;
use std::path::{Path, PathBuf};
use std::process::Command;

use protobuf_py_ext_fuzz::{Input, harness};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict};

const TESTEE_FLAG: &str = "--testee";

/// Finds the conformance runner and reads its requests.
const CONFORMANCE: &str = r#"
from gen.conformance.conformance_pb import (
    ConformanceRequest, ConformanceResponse, TestCategory,
)
from protobuf import Oneof, maximum_supported_edition
from protoc import get_conformance_test_runner_path

runner = str(get_conformance_test_runner_path())
maximum_edition = maximum_supported_edition.name.removeprefix("EDITION_")
skipped = ConformanceResponse(
    result=Oneof(field="skipped", value="recording seeds")
).to_binary()

def read_request(data):
    request = ConformanceRequest.from_binary(data)
    match request.payload:
        case Oneof(field="protobuf_payload", value=value):
            return ("binary", request.message_type, False, value)
        case Oneof(field="json_payload", value=value):
            ignore_unknown_fields = (
                request.test_category
                == TestCategory.JSON_IGNORE_UNKNOWN_PARSING_TEST
            )
            return ("json", request.message_type, ignore_unknown_fields, value.encode())
    return None
"#;

/// Runs [`CONFORMANCE`] in the harness's interpreter.
fn conformance(py: Python<'_>) -> Bound<'_, PyDict> {
    let globals = PyDict::new(py);
    let code = CString::new(CONFORMANCE).expect("no nul in the code");
    if let Err(error) = py.run(&code, Some(&globals), None) {
        error.print(py);
        panic!("the conformance code failed, which needs `uv sync`");
    }
    globals
}

fn item<'py>(globals: &Bound<'py, PyDict>, name: &str) -> Bound<'py, PyAny> {
    globals
        .get_item(name)
        .expect("the code sets the item")
        .expect("the code sets the item")
}

/// Deletes and recreates `dir`.
fn reset(dir: &Path) {
    if dir.exists() {
        std::fs::remove_dir_all(dir).expect("the old seeds are removed");
    }
    std::fs::create_dir_all(dir).expect("the seed directory is created");
}

/// Reads a request, framed by its little-endian length, from stdin.
fn read_request(stdin: &mut impl std::io::Read) -> Option<Vec<u8>> {
    let mut len = [0; 4];
    match stdin.read_exact(&mut len) {
        Ok(()) => {}
        Err(error) if error.kind() == std::io::ErrorKind::UnexpectedEof => return None,
        Err(error) => panic!("the request length is read: {error}"),
    }
    let len = usize::try_from(u32::from_le_bytes(len)).expect("a length");
    let mut request = vec![0; len];
    stdin.read_exact(&mut request).expect("the request is read");
    Some(request)
}

/// Writes each input the conformance runner sends as a seed in `out`, and
/// skips its test.
fn testee(out: &Path) {
    // Initializes the interpreter.
    let _ = harness();
    Python::attach(|py| {
        let globals = conformance(py);
        let read = item(&globals, "read_request");
        let skipped = item(&globals, "skipped");
        let skipped = skipped.cast::<PyBytes>().expect("bytes").as_bytes();
        let skipped_len = u32::try_from(skipped.len()).expect("a short response");
        let mut stdin = std::io::stdin().lock();
        let mut stdout = std::io::stdout().lock();
        while let Some(request) = read_request(&mut stdin) {
            let input = read
                .call1((PyBytes::new(py, &request),))
                .expect("the request decodes");
            if !input.is_none() {
                let (dir, type_name, ignore_unknown_fields, payload): (
                    String,
                    String,
                    bool,
                    Vec<u8>,
                ) = input.extract().expect("the input is a tuple");
                // Skips inputs whose type is not fuzzed, which there should
                // not be any of.
                if let Some(seed) = Input::encode(&type_name, ignore_unknown_fields, &payload) {
                    // Names seeds by their content, since the runner starts
                    // a testee for each suite.
                    let mut hasher = DefaultHasher::new();
                    seed.hash(&mut hasher);
                    let name = format!("{:016x}", hasher.finish());
                    std::fs::write(out.join(dir).join(name), seed).expect("the seed is written");
                }
            }
            stdout
                .write_all(&skipped_len.to_le_bytes())
                .and_then(|()| stdout.write_all(skipped))
                .and_then(|()| stdout.flush())
                .expect("the response is written");
        }
    });
}

fn count(dir: &Path) -> usize {
    std::fs::read_dir(dir)
        .expect("the seeds are listed")
        .count()
}

fn main() {
    let mut args = std::env::args_os().skip(1);
    let first = args.next().expect("the directory to write the seeds to");
    if first == TESTEE_FLAG {
        testee(&PathBuf::from(args.next().expect("the seed directory")));
        return;
    }
    let out = std::path::absolute(PathBuf::from(first)).expect("an absolute path");
    reset(&out.join("binary"));
    reset(&out.join("json"));
    // Initializes the interpreter.
    let _ = harness();
    let (runner, maximum_edition) = Python::attach(|py| {
        let globals = conformance(py);
        let runner: String = item(&globals, "runner").extract().expect("a path");
        let edition: String = item(&globals, "maximum_edition").extract().expect("a name");
        (runner, edition)
    });
    let exe = std::env::current_exe().expect("the example's path");
    // Every test is skipped, which the runner does not count as a failure.
    let status = Command::new(runner)
        .arg("--maximum_edition")
        .arg(maximum_edition)
        .arg(exe)
        .arg(TESTEE_FLAG)
        .arg(&out)
        .status()
        .expect("the conformance runner runs");
    assert!(status.success(), "the conformance runner failed: {status}");
    for target in ["binary", "json"] {
        let dir = out.join(target);
        println!("wrote {} {target} seeds to {}", count(&dir), dir.display());
    }
}
