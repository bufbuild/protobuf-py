# Tutorial

This tutorial is for anyone that has never used Protocol Buffers (Protobuf) before or for those needing a
refresher. It will explain the motivation and concepts of Protocol Buffers while introducing you to
real-world use cases. We will navigate through the steps to work with Protobuf in Python using
protobuf-py - you will need [`uv` installed](https://docs.astral.sh/uv/getting-started/installation/)
to follow along.

## What is Protobuf?

Protobuf is a language and set of tools for defining schemas describing data structures in
a way agnostic to programming language. Let's look at a `.proto` file describing the schema
for a user of some service.

```proto title="proto/user.proto"
syntax = "proto3";

message User {
  string first_name = 1;
  string last_name = 2;
  bool active = 3;
}
```

Here, we have the definition of a user, with two fields to hold string data for their name and
a boolean field for their status. While this file may already be useful for team members to
read and understand the structure of a user, where Protobuf shines is having first-class
support for code generation based on this schema. Protobuf was originally developed with code
generation in mind; it is not a feature tacked on after-the-fact.

## Code generation

Code generation is driven by a Protobuf compiler, which reads `.proto` files and generates
code based on a configuration that specifies plugins to execute. Plugins receive the schema
definition and can generate any output file they wish, for example Python code representing
the schema.

We'll use the [Buf](https://buf.build/product/cli) Protobuf compiler to generate Python code
for this proto.

First, let's initialize a fresh project.

```shellsession
$ uv init hello-proto
$ cd hello-proto
$ uv add protobuf-py
$ uv add --dev buf-bin protoc-gen-py
```

This creates a new project with `main.py`, the `protobuf-py` runtime, and the
`protoc-gen-py` Protobuf plugin.

Now, create `proto/user.proto` as above and add a `buf.gen.yaml` file to the folder.

```yaml title="buf.gen.yaml"
version: v2
inputs:
  - directory: proto
plugins:
  - local: protoc-gen-py
    out: gen
```

This tells `buf` to read from the `proto` directory, invoke the protoc-gen-py plugin,
and output to the `gen` directory. Invoke `buf` to generate code!

```shellsession
$ uv run buf generate
```

You will now have a file, `gen/user_pb.py` with a typical Python class corresponding to the
schema in the proto. Update `main.py` to try it out.

```python title="main.py"
from gen.user_pb import User

user = User(first_name="Yogi", last_name="Bear", active=True)
print(user.first_name)
print(user.last_name)
print(user.active)
print(user)
```

```shellsession
$ uv run python main.py
Yogi
Bear
True
User(first_name='Yogi', last_name='Bear', active=True)
```

We can see that the generated Python class behaves like normal. For a simple, local
data structure, it would be simpler to write the Python class by hand, but Protobuf shines
most brightly in two areas. One is that the list of plugins configured for `buf` can be
anything - if you install [protoc-gen-go](https://github.com/protocolbuffers/protobuf-go)
and add it to the plugins array, you will now have code generation of Python and Go from
a single schema. For systems built from multiple programming languages, being able to
define the schema once and generate code for all of them both reduces work of writing
code in multiple languages, but most importantly reduces the chance of bugs that comes with
it.

The second point where Protobuf shines is having built-in serialization.

## Serialization

Serialization converts a structure to a binary format, generally for sending to a separate
process. Imagine a microservice system where one server sends information about a user
to another via an HTTP request - the information about the user must be serialized to
include in the HTTP request body.

Protobuf defines a binary format tied to the features of the Protobuf schema - all
structures generated from a `.proto` can be serialized to and from this binary format
without writing any serialization code. The binary format is highly optimized for size
and performance - you may have been wondering about the `= 1;`, `= 2;` etc numbers in
the schema, which we call field numbers. The binary format actually uses these numbers
to identify a field of data rather than the names to allow as compact a representation
as possible.

Let's serialize and deserialize the user.

```python title="main.py"
from gen.user_pb import User

user = User(first_name="Yogi", last_name="Bear", active=True)
serialized_user = user.to_binary()
print(len(serialized_user))
user2 = User.from_binary(serialized_user)
print(user2.first_name)
print(user2.last_name)
print(user2.active)
print(user2)
```

```shellsession
$ uv run python main.py
14
Yogi
Bear
True
User(first_name='Yogi', last_name='Bear', active=True)
```

We see that 14 bytes represent the data of the user. Note that assuming a boolean
takes 1 byte, the values we assigned to the user total 9 bytes - 14 bytes is not
much more.

We also see that creating a `User` from that binary, we get back the same data
that can be accessed as before.

Naturally, there is no real use case for the above code that immediately parses
the serialized data in the same function. But now, you can instead send it to
a different server entirely. We could send the bytes over HTTP by hand, but
serializing data for transport is exactly the problem that an RPC framework
solves for us. We'll use [Connect for Python](https://connectrpc.com/docs/python/getting-started/),
which builds directly on `protobuf-py` and generates typed clients and servers
from a schema, just like `protoc-gen-py` generated our message classes.

First, describe the operation we want to expose as a *service* with an RPC
method. Create `proto/user_service.proto`.

```proto title="proto/user_service.proto"
syntax = "proto3";

import "user.proto";

service UserService {
  rpc DeactivateUser(User) returns (User);
}
```

A service is a collection of RPC methods, and each method declares the message
it accepts and the message it returns. Here `DeactivateUser` takes a `User` and
returns a `User`.

Add the Connect runtime and an ASGI server to the project, along with the
`protoc-gen-connectrpc` plugin for code generation.

```shellsession
$ uv add connectrpc uvicorn
$ uv add --dev protoc-gen-connectrpc
```

Now add the Connect plugin to `buf.gen.yaml` so `buf` generates service code
alongside the message code.

```yaml title="buf.gen.yaml"
version: v2
inputs:
  - directory: proto
plugins:
  - local: protoc-gen-py
    out: gen
  - local: protoc-gen-connectrpc
    out: gen
```

Regenerate.

```shellsession
$ uv run buf generate
```

This adds `gen/user_service_connect.py` next to the message code. Let's look at
the pieces it generates (abbreviated).

```python title="gen/user_service_connect.py"
class UserService(Protocol):
    async def deactivate_user(self, request: User, ctx: RequestContext[User, User]) -> User:
        raise ConnectError(Code.UNIMPLEMENTED, 'Not implemented')


class UserServiceASGIApplication(ConnectASGIApplication[UserService]):
    ...


class UserServiceClient(ConnectClient):
    async def deactivate_user(
        self,
        request: User,
        *,
        headers: Headers | Mapping[str, str] | None = None,
        timeout_ms: int | None = None,
    ) -> User:
        ...
```

`UserService` is the interface a server implements - one typed method per RPC,
using our generated `User` message. `UserServiceASGIApplication` wraps an
implementation as a standard [ASGI](https://asgi.readthedocs.io/) app so it can
be served by any ASGI server. `UserServiceClient` is a fully-typed client that
speaks to the server. (Synchronous `UserServiceClientSync` and WSGI variants are
generated too.)

Let's implement the service and call it. Update `main.py`.

```python title="main.py"
import asyncio

import uvicorn
from connectrpc.request import RequestContext

from gen.user_pb import User
from gen.user_service_connect import (
    UserService,
    UserServiceASGIApplication,
    UserServiceClient,
)

class UserServiceImpl(UserService):
    async def deactivate_user(self, request: User, ctx: RequestContext) -> User:
        request.active = False
        return request

async def main():
    app = UserServiceASGIApplication(UserServiceImpl())
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning"))
    server_task = asyncio.create_task(server.serve())
    while not server.started:
        await asyncio.sleep(0.01)

    async with UserServiceClient("http://localhost:8000") as client:
        user = User(first_name="Yogi", last_name="Bear", active=True)
        user2 = await client.deactivate_user(user)
        print(user2)

    server.should_exit = True
    await server_task

if __name__ == "__main__":
    asyncio.run(main())
```

```shellsession
$ uv run python main.py
User(first_name='Yogi', last_name='Bear')
```

We never wrote any serialization or HTTP code - the client took a `User`, the
server received a `User`, returned it with a modification, and the client got a
`User` back. Connect handled serializing the messages to the binary format and
back over the wire for us. While both the server and client are Python in this
example, because plugins can be configured to generate for other languages, the
same schema can produce a Connect client or server in another language - so a
Python client could call a Go server, for example.

Protobuf also supports serializing to JSON. While it is less performant
than the binary format, it can be useful when needing a human readable representation,
for example if writing the data to a log message.

```python title="main.py"
from gen.user_pb import User

user = User(first_name="Yogi", last_name="Bear", active=True)
serialized_user = user.to_json()
print(len(serialized_user))
print(serialized_user)
user2 = User.from_json(serialized_user)
print(user2.first_name)
print(user2.last_name)
print(user2.active)
print(user2)
```

```shellsession
$ uv run python main.py
57
{"firstName": "Yogi", "lastName": "Bear", "active": true}
Yogi
Bear
True
User(first_name='Yogi', last_name='Bear', active=True)
```

## Features

Let's edit `proto/user.proto` and extend the schema to explore more of Protobuf's features.

```proto title="proto/user.proto"
syntax = "proto3";

import "google/protobuf/timestamp.proto";

message User {
  string first_name = 1;
  string last_name = 2;

  reserved 3;

  string display_name = 4;

  enum Status {
    STATUS_UNSPECIFIED = 0;
    STATUS_PENDING = 1;
    STATUS_SUSPENDED = 2;
    STATUS_ACTIVE = 3;
  }
  Status status = 5;

  message Address {
    string location = 1;
    string city = 2;
    string country = 3;
  }
  Address home_address = 6;
  Address work_address = 7;

  User manager = 8;

  repeated string hobbies = 9;

  map<string, string> external_usernames = 10;

  optional uint32 session_timeout_minutes = 11;

  google.protobuf.Timestamp created = 12;
}
```

```shellsession
$ uv run buf generate
```

We now have a more complex data structure. Notice that we updated from a simple boolean status field
to an enum - to accommodate this schema change, we made sure not to reuse the `= 3;` field number. As
explained in [serialization](#serialization), binary format uses the field numbers as keys in the data.
If reusing a number with a completely different type, it can break the interaction between servers
that happen to have been built at different times seeing a different version of the schema. Extending schemas
in Protobuf usually avoids explicit version numbers in favor of avoiding field number reuse to
prevent structure mismatch. Protobuf provides the `reserved` keyword to help not forget.

Now, let's explore the new generated code.

```python title="main.py"
from gen.user_pb import User

user = User()
print(user.first_name)
print(user.status)
print(user.hobbies)
print(user.manager)
```

```shellsession
$ uv run python main.py

UNSPECIFIED
[]
None
```

First, notice how an empty message behaves. Protobuf fields all have a default value corresponding
to their type: a falsy value for most types, except for enums, where the default is the first declared
enum value. Notice how we set the first value to `STATUS_UNSPECIFIED` - this is because otherwise, the
default value would be `STATUS_PENDING` which can cause issues differentiating from a value that hasn't
been provided.

Note that for most fields, we cannot differentiate from explicitly setting a value
to the default value from leaving it empty. In many cases, this is not a problem -
there is no such thing as an empty name, so the default value of `""` for a string
field is sufficient for knowing if the field is set or not. But for when this
isn't sufficient, you can add the `optional` keyword as we did above.

```python title="main.py"
from gen.user_pb import User

def print_session_timeout(user: User) -> None:
    if user.has_field("session_timeout_minutes"):
        if user.session_timeout_minutes != 0:
            print(f"Session timeout: {user.session_timeout_minutes} minutes")
        else:
            print("Session timeout: disabled")
    else:
        print("Session timeout: system default")

user = User(session_timeout_minutes=0)
print_session_timeout(user)
user = User()
print_session_timeout(user)
```

```shellsession
$ uv run python main.py
Session timeout: disabled
Session timeout: system default
```

We can see the use of `has_field` to check whether the value is actually set or not.
Using `has_field` on a field without `optional` will always return `False` for a value
of `0`, regardless of if this was explicitly set or not.

Let's go ahead and fill out the entire proto.

```python title="main.py"
from datetime import datetime, timezone

from protobuf.wkt import Timestamp

from gen.user_pb import User

user = User(
    first_name="Yogi",
    last_name="Bear",
    display_name="Yabba",
    status=User.Status.ACTIVE,
    home_address=User.Address(
        location="123 Main St",
        city="Jellystone",
        country="USA",
    ),
    work_address=User.Address(
        location="456 Park Ave",
        city="Jellystone",
        country="USA",
    ),
    manager=User(
        first_name="Ranger",
        last_name="Smith",
    ),
    hobbies=["picnicking", "fishing"],
    external_usernames={"twitter": "@yogibear", "github": "yogidev"},
    session_timeout_minutes=30,
    created=Timestamp.from_datetime(datetime(1958, 9, 29, 18, 0, 0, tzinfo=timezone.utc)),
)
print(user.to_json())
```

```shellsession
$ uv run python main.py
{"firstName": "Yogi", "lastName": "Bear", "displayName": "Yabba", "status": "STATUS_ACTIVE", "homeAddress": {"location": "123 Main St", "city": "Jellystone", "country": "USA"}, "workAddress": {"location": "456 Park Ave", "city": "Jellystone", "country": "USA"}, "manager": {"firstName": "Ranger", "lastName": "Smith"}, "hobbies": ["picnicking", "fishing"], "externalUsernames": {"twitter": "@yogibear", "github": "yogidev"}, "sessionTimeoutMinutes": 30, "created": "1958-09-29T18:00:00Z"}
```

We see typical Python usage for primitives, enums, submessages, lists, and dicts.
In addition, we see a [well-known type](./well-known-types.md). Protobuf defines certain
types like `Timestamp` and `Duration` with additional functionality - here we see it
can be conveniently converted from Python's `datetime` and the JSON representation
shows a date string instead of the Protobuf components.
