# Working with Messages

Messages are the primary data structures in Protobuf.
Each generated message class behaves like an idiomatic Python object: construct it with keyword arguments, read and write fields as attributes, and use standard operators for equality and copying.

## Constructing

Messages are constructed with keyword arguments.
Every field is optional; unset fields take their default values.

```python
user = User(
    first_name="Homer",
    last_name="Simpson",
    active=True,
    locations=["Springfield"],
    manager=User(first_name="Montgomery", last_name="Burns"),
)
```

Scalar defaults are the zero value for the type (`""`, `0`, `False`).
Message fields default to `None`.
Repeated and map fields default to empty collections.

## Accessing fields

Fields are read and written as typed attributes:

```python
user.first_name           # "Homer"
user.manager.last_name    # "Burns"
user.locations[0]         # "Springfield"

user.first_name = "Bart"
user.locations.append("Capital City")
```

## Field presence and default values

All fields in Protobuf are optional.
When a field is not set, it returns a default value: the zero value for its type (`""`, `0`, `False`, `None`).
This is intentional: it allows the schema to evolve over time without breaking older consumers that don't know about new fields.

The zero value for a field is never serialized.
This means that if you add a new boolean field `verified` to `User`, existing serialized data that doesn't include it will behave as if `verified = False` (the default), which is usually the right thing.

Because of this, it's important to design your schema accordingly.
If `False` or `0` or `""` is a meaningful value that needs to be distinguished from "not set", you need *explicit presence*.

### Implicit vs explicit presence

In proto3, scalar fields use *implicit presence* by default: the zero value is treated as absent.
Add the `optional` keyword to enable explicit presence; the runtime will then track whether the field was set at all:

```proto
syntax = "proto3";

message User {
  string first_name = 1;           // implicit, "" means "not set"
  optional string nickname = 2;    // explicit, "" means "set to empty string"
}
```

Use the `has_field` method to check whether a field with explicit presence has been set:

```python
user = User()
user.has_field("nickname")   # False, not set
user.nickname        # "" (zero value)

user.nickname = ""
user.has_field("nickname")   # True, explicitly set to empty string

user.first_name = ""
user.has_field("first_name") # False, implicit presence: "" == not set
```

Message fields always have explicit presence.
Repeated and map fields always have implicit presence; an empty collection is indistinguishable from an absent one.

To clear a field back to its default (and mark it as unset):

```python
user.clear_field("nickname")
user.has_field("nickname")   # False
```

### Required fields

Fields declared `required` in proto2 (or `features.field_presence = LEGACY_REQUIRED` in editions) are validated on serialization.
If a required field is not set when `to_binary()` or `to_json()` is called, an error is raised.
Missing required fields are silently accepted during parsing, consistent with the behavior of other Protobuf implementations.

!!! warning
    `required` is a legacy feature.
    The [official language guide](https://protobuf.dev/programming-guides/proto2/#required-deprecated) recommends against using it in new schemas.

## Equality

Two messages are equal when they have the same type, the same set fields, and the same values for every set field.
Extensions and unknown fields are not considered.

```python
a = User(first_name="Alice")
b = User(first_name="Alice")
a == b   # True

c = User(first_name="Alice", active=True)
a == c   # False, `active` is set to `True` on `c` but unset on `a`
```

NaN-valued floats follow Python container semantics: the same `nan` object compares equal to itself, but distinct `nan` objects (e.g., two `float("nan")` calls) do not.

## Identifying messages

Every message class has a `desc()` classmethod that returns its [`DescMessage`][protobuf.DescMessage].
Use `type_name` to get the fully qualified name of the message type:

```python
User.desc().type_name   # "example.User"
```

To check whether an unknown value is a message, use `isinstance` with [`Message`][protobuf.Message]:

```python
from protobuf import Message

isinstance(user, Message)   # True
```

To check for a specific message type, use `isinstance` with the generated class directly:

```python
isinstance(user, User)   # True
```

## Copying

Use [`copy.deepcopy()`](https://docs.python.org/3/library/copy.html#copy.deepcopy) for a fully independent copy where all nested messages, repeated fields, and map fields are copied independently.

Use [`copy.copy()`](https://docs.python.org/3/library/copy.html#copy.copy) for a shallow copy.
The copy has independent presence and unknown field tracking, but mutable field values (repeated fields, map fields, nested messages) are shared.

```python
import copy

original = User(first_name="Homer", locations=["Springfield"])
shallow  = copy.copy(original)

shallow.first_name = "Bart"
original.first_name   # "Homer", scalar is independent

shallow.locations.append("Shelbyville")
original.locations    # ["Springfield", "Shelbyville"], list is shared
```

On Python 3.13+, use [`copy.replace()`](https://docs.python.org/3/library/copy.html#copy.replace) to produce a copy with specific fields changed:

```python
updated = copy.replace(original, first_name="Bart")
updated.first_name    # "Bart"
original.first_name   # "Homer", unchanged
```

## Iterating over fields

Iterating over a message yields the [`DescField`][protobuf.DescField] of each field that is currently set:

```python
user = User(first_name="Homer", active=True)

for field in user:
    print(field.name, user[field])
# first_name Homer
# active True
```

## Container protocol

Every message implements the Python container protocol, providing a dynamic alternative to typed attribute access.
This is the same mechanism that serializers and reflection tools use internally. Container methods accept
field descriptors and extensions. For field-name presence checks in generated messages, prefer
`msg.has_field("field_name")`.

```python
desc = next(f for f in User.desc().fields if f.name == "first_name")
user[desc]           # get
user[desc] = "Homer" # set
desc in user         # descriptor presence check
```

## String representation

`repr()` returns a string in constructor syntax, showing only the fields that are set:

```python
user = User(first_name="Homer", active=True)
repr(user)
# User(first_name='Homer', active=True)
```
