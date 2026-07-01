<div align="center">

![The Buf logo](https://raw.githubusercontent.com/bufbuild/protobuf-py/main/.github/buf-logo.svg)

# protobuf-py

[![PyPI version](https://img.shields.io/pypi/v/protobuf-py?style=flat-square
)](https://pypi.org/project/protobuf-py)
[![License](https://img.shields.io/github/license/bufbuild/protobuf-py?style=flat-square
)](https://github.com/bufbuild/protobuf-py/blob/main/LICENSE)
[![Slack](https://img.shields.io/badge/slack-buf-%23e01e5a?style=flat-square)](https://buf.build/links/slack)

`protobuf-py` is an **ergonomic and modern Protobuf library** for Python.

Well-typed, generated code you can read. High-performance encoder/decoder written in Rust. 100% conformance. <br />
Zero dependencies or tooling required.

[Getting started](https://protobufpy.com/getting-started/installation/) •
[Examples](https://example.com) •
[New to Protobuf?](https://example.com)

</div>

```python
from gen.user_pb import User

# Messages are plain Python objects: pass fields as keyword args, or set them later.
user = User(id="123", first_name="Alice")
user.last_name = "Smith"

# Serialize to the Protobuf wire format, then parse it back.
data = user.to_binary()
user = User.from_binary(data)

print(user.first_name)  # Alice
print(user.to_json())   # {"id": "123", "firstName": "Alice", "lastName": "Smith"}
```

Protobuf is the easiest way to build APIs. We recommend using it with [Connect for Python](https://github.com/connectrpc/connect-py), which generates server stubs for you:

```python
from connectrpc.request import RequestContext

from gen.user_connect import UserService, UserServiceASGIApplication
from gen.user_pb import GetUserRequest, GetUserResponse, User

class UserHandler(UserService):
    async def get_user(self, request: GetUserRequest, ctx: RequestContext) -> GetUserResponse:
        user = User(id=request.id, first_name="Alice", last_name="Smith")
        return GetUserResponse(user=user)

# Serve it with any ASGI server, e.g. `uvicorn server:app`.
app = UserServiceASGIApplication(UserHandler())
```

Connect can also generate client libraries for **every major language**, including your frontend. Here's what the generated Python client looks like:

```python
from gen.user_connect import UserServiceClient
from gen.user_pb import GetUserRequest

client = UserServiceClient("http://localhost:8080")
response = client.get_user(GetUserRequest(id="123"))

print(response.user.first_name)  # Alice
```

## Quickstart

```proto
// proto/user.proto
syntax = "proto3";

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message User {
  string id = 1;
  string first_name = 2;
  string last_name = 3;
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
  - local: protoc-gen-connectrpc
    out: src/gen
```

```shellsession
$ uv add protobuf-py connectrpc
$ uv add --dev protoc-gen-py protoc-gen-connectrpc buf-bin
$ uv run -- buf generate
```

That's all - typed messages and Connect stubs now live in `src/gen`.

## Feature highlights

### Generated code you can read

```python
class User(Message[_UserFields]):
    __slots__ = ("id", "first_name", "last_name")

    def __init__(
        self, *,
        id: str = "",
        first_name: str = "",
        last_name: str = "",
    ) -> None:
        ...

    id: str
    first_name: str
    last_name: str
```

### Typed oneofs with pattern matching

```python
from protobuf import Oneof

match msg.result:
    case Oneof(field="value", value=v):
        handle_value(v)
    case Oneof(field="error", value=e):
        handle_error(e)
```

### Well-known types with friendly helpers

```python
from datetime import UTC, datetime, timedelta
from protobuf.wkt import Any, Duration, Timestamp

ts = Timestamp.from_datetime(datetime.now(UTC))
td = Duration.from_timedelta(timedelta(minutes=5))
packed = Any.pack(user)
```

### Seamless reflection

```python
# Iterate over message fields
for field in user:
    # Access field name / value
    value = user[field]
    print(field.name, value)

    # Check for presence
    print(field in user)

    # Assign / delete fields
    user[field] = value
    del user[field]
```

## How it compares

- [`google-protobuf`](https://github.com/protocolbuffers/protobuf) is complete, but generates code with unreadable binary blobs, broken imports, and a hostile API.
- [`betterproto`](https://github.com/danielgtaylor/python-betterproto) improves ergonomics, but it is proto3-only. The original project now points to `betterproto2`, which calls out active development, incomplete docs, and breaking changes.

<details>
<summary>Click here for a full comparison.</summary>

|                                  | `protobuf-py`                               | `google-protobuf`                                           | `betterproto`                                                |
| -------------------------------- | ------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| Spec coverage                    | ✅ 100%                                      | ⚠️ Known conformance failures                                | ❌ proto3-only                                                |
| Type annotations                 | ✅ Built-in                                  | ❌ Third-party tooling needed                                | ✅ Built-in                                                   |
| Readable generated code          | ✅                                           | ❌ Classes are built only at runtime and cannot be inspected | ✅                                                            |
| Imports                          | ✅ Relative imports                          | ❌ Broken without third-party tooling                        | ✅ Relative imports                                           |
| Oneofs                           | ✅ Ergonomic, `match`-compatible             | ❌ String-returning `WhichOneof()`                           | ⚠️ Tuple-returning helpers                                    |
| Enums                            | ✅ Python-native `IntEnum`                   | ❌ `int` + `EnumTypeWrapper`                                 | ⚠️ Custom int subclass                                        |
| Field presence                   | ✅ `msg.has_field("x")` with IDE completions | ⚠️ `HasField("x")` raises for proto3 scalars                 | ⚠️ Helper-based                                               |
| Field assignment (`foo.x = 123`) | ✅ Direct assignment                         | ❌ `CopyFrom()` required                                     | ✅ Direct assignment                                          |
| `copy.copy()` / `copy.replace()` | ✅                                           | ❌                                                           | ❌                                                            |
| Global mutable registry          | ✅ Explicit `Registry`                       | ❌ Process-wide singleton behavior                           | ✅ N/A                                                        |
| Zero dependencies                | ✅                                           | ✅                                                           | ❌ Includes `grpclib`, `python-dateutil`, `typing-extensions` |

</details>

## Migration guide

| `google-protobuf`                          | `protobuf-py`                         |
| ------------------------------------------ | ------------------------------------- |
| `msg.SerializeToString()`                  | `msg.to_binary()`                     |
| `MessageType.FromString(data)`             | `MessageType.from_binary(data)`       |
| `msg.HasField("nickname")`                 | `msg.has_field("nickname")`           |
| `msg.WhichOneof("result")` + string checks | `match msg.result` with typed `Oneof` |
| `msg.Extensions[ext]`                      | `msg[ext]`                            |
| `msg.child.CopyFrom(other)`                | `msg.child = other`                   |
