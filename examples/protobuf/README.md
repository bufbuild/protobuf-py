# protobuf-py Example

This directory contains example code that uses Protocol Buffers to manage a
list of users. The [add.py](./src/example/add.py) script adds a new user, prompting 
you to input the person's information. The [list.py](./src/example/list.py) script
lists users.

Note that this example can be easily implemented in other languages, because
the serialization format is standardized. That means you could add a user to the
list with Dart, and list people with TypeScript interchangeably.


### Run the example

First, clone the repository and install dependencies following the steps from
the [contribution guide](../../.github/CONTRIBUTING.md#how-can-i-contribute). Then
change into the example directory with `cd examples/protobuf`.

To add a user, run:

```shellsession
uv run python -m example.add
```

To list all users:

```shellsession
uv run python -m example.list
```

### Generate code

To regenerate the code, run `uv run buf generate` in this directory.
[`buf.gen.yaml`](./buf.gen.yaml) contains the plugin configuration.

```
uv run buf generate
```

If you want to use `protoc`, the following command is equivalent:

```
protoc --proto_path proto proto/example.proto --py_out=src/example/gen
```
