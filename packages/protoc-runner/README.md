# protoc-runner

protoc-runner is a wheel package published with binaries from [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) for:

- `protoc` - the Protocol Buffers compiler
- `conformance_test_runner` - the official conformance test suite for Protocol Buffers

This package is for use testing internal projects.

## Usage

```python
from protoc import get_protoc_path, get_conformance_test_runner_path
subprocess.run([get_protoc_path(), "-h"], check=True)
subprocess.run([get_conformance_test_runner_path(), "-h"], check=True)
```

## Include protos

`.proto` files for the protoc Well-Known Types and conformance test protos are also packaged.

```python
import shutil

from protoc import get_include_protos_path

shutil.copytree(get_include_protos_path(), ".tmp")
```
