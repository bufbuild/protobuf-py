# Features

## Services

Services defined in a `.proto` file are compiled into [`DescService`][protobuf.DescService] descriptors, but no RPC stubs are generated.
They are accessible via the file descriptor:

```python
for service in example_pb.desc().services:
    print(service.type_name)
```

For RPC clients and servers built on `protobuf-py`, see [Connect for Python](https://github.com/connectrpc/connect-py).

## Comments

Comments in `.proto` files become docstrings on the generated Python classes and attributes:

```proto
// A user in the system.
message User {
  // The user's given name.
  string first_name = 1;
}
```

```python
class User(Message):
    """A user in the system."""
    ...
```

## Reserved names

Python keywords and names that conflict with built-in `Message` attributes are suffixed with a trailing underscore in the generated property name.
This has no impact on the binary encoding or on the JSON representation.

```proto
message Request {
  string from  = 1;   // Python keyword
  string class = 2;   // Python keyword
}
```

```python
req.from_   # "from" on the wire
req.class_  # "class" on the wire
```

## Enum value prefix stripping

Proto convention is to prefix every enum value with the enum name.
The code generator strips this prefix (derived from the `snake_case` form of the enum name) from the generated Python class:

```proto
enum PhoneType {
  PHONE_TYPE_UNSPECIFIED = 0;
  PHONE_TYPE_MOBILE = 1;
  PHONE_TYPE_HOME = 2;
}
```

```python
class PhoneType(Enum):
    UNSPECIFIED = 0
    MOBILE = 1
    HOME = 2
```

The prefix is not stripped if the stripped value would start with a digit or match any other enum value.

```proto
enum PhoneType {
  PHONE_TYPE_UNSPECIFIED = 0;
  PHONE_TYPE_MOBILE = 1;
  PHONE_TYPE_HOME = 2;
  PHONE_TYPE_1800 = 3;
  MOBILE = 4;
}
```

```python
class PhoneType(Enum):
    UNSPECIFIED = 0
    PHONE_TYPE_MOBILE = 1
    HOME = 2
    PHONE_TYPE_1800 = 3
    MOBILE = 4
```

See [Enums](../enums.md) for open/closed behavior and JSON representation.

## Nested types

Nested messages and enums are generated as regular Python nested classes:

```proto
message User {
  enum Role {
    ROLE_UNSPECIFIED = 0;
    ROLE_ADMIN = 1;
  }
}
```

```python
class User(Message[...]):
    class Role(Enum):
        UNSPECIFIED = 0
        ADMIN       = 1
```

Access them as `User.Role`, `User.Role.ADMIN`, etc.
