# Registry

A [`Registry`][protobuf.Registry] is a collection of descriptors that enables lookup by name.
It is only needed when working with [`google.protobuf.Any`](../well-known-types.md#any) or [extensions in ProtoJSON](../extensions.md#extensions-and-json); everywhere else, descriptors are self-contained.

## Creating a registry

Pass file descriptors (or message/enum types) to the constructor:

```python
from protobuf import Registry
from gen import example_pb

registry = Registry(example_pb.desc())
```

Or build one incrementally with `add()`:

```python
registry = Registry()
registry.add(example_pb.desc())
```

## Looking up types

```python
registry.message("example.User")         # DescMessage | None
registry.enum("example.PhoneType")       # DescEnum | None
registry.file("example.proto")           # DescFile | None
registry.extension("example.sensitive")  # DescExtension | None
```

## Using a registry with Any and JSON

Pass the registry when serializing or deserializing messages that contain `google.protobuf.Any` fields or extensions.
See [Any](../well-known-types.md#any) and [Extensions and JSON](../extensions.md#extensions-and-json) for examples.

## Iterating over fields

Iterating over a message yields the [`DescField`][protobuf.DescField] of each currently set field; see [Working with Messages](../messages.md#iterating-over-fields) for details.
The registry pairs naturally with message iteration to build generic tools (serializers, validators, diff tools) that operate on any message type without knowing the concrete type at compile time.
