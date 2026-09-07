//! Native `ProtoJSON` parsing, generic over a `JsonSource`.
//!
//! Mirrors the pure-Python `protobuf._from_json`. Error text matches the
//! reference exactly where practical. Registry-backed Any/extension handling
//! calls the Python `Registry` object directly (never ported to Rust).

use std::collections::HashSet;

use base64::Engine as _;
use pyo3::{
    Bound, Py, PyAny, PyErr, PyResult, Python,
    exceptions::{PyOverflowError, PyTypeError, PyValueError},
    types::{
        PyAnyMethods as _, PyBool, PyBytes, PyDict, PyDictMethods as _, PyFloat, PyInt, PyList,
        PyListMethods as _, PyString, PyStringMethods as _, PyTypeMethods as _,
    },
};

use crate::{
    budget::{self, Budget},
    descriptor::{DescEnum, DescFieldValue, ScalarType},
    json_source::{JiterSource, JsonKind, JsonSource, PyTreeSource},
    marshaler::MessageMarshaler,
    nativemessage::NativeMessage,
    oneof::Oneof,
    parser::{FieldParser, FieldParserValue, ParserFieldType},
    wkt_registry::WktKind,
};

const DEPTH_LIMIT: usize = 100;
const INT32_MIN: i64 = -(1 << 31);
const INT32_MAX: i64 = 1 << 31;
const UINT32_MAX: i64 = 1 << 32;
const FLOAT32_MAX: f64 = 3.402_823_466_385_288_6e38;
const FLOAT32_MIN: f64 = -3.402_823_466_385_288_6e38;

/// Options controlling JSON parsing.
pub(crate) struct FromJsonOpts {
    pub(crate) ignore_unknown_fields: bool,
    pub(crate) registry: Option<Py<PyAny>>,
}

#[derive(Clone, Copy)]
enum Exc {
    Value,
    Type,
    Overflow,
}

/// Parses a JSON document (str/bytes) into an existing message.
pub(crate) fn merge_from_json<'py>(
    py: Python<'py>,
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    data: &[u8],
    opts: &FromJsonOpts,
    budget: &mut Budget,
) -> PyResult<()> {
    let mut src = JiterSource::new(py, data);
    read_message(marshaler, message, &mut src, opts, 0, budget)?;
    src.finish()
}

/// Parses a message from a Python JSON tree (`message_from_json_value`).
pub(crate) fn read_message_from_tree<'py>(
    py: Python<'py>,
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    tree: Bound<'py, PyAny>,
    opts: &FromJsonOpts,
    budget: &mut Budget,
) -> PyResult<()> {
    let mut src = PyTreeSource::new(py, tree);
    read_message(marshaler, message, &mut src, opts, 0, budget)
}

/// Reads a message value, dispatching on its well-known-type kind. Ordinary
/// (non-WKT) messages take the generic object path; WKTs go through
/// `WktKind::read_json`.
pub(crate) fn read_message<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    budget: &mut Budget,
) -> PyResult<()> {
    if depth > DEPTH_LIMIT {
        return Err(pyo3::exceptions::PyRecursionError::new_err(format!(
            "exceeded maximum recursion depth {DEPTH_LIMIT} while parsing message"
        )));
    }
    match &marshaler.wkt {
        Some(wkt) => wkt.read_json(marshaler, message, src, opts, depth, budget),
        None => read_generic_object(marshaler, message, src, opts, depth, budget),
    }
}

fn read_generic_object<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    budget: &mut Budget,
) -> PyResult<()> {
    let py = src.py();
    if src.peek()? != JsonKind::Object {
        let value = read_json_value(src, budget)?;
        let qualname = marshaler.python_type.bind(py).qualname()?;
        return Err(PyTypeError::new_err(format!(
            "cannot decode {qualname} from JSON: {}",
            value.str()?
        )));
    }

    // Duplicate keys are accepted with last-in-wins semantics (per the
    // ProtoJSON spec). Because we are streaming values from the JSON, we do not
    // get "pre-collapsed" duplicates like `json.loads` would provide. So we keep
    // track of seen field numbers and reset to the default when encountering one.
    // This also accounts for duplicates with different JSON names.
    let mut seen: HashSet<u32> = HashSet::new();
    src.for_each_object_key(|key, src| {
        if let Some(&number) = marshaler.json_names.get(key) {
            let parser = marshaler
                .parser
                .field(number)
                .ok_or_else(|| PyValueError::new_err("field table lookup failed"))?;
            // A scalar oneof field set to `null` leaves the oneof unset.
            if parser.oneof_name.is_some()
                && matches!(parser.value, FieldParserValue::Scalar(_))
                && src.peek()? == JsonKind::Null
            {
                src.next_null()?;
                return Ok(());
            }
            if merges_on_duplicate(parser) && !seen.insert(number) {
                reset_duplicate_field(py, parser, message)?;
            }
            read_field(marshaler, parser, message, src, opts, depth, budget)?;
        } else {
            handle_unknown_key(marshaler, message, key, src, opts, depth, budget)?;
        }
        Ok(())
    })?;
    Ok(())
}

/// Whether a repeat of this field merges into the value already read (repeated
/// appends, maps add keys, singular messages merge fields) and so must be reset
/// for last-in-wins.
fn merges_on_duplicate(parser: &FieldParser) -> bool {
    match &parser.type_ {
        ParserFieldType::List { .. } | ParserFieldType::Map { .. } => true,
        ParserFieldType::Singular { oneof_attr, .. } => {
            oneof_attr.is_none() && matches!(parser.value, FieldParserValue::Message { .. })
        }
    }
}

/// Resets a field to its default before a duplicate JSON key is applied, so the
/// later occurrence replaces the earlier one rather than merging into it.
fn reset_duplicate_field<'py>(
    py: Python<'py>,
    parser: &FieldParser,
    message: &Bound<'py, NativeMessage>,
) -> PyResult<()> {
    match &parser.type_ {
        ParserFieldType::List { .. } => parser.attr.set(message.as_any(), &PyList::empty(py)),
        ParserFieldType::Map { .. } => parser.attr.set(message.as_any(), &PyDict::new(py)),
        ParserFieldType::Singular { .. } => {
            parser.attr.set(message.as_any(), py.None().bind(py))?;
            message.get().clear_present_field(parser.number);
            Ok(())
        }
    }
}

fn read_field<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    parser: &FieldParser,
    message: &Bound<'py, NativeMessage>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    budget: &mut Budget,
) -> PyResult<()> {
    match &parser.type_ {
        ParserFieldType::Singular {
            oneof_attr,
            requires_presence,
        } => read_singular(
            marshaler,
            parser,
            message,
            src,
            opts,
            depth,
            oneof_attr.as_ref(),
            *requires_presence,
            budget,
        ),
        ParserFieldType::List { .. } => {
            read_list(marshaler, parser, message, src, opts, depth, budget)
        }
        ParserFieldType::Map {
            key_type,
            value_parser,
            ..
        } => read_map(
            marshaler,
            parser,
            message,
            src,
            opts,
            depth,
            *key_type,
            value_parser,
            budget,
        ),
    }
}

#[allow(clippy::too_many_arguments, reason = "internal parser")]
fn read_singular<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    parser: &FieldParser,
    message: &Bound<'py, NativeMessage>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    oneof_attr: Option<&crate::attribute_access::AttributeAccess>,
    requires_presence: bool,
    budget: &mut Budget,
) -> PyResult<()> {
    let py = src.py();
    match &parser.value {
        FieldParserValue::Scalar(scalar) => {
            if src.peek()? == JsonKind::Null {
                src.next_null()?;
                del_singular(
                    py,
                    parser,
                    message,
                    oneof_attr,
                    &scalar.zero_value(py).into_bound(py),
                )?;
                return Ok(());
            }
            let name = parser.name.bind(py);
            let ctx = FieldContext::Field { marshaler, name };
            let value = read_scalar(&ctx, src, *scalar, budget)?;
            if oneof_attr.is_some() {
                budget.charge(budget::ONEOF_SIZE)?;
            }
            parser.assign_singular(py, message, &value, oneof_attr, requires_presence)
        }
        FieldParserValue::Enum(enum_) => {
            if src.peek()? == JsonKind::Null && !enum_.is_null_value {
                src.next_null()?;
                del_singular(
                    py,
                    parser,
                    message,
                    oneof_attr,
                    &enum_.zero_value.bind(py).clone(),
                )?;
                return Ok(());
            }
            if let Some(value) = read_enum(enum_, src, opts, budget)? {
                if oneof_attr.is_some() {
                    budget.charge(budget::ONEOF_SIZE)?;
                }
                parser.assign_singular(py, message, &value, oneof_attr, requires_presence)?;
            }
            Ok(())
        }
        FieldParserValue::Message {
            message: msg_desc, ..
        } => {
            let inner = msg_desc.get_marshaler(py)?;
            let is_value = matches!(inner.wkt.as_deref(), Some(WktKind::Value(_)));
            if src.peek()? == JsonKind::Null && !is_value {
                src.next_null()?;
                del_singular(py, parser, message, oneof_attr, &py.None().into_bound(py))?;
                return Ok(());
            }
            let existing = parser.get_field_value(py, message)?;
            let target = match existing {
                Some(value) if !value.is_none() => value.cast_into::<NativeMessage>()?,
                _ => {
                    budget.charge(inner.alloc_size)?;
                    inner.new_empty_message(py, msg_desc.get_python_type(py))?
                }
            };
            read_message(inner, &target, src, opts, depth + 1, budget)?;
            if oneof_attr.is_some() {
                budget.charge(budget::ONEOF_SIZE)?;
            }
            parser.assign_singular(py, message, target.as_any(), oneof_attr, requires_presence)
        }
    }
}

/// Clears a singular field for a resetting `null`.
fn del_singular<'py>(
    py: Python<'py>,
    parser: &FieldParser,
    message: &Bound<'py, NativeMessage>,
    oneof_attr: Option<&crate::attribute_access::AttributeAccess>,
    default: &Bound<'py, PyAny>,
) -> PyResult<()> {
    if let Some(oneof_attr) = oneof_attr {
        let current = oneof_attr.get(py, message.as_any())?;
        if let Ok(oneof) = current.cast::<Oneof>()
            && oneof
                .get()
                .field
                .bind(py)
                .eq(parser.local_name_py.bind(py))?
        {
            oneof_attr.set(message.as_any(), py.None().bind(py))?;
        }
    } else {
        parser.attr.set(message.as_any(), default)?;
        message.get().clear_present_field(parser.number);
    }
    Ok(())
}

fn read_list<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    parser: &FieldParser,
    message: &Bound<'py, NativeMessage>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    budget: &mut Budget,
) -> PyResult<()> {
    let py = src.py();
    let name = parser.name.bind(py);
    let ctx = FieldContext::Field { marshaler, name };
    if src.peek()? == JsonKind::Null {
        src.next_null()?;
        return Ok(());
    }
    if src.peek()? != JsonKind::Array {
        return Err(ctx.error(
            &format!(
                "expected list got {}",
                read_json_value(src, budget)?.get_type()
            ),
            Exc::Type,
        ));
    }
    let list = parser
        .attr
        .get(py, message.as_any())?
        .cast_into::<PyList>()?;
    src.for_each_array_item(|src| {
        if let Some(value) =
            read_container_item(&ctx, &parser.value, src, opts, depth, false, budget)?
        {
            budget.charge(budget::LIST_SLOT_SIZE)?;
            list.append(value)?;
        }
        Ok(())
    })?;
    Ok(())
}

#[allow(clippy::too_many_arguments, reason = "internal parser")]
fn read_map<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    parser: &FieldParser,
    message: &Bound<'py, NativeMessage>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    key_type: ScalarType,
    value_parser: &FieldParser,
    budget: &mut Budget,
) -> PyResult<()> {
    let py = src.py();
    let name = parser.name.bind(py);
    let ctx = FieldContext::Field { marshaler, name };
    if src.peek()? == JsonKind::Null {
        src.next_null()?;
        return Ok(());
    }
    if src.peek()? != JsonKind::Object {
        return Err(ctx.error(
            &format!(
                "expected dict got {}",
                read_json_value(src, budget)?.get_type()
            ),
            Exc::Type,
        ));
    }
    let dict = parser
        .attr
        .get(py, message.as_any())?
        .cast_into::<PyDict>()?;
    src.for_each_object_key(|key, src| {
        let map_key = read_map_key(py, &ctx, key_type, key, budget)?;
        if let Some(value) =
            read_container_item(&ctx, &value_parser.value, src, opts, depth, true, budget)?
        {
            budget.charge(budget::DICT_ENTRY_SIZE)?;
            dict.set_item(map_key, value)?;
        }
        Ok(())
    })?;
    Ok(())
}

/// Reads a list element or map value.
#[allow(clippy::too_many_arguments, reason = "internal parser")]
fn read_container_item<'py, R: JsonSource<'py>>(
    ctx: &FieldContext<'_, 'py>,
    element: &FieldParserValue,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    is_map: bool,
    budget: &mut Budget,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    let py = src.py();
    let is_null = src.peek()? == JsonKind::Null;
    match element {
        FieldParserValue::Scalar(scalar) if !is_null => {
            Ok(Some(read_scalar(ctx, src, *scalar, budget)?))
        }
        FieldParserValue::Message {
            message: msg_desc, ..
        } => {
            let inner = msg_desc.get_marshaler(py)?;
            let is_value = matches!(inner.wkt.as_deref(), Some(WktKind::Value(_)));
            if is_null && !is_value {
                src.next_null()?;
                return Err(container_null_error(ctx, is_map));
            }
            budget.charge(inner.alloc_size)?;
            let target = inner.new_empty_message(py, msg_desc.get_python_type(py))?;
            read_message(inner, &target, src, opts, depth + 1, budget)?;
            Ok(Some(target.into_any()))
        }
        FieldParserValue::Enum(enum_) if !is_null || enum_.is_null_value => {
            read_enum(enum_, src, opts, budget)
        }
        _ => {
            // Resetting null for a list item / map value: error.
            src.next_null()?;
            Err(container_null_error(ctx, is_map))
        }
    }
}

fn container_null_error(ctx: &FieldContext<'_, '_>, is_map: bool) -> PyErr {
    let what = if is_map { "map value" } else { "list item" };
    ctx.error(&format!("unexpected null value for {what}"), Exc::Value)
}

fn read_map_key<'py>(
    py: Python<'py>,
    ctx: &FieldContext<'_, 'py>,
    key_type: ScalarType,
    raw_key: &str,
    budget: &mut Budget,
) -> PyResult<Bound<'py, PyAny>> {
    match key_type {
        ScalarType::Bool => match raw_key {
            "true" => Ok(PyBool::new(py, true).to_owned().into_any()),
            "false" => Ok(PyBool::new(py, false).to_owned().into_any()),
            other => Err(ctx.error(
                &format!("unexpected bool map key value {other}"),
                Exc::Value,
            )),
        },
        ScalarType::String => {
            budget.charge(budget::STR_OVERHEAD + raw_key.chars().count())?;
            Ok(PyString::new(py, raw_key).into_any())
        }
        _ => {
            budget.charge(budget::INT_SIZE)?;
            parse_int_string(py, ctx, raw_key, key_type)
        }
    }
}

/// Reads a scalar value.
pub(crate) fn read_scalar<'py, R: JsonSource<'py>>(
    ctx: &FieldContext<'_, 'py>,
    src: &mut R,
    scalar: ScalarType,
    budget: &mut Budget,
) -> PyResult<Bound<'py, PyAny>> {
    let py = src.py();
    match scalar {
        ScalarType::Bool => {
            if src.peek()? != JsonKind::Bool {
                let value = read_json_value(src, budget)?;
                return Err(ctx.error(
                    &format!("unexpected json type: {}", value.get_type()),
                    Exc::Type,
                ));
            }
            Ok(PyBool::new(py, src.next_bool()?).to_owned().into_any())
        }
        ScalarType::Float => {
            let value = parse_float(ctx, src, budget)?;
            if value.is_finite() && !(FLOAT32_MIN..=FLOAT32_MAX).contains(&value) {
                return Err(ctx.error(&format!("float value out of range: {value}"), Exc::Overflow));
            }
            budget.charge(budget::FLOAT_SIZE)?;
            Ok(PyFloat::new(py, value).into_any())
        }
        ScalarType::Double => {
            let value = parse_float(ctx, src, budget)?;
            budget.charge(budget::FLOAT_SIZE)?;
            Ok(PyFloat::new(py, value).into_any())
        }
        ScalarType::String => {
            let value = read_string(ctx, src, budget)?;
            // Character count approximates the payload size.
            budget.charge(budget::STR_OVERHEAD + value.len()?)?;
            Ok(value.into_any())
        }
        ScalarType::Bytes => read_bytes(ctx, src, budget),
        _ => {
            budget.charge(budget::INT_SIZE)?;
            read_int(ctx, src, scalar, budget)
        }
    }
}

fn read_string<'py, R: JsonSource<'py>>(
    ctx: &FieldContext<'_, 'py>,
    src: &mut R,
    budget: &mut Budget,
) -> PyResult<Bound<'py, PyString>> {
    if src.peek()? != JsonKind::String {
        let value = read_json_value(src, budget)?;
        return Err(ctx.error(
            &format!("expected string got: {}", value.get_type()),
            Exc::Type,
        ));
    }
    src.next_py_str()
}

fn read_bytes<'py, R: JsonSource<'py>>(
    ctx: &FieldContext<'_, 'py>,
    src: &mut R,
    budget: &mut Budget,
) -> PyResult<Bound<'py, PyAny>> {
    let py = src.py();
    if src.peek()? != JsonKind::String {
        let value = read_json_value(src, budget)?;
        return Err(ctx.error(
            &format!("expected base64-encoded string got: {}", value.get_type()),
            Exc::Type,
        ));
    }
    // Autodetect standard vs URL-safe alphabet. The
    // engines are lenient about padding and non-canonical trailing bits, like
    // Python's `base64.b64decode(..., validate=True)`.
    let decoded = src.with_next_str(|text| {
        let decoded = if text.contains('-') || text.contains('_') {
            base64_url_safe().decode(text)
        } else {
            base64_standard().decode(text)
        }
        .map_err(|_| ctx.error("invalid base64 data", Exc::Value))?;
        Ok(decoded)
    })?;
    budget.charge(budget::BYTES_OVERHEAD + decoded.len())?;
    Ok(PyBytes::new(py, &decoded).into_any())
}

/// Lenient base64 decode config matching Python's `b64decode`: optional padding,
/// non-canonical trailing bits allowed.
fn base64_decode_config() -> base64::engine::GeneralPurposeConfig {
    base64::engine::GeneralPurposeConfig::new()
        .with_decode_allow_trailing_bits(true)
        .with_decode_padding_mode(base64::engine::DecodePaddingMode::Indifferent)
}

fn base64_standard() -> base64::engine::GeneralPurpose {
    base64::engine::GeneralPurpose::new(&base64::alphabet::STANDARD, base64_decode_config())
}

fn base64_url_safe() -> base64::engine::GeneralPurpose {
    base64::engine::GeneralPurpose::new(&base64::alphabet::URL_SAFE, base64_decode_config())
}

/// Parses a float/double.
fn parse_float<'py, R: JsonSource<'py>>(
    ctx: &FieldContext<'_, 'py>,
    src: &mut R,
    budget: &mut Budget,
) -> PyResult<f64> {
    match src.peek()? {
        JsonKind::Number => {
            let value = src.next_float()?;
            if !value.is_finite() {
                return Err(ctx.error("unexpected infinite/NaN number", Exc::Value));
            }
            Ok(value)
        }
        JsonKind::String => src.with_next_str(|text| match text {
            "Infinity" => Ok(f64::INFINITY),
            "-Infinity" => Ok(f64::NEG_INFINITY),
            "NaN" => Ok(f64::NAN),
            _ => {
                if text.is_empty() || text.trim() != text {
                    return Err(
                        ctx.error(&format!("invalid float/double value: {text}"), Exc::Value)
                    );
                }
                match text.parse::<f64>() {
                    Ok(value) if value.is_finite() => Ok(value),
                    Ok(_) => Err(ctx.error("unexpected infinite/NaN number", Exc::Value)),
                    Err(_) => {
                        Err(ctx.error(&format!("invalid float/double value: {text}"), Exc::Value))
                    }
                }
            }
        }),
        _ => {
            let value = read_json_value(src, budget)?;
            Err(ctx.error(
                &format!("unexpected json type: {}", value.get_type()),
                Exc::Type,
            ))
        }
    }
}

/// Parses an integer scalar.
fn read_int<'py, R: JsonSource<'py>>(
    ctx: &FieldContext<'_, 'py>,
    src: &mut R,
    int_type: ScalarType,
    budget: &mut Budget,
) -> PyResult<Bound<'py, PyAny>> {
    let py = src.py();
    let value = match src.peek()? {
        JsonKind::Number => {
            let number = src.next_number()?;
            if number.is_instance_of::<PyInt>() {
                number
            } else {
                let float_value = number.extract::<f64>()?;
                if float_value.fract() != 0.0 {
                    return Err(ctx.error(
                        &format!("expected integer, got non-integer float: {}", number.str()?),
                        Exc::Value,
                    ));
                }
                py_int_from_float(py, &number)?
            }
        }
        JsonKind::String => {
            return src.with_next_str(|text| {
                parse_int_string(py, ctx, text, int_type)
                    .and_then(|value| range_check_int(ctx, value, int_type))
            });
        }
        _ => {
            let value = read_json_value(src, budget)?;
            return Err(ctx.error(
                &format!("unexpected json type: {}", value.get_type()),
                Exc::Type,
            ));
        }
    };
    range_check_int(ctx, value, int_type)
}

/// Parses an integer from a quoted string.
fn parse_int_string<'py>(
    py: Python<'py>,
    ctx: &FieldContext<'_, 'py>,
    text: &str,
    _int_type: ScalarType,
) -> PyResult<Bound<'py, PyAny>> {
    if text.is_empty() || text.trim() != text {
        return Err(ctx.error(&format!("invalid integer value: {text}"), Exc::Value));
    }
    let int_type = py.get_type::<PyInt>();
    if let Ok(value) = int_type.call1((text, 10)) {
        return Ok(value);
    }
    // Fall back to a float string that is integer-valued (e.g. "3.0").
    match text.parse::<f64>() {
        Ok(float_value) if float_value.fract() == 0.0 => {
            let float_obj = PyFloat::new(py, float_value);
            py_int_from_float(py, &float_obj)
        }
        _ => Err(ctx.error(&format!("invalid integer value: '{text}'"), Exc::Value)),
    }
}

fn py_int_from_float<'py>(
    py: Python<'py>,
    value: &Bound<'py, PyAny>,
) -> PyResult<Bound<'py, PyAny>> {
    py.get_type::<PyInt>().call1((value,))
}

fn range_check_int<'py>(
    ctx: &FieldContext<'_, 'py>,
    value: Bound<'py, PyAny>,
    int_type: ScalarType,
) -> PyResult<Bound<'py, PyAny>> {
    let (ok, name) = match int_type {
        ScalarType::Int32 | ScalarType::Sint32 | ScalarType::Sfixed32 => (
            matches!(value.extract::<i64>(), Ok(v) if (INT32_MIN..INT32_MAX).contains(&v)),
            "int32",
        ),
        ScalarType::Uint32 | ScalarType::Fixed32 => (
            matches!(value.extract::<i64>(), Ok(v) if (0..UINT32_MAX).contains(&v)),
            "uint32",
        ),
        ScalarType::Int64 | ScalarType::Sint64 | ScalarType::Sfixed64 => {
            (value.extract::<i64>().is_ok(), "int64")
        }
        ScalarType::Uint64 | ScalarType::Fixed64 => (value.extract::<u64>().is_ok(), "uint64"),
        _ => (true, ""),
    };
    if ok {
        Ok(value)
    } else {
        Err(ctx.error(
            &format!("value {} out of range for {name}", value.str()?),
            Exc::Overflow,
        ))
    }
}

/// Reads an enum value. Returns `None` when an unknown
/// value is ignored via `ignore_unknown_fields`.
fn read_enum<'py, R: JsonSource<'py>>(
    enum_desc: &DescEnum,
    src: &mut R,
    opts: &FromJsonOpts,
    budget: &mut Budget,
) -> PyResult<Option<Bound<'py, PyAny>>> {
    let py = src.py();
    match src.peek()? {
        JsonKind::Null => {
            src.next_null()?;
            // `_read_enum` returns the first declared value for null.
            Ok(Some(enum_desc.zero_value.bind(py).clone()))
        }
        JsonKind::Number => {
            let number = src.next_number()?;
            if !number.is_instance_of::<PyInt>() {
                return Err(decode_enum_error(py, enum_desc, &number));
            }
            let Ok(int_value) = number.extract::<i32>() else {
                // Out of i32 range: unknown value.
                if opts.ignore_unknown_fields {
                    return Ok(None);
                }
                budget.charge(budget::INT_SIZE + budget::GC_HEAD_SIZE)?;
                return Ok(Some(enum_desc.py_type.bind(py).call1((number,))?));
            };
            if let Some(value) = enum_desc.values.get(&int_value) {
                Ok(Some(value.bind(py).clone()))
            } else if opts.ignore_unknown_fields {
                Ok(None)
            } else {
                // Open enum: succeeds; closed enum: raises via Python enum call.
                budget.charge(budget::INT_SIZE + budget::GC_HEAD_SIZE)?;
                Ok(Some(enum_desc.py_type.bind(py).call1((int_value,))?))
            }
        }
        JsonKind::String => src.with_next_str(|name| {
            if let Some(number) = enum_desc.numbers_by_name.get(name) {
                let value = enum_desc
                    .values
                    .get(number)
                    .ok_or_else(|| PyValueError::new_err("enum value table lookup failed"))?;
                Ok(Some(value.bind(py).clone()))
            } else if opts.ignore_unknown_fields {
                Ok(None)
            } else {
                let value = read_json_value_from_string(py, name);
                Err(decode_enum_error(py, enum_desc, &value))
            }
        }),
        _ => {
            let value = read_json_value(src, budget)?;
            Err(decode_enum_error(py, enum_desc, &value))
        }
    }
}

fn decode_enum_error(py: Python<'_>, enum_desc: &DescEnum, value: &Bound<'_, PyAny>) -> PyErr {
    let type_name = enum_desc.type_name.bind(py).to_str().unwrap_or_default();
    match value.str() {
        Ok(text) => PyValueError::new_err(format!("cannot decode {type_name} from JSON: {text}")),
        Err(err) => err,
    }
}

fn read_json_value_from_string<'py>(py: Python<'py>, text: &str) -> Bound<'py, PyAny> {
    PyString::new(py, text).into_any()
}

fn handle_unknown_key<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    raw_key: &str,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    budget: &mut Budget,
) -> PyResult<()> {
    let py = src.py();
    if raw_key.starts_with('[')
        && raw_key.ends_with(']')
        && let Some(registry) = &opts.registry
    {
        let registry = registry.bind(py);
        let ext_name = &raw_key[1..raw_key.len() - 1];
        let extension = registry.call_method1(&marshaler.constants.extension, (ext_name,))?;
        if !extension.is_none() {
            // Only read if the extendee matches this message.
            let extendee = extension.getattr("extendee")?;
            let extendee_name = extendee.getattr(&marshaler.constants.type_name)?;
            let extendee_name = extendee_name.cast::<PyString>()?.to_str()?;
            if extendee_name == &*marshaler.type_name {
                read_extension(marshaler, message, &extension, src, opts, depth, budget)?;
            } else {
                src.skip()?;
            }
            return Ok(());
        }
    }
    if opts.ignore_unknown_fields {
        src.skip()
    } else {
        Err(PyValueError::new_err(format!(
            "cannot decode {} from JSON: key: '{raw_key}' is unknown",
            marshaler.type_name
        )))
    }
}

/// Reads an extension value from the stream and stores it on the message.
fn read_extension<'py, R: JsonSource<'py>>(
    marshaler: &MessageMarshaler,
    message: &Bound<'py, NativeMessage>,
    extension: &Bound<'py, PyAny>,
    src: &mut R,
    opts: &FromJsonOpts,
    depth: usize,
    budget: &mut Budget,
) -> PyResult<()> {
    let py = src.py();
    let ext_type = extension.getattr(&marshaler.constants.type_)?;
    let ext_type_name = extension
        .getattr(&marshaler.constants.type_name)?
        .extract::<String>()?;
    let ctx = FieldContext::Extension {
        type_name: &ext_type_name,
    };
    let ext_value = extension.getattr(&marshaler.constants.value)?;
    let desc_value = DescFieldValue::new(py, &ext_value, &marshaler.constants)?;
    let target = message.as_any();
    match &desc_value {
        DescFieldValue::Scalar { scalar_type, .. } => {
            if src.peek()? == JsonKind::Null {
                src.next_null()?;
                target.del_item(&ext_type)?;
            } else {
                let value = read_scalar(&ctx, src, *scalar_type, budget)?;
                target.set_item(&ext_type, value)?;
            }
        }
        DescFieldValue::Enum { enum_, .. } => {
            if src.peek()? == JsonKind::Null && !enum_.is_null_value {
                src.next_null()?;
                target.del_item(&ext_type)?;
            } else if let Some(value) = read_enum(enum_, src, opts, budget)? {
                target.set_item(&ext_type, value)?;
            }
        }
        DescFieldValue::Message {
            message: msg_desc, ..
        } => {
            let inner = msg_desc.get_marshaler(py)?;
            let is_value = matches!(inner.wkt.as_deref(), Some(WktKind::Value(_)));
            if src.peek()? == JsonKind::Null && !is_value {
                src.next_null()?;
                target.del_item(&ext_type)?;
            } else {
                budget.charge(inner.alloc_size)?;
                let value = inner.new_empty_message(py, msg_desc.get_python_type(py))?;
                read_message(inner, &value, src, opts, depth + 1, budget)?;
                target.set_item(&ext_type, value)?;
            }
        }
        DescFieldValue::List { element, .. } => {
            // A `null` list is a no-op.
            if src.peek()? == JsonKind::Null {
                src.next_null()?;
                return Ok(());
            }
            if src.peek()? != JsonKind::Array {
                return Err(ctx.error(
                    &format!(
                        "expected list got {}",
                        read_json_value(src, budget)?.get_type()
                    ),
                    Exc::Type,
                ));
            }
            let element_value = FieldParserValue::from_desc_single(element);
            budget.charge(budget::EMPTY_LIST_SIZE)?;
            let list = PyList::empty(py);
            src.for_each_array_item(|src| {
                if let Some(value) =
                    read_container_item(&ctx, &element_value, src, opts, depth, false, budget)?
                {
                    budget.charge(budget::LIST_SLOT_SIZE)?;
                    list.append(value)?;
                }
                Ok(())
            })?;
            target.set_item(&ext_type, list)?;
        }
        // Protobuf does not permit map extensions.
        DescFieldValue::Map { .. } => {
            return Err(PyValueError::new_err("map extensions are not supported"));
        }
    }
    Ok(())
}

/// Materializes the next JSON value as a Python object.
pub(crate) fn read_json_value<'py, R: JsonSource<'py>>(
    src: &mut R,
    budget: &mut Budget,
) -> PyResult<Bound<'py, PyAny>> {
    let py = src.py();
    match src.peek()? {
        JsonKind::Null => {
            src.next_null()?;
            Ok(py.None().into_bound(py))
        }
        JsonKind::Bool => Ok(PyBool::new(py, src.next_bool()?).to_owned().into_any()),
        JsonKind::Number => {
            budget.charge(budget::INT_SIZE)?;
            src.next_number()
        }
        JsonKind::String => {
            let value = src.next_py_str()?;
            budget.charge(budget::STR_OVERHEAD + value.len()?)?;
            Ok(value.into_any())
        }
        JsonKind::Array => {
            budget.charge(budget::EMPTY_LIST_SIZE)?;
            let list = PyList::empty(py);
            src.for_each_array_item(|src| {
                let value = read_json_value(src, budget)?;
                budget.charge(budget::LIST_SLOT_SIZE)?;
                list.append(value)?;
                Ok(())
            })?;
            Ok(list.into_any())
        }
        JsonKind::Object => {
            budget.charge(budget::EMPTY_DICT_SIZE)?;
            let dict = PyDict::new(py);
            src.for_each_object_key(|key, src| {
                let value = read_json_value(src, budget)?;
                budget
                    .charge(budget::DICT_ENTRY_SIZE + budget::STR_OVERHEAD + key.chars().count())?;
                dict.set_item(PyString::new(py, key), value)?;
                Ok(())
            })?;
            Ok(dict.into_any())
        }
    }
}

/// Error context for a value being parsed.
pub(crate) enum FieldContext<'a, 'py> {
    Field {
        marshaler: &'a MessageMarshaler,
        name: &'a Bound<'py, PyString>,
    },
    Extension {
        type_name: &'a str,
    },
}

impl FieldContext<'_, '_> {
    fn error(&self, message: &str, exc: Exc) -> PyErr {
        let full = match self {
            FieldContext::Field { marshaler, name } => {
                format!("{message} for field {}.{name}", marshaler.type_name)
            }
            FieldContext::Extension { type_name } => {
                format!("{message} for extension {type_name}")
            }
        };
        match exc {
            Exc::Value => PyValueError::new_err(full),
            Exc::Type => PyTypeError::new_err(full),
            Exc::Overflow => PyOverflowError::new_err(full),
        }
    }
}
