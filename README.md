![The Buf logo](https://raw.githubusercontent.com/bufbuild/protobuf-py/main/.github/buf-logo.svg)

# protobuf-py

[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/bufbuild/protobuf-py/blob/main/LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/protobuf-py)](https://pypi.org/project/protobuf-py)
[![Slack](https://img.shields.io/badge/slack-buf-%23e01563)][badges_slack]

`protobuf-py` is a from-scratch Protobuf library for Python 3.10+.

100% Protobuf conformance with full support for proto2, proto3, and editions. Generated code is readable, typed, and works out of the box with no dependencies or extra tooling required. Native Rust module for high-performance encoding/decoding.

```python
from gen.example_pb import User

# Messages are plain Python objects: pass fields as keyword args, or set them later.
user = User(first_name="Alice", last_name="Smith", active=True)
user.locations = ["NYC", "LDN"]

# Serialize to the Protobuf wire format, then parse it back.
data = user.to_binary()
user = User.from_binary(data)

print(user.first_name)  # Alice
print(user.to_json())   # {"firstName": "Alice", "lastName": "Smith", ...}
```

The easiest way to build services with `protobuf-py` is with [Connect for Python](https://github.com/connectrpc/connect-py):

```python
from connectrpc.request import RequestContext

from gen.example_connect import UserService, UserServiceASGIApplication
from gen.example_pb import GetUserRequest, GetUserResponse, User

class UserHandler(UserService):
    async def get_user(self, request: GetUserRequest, ctx: RequestContext) -> GetUserResponse:
        return GetUserResponse(user=User(first_name="Alice", active=True))

app = UserServiceASGIApplication(UserHandler())
```

## How it compares

[`google-protobuf`](https://github.com/protocolbuffers/protobuf) implements the full protobuf surface, but its Python API still carries Python-2-era patterns like `SerializeToString()`, `HasField("x")`, and `WhichOneof("group")`. Generated modules use opaque descriptor blobs and absolute imports, and that import behavior causes enough packaging pain that [`fix-protobuf-imports`](https://pypi.org/project/fix-protobuf-imports/) exists just to patch generated output.

[`betterproto`](https://github.com/danielgtaylor/python-betterproto) improved ergonomics, but it remains proto3-only and does not cover core protobuf features like proto2, editions, and extensions. The original project now points to `betterproto2`, and that project still calls out active development, incomplete docs, and breaking changes.

[`protobuf-py`](https://pypi.org/project/protobuf-py/) is the only option that combines complete protobuf semantics with an idiomatic Python interface. You get typed generated classes, relative-import-friendly output, first-class oneof pattern matching, and modern copy semantics without extra runtime dependencies.

| | `protobuf-py` | `google-protobuf` | `betterproto` |
|---|---|---|---|
| Spec coverage | ✅ Full (proto2, proto3, editions, extensions, custom options) | ✅ Full | ❌ Partial (proto3-only) |
| Type annotations | ✅ Built-in | ❌ Third-party tooling needed | ✅ Built-in |
| Conformance tests | ✅ 100% pass rate | ⚠️ Contains known failures | ❌ No conformance suite |
| Readable generated code | ✅ | ❌ Classes are built only at runtime and cannot be inspected | ✅ |
| Imports | ✅ Relative imports | ❌ Broken without third-party tooling | ✅ Relative imports |
| Oneofs | ✅ Ergonomic, `match`-compatible | ❌ String-returning `WhichOneof()` | ⚠️ Tuple-returning helpers |
| Enums | ✅ Python-native `IntEnum` | ❌ `int` + `EnumTypeWrapper` | ⚠️ Custom int subclass |
| Field presence | ✅ `msg.has_field("x")` with IDE completions | ⚠️ `HasField("x")` raises for proto3 scalars | ⚠️ Helper-based |
| Field assignment (`foo.x = 123`) | ✅ Direct assignment | ❌ `CopyFrom()` required | ✅ Direct assignment |
| `copy.copy()` / `copy.replace()` | ✅ | ❌ | ❌ |
| Global mutable registry | ✅ Explicit `Registry` | ❌ Process-wide singleton behavior | ✅ N/A |
| Zero dependencies | ✅ | ✅ | ❌ Includes `grpclib`, `python-dateutil`, `typing-extensions` |

## Quickstart

```proto
// proto/user.proto
syntax = "proto3";

message User {
  string first_name = 1;
  string last_name = 2;
  bool active = 3;
}
```

```yaml
# buf.gen.yaml
version: v2
inputs:
  - directory: proto
plugins:
  - local: protoc-gen-py
    out: src/gen
```

```shellsession
$ uv add protobuf-py
$ uv add --dev protoc-gen-py buf-bin
$ uv run -- buf generate
```

You now have a typed `src/gen/user_pb.py` you can import directly.

## Generated code you can read

`protoc-gen-py` - `protobuf-py`'s code generation plugin, - emits regular typed Python classes. See [Getting started](https://protobufpy.com/getting-started/installation/) and [Writing plugins](https://protobufpy.com/writing-plugins/) for setup and configuration details.

```python
_UserFields: TypeAlias = Literal["first_name", "last_name", "active", "manager", "locations", "projects"]

class User(Message[_UserFields]):
    __slots__ = ("first_name", "last_name", "active", "manager", "locations", "projects")

    if TYPE_CHECKING:
        def __init__(
            self,
            *,
            first_name: str = "",
            last_name: str = "",
            active: bool = False,
            manager: User | None = None,
            locations: list[str] | None = None,
            projects: dict[str, str] | None = None,
        ) -> None: ...

        first_name: str
        last_name: str
        active: bool
        manager: User | None
        locations: list[str]
        projects: dict[str, str]
```

## Feature highlights

**Typed oneofs with pattern matching**

```python
from protobuf import Oneof

match msg.result:
    case Oneof(field="value", value=v):
        handle_value(v)
    case Oneof(field="error", value=e):
        handle_error(e)
```

**Well-known types with Python-friendly helpers**

```python
from datetime import UTC, datetime, timedelta
from protobuf.wkt import Any, Duration, Timestamp

ts = Timestamp.from_datetime(datetime.now(UTC))
td = Duration.from_timedelta(timedelta(minutes=5))
packed = Any.pack(user)
```

**Container protocol for dynamic tools and reflection**

```python
for field in user:
    value = user[field]
    print(field.name, value)
    print(field in user)  # descriptor presence
    del user[field]
    user[field] = value
```

**Project structure that behaves like Python**

- Generated files use relative imports.
- Generated modules fit normal package layouts.
- `__init__.py` files for generated package directories are created by default.

## Migration

| `google-protobuf` | `protobuf-py` |
|---|---|
| `msg.SerializeToString()` | `msg.to_binary()` |
| `MessageType.FromString(data)` | `MessageType.from_binary(data)` |
| `msg.HasField("nickname")` | `msg.has_field("nickname")` |
| `msg.WhichOneof("result")` + string checks | `match msg.result` with typed `Oneof` |
| `msg.Extensions[ext]` | `msg[ext]` |
| `msg.child.CopyFrom(other)` | `msg.child = other` |

## Documentation

- [Docs site](https://protobufpy.com/)
- [Getting started](https://protobufpy.com/getting-started/installation/)
- [Working with messages](https://protobufpy.com/messages/)
- [Serialization](https://protobufpy.com/serialization/)
- [Well-known types](https://protobufpy.com/well-known-types/)
- [Reflection](https://protobufpy.com/reflection/)
- [Writing plugins](https://protobufpy.com/writing-plugins/)
- [API reference](https://protobufpy.com/api/)
- [Code example](./examples/protobuf) — A working example that uses Protobuf to manage a persistent list of users.
- [Connect for Python](https://github.com/connectrpc/connect-py) — RPC clients and servers built on `protobuf-py`.

## Packages

- [`protobuf-py`](https://pypi.org/project/protobuf-py/): The runtime library. Contains base types, generated well-known types, and serialization.
- [`protoc-gen-py`](https://pypi.org/project/protoc-gen-py/): The code generator plugin. Generates Python code that depends on `protobuf-py`.
- [`protobuf-py-ext`](https://pypi.org/project/protobuf-py-ext/): The optional native extension for high performance. Used transparently when installed.

### Native extension platform support

We currently publish `protobuf-py-ext` wheels for

- Linux: arm64 / amd64 - glibc / musl
- macOS: arm64
- Windows: amd64 / arm64

`protobuf-py` includes a dependency on `protobuf-py-ext` for these platforms, meaning therea are no extra steps for
you to use it.

Optimized wheels are published for the latest 3 versions of Python on Linux and MacOS, while other supported
versions use the Python [stable ABI](https://docs.python.org/3/c-api/stable.html#stable-application-binary-interface),
which will also work on unreleased Python versions and still has great performance.

We believe this covers almost all users, which is important because the native extension generally improves performance
by an order of magnitude or two.

If you happen to be using an unsupported platform, feel free to file an issue so we can consider
officially supporting it. In addition, you can easily build the extension for use on any other platform. Ensure [Rust](https://rust-lang.org/tools/install/)
is installed and add `protobuf-py-ext` to your dependencies

```shellsession
$ uv add protobuf-py-ext
```

When your project is synced on a non-supported platform, Rust will automatically be invoked to build the
extension package and it will be used with no other steps.


## Compatibility

Python 3.10 and later versions are supported as long as they are [maintained by CPython](https://devguide.python.org/versions/).

Versioning follows [semantic versioning](https://semver.org/), with a major version increase accompanying breaking changes
and other features introduced with minor version increases. Patch version increases only contain bugfixes.
More details on what we consider breaking and not can be found in the [FAQ](https://protobufpy.com/faq/#what-are-the-compatibility-guarantees).

## Status: Pre-release

protobuf-py is not yet stable. The API may change before 1.0.

## Legal

Offered under the [Apache 2 license](./LICENSE).

[badges_slack]: https://buf.build/links/slack
