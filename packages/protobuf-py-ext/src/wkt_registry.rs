//! Central registry for well-known types to handle special JSON marshaling.
//! Closely mirrors `_wkt_registry.py`.

use std::collections::HashMap;

use buffa::json_helpers::wkt as buffa_wkt;
use bytes::Bytes;
use pyo3::{
    Bound, IntoPyObjectExt as _, Py, PyAny, PyResult, Python,
    exceptions::{PyTypeError, PyValueError},
    types::{
        PyAnyMethods as _, PyBool, PyDict, PyDictMethods as _, PyFloat, PyInt, PyList,
        PyListMethods as _, PyString, PyStringMethods as _, PyType,
    },
};

use crate::{
    attribute_access::AttributeAccess,
    constants::Constants,
    descriptor::{DescField, DescFieldValue, DescMessage, DescSingleValue, ScalarType},
    json_parse::{FieldContext, FromJsonOpts, read_json_value, read_message, read_scalar},
    json_serialize::{
        JsonOpts, read_int32_attr, read_int64_attr, write_message_json, write_scalar_json,
    },
    json_sink::JsonSink,
    json_source::{JsonKind, JsonSource, PyTreeSource},
    marshaler::MessageMarshaler,
    nativemessage::NativeMessage,
    oneof::Oneof,
    serializer::MessageSerializer,
};

/// `google.protobuf.Timestamp`.
pub(crate) struct WktTimestamp {
    seconds: AttributeAccess,
    nanos: AttributeAccess,
}

impl WktTimestamp {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        _opts: &JsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let secs = read_int64_attr(py, message, &self.seconds)?;
        let nanos = read_int32_attr(py, message, &self.nanos)?;
        sink.str(&format_timestamp(secs, nanos)?)
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        _opts: &FromJsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        let (secs, nanos) = with_wkt_str(marshaler, src, |text| {
            parse_timestamp(&marshaler.type_name, text)
        })?;
        self.seconds
            .set(message.as_any(), PyInt::new(py, secs).as_any())?;
        self.nanos
            .set(message.as_any(), PyInt::new(py, nanos).as_any())?;
        Ok(())
    }
}

/// `google.protobuf.Duration`.
pub(crate) struct WktDuration {
    seconds: AttributeAccess,
    nanos: AttributeAccess,
}

impl WktDuration {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        _opts: &JsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let secs = read_int64_attr(py, message, &self.seconds)?;
        let nanos = read_int32_attr(py, message, &self.nanos)?;
        sink.str(&format_duration(secs, nanos)?)
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        _opts: &FromJsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        let (secs, nanos) = with_wkt_str(marshaler, src, |text| {
            parse_duration(&marshaler.type_name, text)
        })?;
        self.seconds
            .set(message.as_any(), PyInt::new(py, secs).as_any())?;
        self.nanos
            .set(message.as_any(), PyInt::new(py, nanos).as_any())?;
        Ok(())
    }
}

/// `google.protobuf.Any`.
pub(crate) struct WktAny {
    type_url: AttributeAccess,
    value: AttributeAccess,
}

impl WktAny {
    fn write_json<S: JsonSink>(
        &self,
        marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let constants = &marshaler.constants;
        let type_url_py = self.type_url.get(py, message.as_any())?;
        let type_url = type_url_py.extract::<&str>()?;
        if type_url.is_empty() {
            sink.begin_object()?;
            sink.end_object()?;
            return Ok(());
        }
        let Some(registry) = &opts.registry else {
            return Err(PyValueError::new_err(format!(
                "any \"{type_url}\" is not in the type registry"
            )));
        };
        let registry = registry.bind(py);
        let type_name = type_url_to_name(type_url)?;
        let desc = registry.call_method1(constants.message.bind(py), (type_name,))?;
        if desc.is_none() {
            return Err(PyValueError::new_err(format!(
                "any: \"{type_url}\" is not in the type registry"
            )));
        }
        let inner_type = desc.getattr(&constants.type_)?.cast_into::<PyType>()?;
        let inner_marshaler = inner_type
            .getattr(&constants.ext_marshaler)?
            .cast_into::<MessageMarshaler>()?;
        let inner_marshaler = inner_marshaler.get();

        let value = self.value.get(py, message.as_any())?.extract::<Bytes>()?;
        let inner_msg = inner_marshaler.new_empty_message(py, &inner_type)?;
        inner_marshaler.merge_from_binary(py, &inner_msg, value, false)?;

        sink.begin_object()?;
        if inner_marshaler.wkt.is_none() {
            // Regular message: inline its fields after `@type`.
            sink.key("@type")?;
            sink.str(type_url)?;
            inner_marshaler.write_message_fields(py, &inner_msg, sink, opts, depth + 1)?;
        } else {
            // Well-known type with a custom JSON representation: wrap in `value`.
            sink.key("@type")?;
            sink.str(type_url)?;
            sink.key("value")?;
            inner_marshaler.write_json(py, &inner_msg, sink, opts, depth + 1)?;
        }
        sink.end_object()?;
        Ok(())
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        opts: &FromJsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        let message_type_name = &marshaler.type_name;
        // For a string input, this will eagerly parse out a whole dictionary since
        // we need to first find `@type` before parsing.
        let tree = read_json_value(src)?;
        let Ok(dict) = tree.cast::<PyDict>() else {
            return Err(PyTypeError::new_err(format!(
                "cannot decode {message_type_name} from JSON: {}",
                tree.str()?
            )));
        };
        if dict.is_empty() {
            return Ok(());
        }
        let type_url_py = dict
            .get_item("@type")?
            .unwrap_or_else(|| py.None().into_bound(py));
        let type_url = match type_url_py.extract::<&str>() {
            Ok(type_url) if !type_url.is_empty() => type_url,
            _ => {
                return Err(PyValueError::new_err(format!(
                    "cannot decode {message_type_name} from JSON: {dict}, @type is invalid: {type_url_py}",
                )));
            }
        };
        let type_name = match type_url.rfind('/') {
            Some(index) => &type_url[index + 1..],
            None => type_url,
        };
        let registry = opts.registry.as_ref().map(|registry| registry.bind(py));
        let desc = match &registry {
            Some(registry) => registry.call_method1(&marshaler.constants.message, (type_name,))?,
            None => py.None().into_bound(py),
        };
        if desc.is_none() {
            return Err(PyValueError::new_err(format!(
                "cannot decode {message_type_name} from JSON: {type_url} is not in the type registry"
            )));
        }
        let inner_type = desc
            .getattr(&marshaler.constants.type_)?
            .cast_into::<PyType>()?;
        let inner_marshaler = inner_type
            .getattr(&marshaler.constants.ext_marshaler)?
            .cast_into::<MessageMarshaler>()?;
        let inner_marshaler = inner_marshaler.get();
        let inner_msg = inner_marshaler.new_empty_message(py, &inner_type)?;

        let is_wkt = inner_marshaler.wkt.is_some();
        if is_wkt && dict.contains("value")? {
            let value = dict
                .get_item("value")?
                .unwrap_or_else(|| py.None().into_bound(py));
            let mut sub = PyTreeSource::new(py, value);
            read_message(inner_marshaler, &inner_msg, &mut sub, opts, 1)?;
        } else {
            let copy = dict.copy()?;
            copy.del_item("@type")?;
            let mut sub = PyTreeSource::new(py, copy.into_any());
            read_message(inner_marshaler, &inner_msg, &mut sub, opts, 1)?;
        }

        // Any.pack
        let packed_url = format!("type.googleapis.com/{}", inner_marshaler.type_name);
        let packed_value = inner_marshaler.to_binary(py, &inner_msg, true)?;
        self.type_url
            .set(message.as_any(), &PyString::new(py, &packed_url).into_any())?;
        self.value.set(message.as_any(), packed_value.as_any())?;
        Ok(())
    }
}

/// `google.protobuf.FieldMask`.
pub(crate) struct WktFieldMask {
    paths: AttributeAccess,
}

impl WktFieldMask {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        _opts: &JsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let paths = self
            .paths
            .get(py, message.as_any())?
            .cast_into::<PyList>()?;
        if paths.is_empty() {
            return sink.str("");
        }
        let mut out = String::new();
        for path in paths {
            let path = path.extract::<&str>()?;
            if !buffa_wkt::field_mask_path_round_trips(path) {
                return Err(PyValueError::new_err(format!(
                    "invalid FieldMask path: lowerCamelCase of {path} is irreversible"
                )));
            }
            out.push_str(&buffa_wkt::snake_to_camel(path));
            out.push(',');
        }
        // Drop trailing comma.
        sink.str(&out[..out.len() - 1])
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        _opts: &FromJsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        let paths = self
            .paths
            .get(py, message.as_any())?
            .cast_into::<PyList>()?;
        with_wkt_str(marshaler, src, |text| {
            if text.is_empty() {
                return Ok(());
            }
            for part in text.split(',') {
                if part.contains('_') {
                    return Err(PyValueError::new_err(format!(
                        "cannot decode {} from JSON: path names must be lowerCamelCase",
                        marshaler.type_name
                    )));
                }
                paths.append(buffa_wkt::camel_to_snake(part))?;
            }
            Ok(())
        })
    }
}

/// `google.protobuf.Struct`; `value` is the `google.protobuf.Value` element.
pub(crate) struct WktStruct {
    fields: AttributeAccess,
    value: DescMessage,
}

impl WktStruct {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let map = self
            .fields
            .get(py, message.as_any())?
            .cast_into::<PyDict>()?;
        sink.begin_object()?;
        for (key, entry) in map {
            sink.py_key(key.cast::<PyString>()?)?;
            write_message_json(py, &self.value, &entry, sink, opts, depth)?;
        }
        sink.end_object()?;
        Ok(())
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        opts: &FromJsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        if src.peek()? != JsonKind::Object {
            let json = read_json_value(src)?;
            return Err(PyTypeError::new_err(format!(
                "cannot decode {} from JSON: {}",
                marshaler.type_name,
                json.str()?
            )));
        }
        let value_marshaler = self.value.get_marshaler(py)?;
        let dict = self
            .fields
            .get(py, message.as_any())?
            .cast_into::<PyDict>()?;
        // Duplicate keys use last-in-wins semantics (per the ProtoJSON spec).
        src.for_each_object_key(|key, src| {
            let value_msg =
                value_marshaler.new_empty_message(py, self.value.get_python_type(py))?;
            read_message(value_marshaler, &value_msg, src, opts, depth + 1)?;
            dict.set_item(key, value_msg)?;
            Ok(())
        })?;
        Ok(())
    }
}

/// `google.protobuf.ListValue`; `element` is the `google.protobuf.Value`.
pub(crate) struct WktListValue {
    values: AttributeAccess,
    element: DescMessage,
}

impl WktListValue {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let values = self
            .values
            .get(py, message.as_any())?
            .cast_into::<PyList>()?;
        sink.begin_array()?;
        for item in values.iter() {
            write_message_json(py, &self.element, &item, sink, opts, depth)?;
        }
        sink.end_array()?;
        Ok(())
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        opts: &FromJsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        if src.peek()? != JsonKind::Array {
            let json = read_json_value(src)?;
            return Err(PyTypeError::new_err(format!(
                "cannot decode {} from JSON: {}",
                marshaler.type_name,
                json.str()?
            )));
        }
        let element_marshaler = self.element.get_marshaler(py)?;
        let list = self
            .values
            .get(py, message.as_any())?
            .cast_into::<PyList>()?;
        src.for_each_array_item(|src| {
            let value_msg =
                element_marshaler.new_empty_message(py, self.element.get_python_type(py))?;
            read_message(element_marshaler, &value_msg, src, opts, depth + 1)?;
            list.append(value_msg)?;
            Ok(())
        })?;
        Ok(())
    }
}

/// `google.protobuf.Value`.
pub(crate) struct WktValue {
    kind: AttributeAccess,
    null_name: Py<PyString>,
    number_name: Py<PyString>,
    string_name: Py<PyString>,
    bool_name: Py<PyString>,
    struct_name: Py<PyString>,
    list_name: Py<PyString>,
    null_zero: Py<PyAny>,
    struct_message: DescMessage,
    list_message: DescMessage,
}

impl WktValue {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let Ok(oneof) = self.kind.get(py, message.as_any())?.cast_into::<Oneof>() else {
            return Err(PyValueError::new_err(
                "value must have exactly one field set",
            ));
        };
        let oneof = oneof.get();
        let field = oneof.field.bind(py).extract::<&str>()?;
        let kind_value = oneof.value.bind(py);
        match field {
            "null_value" => sink.null(),
            "number_value" => {
                let number = kind_value.extract::<f64>()?;
                if !number.is_finite() {
                    return Err(PyValueError::new_err("value cannot be NaN or Infinity"));
                }
                sink.py_number(kind_value)
            }
            "string_value" => sink.py_str(kind_value.cast::<PyString>()?),
            "bool_value" => sink.bool(kind_value.extract::<bool>()?),
            "struct_value" => {
                write_message_json(py, &self.struct_message, kind_value, sink, opts, depth)
            }
            "list_value" => {
                write_message_json(py, &self.list_message, kind_value, sink, opts, depth)
            }
            _ => Err(PyValueError::new_err(
                "value must have exactly one field set",
            )),
        }
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        _marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        opts: &FromJsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        let oneof = match src.peek()? {
            JsonKind::Null => {
                src.next_null()?;
                Oneof::new(self.null_name.bind(py), self.null_zero.bind(py))
            }
            JsonKind::Bool => Oneof::new(
                self.bool_name.bind(py),
                &PyBool::new(py, src.next_bool()?).into_bound_py_any(py)?,
            ),
            JsonKind::Number => {
                let number = src.next_float()?;
                Oneof::new(
                    self.number_name.bind(py),
                    &PyFloat::new(py, number).into_any(),
                )
            }
            JsonKind::String => {
                let string = src.next_py_str()?;
                Oneof::new(self.string_name.bind(py), &string)
            }
            JsonKind::Array => {
                let desc = &self.list_message;
                let inner = desc.get_marshaler(py)?;
                let list_msg = inner.new_empty_message(py, desc.get_python_type(py))?;
                read_message(inner, &list_msg, src, opts, depth + 1)?;
                Oneof::new(self.list_name.bind(py), &list_msg.into_any())
            }
            JsonKind::Object => {
                let desc = &self.struct_message;
                let inner = desc.get_marshaler(py)?;
                let struct_msg = inner.new_empty_message(py, desc.get_python_type(py))?;
                read_message(inner, &struct_msg, src, opts, depth + 1)?;
                Oneof::new(self.struct_name.bind(py), &struct_msg.into_any())
            }
        };
        self.kind
            .set(message.as_any(), &oneof.into_bound_py_any(py)?)
    }
}

/// A wrapper typ.
pub(crate) struct WktWrapper {
    field: AttributeAccess,
    scalar: ScalarType,
    /// Proto field name for errors.
    name: Py<PyString>,
}

impl WktWrapper {
    fn write_json<S: JsonSink>(
        &self,
        _marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        _opts: &JsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let value = self.field.get(py, message.as_any())?;
        write_scalar_json(self.scalar, &value, sink)
    }

    fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        _opts: &FromJsonOpts,
        _depth: usize,
    ) -> PyResult<()> {
        let py = src.py();
        if src.peek()? == JsonKind::Null {
            src.next_null()?;
            self.field
                .set(message.as_any(), &self.scalar.zero_value(py).into_bound(py))?;
            return Ok(());
        }
        let name = self.name.bind(py);
        let ctx = FieldContext::Field { marshaler, name };
        let value = read_scalar(&ctx, src, self.scalar)?;
        self.field.set(message.as_any(), &value)
    }
}

/// Well-known-type classification with pre-resolved accessors.
pub(crate) enum WktKind {
    Timestamp(WktTimestamp),
    Duration(WktDuration),
    Any(WktAny),
    FieldMask(WktFieldMask),
    Struct(WktStruct),
    ListValue(WktListValue),
    Value(WktValue),
    Wrapper(WktWrapper),
}

impl WktKind {
    /// Serializes the message.
    pub(crate) fn write_json<S: JsonSink>(
        &self,
        marshaler: &MessageMarshaler,
        py: Python<'_>,
        message: &Bound<'_, NativeMessage>,
        sink: &mut S,
        opts: &JsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        match self {
            WktKind::Timestamp(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::Duration(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::Any(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::FieldMask(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::Struct(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::ListValue(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::Value(w) => w.write_json(marshaler, py, message, sink, opts, depth),
            WktKind::Wrapper(w) => w.write_json(marshaler, py, message, sink, opts, depth),
        }
    }

    /// Parses the message.
    pub(crate) fn read_json<'py, R: JsonSource<'py>>(
        &self,
        marshaler: &MessageMarshaler,
        message: &Bound<'py, NativeMessage>,
        src: &mut R,
        opts: &FromJsonOpts,
        depth: usize,
    ) -> PyResult<()> {
        match self {
            WktKind::Timestamp(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::Duration(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::Any(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::FieldMask(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::Struct(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::ListValue(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::Value(w) => w.read_json(marshaler, message, src, opts, depth),
            WktKind::Wrapper(w) => w.read_json(marshaler, message, src, opts, depth),
        }
    }

    /// Detects if the message is a WKT. This includes ones that arenot actually our `protobuf.wkt` packaged types.
    pub(crate) fn detect(
        py: Python<'_>,
        message_desc: &Bound<'_, PyAny>,
        fields: &[DescField],
        serializer: &MessageSerializer,
        constants: &Constants,
    ) -> PyResult<Option<Box<WktKind>>> {
        let type_name_py = message_desc.getattr(&constants.type_name)?;
        let type_name = type_name_py.extract::<&str>()?;
        if !type_name.starts_with("google.protobuf.") {
            return Ok(None);
        }
        let file_name_any = message_desc
            .getattr(&constants.file)?
            .getattr(&constants.name)?;
        if !file_name_any
            .extract::<&str>()?
            .starts_with("google/protobuf/")
        {
            return Ok(None);
        }

        // Proto field name -> field index.
        let mut by_name: HashMap<String, usize> = HashMap::with_capacity(fields.len());
        for (index, field) in fields.iter().enumerate() {
            by_name.insert(field.name.bind(py).to_str()?.to_owned(), index);
        }

        // Clones the accessor for field index `i`.
        let attr = |i: usize| serializer.fields()[i].attr.clone_ref(py);

        let kind = match type_name {
            "google.protobuf.Timestamp" => {
                timestamp_duration_fields(fields, &by_name).map(|(s, n)| {
                    WktKind::Timestamp(WktTimestamp {
                        seconds: attr(s),
                        nanos: attr(n),
                    })
                })
            }
            "google.protobuf.Duration" => {
                timestamp_duration_fields(fields, &by_name).map(|(s, n)| {
                    WktKind::Duration(WktDuration {
                        seconds: attr(s),
                        nanos: attr(n),
                    })
                })
            }
            "google.protobuf.Any" => match_any(fields, &by_name).map(|(url, value)| {
                WktKind::Any(WktAny {
                    type_url: attr(url),
                    value: attr(value),
                })
            }),
            "google.protobuf.FieldMask" => match_field_mask(fields, &by_name)
                .map(|paths| WktKind::FieldMask(WktFieldMask { paths: attr(paths) })),
            "google.protobuf.Struct" => match_struct(fields, &by_name).map(|fields_idx| {
                WktKind::Struct(WktStruct {
                    fields: attr(fields_idx),
                    value: message_of(&fields[fields_idx].value),
                })
            }),
            "google.protobuf.ListValue" => match_list_value(fields, &by_name).map(|values| {
                WktKind::ListValue(WktListValue {
                    values: attr(values),
                    element: message_of(&fields[values].value),
                })
            }),
            "google.protobuf.Value" => match_value(py, fields, serializer, &by_name),
            _ => match_wrapper(fields, &by_name).map(|scalar| {
                WktKind::Wrapper(WktWrapper {
                    field: attr(0),
                    scalar,
                    name: fields[0].name.clone_ref(py),
                })
            }),
        };
        Ok(kind.map(Box::new))
    }
}

/// Extracts the nested message descriptor from a singular/list/map value that is
/// known (by prior shape check) to be message-typed.
fn message_of(value: &DescFieldValue) -> DescMessage {
    match value {
        DescFieldValue::Message { message, .. }
        | DescFieldValue::List {
            element: DescSingleValue::Message { message, .. },
            ..
        }
        | DescFieldValue::Map {
            value: DescSingleValue::Message { message, .. },
            ..
        } => message.clone(),
        _ => unreachable!("caller verified this field is message-typed"),
    }
}

fn is_scalar(value: &DescFieldValue, want: ScalarType) -> bool {
    matches!(value, DescFieldValue::Scalar { scalar_type, .. } if *scalar_type == want)
}

fn is_enum(value: &DescFieldValue) -> bool {
    matches!(value, DescFieldValue::Enum { .. })
}

fn is_message(value: &DescFieldValue) -> bool {
    matches!(value, DescFieldValue::Message { .. })
}

fn is_list_scalar(value: &DescFieldValue, want: ScalarType) -> bool {
    matches!(value, DescFieldValue::List { element: DescSingleValue::Scalar(t), .. } if *t == want)
}

fn is_list_message(value: &DescFieldValue) -> bool {
    matches!(
        value,
        DescFieldValue::List {
            element: DescSingleValue::Message { .. },
            ..
        }
    )
}

fn is_map_key(value: &DescFieldValue, want: ScalarType) -> bool {
    matches!(value, DescFieldValue::Map { key_type, .. } if *key_type == want)
}

/// Timestamp/Duration share the same shape: int64 `seconds` + int32 `nanos`.
fn timestamp_duration_fields(
    fields: &[DescField],
    by_name: &HashMap<String, usize>,
) -> Option<(usize, usize)> {
    let seconds = *by_name.get("seconds")?;
    let nanos = *by_name.get("nanos")?;
    (is_scalar(&fields[seconds].value, ScalarType::Int64)
        && is_scalar(&fields[nanos].value, ScalarType::Int32))
    .then_some((seconds, nanos))
}

fn match_any(fields: &[DescField], by_name: &HashMap<String, usize>) -> Option<(usize, usize)> {
    let type_url = *by_name.get("type_url")?;
    let value = *by_name.get("value")?;
    (is_scalar(&fields[type_url].value, ScalarType::String)
        && is_scalar(&fields[value].value, ScalarType::Bytes))
    .then_some((type_url, value))
}

fn match_field_mask(fields: &[DescField], by_name: &HashMap<String, usize>) -> Option<usize> {
    let paths = *by_name.get("paths")?;
    is_list_scalar(&fields[paths].value, ScalarType::String).then_some(paths)
}

fn match_struct(fields: &[DescField], by_name: &HashMap<String, usize>) -> Option<usize> {
    let fields_idx = *by_name.get("fields")?;
    is_map_key(&fields[fields_idx].value, ScalarType::String).then_some(fields_idx)
}

fn match_list_value(fields: &[DescField], by_name: &HashMap<String, usize>) -> Option<usize> {
    let values = *by_name.get("values")?;
    is_list_message(&fields[values].value).then_some(values)
}

fn match_value(
    py: Python<'_>,
    fields: &[DescField],
    serializer: &MessageSerializer,
    by_name: &HashMap<String, usize>,
) -> Option<WktKind> {
    let (
        Some(null_value),
        Some(number_value),
        Some(string_value),
        Some(bool_value),
        Some(struct_value),
        Some(list_value),
    ) = (
        by_name.get("null_value").copied(),
        by_name.get("number_value").copied(),
        by_name.get("string_value").copied(),
        by_name.get("bool_value").copied(),
        by_name.get("struct_value").copied(),
        by_name.get("list_value").copied(),
    )
    else {
        return None;
    };
    if !(is_enum(&fields[null_value].value)
        && is_scalar(&fields[number_value].value, ScalarType::Double)
        && is_scalar(&fields[string_value].value, ScalarType::String)
        && is_scalar(&fields[bool_value].value, ScalarType::Bool)
        && is_message(&fields[struct_value].value)
        && is_message(&fields[list_value].value))
    {
        return None;
    }
    let null_zero = match &fields[null_value].value {
        DescFieldValue::Enum { enum_, .. } => enum_.zero_value.clone_ref(py),
        _ => return None,
    };
    // All `kind` members share the oneof accessor stored on each field.
    let kind = serializer.fields()[null_value]
        .oneof
        .as_ref()?
        .clone_ref(py);
    let local = |i: usize| fields[i].local_name.clone_ref(py);
    Some(WktKind::Value(WktValue {
        kind,
        null_name: local(null_value),
        number_name: local(number_value),
        string_name: local(string_value),
        bool_name: local(bool_value),
        struct_name: local(struct_value),
        list_name: local(list_value),
        null_zero,
        struct_message: message_of(&fields[struct_value].value),
        list_message: message_of(&fields[list_value].value),
    }))
}

fn match_wrapper(fields: &[DescField], by_name: &HashMap<String, usize>) -> Option<ScalarType> {
    // Structural fallthrough: exactly one scalar field named `value`.
    if fields.len() != 1 || by_name.get("value") != Some(&0) {
        return None;
    }
    match &fields[0].value {
        DescFieldValue::Scalar { scalar_type, .. } => Some(*scalar_type),
        _ => None,
    }
}

fn with_wkt_str<'py, S: JsonSource<'py>, R>(
    marshaler: &MessageMarshaler,
    src: &mut S,
    f: impl FnOnce(&str) -> PyResult<R>,
) -> PyResult<R> {
    if src.peek()? != JsonKind::String {
        let value = read_json_value(src)?;
        return Err(PyTypeError::new_err(format!(
            "cannot decode {} from JSON: {}",
            marshaler.type_name,
            value.str()?
        )));
    }
    src.with_next_str(f)
}

fn type_url_to_name(url: &str) -> PyResult<&str> {
    let name = match url.rfind('/') {
        Some(index) => &url[index + 1..],
        None => url,
    };
    if name.is_empty() {
        return Err(PyValueError::new_err(format!("invalid type url: {url}")));
    }
    Ok(name)
}

// We go ahead and reuse buffa's logic for formatting, similar to how we use
// it for varint handling in binary marhsaling. It's unclear if these are true
// public API, but we'll just vendor them in the future if needed.
// We make sure most error messages match our Python implementation, sometimes meaning
// double (cheap) validation.

const NANOS_PER_SECOND_MAX: i32 = 999_999_999;

fn format_timestamp(seconds: i64, nanos: i32) -> PyResult<String> {
    if !(buffa_wkt::MIN_TIMESTAMP_SECS..=buffa_wkt::MAX_TIMESTAMP_SECS).contains(&seconds) {
        return Err(PyValueError::new_err("timestamp seconds out of range"));
    }
    if !(0..=NANOS_PER_SECOND_MAX).contains(&nanos) {
        return Err(PyValueError::new_err("timestamp nanos out of range"));
    }
    buffa_wkt::fmt_timestamp(seconds, nanos).map_err(PyValueError::new_err)
}

fn format_duration(seconds: i64, nanos: i32) -> PyResult<String> {
    if !(-buffa_wkt::MAX_DURATION_SECS..=buffa_wkt::MAX_DURATION_SECS).contains(&seconds) {
        return Err(PyValueError::new_err("duration seconds out of range"));
    }
    if !(-NANOS_PER_SECOND_MAX..=NANOS_PER_SECOND_MAX).contains(&nanos) {
        return Err(PyValueError::new_err("duration nanos out of range"));
    }
    if (seconds > 0 && nanos < 0) || (seconds < 0 && nanos > 0) {
        return Err(PyValueError::new_err(
            "duration seconds and nanos have different signs",
        ));
    }
    buffa_wkt::fmt_duration(seconds, nanos).map_err(PyValueError::new_err)
}

fn parse_timestamp(type_name: &str, text: &str) -> PyResult<(i64, i32)> {
    buffa_wkt::parse_timestamp(text).map_err(|err| {
        // String matching on an error message not the best, but it works and
        // saves us a lot of parsing logic, notably tricky calendar date checking.
        let detail = if err.starts_with("Timestamp out of range") {
            "must be from 0001-01-01T00:00:00Z to 9999-12-31T23:59:59Z inclusive"
        } else {
            "invalid RFC 3339 string"
        };
        PyValueError::new_err(format!("cannot decode {type_name} from JSON: {detail}"))
    })
}

fn parse_duration(type_name: &str, text: &str) -> PyResult<(i64, i32)> {
    buffa_wkt::parse_duration(text)
        .map_err(|_| PyValueError::new_err(format!("cannot decode {type_name} from JSON: {text}")))
}
