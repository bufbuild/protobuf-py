# Descriptors

Descriptors are the runtime representation of your schema. Every field, message, enum, and service has a corresponding descriptor object that drives serialization, presence tracking, and reflection.

## Walking through a schema

The file-level descriptor exported from a generated `_pb.py` file is a `DescFile`.
You can walk its entire contents:

```python
from gen import example_pb

# All top-level messages
for msg in example_pb.desc().messages:
    print(msg.type_name)   # "example.User"

    # Fields on each message
    for field in msg.fields:
        print(field.name, field.number)

    # Nested types
    for nested in msg.nested_messages:
        print(nested.type_name)

# All top-level enums
for enum in example_pb.desc().enums:
    print(enum.type_name)
    for value in enum.values:
        print(value.name, value.number)

# All services
for service in example_pb.desc().services:
    print(service.type_name)
    for method in service.methods:
        print(method.name)
```

## Walking through message fields

There are three ways to iterate over a message's fields, depending on how you want to handle `oneof` groups.

Use **`fields`** for all fields, including those inside a `oneof`:

```python
for field in User.desc().fields:
    print(field.name)   # first_name, last_name, active, manager, locations, projects
```

Scalar, message, and enum fields (but not repeated or map fields) also have an `oneof` attribute:

```python
from protobuf import DescFieldValueScalar, DescFieldValueMessage, DescFieldValueEnum

for field in User.desc().fields:
    if isinstance(field.value, (DescFieldValueScalar, DescFieldValueMessage, DescFieldValueEnum)):
        print(field.value.oneof)  # DescOneof | None — set if the field is inside a oneof
```

Use **`oneofs`** for `oneof` groups only; iterate into their fields:

```python
for oneof in User.desc().oneofs:
    print(oneof.name)
    for field in oneof.fields:
        print(field.name)
```

**`members`**: standalone fields and `oneof` groups together, in source order.
Use this when writing a code generator that needs to emit fields and oneofs in declaration order:

```python
from protobuf import DescField, DescOneof

for member in User.desc().members:
    match member:
        case DescField():
            print(f"field: {member.name}")
        case DescOneof():
            print(f"oneof: {member.name}")
            for field in member.fields:
                print(f"  field: {field.name}")
```

## DescField

[`DescField`][protobuf.DescField] is a field with `value` set to a union of five types, one for each field kind.
Use `match` on the `value` to handle each kind specifically:

```python
from protobuf import DescFieldValueScalar, DescFieldValueMessage, DescFieldValueEnum, DescFieldValueList, DescFieldValueMap

for field in User.desc().fields:
    name = field.name
    match value := field.value:
        case DescFieldValueScalar(scalar=scalar):
            print(f"{name}: scalar {scalar.name}")
        case DescFieldValueMessage(message=msg_desc):
            print(f"{name}: message {msg_desc.type_name}")
        case DescFieldValueEnum(enum=enum_desc):
            print(f"{name}: enum {enum_desc.type_name}")
        case DescFieldValueList():
            print(f"{name}: repeated")
        case DescFieldValueMap():
            print(f"{name}: map")
```

All field types share common attributes:

```python
field.name         # proto name ("first_name")
field.local_name   # Python attribute name (same unless reserved keyword)
field.number       # field number
field.json_name    # JSON key ("firstName")
field.presence     # EXPLICIT, IMPLICIT, or LEGACY_REQUIRED
field.deprecated   # bool
field.parent       # DescMessage that owns this field
```

## DescEnum

[`DescEnum`][protobuf.DescEnum] describes an enum type:

```python
from gen.example_pb import PhoneType

desc = PhoneType.desc()   # DescEnum
desc.name                 # "PhoneType"
desc.open                 # True (proto3) or False (proto2)
for v in desc.values:
    print(v.name, v.number)
```
