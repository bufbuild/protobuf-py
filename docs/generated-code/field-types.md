# Field Types

This page describes how each Protobuf field kind is represented in generated Python code.
The following example message is used throughout:

```proto
syntax = "proto3";
package example;

message User {
  string first_name = 1;
  string last_name = 2;
  bool active = 3;
  User manager = 4;
  repeated string locations = 5;
  map<string, string> projects = 6;
}
```

## Scalar fields

Scalar field types are the primitive types.
They map to Python types as follows:

| Protobuf type | Python type | Default |
|---|---|---|
| `double` | `float` | `0.0` |
| `float` | `float` | `0.0` |
| `int32` | `int` | `0` |
| `int64` | `int` | `0` |
| `uint32` | `int` | `0` |
| `uint64` | `int` | `0` |
| `sint32` | `int` | `0` |
| `sint64` | `int` | `0` |
| `fixed32` | `int` | `0` |
| `fixed64` | `int` | `0` |
| `sfixed32` | `int` | `0` |
| `sfixed64` | `int` | `0` |
| `bool` | `bool` | `False` |
| `string` | `str` | `""` |
| `bytes` | `bytes` | `b""` |

Scalar fields default to the zero value for their type.
In proto3, zero values are not serialized. See [proto3 optional](../messages.md#implicit-vs-explicit-presence) if you need to distinguish "not set" from "set to zero".

## Message fields

A field whose type is another message is typed as `MessageType | None`.
The default value is `None` when the field is not set.

```proto
User manager = 4;
```

```python
user = User()
user.manager        # None

user.manager = User(first_name="Burns")
user.manager.first_name  # "Burns"
```

## Enum fields

Enum fields are typed as the generated `Enum` subclass.
Because `Enum` extends `IntEnum`, values compare equal to plain integers and can be used anywhere an integer is expected:

```python
user = User(phone_type=PhoneType.MOBILE)
user.phone_type   # PhoneType.MOBILE (== 1)
```

See [Enum value prefix stripping](./features.md#enum-value-prefix-stripping) for how value names are generated, and [Enums](../enums.md) for open/closed behavior and JSON representation.

## Repeated fields

Repeated fields are typed as `list[T]` and default to an empty list.

```proto
repeated string locations = 5;
```

```python
user = User()
user.locations              # []
user.locations.append("Springfield")
user.locations              # ["Springfield"]
```

Standard list operations work as expected: `append`, `extend`, `insert`, indexing, and slicing.

## Map fields

Map fields are typed as `dict[K, V]` and default to an empty dict.

```proto
map<string, string> projects = 6;
```

```python
user = User()
user.projects["SPP"] = "Springfield Power Plant"
user.projects           # {"SPP": "Springfield Power Plant"}
```

## Oneof fields

A `oneof` group is represented as a [`Oneof`][protobuf.Oneof] with `field` and `value` attributes.
The property for the group returns `None` when no field in the group is set.

```proto
message Response {
  oneof result {
    string value = 1;
    string error = 2;
  }
}
```

```python
r = Response(result=Oneof(field="value", value="ok"))
r.result   # Oneof(field="value", value="ok")
```

Setting any field in a oneof automatically clears the others.
`Oneof` works naturally with Python's `match` statement for type-safe dispatch:

```python
match r.result:
    case Oneof(field="value", value=v):
        print("success:", v)
    case Oneof(field="error", value=e):
        print("error:", e)
    case None:
        print("not set")
```
