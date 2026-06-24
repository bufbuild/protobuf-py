# protoc-gen-py

The code generator plugin for Protocol Buffers for Python. Learn more about the project at [github.com/bufbuild/protobuf-py](https://github.com/bufbuild/protobuf-py).

## Installation

`protoc-gen-py` generates base types—messages and enumerations—from your Protocol Buffer schema. The generated code requires the runtime library [protobuf-py](https://pypi.org/project/protobuf-py/). It's compatible with Protocol Buffer compilers like [buf](https://github.com/bufbuild/buf) and [protoc](https://github.com/protocolbuffers/protobuf/releases).

To install the runtime library and the plugin, run:

```shellsession
$ uv add protobuf-py protoc-gen-py buf-bin
```

## Generating code

### With buf

Add a new `buf.gen.yaml` configuration file:

```yaml
version: v2
inputs:
  - directory: proto
plugins:
  # This will invoke protoc-gen-py and write output to src/gen
  - local: protoc-gen-py
    out: src/gen
```

To generate code for all Protobuf files within your project, run:

```shellsession
$ uv run -- buf generate
```

Note that `buf` can generate from various [inputs](https://buf.build/docs/reference/inputs), not just local Protobuf files.

### With `protoc`

```shellsession
$ uv run protoc --proto_path proto \
    --py_out src/gen \
    proto/a.proto proto/b.proto proto/c.proto
```

## Plugin options

### `init_files`

By default, the plugin creates `__init__.py` files in every directory of the generated output.
Set `init_files=false` to suppress this and produce [namespace packages](https://packaging.python.org/en/latest/guides/packaging-namespace-packages/) instead. Namespace packages allow multiple distribution packages to include modules under the same top-level package.
For example, in `buf.gen.yaml`:

```yaml
plugins:
  - local: protoc-gen-py
    out: src/gen
    opt: init_files=false
```
