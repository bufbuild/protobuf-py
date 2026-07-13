# Serializing Messages

Messages can be serialized to and from two formats: **binary** and **JSON**.

As a general guide: use JSON when you need human-readable output or interoperability with non-Protobuf consumers.
Use binary for everything else; it is more compact, faster to parse, and more resilient to schema changes.
For example, you can rename a field in your `.proto` file and still parse binary data serialized with the previous version, because binary encoding uses field numbers rather than names.
JSON output uses field names, so a rename will break consumers unless you use the `json_name` option.

JSON output follows the [Protobuf JSON specification](https://protobuf.dev/programming-guides/json/).
Both formats pass the conformance test suite, ensuring interoperability with implementations in other languages.

## Binary

```python
# Serialize
data: bytes = user.to_binary()

# Deserialize
user = User.from_binary(data)
```

### Options

When a message is parsed from binary data containing field numbers it doesn't recognize, the unknown fields are stored internally and re-emitted during serialization.
This means a message can pass through an intermediary that doesn't know about newer fields without losing data.

`write_unknown_fields`: set to `False` to discard unknown fields on serialization:

```python
data = user.to_binary(write_unknown_fields=False)
```

`ignore_unknown_fields`: set to `True` to discard unknown fields on parse so they are never stored:

```python
user = User.from_binary(data, ignore_unknown_fields=True)
```

## JSON

```python
# Serialize
text: str = user.to_json()

# Deserialize
user = User.from_json(text)
```

Field names are converted to `camelCase` in the JSON output, per the Protobuf JSON specification.
`first_name` becomes `"firstName"`, `last_name` becomes `"lastName"`, and so on.

### Options

`always_emit_implicit`: by default, fields with *implicit presence* are omitted from the output when they hold the zero value.
Set this to `True` to always include them:

```python
user = User()   # first_name is "" (zero value)
user.to_json()  # {} (first_name omitted)
user.to_json(always_emit_implicit=True)  # {"firstName":""}
```

`print_enums_as_ints`: by default, enum values are serialized as string names.
Set this to `True` to serialize them as integers instead:

```python
msg.to_json(print_enums_as_ints=True)
# {"status":1} instead of {"status":"ACTIVE"}
```

`use_proto_field_name`: by default, field names are converted to `camelCase` in JSON output.
Set this to `True` to use the original `snake_case` proto field names instead:

```python
user.to_json(use_proto_field_name=True)
# {"first_name":"Homer"} instead of {"firstName":"Homer"}
```

`registry`: required when the message contains a [`google.protobuf.Any`](./well-known-types.md#any) field or extensions.
See [`Registry`](./reflection/registry.md) for how to construct and populate one.
Extensions not found in the registry are silently omitted from the output.

```python
registry = Registry()
# ... register types ...
user.to_json(registry=registry)
```

`ignore_unknown_fields` on `from_json`: by default, JSON keys that don't correspond to a known field raise an error.
Set this to `True` to silently skip them:

```python
user = User.from_json(text, ignore_unknown_fields=True)
```

## Merging

Instead of creating a new message, you can parse data into an existing one.
This is useful for applying partial updates or combining data from multiple sources.

```python
from protobuf import merge_from_binary, merge_from_json, merge_from

# Merge binary data into an existing message
merge_from_binary(user, data)

# Merge JSON into an existing message
merge_from_json(user, text)

# Merge one message into another of the same type
merge_from(target, source)
```

Merge semantics follow the Protobuf specification:

- **Scalar and enum fields**: the source value overwrites the target.
- **Message fields**: merged recursively if the target field is already set; otherwise the source value is set directly.
- **Repeated fields**: source elements are appended to the target list.
- **Map fields**: source entries are added; existing keys are overwritten. Message-valued map entries are not recursively merged.
- **Unknown fields**: retained in the target unless `ignore_unknown_fields=True` is passed.

## Text Format

In addition to binary and JSON, Protobuf also provides [text format](https://protobuf.dev/reference/protobuf/textformat-spec/), a plain-text syntax used for debugging, tests, and config files.
You can use it to read and write `.txtpb` files.

```python
from protobuf.txtpb import message_from_text, message_to_text

# Serialize
text: str = message_to_text(user)

# Deserialize
user = message_from_text(User, text)
```

Serializing the example message from the [tutorial](./tutorial.md) prints:

```txtpb
first_name: "Alice"
last_name: "Smith"
active: true
locations: "NYC"
locations: "LDN"
projects {
  key: "atlas"
  value: "infra"
}
```

The output matches the canonical writer used by `google.protobuf.text_format` (the same style `protoc --decode` and other Protobuf implementations produce): two-space indentation, one field per line, and no colon before a message value's `{`.
Text written by `message_to_text` can be read by the buf CLI, `protoc`, and other implementations, and text they produce can be read by `message_from_text`.

### Options

`registry`: required to write and read [`google.protobuf.Any`](./well-known-types.md#any) fields in their expanded `[type.url] {...}` form, and extension fields (`[pkg.extension_name]`).
Without it, an Any is written as its raw `type_url`/`value` fields, and extensions are omitted from output and rejected on parse.

```python
message_to_text(user, registry=registry)
user = message_from_text(User, text, registry=registry)
```

`print_unknown_fields`: set to `True` to print unknown fields by their field number.
This is a debugging aid only: `message_from_text` rejects fields addressed by number, so output that includes them cannot be parsed back.

```python
message_to_text(user, print_unknown_fields=True)
```

`ignore_unknown_fields`: set to `True` to silently skip unknown fields on parse instead of raising an error.

```python
user = message_from_text(User, text, ignore_unknown_fields=True)
```

To merge into an existing message, use `merge_from_text`:

```python
from protobuf.txtpb import merge_from_text

merge_from_text(user, text)
```
