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

from protobuf._file_registry import add_file
from protobuf._registry import Registry

if TYPE_CHECKING:
    from protobuf.wkt import FileDescriptorProto


class FileDescriptorSetMixin:
    __slots__ = ()

    if TYPE_CHECKING:
        file: list[FileDescriptorProto]

    def to_registry(self) -> Registry:
        """Converts the file descriptors in this set into a [Registry][protobuf.Registry]."""
        registry = Registry()
        for file in self.file:
            add_file(registry, file, stubs={})
        return registry
