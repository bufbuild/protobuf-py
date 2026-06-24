# Generated Code

Running `buf generate` produces one `_pb.py` file per `.proto` file.
These files are checked into version control and should never be edited by hand; they contain a `DO NOT EDIT` comment and will be overwritten on the next run.

## Files

A `.proto` file named `example.proto` generates `example_pb.py`.
The generated file imports only from a fixed set of sources:

- `protobuf`: public base types (`Message`, `Enum`, `Extension`)
- `protobuf.wkt`: well-known type descriptors
- Other `_pb.py` files: cross-file proto dependencies
- `protobuf._codegen`: internal codegen machinery (not for application use)

`protobuf._codegen` is a private contract between the runtime and the code generator.
Application code should not import from it directly.

A file-level descriptor object is also exported, accessible with `desc()`:

```python
from gen import example_pb
example_pb.desc()   # DescFile
```

This is used to register types in a [`Registry`](../reflection/registry.md) or to walk the schema with [reflection](../reflection/index.md).

## Messages

Each Protobuf message becomes a subclass of [`Message`][protobuf.Message].
The generated class carries no serialization logic; all behavior is driven by an embedded descriptor.

```proto title="example.proto"
message User {
  string first_name = 1;
  string last_name = 2;
  bool active = 3;
}
```

```python title="example_pb.py"
_UserFields: TypeAlias = Literal["first_name", "last_name", "active"]

class User(Message[_UserFields]):
    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            first_name: str = "",
            last_name:  str = "",
            active:     bool = False,
        ) -> None: ...

        first_name: str
        last_name:  str
        active:     bool
```

The `TYPE_CHECKING` block exists only for type checkers and IDEs; the actual runtime behavior is inherited from `Message`.
Proto field names are `snake_case` and map directly to Python attribute names.

## Enums

Each Protobuf enum becomes a subclass of [`Enum`][protobuf.Enum].
The shared enum prefix is stripped from value names:

```python
class Role(Enum):
    UNSPECIFIED = 0
    ADMIN = 1
    VIEWER = 2
```

## Extensions

Each extension becomes an [`Extension`][protobuf.Extension] object typed with its extendee and value type:

```python
ext_my_option: Extension[FieldOptions, str] = Extension(...)
```

See [Extensions](../extensions.md) for how to use them.

## Next steps

- [Field types](./field-types.md): How each Protobuf field kind maps to Python
- [Features](./features.md): Optional fields, required fields, services, comments, reserved names
