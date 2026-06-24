# Custom Options

[Custom options](../extensions.md#extensions-in-custom-options) are extensions on the compiler's descriptor option messages.
Access them through the `proto` attribute of any descriptor, which holds the raw compiler-generated descriptor message:

```python
from gen.options_pb import ext_sensitive   # an Extension[FieldOptions, bool]

for field in User.desc().fields:
    if field.proto.options is not None and field.proto.options[ext_sensitive]:
        print(f"{field.name} is sensitive")
```

This works for any descriptor type (`DescMessage`, `DescField`, `DescEnum`, `DescService`, `DescMethod`) via their respective `proto.options` attribute.

## How this works

Every descriptor wraps a compiler-generated proto message.
The `proto` attribute gives you direct access to that message, including its `options` field.
Custom options extend those option messages, so reading them is the same as reading any extension:

```python
from gen.options_pb import ext_deprecated_reason   # Extension[MessageOptions, str]

for msg in example_pb.desc().messages:
    if msg.proto.options is None:
        continue
    reason = msg.proto.options[ext_deprecated_reason]
    if reason:
        print(f"{msg.name} is deprecated: {reason}")
```

## Reading options in plugins

The same `proto.options` pattern works inside a plugin's `generate` callback; the descriptors in the schema carry the raw compiler messages.
See [Writing Plugins](../writing-plugins/options.md) for a complete example.

See [Custom options](../extensions.md#extensions-in-custom-options) for the full walkthrough of defining and annotating options.
