# protobuf-py

The only modern, complete Python protobuf library.

100% Protobuf conformance with full support for `proto2`, `proto3`, and editions.
Generated code is readable, typed, and works out of the box with no dependencies or extra tooling required.
Native Rust module for high-performance encoding/decoding.

The Pythonic API results in code that you are happy to read.

```python
from gen.user import User

user = User(first_name="Alice", last_name="Smith", active=True)

wire = user.to_binary()
same = User.from_binary(wire)

print(same.to_json())
```

[Get started](./getting-started/installation.md) or read on for how it compares.

## How it compares

<div class="comparison" markdown>

| | protobuf-py | google-protobuf | betterproto |
|---|---|---|---|
| Spec coverage | ✅ Full | ✅ Full | ❌ proto3-only |
| Type annotations | ✅ Built-in | ❌ Requires third-party tooling | ✅ Built-in |
| Readable generated code | ✅ | ❌ Classes are constructed at runtime | ✅ |
| Relative imports | ✅ | ❌ Requires third-party tooling | ✅ |
| Pythonic API | ✅ | ❌ | ⚠️ Partial |

</div>

[`google-protobuf`](https://github.com/protocolbuffers/protobuf) covers the spec but ships a Python-2-era API and opaque descriptor blobs.

[`betterproto`](https://github.com/danielgtaylor/python-betterproto) proved the demand for an idiomatic library but is proto3-only, with no support for extensions or editions.

`protobuf-py` combines complete Protobuf semantics with an idiomatic Python interface and excellent performance.

## What you get

**Complete spec coverage.** `proto2`, `proto3`, editions, extensions, custom options, reflection, descriptors. 100% conformance.

**Typed from the start.** `mypy`, `pyright`, and `ty` work out of the box. Enums are real `IntEnum` instances, `oneof`s work with `match` statements, and type narrowing Just Works.

**Generated code you can read.** Real Python classes with real fields. Go-to-definition works, because there is a definition to go to.

**Imports that fit your project.** Generated files use relative imports. Drop them in `gen/`, `internal/`, or wherever else you like. No more piping output through `sed` or reaching for `fix-protobuf-imports`.

**Native performance.** A Rust extension ships for major platforms, gracefully falling back to pure Python elsewhere.

**A Pythonic API.** Messages feel like regular Python objects. Direct assignment and `copy.replace` work as you'd expect.

**No global descriptor pool.** Types live in explicit [`Registry`](./reflection/registry.md) instances. Two copies of the same `.proto` no longer fight over a process-wide singleton.

**Zero dependencies.** The whole thing runs on Python 3.10+.

[Get started](./getting-started/installation.md)

## Building RPC APIs

`protobuf-py` gives you the message types. To turn your services into working RPC clients and servers, reach for [Connect for Python](https://github.com/connectrpc/connect-py). It builds directly on `protobuf-py` and is the best way to build APIs.

