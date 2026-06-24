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
user.to_json(always_emit_implicit=True)  # {"firstName": ""}
```

`print_enums_as_ints`: by default, enum values are serialized as string names.
Set this to `True` to serialize them as integers instead:

```python
msg.to_json(print_enums_as_ints=True)
# {"status": 1} instead of {"status": "ACTIVE"}
```

`use_proto_field_name`: by default, field names are converted to `camelCase` in JSON output.
Set this to `True` to use the original `snake_case` proto field names instead:

```python
user.to_json(use_proto_field_name=True)
# {"first_name": "Homer"} instead of {"firstName": "Homer"}
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

