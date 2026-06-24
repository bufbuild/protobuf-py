# Generating Files

[`File`][protobuf.plugin.File] is the object you write code into.
You get one from `schema.generate_file()` and then call methods on it to build up the file's content.

## Printing lines

`print()` adds a line to the file.
Pass strings, numbers, booleans, bytes, or [`Ident`][protobuf.plugin.Ident] objects:

```python
f.print("x: int = ", 42)
# x: int = 42
```

## Imports

### Referencing generated types

`File.print` accepts descriptor objects directly — pass a `DescMessage`, `DescEnum`, or `DescExtension` and the framework resolves the correct module path and symbol name, emitting a runtime import.
Inside a `type_checking()` block, the import is automatically placed under `if TYPE_CHECKING:` instead.

Use [`Ident.for_desc()`][protobuf.plugin.Ident.for_desc] when you need to:

- **Force a type-only import**: pass `type_only=True` to place the import under `if TYPE_CHECKING:` regardless of where the identifier appears.
- **Build a derived identifier**: use the result to construct a related name, such as `<MessageName>Validator`.

```python
from protobuf.plugin import Ident

request = Ident.for_desc(method.input, type_only=True)
response = Ident.for_desc(method.output, type_only=True)
with f.scope("def handle(self, request: ", request, ") -> ", response, ":"):
    f.print("...")
```

Output:

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .example_pb import MyRequest, MyResponse


def handle(self, request: MyRequest) -> MyResponse:
    ...
```

`Ident.for_desc()` accepts `DescMessage`, `DescEnum`, `DescExtension`, or `DescFile` (for the file descriptor variable).

### Other imports

For symbols not from generated `_pb` files, create a [`Module`][protobuf.plugin.Module] and call `.ident()`:

```python
from protobuf.plugin import Module

_PROTOCOL = Module("typing").ident("Protocol")

f.print("class UserService(", _PROTOCOL, "):")
# Generates:
#   from typing import Protocol
#   class UserService(Protocol):
```

[`Module`][protobuf.plugin.Module] represents a module path.
Absolute paths (no leading dot) generate absolute imports; paths starting with `.` generate relative imports:

```python
Module("protobuf")            # from protobuf import ...
Module(".gen.example_pb")     # from .gen.example_pb import ...

# Derive a relative module path from a proto file descriptor
Module.for_desc(desc, "_pb")  # e.g. ".example_pb" for "example.proto"
```

!!! note
    Relative paths are always interpreted from the generation root, not from the generated file's own location in the output tree.

## Naming generated symbols

Use `f.ident(name)` to create an identifier for a symbol *defined* in the file being generated.
When printed, it outputs just the name with no import, and signals to the framework that the name is taken so any imported symbol that would otherwise collide with it gets aliased instead:

```python
class_name = f.ident(service.name)
with f.scope("class ", class_name, "(", _PROTOCOL, "):"):
    ...
```

Use `Module.ident()` or `Ident.for_desc()` when *importing* a symbol from another module.
Use `f.ident()` when *defining* a symbol in the current file.

## Scopes

Use `scope()` to open an indented block:

```python
with f.scope("class Foo:"):
    f.print("x: int = 0")
# class Foo:
#     x: int = 0
```

Scopes nest arbitrarily.

## Type-only imports

The `type_only=True` parameter works on `Module.ident()` too, not just `Ident.for_desc()`:

```python
ident = module.ident("MyType", type_only=True)
```

The framework collects all type-only identifiers and emits them together at the top of the file:

```python
if TYPE_CHECKING:
    from .example_pb import MyType
```

To emit an `if TYPE_CHECKING:` block in the file body, use `type_checking()`.
Any identifier printed inside also has its import placed in the type-only imports section at the top of the file:

```python
_FOO = Module("mylib").ident("Foo")

with f.type_checking():
    f.print("x: ", _FOO)
```

Output (abbreviated — imports and body are separate sections of the file):

```python
# imports section:
if TYPE_CHECKING:
    from mylib import Foo

# file body:
if TYPE_CHECKING:
    x: Foo
```

## Docstrings

Use `doc()` to write a properly-escaped docstring.
Pass a summary string to put it on the opening line:

```python
with f.doc("A single-line docstring."):
    pass
# """A single-line docstring."""

with f.doc("Short description."):
    f.print()
    f.print("Longer paragraph.")
# """Short description.
#
# Longer paragraph.
# """
```

Call `doc()` with no arguments when the content comes from elsewhere, such as forwarded proto comments:

```python
with f.doc():
    f.print("First line of content.")
    f.print()
    f.print("Second paragraph.")
# """
# First line of content.
#
# Second paragraph.
# """
```

## Forwarding proto comments

Use [`get_comments()`][protobuf.plugin.get_comments] to retrieve the proto source comments for any descriptor element and forward them into generated docstrings.
Combine it with the no-args `doc()` form to preserve multi-line comments:

```python
from protobuf.plugin import get_comments

with f.doc():
    comments = get_comments(method_desc)
    if comments.leading:
        for line in comments.leading.removesuffix("\n").splitlines():
            f.print(line.removeprefix(" "))
        f.print()
    f.print("Generated from method: '", method_desc.parent.type_name, ".", method_desc.name, "'.")
```

`get_comments()` accepts `DescService`, `DescMethod`, `DescMessage`, `DescField`, `DescEnum`, `DescEnumValue`, `DescOneof`, or `DescExtension`.

## Preamble

Call `preamble()` once per file to emit the standard file header.
Pass the `DescFile` the output was generated from:

```python
f = schema.generate_file(desc, "_hello.py")
f.preamble(desc)
```

Always call `preamble()` first, before any other `print()` calls.
It emits a DO NOT EDIT header derived from the source file and plugin name:

```python
# Generated from example/v1/example.proto. DO NOT EDIT.
# Generated by protoc-gen-hello v0.1.0 with parameter "".
```

It also emits `# ruff: noqa` to suppress linting on generated code, and
`# fmt: off` to prevent formatters from modifying it.
Use the `no_fmt_off` option (see [Options](./options.md#no_fmt_off)) to omit
`# fmt: off` if you want ruff to format the output.

!!! note
    Every `.py` file also has `from __future__ import annotations` inserted
    automatically — with or without a preamble.
