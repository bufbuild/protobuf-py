//! Parses arbitrary bytes as binary protobuf with the extension and with
//! protobuf-py's Python code, then checks that they agree, and that they
//! serialize the message alike. The first two bytes select the message type
//! and the third the options.

#![no_main]

use libfuzzer_sys::fuzz_target;
use protobuf_py_ext_fuzz::{Input, check_serialization, harness, parse_binary};
use pyo3::Python;

fuzz_target!(|data: &[u8]| {
    let Some(input) = Input::new(data) else {
        return;
    };
    Python::attach(|py| {
        let class = harness().types[input.type_index].bind(py);
        if let Some(message) = parse_binary(class, input.payload, input.ignore_unknown_fields) {
            check_serialization(&message, input.json_options);
        }
    });
});
