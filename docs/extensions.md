# Extensions

Extensions are fields that are defined outside the message they extend.
They allow third-party code to attach data to a message type without modifying its original definition.

## Defining extensions

An extension is declared in a `.proto` file with the `extend` keyword:

```proto
syntax = "proto2";

import "google/protobuf/descriptor.proto";

extend google.protobuf.FieldOptions {
  string custom_option = 50000;
}
```

The code generator produces an [`Extension`][protobuf.Extension] object for each extension:

```python
# In the generated _pb.py file:
ext_custom_option: Extension[FieldOptions, str] = Extension(...)
```

## Using extensions

Extensions are accessed through the same container protocol as regular fields, with the `Extension` object as the key:

```python
from gen.options_pb import ext_custom_option
from protobuf.wkt import FieldOptions

opts = FieldOptions()

# Set
opts[ext_custom_option] = "hello"

# Presence check
ext_custom_option in opts   # True

# Get
opts[ext_custom_option]     # "hello"

# Clear
del opts[ext_custom_option]
ext_custom_option in opts   # False
opts[ext_custom_option]     # "" (zero value)
```

Extensions always track presence; `ext in msg` returns `True` even when the extension is set to its zero value:

```python
opts[ext_custom_option] = ""
ext_custom_option in opts   # True
opts[ext_custom_option]     # ""
```

## Extensions in custom options

The most common use of extensions is to define *custom options*: annotations that attach metadata to fields, messages, or services in a schema.
This is how tools like [protovalidate](https://protovalidate.com), gRPC gateway, and OpenAPI generators communicate configuration through the `.proto` file itself.

### Defining a custom option

Create a file `proto/options.proto` that extends one of the Protobuf descriptor option messages:

```proto title="proto/options.proto"
syntax = "proto2";
package example;

import "google/protobuf/descriptor.proto";

// Mark a field as containing sensitive data that should be redacted in logs.
extend google.protobuf.FieldOptions {
  optional bool sensitive = 50001;
}
```

### Using the option

Annotate a field in your message with the option:

```proto title="proto/user.proto"
syntax = "proto3";
package example;

import "options.proto";

message User {
  string first_name = 1;
  string last_name = 2 [(example.sensitive) = true];
  bool active = 3;
}
```

Regenerate code with `buf generate`.
The generated `options_pb.py` exports the `ext_sensitive` extension object.

### Reading the option at runtime

Access the field's descriptor and use the extension to read the option value:

```python
from gen.options_pb import ext_sensitive
from gen.user_pb import User

for field in User.desc().fields:
    if field.proto.options is not None and field.proto.options[ext_sensitive]:
        print(f"{field.name} is sensitive")
# last_name is sensitive
```

This pattern lets you write generic tools (log redactors, schema validators, documentation generators) that work across any message by inspecting the descriptors and options at runtime.
See [Custom Options](./reflection/custom-options.md) for more on reading options through reflection.

## Extensions and JSON

Serializing or deserializing a message that contains extensions to/from ProtoJSON requires a [`Registry`][protobuf.Registry] with the extension registered.
Extensions not found in the registry are silently omitted from JSON output.

```python
from protobuf import Registry

registry = Registry()
registry.add(ext_custom_option)   # the extension to register

text = opts.to_json(registry=registry)
opts = FieldOptions.from_json(text, registry=registry)
```

## How extensions are stored

Extensions are stored in the message's unknown fields in their wire format and parsed on each access.
This means importing a file that defines extensions has no side effects: there is no global registration step, and extensions from different files can never conflict.
