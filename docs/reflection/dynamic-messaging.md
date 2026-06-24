# Dynamic Messaging

Dynamic messaging lets you work with Protobuf message types that are unknown at compile time.
Instead of importing generated classes, you load a serialized schema (a `FileDescriptorSet` compiled from your `.proto` files) at runtime and instantiate messages from their descriptors.

This is useful for:

- Generic tools (decoders, validators, diff tools) that accept arbitrary message types as input.
- Proxies or middleware that forward or transform messages without owning the schema.
- Test harnesses that construct messages from fixture data without depending on generated code.

Let's explore dynamic messaging by writing a simple tool to output a diff of two arbitrary Protobuf messages.

## Setup

First, let's set up the Protobuf messages we will be diffing. Our tool will operate on these without any
generated code, so we set them up in a separate directory. This folder represents a consumer project.

We use the same Protobuf schema as the [tutorial](../tutorial.md).

```shellsession
$ mkdir user
$ cd user
```

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

To tell a dynamic messaging tool how to work with this Protobuf, we compile it to a `FileDescriptorSet` using `buf`.

```shellsession
$ buf build --as-file-descriptor-set proto -o descriptors.binpb
```

`descriptors.binpb` contains all the information about our schema - tools that work with arbitrary Protobuf messages
can read it to know how to process them.

Let's also create the two payloads we will diff. We use JSON for readability in this tutorial but binary format
would work in the same way.

```json title="pooh.json"
{
  "firstName": "Pooh",
  "lastName": "Bear",
  "displayName": "Winnie",
  "status": "STATUS_PENDING",
  "homeAddress": {
    "location": "Hundred Acre Wood",
    "city": "Ashdown Forest",
    "country": "UK"
  },
  "manager": {
    "firstName": "Christopher",
    "lastName": "Robin"
  },
  "hobbies": ["honey", "napping"],
  "externalUsernames": {
    "twitter": "@poohbear",
    "github": "poohdev"
  },
  "created": "1926-10-14T12:00:00Z"
}
```

```json title="yogi.json"
{
  "firstName": "Yogi",
  "lastName": "Bear",
  "displayName": "Yabba",
  "status": "STATUS_ACTIVE",
  "homeAddress": {
    "location": "123 Main St",
    "city": "Jellystone",
    "country": "USA"
  },
  "workAddress": {
    "location": "456 Park Ave",
    "city": "Jellystone",
    "country": "USA"
  },
  "manager": {
    "firstName": "Ranger",
    "lastName": "Smith"
  },
  "hobbies": ["picnicking", "fishing"],
  "externalUsernames": {
    "twitter": "@yogibear",
    "github": "yogidev"
  },
  "sessionTimeoutMinutes": 30,
  "created": "1958-09-29T18:00:00Z"
}
```

Now, let's get started on our tool! We set it up in a sibling directory of `user`. Since dynamic messaging is
often used in shared tools, we use a `lib` project to demonstrate a project that can be published to PyPI for
consumption by anyone.

```shellsession
$ cd ..
$ uv init --lib protodiff
$ cd protodiff
$ uv add protobuf-py
```

## Reading the descriptor set

We need to start by reading a user-provided descriptor set to know how to operate on messages.
We accept the path to the descriptor set as an argument and parse it into a `FileDescriptorSet`.
`FileDescriptorSet` is itself a Protobuf message, and is provided as part of the protobuf-py
runtime's well-known types - after reading the serialized descriptor set, we parse it just like
any other message.

```python title="src/protodiff/__init__.py"
import argparse
from pathlib import Path

from protobuf.wkt import FileDescriptorSet

def main() -> None:
    parser = argparse.ArgumentParser(description="Diff two Protobuf messages")
    parser.add_argument(
        "--descriptors",
        help="Path to the descriptors file for the input messages",
    )
    args = parser.parse_args()
    fds = FileDescriptorSet.from_binary(Path(args.descriptors).read_bytes())
    print(fds)

if __name__ == "__main__":
    main()
```

Also add the script to `pyproject.toml` so it's ready to run with `uv` or even publish to PyPI.

```toml title="pyproject.toml"
...
[project.scripts]
protodiff = "protodiff:main"
...
```

Now, run the script, passing in the descriptors file we generated in the `user` directory above.

```shellsession
$ uv run protodiff --descriptors ../user/descriptors.binpb
```

You will see a large amount of output corresponding to the descriptors - you may be able to spot
some of the familiar fields in there, such as the definition for `first_name`,
`{"name": "first_name", "number": 1, "label": "LABEL_OPTIONAL", "type": "TYPE_STRING", "jsonName": "firstName"}`.
This output has all the information from `user.proto`, easily parsed out of the descriptors we passed.

## Reading the input messages

Now, let's read the message payloads. The key step is to convert the `FileDescriptorSet` into a `Registry`
by calling `to_registry`. This takes the raw definition we read from the descriptors and processes it for use
with the same `Message` API we always use for accessing Protobuf messages.

```python title="src/protodiff/__init__.py"
import argparse
from pathlib import Path

from protobuf.wkt import FileDescriptorSet

def main() -> None:
    parser = argparse.ArgumentParser(description="Diff two Protobuf messages")
    parser.add_argument(
        "--descriptors",
        help="Path to the descriptors file for the input messages",
    )
    parser.add_argument("--type", help="Fully qualified message type name, e.g. 'my.package.Message'")
    parser.add_argument("message1", help="Path to the first message file")
    parser.add_argument("message2", help="Path to the second message file")
    args = parser.parse_args()
    fds = FileDescriptorSet.from_binary(Path(args.descriptors).read_bytes())
    registry = fds.to_registry()

    desc_message = registry.message(args.type)
    if not desc_message:
        raise ValueError(f"Message type {args.type} not found in descriptors")

    message1_bytes = Path(args.message1).read_bytes()
    message2_bytes = Path(args.message2).read_bytes()

    message1 = desc_message.type.from_json(message1_bytes)
    message2 = desc_message.type.from_json(message2_bytes)
    print(message1)
    print(message2)

if __name__ == "__main__":
    main()
```

```shellsession
$ uv run protodiff --descriptors ../user/descriptors.binpb --type User ../user/pooh.json ../user/yogi.json
User(first_name='Pooh', last_name='Bear', display_name='Winnie', status=User.Status.PENDING, home_address=User.Address(location='Hundred Acre Wood', city='Ashdown Forest', country='UK'), manager=User(first_name='Christopher', last_name='Robin'), hobbies=['honey', 'napping'], external_usernames={'twitter': '@poohbear', 'github': 'poohdev'}, created=Timestamp(seconds=-1363780800))
User(first_name='Yogi', last_name='Bear', display_name='Yabba', status=User.Status.ACTIVE, home_address=User.Address(location='123 Main St', city='Jellystone', country='USA'), work_address=User.Address(location='456 Park Ave', city='Jellystone', country='USA'), manager=User(first_name='Ranger', last_name='Smith'), hobbies=['picnicking', 'fishing'], external_usernames={'twitter': '@yogibear', 'github': 'yogidev'}, session_timeout_minutes=30, created=Timestamp(seconds=-355212000))
```

We see we now have the user's messages loaded, printed out with familiar Python `repr` syntax.
Note how we can do this without any generated code or knowledge of the type `User` - this tool
uses dynamic messaging to reconstruct any messages the user passes in with their descriptors.
Also, while we use `from_json`, you can see how it is simple to use `from_binary` instead for
binary format, or better yet, to provide an argument like `--format` to allow the user to select it.

## Operating on input messages

It's time to implement the actual diff logic. Our tool now has the messages and the descriptor
for the message. This means that we can use standard reflection APIs through [the descriptor](./descriptors.md)
to read through the fields in each message, printing out any differences.

```python title="src/protodiff/__init__.py"
import argparse
from pathlib import Path
from typing import TYPE_CHECKING

from protobuf import DescMessage, DescFieldValueMessage, DescFieldValueList, DescFieldValueMap
from protobuf.wkt import FileDescriptorSet, Timestamp

if TYPE_CHECKING:
    from protobuf import Message

def _diff_scalars(field_name: str, value1: object, value2: object) -> None:
    if value1 != value2:
        print(f"{field_name}: {value1} != {value2}")

def _diff_messages(field_name: str, desc_message: DescMessage, message1: Message, message2: Message) -> None:
    if desc_message.type_name == "google.protobuf.Timestamp":
        if message1.to_datetime() != message2.to_datetime():
            print(f"{field_name}: {message1.to_datetime()} != {message2.to_datetime()}")
        return
    for field in desc_message.fields:
        if field not in message1 and field not in message2:
            continue
        if field in message1 and field not in message2:
            print(f"{field_name}.{field.name}: <present> != <missing>")
            continue
        if field not in message1 and field in message2:
            print(f"{field_name}.{field.name}: <missing> != <present>")
            continue
        value1 = message1[field]
        value2 = message2[field]
        match field.value:
            case DescFieldValueMessage(message=nested_desc_message):
                _diff_messages(f"{field_name}.{field.name}", nested_desc_message, value1, value2)
            case DescFieldValueList(element=element_type):
                if len(value1) != len(value2):
                    print(f"{field_name}.{field.name}: list length {len(value1)} != {len(value2)}")
                    continue
                for i, (item1, item2) in enumerate(zip(value1, value2)):
                    if isinstance(element_type, DescMessage):
                        _diff_messages(f"{field_name}.{field.name}[{i}]", element_type, item1, item2)
                    else:
                        _diff_scalars(f"{field_name}.{field.name}[{i}]", item1, item2)
            case DescFieldValueMap(key=key_type, value=value_type):
                keys1 = set(value1.keys())
                keys2 = set(value2.keys())
                for key in keys1 - keys2:
                    print(f"{field_name}.{field.name}[{key}]: <present> != <missing>")
                for key in keys2 - keys1:
                    print(f"{field_name}.{field.name}[{key}]: <missing> != <present>")
                for key in keys1 & keys2:
                    item1 = value1[key]
                    item2 = value2[key]
                    if isinstance(value_type, DescMessage):
                        _diff_messages(f"{field_name}.{field.name}[{key}]", value_type, item1, item2)
                    else:
                        _diff_scalars(f"{field_name}.{field.name}[{key}]", item1, item2)
            case _:
                _diff_scalars(f"{field_name}.{field.name}", value1, value2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Diff two Protobuf messages")
    parser.add_argument(
        "--descriptors",
        help="Path to the descriptors file for the input messages",
    )
    parser.add_argument("--type", help="Fully qualified message type name, e.g. 'my.package.Message'")
    parser.add_argument("message1", help="Path to the first message file")
    parser.add_argument("message2", help="Path to the second message file")
    args = parser.parse_args()
    fds = FileDescriptorSet.from_binary(Path(args.descriptors).read_bytes())
    registry = fds.to_registry()

    desc_message = registry.message(args.type)
    if not desc_message:
        raise ValueError(f"Message type {args.type} not found in descriptors")

    message1_bytes = Path(args.message1).read_bytes()
    message2_bytes = Path(args.message2).read_bytes()

    message1 = desc_message.type.from_json(message1_bytes)
    message2 = desc_message.type.from_json(message2_bytes)
    _diff_messages("", desc_message, message1, message2)

if __name__ == "__main__":
    main()
```

```shellsession
$ uv run protodiff --descriptors ../user/descriptors.binpb --type User ../user/pooh.json ../user/yogi.json
.first_name: Pooh != Yogi
.display_name: Winnie != Yabba
.status: PENDING != ACTIVE
.home_address.location: Hundred Acre Wood != 123 Main St
.home_address.city: Ashdown Forest != Jellystone
.home_address.country: UK != USA
.work_address: <missing> != <present>
.manager.first_name: Christopher != Ranger
.manager.last_name: Robin != Smith
.hobbies[0]: honey != picnicking
.hobbies[1]: napping != fishing
.external_usernames[github]: poohdev != yogidev
.external_usernames[twitter]: @poohbear != @yogibear
.session_timeout_minutes: <missing> != <present>
.created: 1926-10-14 12:00:00+00:00 != 1958-09-29 18:00:00+00:00
```

We can see the core of the diffing logic is looping through `DescMessage.fields`, using
descriptor containment (`field in message`) to see if the field is present in one message
or the other, and when they are both present, using `__getitem__` to get the value. It then
examines the type of the field to possibly iterate through nested messages, repeated fields,
or map fields.
We also see special handling of Protobuf well-known types, where protobuf-py provides
additional utilities, in this case allowing us to print the diff as a standard timestamp string.
If your use case needs it, `__setitem__` and `__delitem__` will work fine for mutations.

The sky is the limit from here - a more complete tool would at least need to handle
additional WKTs, and would probably print present vs missing diffs differently and
maybe even have colors. Any similar tool will follow the same general structure of

1. Load a `FileDescriptorSet` and convert to `Registry`
2. Find the `DescMessage` for the input in the `Registry`
3. Use `DescMessage` to parse input messages
4. Loop through `DescMessage.fields` to examine input messages

We hope to see a lot of great programs using dynamic messaging to enrich the toolbox
for protobuf-py users!

## See also

- [Dynamic Messaging](https://buf.build/docs/reference/descriptors/#dynamic-messaging): language-agnostic overview of the concept in the Buf docs.
