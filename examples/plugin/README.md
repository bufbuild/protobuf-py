# Custom Plugin Example

This directory demonstrates how to write a custom protoc plugin using the
protobuf-py plugin framework. The plugin,
[`protoc-gen-rpc`](./src/protoc_gen_rpc/__init__.py), generates Python
`Protocol` classes for unary RPCs.


### Run the example

First, clone the repository and install dependencies following the steps from
the [contribution guide](../../.github/CONTRIBUTING.md#how-can-i-contribute). Then
change into the plugin directory with `cd examples/plugin`.

To run the tests:

```shellsession
uv run pytest
```

### Generate code

To regenerate the code, run `uv run buf generate` in this directory.
[`buf.gen.yaml`](./buf.gen.yaml) contains the plugin configuration.

```shellsession
uv run buf generate
```
