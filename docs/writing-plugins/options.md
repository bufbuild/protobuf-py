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

The framework reserves certain option names for all plugins, currently: `no_fmt_off`.
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
