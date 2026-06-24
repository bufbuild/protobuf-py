# Enums

Protobuf enums map to Python `IntEnum` subclasses.
Values compare equal to plain integers and can be used anywhere an integer is expected.

```python
from gen.example_pb import PhoneType

user.phone_type = PhoneType.MOBILE
user.phone_type == 1   # True
```

## Open and closed enums

In proto3 and editions, enums are *open* by default: unknown integer values are accepted during parsing and preserved for round-tripping.
Proto2 enums are *closed*: unknown values are rejected during parsing.

The `desc().open` attribute indicates which behavior applies:

```python
PhoneType.desc().open   # True (proto3), False (proto2/closed)
```

## JSON representation

By default, enum values serialize to their string name in ProtoJSON:

```python
msg.to_json()   # {"phoneType": "PHONE_TYPE_MOBILE"}
```

To serialize as integers instead, pass `print_enums_as_ints=True`:

```python
msg.to_json(print_enums_as_ints=True)   # {"phoneType": 1}
```

See [Serialization](./serialization.md) for the full list of JSON options.

For details on how enum value names are generated, see [Enum value prefix stripping](./generated-code/features.md#enum-value-prefix-stripping).
