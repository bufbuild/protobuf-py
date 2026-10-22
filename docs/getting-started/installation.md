# Installation

Before you can generate or use Protobuf messages, you need a runtime library, a code generator, and the Buf CLI.
!!! note
    protobuf-py requires **Python 3.10 or later**.

## Packages

There are two packages to install:

- **`protobuf-py`**, the runtime library.
  Contains base types, serialization, and the pre-generated well-known types.
  This is the only runtime dependency your application needs.
  On Linux, macOS, and Windows it also installs `protobuf-py-ext`, a native Rust extension that accelerates encoding and decoding.
  Everywhere else it falls back to pure Python.
- **`protoc-gen-py`**, the code generator plugin.
  Invoked by `buf` to produce Python classes from `.proto` files.
  This is a development-time tool, not a runtime dependency.

You also need the **Buf CLI** to compile `.proto` files and run the code generator.
The easiest way to get it is via the **`buf-bin`** package, which installs the `buf` binary into your virtual environment.

!!! tip "Pure Python"
    If you need a pure Python installation on every platform, for example in environments where you cannot ship compiled code, depend on **`protobuf-py-pure`** instead of `protobuf-py`.
    It is the same runtime without the native extension and has no third-party dependencies.

## Installing

=== "uv"

    Add the runtime to your project's dependencies:

    ```shellsession
    $ uv add protobuf-py
    ```

    Add the code generator and Buf CLI as development dependencies:

    ```shellsession
    $ uv add --dev protoc-gen-py buf-bin
    ```

=== "pip"

    Create and activate a virtual environment, then install:

    ```shellsession
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    $ pip install protobuf-py protoc-gen-py buf-bin
    ```

## Verifying

Check that the Buf CLI is available:

=== "uv"

    ```shellsession
    $ uv run buf --version
    ```

=== "pip"

    ```shellsession
    $ buf --version
    ```

## Next steps

Continue to [Quickstart](./quickstart.md) to write a schema, generate code, and use it.
