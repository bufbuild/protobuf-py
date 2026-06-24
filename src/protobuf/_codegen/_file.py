# Copyright (c) 2025-2026 Buf Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from typing import TYPE_CHECKING

from protobuf._file_registry import create_file_registry

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from protobuf._descriptors import DescFile
    from protobuf._enum import Enum
    from protobuf._extension import Extension
    from protobuf._message import Message


def file_desc(
    proto_bytes: bytes,
    dependencies: Sequence[DescFile],
    stubs: Mapping[str, type[Message | Enum] | Extension],
) -> DescFile:
    """Create a DescFile from a serialized FileDescriptorProto."""
    from protobuf.wkt._gen.descriptor_pb import FileDescriptorProto  # noqa: PLC0415

    proto = FileDescriptorProto.from_binary(proto_bytes)
    reg = create_file_registry(
        proto,
        lambda path: next((dep for dep in dependencies if dep.name == path), None),
        stubs=stubs,
    )
    res = reg.file(proto.name)
    assert res is not None  # noqa: S101 # We just added the file.
    return res
