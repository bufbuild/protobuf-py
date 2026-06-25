# protoc-gen-grpc-py

The gRPC code generator plugin for Protocol Buffers for Python. Learn more about the project at [github.com/bufbuild/protobuf-py](https://github.com/bufbuild/protobuf-py).

## Overview

`protoc-gen-grpc-py` generates fully typed, idiomatic [gRPC](https://grpc.io) clients and servicers that use [protobuf-py](https://pypi.org/project/protobuf-py/) messages for serialization. Unlike the stock gRPC Python plugin, the generated stubs:

- are fully typed, so editors and type checkers understand every RPC method
- serialize `protobuf-py` messages directly, with no dependency on the `_pb2` Protobuf runtime
- ship both asyncio (`grpc.aio`) and synchronous variants.

For each service it emits a servicer base class (with an `add_to_server` method) and a client, in both async and sync flavors (the sync names are suffixed with `Sync`). Message types are generated separately by [`protoc-gen-py`](https://pypi.org/project/protoc-gen-py/).

## Installation

The generated code requires the runtime libraries [protobuf-py](https://pypi.org/project/protobuf-py/) and [grpcio](https://pypi.org/project/grpcio/). The plugin is compatible with Protocol Buffer compilers like [buf](https://github.com/bufbuild/buf) and [protoc](https://github.com/protocolbuffers/protobuf/releases).

```shellsession
$ uv add protobuf-py grpcio
$ uv add --dev protoc-gen-py protoc-gen-grpc-py buf-bin
```

## Generating code

### With buf

Add `protoc-gen-grpc-py` alongside `protoc-gen-py` in your `buf.gen.yaml`:

```yaml
version: v2
inputs:
  - directory: proto
plugins:
  # Generates message types (*_pb.py).
  - local: protoc-gen-py
    out: src/gen
  # Generates gRPC service stubs (*_pb_grpc.py).
  - local: protoc-gen-grpc-py
    out: src/gen
```

To generate code for all Protobuf files within your project, run:

```shellsession
$ uv run -- buf generate
```

### With `protoc`

```shellsession
$ uv run protoc --proto_path proto \
    --py_out src/gen \
    --grpc-py_out src/gen \
    proto/a.proto proto/b.proto proto/c.proto
```

A `*_pb_grpc.py` file is generated only for proto files that declare a service. The plugin does not emit `__init__.py` files; let `protoc-gen-py` manage those.

## Plugin options

### `io`

Controls which flavor of code is generated:

- unset (default): generate both asynchronous (`grpc.aio`) and synchronous (`grpc`) code;
- `io=async`: generate only asynchronous code;
- `io=sync`: generate only synchronous code.

For example, in `buf.gen.yaml`:

```yaml
plugins:
  - local: protoc-gen-grpc-py
    out: src/gen
    opt: io=async
```

## Example

See the [gRPC example](https://github.com/bufbuild/protobuf-py/tree/main/examples/grpc) for a complete client and server using the generated stubs.
