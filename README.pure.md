# protobuf-py-pure

`protobuf-py-pure` is the pure Python implementation of [protobuf-py](https://pypi.org/project/protobuf-py/), an ergonomic and modern Protobuf library for Python.
It contains the entire runtime, including the base types, serialization, and the pre-generated well-known types, and has no compiled code and no third-party dependencies.

**Most users should depend on [`protobuf-py`](https://pypi.org/project/protobuf-py/) instead.**
It installs this package along with `protobuf-py-ext`, a native extension written in Rust that accelerates encoding and decoding on the platforms it is published for, falling back to this package everywhere else.

Depend on `protobuf-py-pure` directly when you need a pure Python installation with the same behavior on every platform, for example in environments you do not control or when a compiled extension is not acceptable such as WebAssembly.

```shellsession
$ uv add protobuf-py-pure
```

See the [protobuf-py documentation](https://protobufpy.com/) for installation, a quickstart, and the full feature list.
