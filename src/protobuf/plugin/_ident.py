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
"""Python identifier and module path types for code generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import final

from protobuf._descriptors import DescEnum, DescExtension, DescFile, DescMessage
from protobuf._sanitization import (
    escape_extension_name,
    escape_identifier,
    escape_proto_module_component,
)


@final
@dataclass(frozen=True, order=True)
class Module:
    """A Python module path used for import resolution.

    Attributes:
        path: The import path of the module. If it starts with a `.`,
            it is treated as relative to the generation root; otherwise
            it is a fully qualified import.
    """

    @classmethod
    def for_desc(
        cls, desc: DescFile, suffix: str, *, escape_with_hash: bool = False
    ) -> Module:
        """Derive a relative module path from a file descriptor.

        Intermediate path components are sanitized (Python keywords and
        the `_pb` suffix are escaped).  The final component gets
        `suffix` appended.

        Args:
            desc: The file descriptor.
            suffix: Appended to the final path component, e.g.
                `"_pb"` turns `any.proto` into module `any_pb`.
            escape_with_hash: If true, the module name is escaped with a hash suffix to avoid
                potential collisions with other artifacts.

        Returns:
            A relative `Module`.

        Examples:
            `google/protobuf/any.proto` with suffix `"_pb"` produces
            `.google.protobuf.any_pb`.
        """
        parts = desc.name.removesuffix(".proto").split("/")
        sanitized = [
            escape_proto_module_component(part, escape_with_hash=escape_with_hash)
            for part in parts
        ]
        sanitized[-1] = sanitized[-1] + suffix
        return cls(f".{'.'.join(sanitized)}")

    path: str

    def ident(self, name: str, *, type_only: bool = False) -> Ident:
        """Return an identifier belonging to this module.

        Args:
            name: The symbol name.
            type_only: If true, the import is only emitted inside an
                `if TYPE_CHECKING:` block.

        Returns:
            A `Ident` linked to this module.
        """
        return Ident(name, self, type_only)

    def module(self, name: str) -> Module:
        """Return a child module.

        Args:
            name: The child module name.

        Returns:
            A new `Module` with `name` appended to this module's path.
        """
        return Module(f"{self.path}.{escape_identifier(name)}")


@final
@dataclass(frozen=True, order=True)
class Ident:
    """A Python identifier with its owning module.

    Attributes:
        name: The symbol name.
        module: The module this identifier is imported from.
        type_only: If true, the import is only emitted inside an
            `if TYPE_CHECKING:` block.
    """

    @classmethod
    def for_desc(
        cls,
        desc: DescEnum | DescMessage | DescExtension | DescFile,
        *,
        type_only: bool = False,
        escape_module_with_hash: bool = False,
    ) -> Ident:
        """Derive an importable identifier from a descriptor.

        For `DescFile`, the returned name is the module for the file
        within its Module, (e.g. `baz_pb` in `.foo.bar`). For message, enum, and
        extension descriptors the name is the generated symbol.

        Args:
            desc: A file, message, enum, or extension descriptor.
            type_only: If true, the import is only emitted inside an
                `if TYPE_CHECKING:` block.
            escape_module_with_hash: If true, the module name is escaped with a hash suffix to avoid
                potential collisions with other artifacts.

        Returns:
            An `Ident` linked to the derived module.
        """
        if isinstance(desc, DescFile):
            module = Module.for_desc(
                desc, "_pb", escape_with_hash=escape_module_with_hash
            )
            parent, _, module_name = module.path.rpartition(".")
            if not parent:
                parent = "."
            return cls(module_name, Module(parent), type_only, _desc=desc)
        module = Module.for_desc(
            desc.file, "_pb", escape_with_hash=escape_module_with_hash
        )
        identifier = (
            desc.type_name
            if desc.file.proto.package == ""
            else desc.type_name.removeprefix(f"{desc.file.proto.package}.")
        )
        match desc:
            case DescEnum() | DescMessage():
                identifier = desc._local_qualname
            case DescExtension():
                identifier = escape_extension_name(desc.name)
                if desc.parent:
                    identifier = f"{desc.parent._local_qualname}.{identifier}"
        return cls(identifier, module, type_only, _desc=desc)

    name: str
    module: Module
    type_only: bool = field(default=False, hash=False, compare=False)

    _desc: DescEnum | DescMessage | DescExtension | DescFile | None = field(
        default=None, repr=False, hash=False, compare=False
    )
