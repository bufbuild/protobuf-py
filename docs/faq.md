# Frequently Asked Questions

Common questions about the library.

## Messages

### Why does my field always return `""`, `0`, or `False` even when I never set it?

That is the zero value, and it is the correct default.
In Protobuf, every field has a defined default: `""` for strings, `0` for numeric types, `False` for booleans, `None` for messages.
An unset field and a field explicitly set to its zero value are indistinguishable when using *implicit presence* (the default for proto3 scalar fields).

If you need to tell the difference, use the `optional` keyword to enable *explicit presence* for that field:

```proto
message User {
  optional string nickname = 1;  // "" means "set to empty"; missing means "not set"
}
```

For more information, see [Field presence and default values](./messages.md#field-presence-and-default-values).

---

### How do I check whether a field is set?

Use the `has_field` method.
It returns `True` only if the field was explicitly set:

```python
user.has_field("nickname")   # True if nickname was set, even to ""
```

This only works for fields with *explicit presence*: `optional` scalar fields, message fields, and fields in a `oneof`.
For implicit-presence fields (plain proto3 scalars), the zero value is always treated as absent, so explicitly
setting to the zero value will still result in `False`.

For more information, see [Implicit vs explicit presence](./messages.md#implicit-vs-explicit-presence).

---

### How do I deep-copy a message?

Use [`copy.deepcopy()`](https://docs.python.org/3/library/copy.html#copy.deepcopy):

```python
import copy

clone = copy.deepcopy(original)
```

For shallow copies and partial copies, see [Copying](./messages.md#copying).

---

## Serialization

### Why does my field disappear from JSON output?

Fields with *implicit presence* that hold their zero value are omitted from JSON by default, per the Protobuf JSON specification.
Pass `always_emit_implicit=True` to include them:

```python
user = User(first_name="")
user.to_json()                          # {}
user.to_json(always_emit_implicit=True) # {"firstName": ""}
```

For more information, see [JSON](./serialization.md#json).

---

### Why are field names `firstName` in JSON instead of `first_name`?

The Protobuf JSON specification requires `lowerCamelCase` field names.
Pass `use_proto_field_name=True` to use the original `snake_case` names instead:

```python
user.to_json(use_proto_field_name=True)   # {"first_name": "Homer"}
```

Note: if you rename a field in the `.proto` file, JSON consumers will break because JSON uses names, not field numbers.
Binary encoding uses field numbers, so binary consumers survive renames.

For more information, see [JSON](./serialization.md#json).

---

### What happens to fields I don't recognize during parsing?

Unknown fields are preserved on the message and re-emitted during serialization.
This lets a message pass through an intermediary that doesn't know about newer fields without losing data.

To discard unknown fields on parse:

```python
user = User.from_binary(data, ignore_unknown_fields=True)
```

To omit them on serialize:

```python
data = user.to_binary(write_unknown_fields=False)
```

For more information, see [Binary](./serialization.md#binary).

---


## Generated code

### How do `oneof` fields work?

A `oneof` group is exposed as a single attribute typed as `Oneof[field_name, value_type] | None`, where `None` means no field in the group is set.
Setting any field in the group automatically clears the others.

See [Oneof fields](./generated-code/field-types.md#oneof-fields) for details and a `match` example.

---

## Why is the package named `protobuf`?

The upstream Protobuf implementation is published to PyPI as `protobuf`, with a package named `google.protobuf`.
Our use of the package name `protobuf` matches the PyPI project, which is not ideal. We chose to prioritize _your code_ though.

We believe neither of these

```python
from bufbuild.protobuf import Message

from protobuf_python import Message
```

look anywhere near as good as

```python
from protobuf import Message
```

in your apps. We realize this may make it harder to trace back to our PyPI package from just reading the import but
hope over time the ecosystem around protobuf-py grows to where this is not an issue anymore.

## What are the compatibility guarantees?

Python 3.10 and later versions are supported as long as they are [maintained by CPython](https://devguide.python.org/versions/).

Versioning follows [semantic versioning](https://semver.org/), with a major version increase accompanying breaking changes
and other features introduced with minor version increases. Patch version increases only contain bugfixes.

Breaking changes generally consist of source-level changes to the public API such as method names and parameter names usable as
keyword arguments. In practice, these are the changes that would break type-checking for existing code.

Certain runtime behaviors are explicitly considered non-breaking. On a case-by-case basis, changes to them may be released in
either major or minor versions.

- Exact match of serialized output payloads. For example, it is possible for ordering of fields to change in binary or JSON
  output, or whitespace to change in JSON.
- Behavior for malformed payloads or schemas where the Protobuf specification is ambiguous or silent. For example, a future release
  may reject invalid input that previously parsed, or accept unexpected input that previously raised.
- Error message strings. If you find yourself wanting to match against an error message string, file an issue
  so we can consider creating a dedicated `Exception` type for it.
- Python introspection via `inspect`. For example, a change in attribute access from `__getattr__` to `@property` that retains
  source-level compatibility.
  - Introspection of Protobuf messages should almost always use descriptors rather than Python introspection, which will always
    be supported.
- Implicit exceptions that are not explicitly raised in this codebase or documented in docstrings. Either these exceptions are
  expected to bubble up through calling code or may need fixes in this library. For example, if a function accepts `bytes` but
  raises `TypeError` on `bytearray`, it may be fixed to accept the latter.
- Type annotations may be narrowed for illegitimate usage. For example, a function that accepts `Sequence[int]` and raises a
  `TypeError` for `bytes` at runtime may be narrowed to disallow `bytes` if Python supports it in the future.
- Dropping support for EOL Python versions can happen on minor version releases.

In addition, currently we only guarantee code generated by the same version of `protoc-gen-py` as `protobuf-py` will work.
This will be relaxed in the future.
