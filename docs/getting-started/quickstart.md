# Quickstart

This guide walks through the full workflow: writing a `.proto` schema, generating Python code, and using the result in your application.

## Write a schema

Create a `proto/` directory and add a file called `user.proto`:

```proto title="proto/user.proto"
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

Each numbered field is a typed attribute on the generated Python class.
The field numbers are used in the binary encoding and must not change once in use.

## Configure code generation

Create a `buf.gen.yaml` at the root of your project:

```yaml title="buf.gen.yaml"
version: v2
inputs:
  - directory: proto
plugins:
  - local: protoc-gen-py
    out: src/gen
```

This tells `buf` to read `.proto` files from the `proto/` directory and write generated Python files to `src/gen/`.

## Generate

Run `buf generate` to produce the Python classes:

=== "uv"

    ```shellsession
    $ uv run buf generate
    ```

=== "pip"

    ```shellsession
    $ buf generate
    ```

This creates `src/gen/user_pb.py` containing a `User` class.
The generated file is checked in to version control; re-run generation only when the schema changes.

!!! warning
    Generated files should never be edited by hand.
    They contain a `DO NOT EDIT` comment and will be overwritten on the next `buf generate`.

## Create messages

Import and instantiate the generated class using keyword arguments:

```python title="main.py"
from gen.user_pb import User

user = User(
    first_name="Homer",
    last_name="Simpson",
    active=True,
    locations=["Springfield"],
    projects={"SPP": "Springfield Power Plant"},
    manager=User(
        first_name="Montgomery",
        last_name="Burns",
    ),
)
```

All arguments are optional.
Scalar fields default to their zero value (`""`, `0`, `False`), message fields default to `None`, and repeated and map fields default to empty collections.

## Access fields

Fields are accessible as typed attributes:

```python
user.first_name          # "Homer"
user.active              # True
user.manager.last_name   # "Burns"
user.locations[0]        # "Springfield"
user.projects["SPP"]     # "Springfield Power Plant"
```

Repeated fields are Python lists and map fields are Python dicts, so standard Python operations work as expected:

```python
user.locations.append("Capital City")
user.projects["SNPP"] = "Springfield Nuclear Power Plant"
```

## Serialize and deserialize

### Binary

Binary encoding is compact and efficient, and is the standard choice for storage and inter-service communication:

```python
# Serialize to bytes
data: bytes = user.to_binary()

# Deserialize from bytes
user = User.from_binary(data)
```

### JSON

JSON encoding is human-readable and works with any standard JSON parser.
Field names are converted to camelCase per the Protobuf JSON specification:

```python
# Serialize to a JSON string
text: str = user.to_json()
# {"firstName": "Homer", "lastName": "Simpson", ...}

# Deserialize from a JSON string
user = User.from_json(text)
```

## Next steps

- Explore the [Serialization](../serialization.md) page for the full set of options including merging, unknown fields, and JSON formatting.
- Explore the [API Reference](../api/index.md) for the full `Message` interface, including presence checking, reflection, and merge semantics.
- Read about [Well-Known Types](../well-known-types.md) like `Timestamp`, `Duration`, and `Any`.
