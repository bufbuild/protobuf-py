//! Parses arbitrary bytes as `ProtoJSON` with the extension and with
//! protobuf-py's Python code, then checks that they agree, and that they
//! serialize the message alike. The first two bytes select the message type
//! and the third the options.

#![no_main]

use libfuzzer_sys::fuzz_target;
use protobuf_py_ext_fuzz::{Input, check_serialization, harness, parse_json};
use pyo3::Python;
use pyo3::types::PyBytes;

fuzz_target!(|data: &[u8]| {
    let Some(input) = Input::new(data) else {
        return;
    };
    Python::attach(|py| {
        let class = harness().types[input.type_index].bind(py);
        let json = PyBytes::new(py, input.payload).into_any();
        if let Some(message) = parse_json(class, &json, input.ignore_unknown_fields) {
            check_serialization(&message, input.json_options);
        }
    });
});
