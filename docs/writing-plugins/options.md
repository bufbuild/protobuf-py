# Options

Plugins can declare typed options that users pass via `buf.gen.yaml`, giving them a structured way to configure code generation behavior.

## Plugin options

Define plugin options as a dataclass and pass it as the third argument to `run()`:

```python title="protoc-gen-hello"
from dataclasses import dataclass
from protobuf.plugin import Schema, run


@dataclass
class Options:
    verbose: bool = False


def generate(schema: Schema[Options]) -> None:
    if schema.options.verbose:
        ...


run("protoc-gen-hello", "0.1.0", Options, generate)
```

Pass options in `buf.gen.yaml` as a comma-separated `opt:` value:

```yaml title="buf.gen.yaml"
plugins:
  - local: protoc-gen-hello
    out: src/gen
    opt: verbose=true
```

Supported field types: `str`, `bool`, `int`, `float`, `Literal[...]`, `StrEnum`, `IntEnum`, `list[T]`, `dict[str, T]`.
`| None` can be added for optional options.

## Framework-reserved options

The framework reserves certain option names for all plugins, currently: `no_fmt_off`, `escape_module_with_hash`, and `map_imports`.
If your `Options` dataclass defines a field with a reserved name, `run()` raises a `ValueError`.

### no_fmt_off

When set, omits the `# fmt: off` line from the generated file preamble.
Use this when you want ruff to format the generated output:

```yaml title="buf.gen.yaml"
plugins:
  - local: protoc-gen-hello
    out: src/gen
    opt: no_fmt_off
```

### escape_module_with_hash

Module names are derived from proto file paths, and characters that aren't valid in a Python module name (such as `.` or `-`) are replaced with underscores.
That replacement can cause separate proto files to map to the same module name.
When set, this option appends a short hash suffix, derived from the original unsanitized name, to avoid those collisions:

```yaml title="buf.gen.yaml"
plugins:
  - local: protoc-gen-hello
    out: src/gen
    opt: escape_module_with_hash
```

### map_imports

By default, generated code imports dependencies from the local output with a relative import.
For example, the module generated for `foo/bar.proto` imports a message from `buf/validate/validate.proto` as `from ..buf.validate.validate_pb import Rule`.

If a dependency is provided by a package instead, use `map_imports` to import it from there.
The option takes the form `map_imports=<pattern>:<target>` and can be given multiple times.
The pattern is matched against the path of the Protobuf file, and the first matching pattern wins.
The target is a Python package that is prepended to the module path derived from the Protobuf file:

```yaml title="buf.gen.yaml"
plugins:
  - local: protoc-gen-hello
    out: src/gen
    opt: map_imports=google/type/:mypkg.gen
```

With this option, a message from `google/type/date.proto` is imported as `from mypkg.gen.google.type.date_pb import Date`.

Patterns support a subset of glob:

- `*` matches zero or more characters except `/`.
- `**` matches zero or more characters, including `/`.
- `**/` matches zero or more directories.
- A trailing `/` matches every file in the directory and its subdirectories.

An empty target imports from the canonical module path: the module path derived from the Protobuf file, relative to the root of `sys.path`.
This is the layout of generated SDKs installed as separate packages, such as those from the Buf Python registry.
For example, when `buf/validate/validate.proto` is provided by an installed package:

```yaml title="buf.gen.yaml"
plugins:
  - local: protoc-gen-hello
    out: src/gen
    opt: "map_imports=buf/validate/:"
```

This generates `from buf.validate import validate_pb` and `from buf.validate.validate_pb import Rule`.
A mapped module at the top level, such as one generated for a Protobuf file at the root, is written as a plain `import foo_pb` statement.

Mapping applies to imports derived from descriptors.
Identifiers constructed directly from a `Module` are not mapped, and well-known types are always imported from `protobuf.wkt`.

## Example: Sensitive fields plugin

Here is a plugin that generates a `_sensitive.py` file for each proto file, listing all fields marked with the `sensitive` custom option from [extensions](../extensions.md#extensions-in-custom-options):

```python title="protoc-gen-sensitive"
#!/usr/bin/env python3
from protobuf.plugin import Schema, run
from gen.options_pb import ext_sensitive


def generate(schema: Schema) -> None:
    for desc in schema.files_to_generate:
        f = schema.generate_file(desc, "_sensitive.py")
        f.preamble(desc)
        f.print()

        sensitive_fields = [
            (msg, field)
            for msg in desc.messages
            for field in msg.fields
            if field.proto.options is not None and field.proto.options[ext_sensitive]
        ]

        with f.scope("SENSITIVE_FIELDS: list[tuple[str, str]] = ["):
            for msg, field in sensitive_fields:
                f.print(f'("{msg.name}", "{field.name}"),')
        f.print("]")


run("protoc-gen-sensitive", "0.1.0", generate)
```
