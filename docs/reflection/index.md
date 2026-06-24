# Reflection

protobuf-py exposes the full Protobuf descriptor model at runtime.
Descriptors are the single source of truth for every message and enum: they describe the schema, and all serialization, presence tracking, and field access are driven through them.

## Descriptor types

Descriptors wrap the compiler's internal descriptor messages and give them a convenient Python API.
Their names all start with `Desc`:

| Type | Wraps | Purpose |
|---|---|---|
| [`DescFile`][protobuf.DescFile] | `FileDescriptorProto` | A single `.proto` source file. Root of the hierarchy. |
| [`DescMessage`][protobuf.DescMessage] | `DescriptorProto` | A message declaration. |
| [`DescField`][protobuf.DescField] | `FieldDescriptorProto` | A field declared in a message. |
| [`DescOneof`][protobuf.DescOneof] | `OneofDescriptorProto` | A `oneof` group in a message. |
| [`DescEnum`][protobuf.DescEnum] | `EnumDescriptorProto` | An enum declaration. |
| [`DescEnumValue`][protobuf.DescEnumValue] | `EnumValueDescriptorProto` | A single enum value. |
| [`DescExtension`][protobuf.DescExtension] | `FieldDescriptorProto` | An extension field defined outside its container message. |
| [`DescService`][protobuf.DescService] | `ServiceDescriptorProto` | An RPC service. |
| [`DescMethod`][protobuf.DescMethod] | `MethodDescriptorProto` | A single RPC method. |

Descriptors form a hierarchy rooted at a file:

```
DescFile
 ├─ messages: DescMessage
 │   ├─ fields:            DescField
 │   ├─ oneofs:            DescOneof
 │   ├─ members:           DescField | DescOneof  (fields + oneofs in source order)
 │   ├─ nested_messages:   DescMessage
 │   ├─ nested_enums:      DescEnum
 │   └─ nested_extensions: DescExtension
 ├─ enums: DescEnum
 │   └─ values: DescEnumValue
 ├─ extensions: DescExtension
 └─ services: DescService
     └─ methods: DescMethod
```

## Getting a descriptor

Every generated class carries its descriptor.
Use [`Message.desc()`][protobuf.Message.desc] to retrieve it:

```python
from gen.example_pb import User

desc = User.desc()    # DescMessage
desc.name             # "User"
desc.type_name        # "example.User"
```

The file-level descriptor is exported as a getter function from the generated `_pb.py`:

```python
from gen import example_pb

example_pb.desc().name        # "example.proto"
example_pb.desc().messages    # [DescMessage, ...]
```

## Next steps

- [Descriptors](./descriptors.md): walking through a schema, field descriptors, enums
- [Registry](./registry.md): looking up types by name
- [Dynamic Messaging](./dynamic-messaging.md): instantiating messages from runtime-loaded schemas
- [Custom options](./custom-options.md): reading annotations from proto files
