# Well-Known Types

The Protobuf standard library defines a set of common message types known as *well-known types* (WKTs).
These are pre-generated and shipped with the runtime in [`protobuf.wkt`][protobuf.wkt], so you don't need to generate them yourself.

```python
from protobuf.wkt import Timestamp, Duration, Any
```

In addition to the generated message classes, helper methods provide idiomatic Python conversions for the most commonly used types.

## Timestamp

`Timestamp` represents a point in time with nanosecond precision.

```python
from protobuf.wkt import Timestamp
from datetime import datetime, timezone

# Current time
ts = Timestamp.now()

# From a datetime
ts = Timestamp.from_datetime(datetime(2024, 1, 1, tzinfo=timezone.utc))

# From seconds since Unix epoch
ts = Timestamp.from_seconds(1704067200.0)

# From nanoseconds since Unix epoch
ts = Timestamp.from_nanos(1_704_067_200_000_000_000)

# Convert back
dt: datetime  = ts.to_datetime()
s:  float     = ts.to_seconds()
ns: int       = ts.to_nanos()
```

`Timestamp` serializes to an RFC 3339 string in ProtoJSON (`"2024-01-01T00:00:00Z"`).

## Duration

`Duration` represents a span of time with nanosecond precision.

```python
from protobuf.wkt import Duration
from datetime import timedelta

# From a timedelta
d = Duration.from_timedelta(timedelta(hours=1, minutes=30))

# From seconds
d = Duration.from_seconds(5400.0)

# From nanoseconds
d = Duration.from_nanos(5_400_000_000_000)

# Convert back
td: timedelta = d.to_timedelta()
s:  float     = d.to_seconds()
ns: int       = d.to_nanos()
```

`Duration` serializes to a seconds string in ProtoJSON (`"5400s"`).

## Any

`Any` wraps an arbitrary message together with its type URL so that heterogeneous values can be passed through APIs that don't know the concrete type in advance.

```python
from protobuf.wkt import Any
from protobuf import Registry

# Pack a message into an Any
user = User(first_name="Alice")
any_msg = Any.pack(user)

# Check the type without unpacking
any_msg.is_type(User)            # True
any_msg.is_type("example.User") # True (by type name)

# Unpack
user = any_msg.unpack(User)      # User | None
```

`unpack()` returns `None` if the `Any` is empty or contains a different type.

Serializing and deserializing `Any` to ProtoJSON requires a [`Registry`][protobuf.Registry] so the runtime can look up the packed type by its URL:

```python
registry = Registry()
registry.add(example_pb.desc())   # register the file containing User

text = any_msg.to_json(registry=registry)
restored = Any.from_json(text, registry=registry)
```

## Value

`Value` represents an arbitrary value that can be represented as JSON. This can be used to convert values decoded from JSON
for use with other Protobuf messages or to represent a polymorphic value within a message.

`Value` can be easily converted to and from standard Python types. Note that because it represents JSON, all numbers, including int,
are treated as floating point.

```python
>>> from protobuf.wkt import Value

>>> v = Value.from_python(True)
>>> v.to_python()
True

>>> v = Value.from_python({
    "animal": "cat",
    "lives": 9,
    "hobbies": ["sleeping", "purring"],
    "relations": [
        {
            "animal": "dog",
            "kind": "rival",
        },
        {
            "animal": "mouse",
            "kind": "toy",
        }
    ]
})
>>> v.to_python() # Notice 9 has been converted to a float
{'animal': 'cat', 'lives': 9.0, 'hobbies': ['sleeping', 'purring'], 'relations': [{'animal': 'dog', 'kind': 'rival'}, {'animal': 'mouse', 'kind': 'toy'}]}
```

## Other well-known types

[`protobuf.wkt`][protobuf.wkt] also includes:

- `FieldMask`: a set of field paths used to specify which fields to read or update in partial operations.
- `Empty`: a message with no fields, used as a placeholder response type in RPC services.
- Wrapper types (`BoolValue`, `StringValue`, `Int32Value`, etc.): regular messages that box a scalar to distinguish "not set" from the zero value. Prefer `optional` fields in new schemas instead.
- `FileDescriptorSet`: a collection of file descriptors; its `to_registry()` method is the entry point for dynamic messaging.
- Descriptor types (`FileDescriptorProto`, `DescriptorProto`, etc.): the Protobuf descriptor model itself, used for reflection.
- Compiler plugin types (`CodeGeneratorRequest`, `CodeGeneratorResponse`): used when [writing plugins](./api/plugin.md).

See the [API reference](./api/wkt.md) for the complete list.
