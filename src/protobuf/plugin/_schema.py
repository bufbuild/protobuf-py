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

from typing import TYPE_CHECKING, Generic, Protocol, TypeVar, overload

from protobuf import DescFile
from protobuf._file_registry import _get_file_edition
from protobuf.wkt import FileDescriptorSet

from ._file import File, _File
from ._ident import Module

if TYPE_CHECKING:
    from collections.abc import Sequence

    from protobuf.wkt import CodeGeneratorRequest

T_co = TypeVar("T_co", covariant=True)


class Schema(Protocol[T_co]):
    """Schema describes the files and types that the plugin is requested to generate."""

    @property
    def options(self) -> T_co:
        """Parsed plugin options."""
        ...

    @property
    def files_to_generate(self) -> Sequence[DescFile]:
        """Files we are asked to generate."""
        ...

    @property
    def all_files(self) -> Sequence[DescFile]:
        """All files including transitive dependencies."""
        ...

    @overload
    def generate_file(self, path: str, /) -> File: ...

    @overload
    def generate_file(self, desc: DescFile, suffix: str, /) -> File: ...

    def generate_file(
        self, path_or_desc: str | DescFile = "", suffix: str = "", /
    ) -> File:
        """Create a generated file.

        Two calling conventions are supported:

        `generate_file(path)`
            Create a file at an arbitrary output path relative to the
            generation root.

        `generate_file(desc, suffix)`
            Create a file with a path derived from the descriptor:
            `<proto path without .proto><suffix>.py`.

        Args:
            path_or_desc: Either a string path (e.g.
                `"my_package/__init__.py"`) or a `DescFile` to
                derive the path from.
            suffix: When `path_or_desc` is a `DescFile`, the
                suffix to append, with file extension. For example,
                `"_pb.py"` turns `google/protobuf/any.proto` into
                `google/protobuf/any_pb.py`, while `"_pb.txt"` turns it into
                `google/protobuf/any_pb.txt`.

        Returns:
            A new `File` for writing content into.
        """
        ...


class _Schema(Generic[T_co]):
    def __init__(
        self,
        req: CodeGeneratorRequest,
        options: T_co,
        *,
        minimum_edition: int,
        maximum_edition: int,
        name: str,
        version: str,
        escape_module_with_hash: bool,
    ) -> None:
        self._options = options
        self._name = name
        self._version = version
        self._parameter = req.parameter
        self._generated_files: dict[str, _File] = {}
        self._escape_module_with_hash = escape_module_with_hash

        file_to_generate = frozenset(req.file_to_generate)
        source_by_name = {s.name: s for s in req.source_file_descriptors}
        for file in req.proto_file:
            if file.name not in file_to_generate:
                continue
            edition = _get_file_edition(source_by_name.get(file.name, file))
            if edition < minimum_edition or edition > maximum_edition:
                msg = f"{file.name} has edition {edition}, which is outside the supported range {minimum_edition} to {maximum_edition}"
                raise ValueError(msg)

        reg = FileDescriptorSet(
            file=[source_by_name.get(f.name, f) for f in req.proto_file]
        ).to_registry()
        all_files: list[DescFile] = []
        for f in req.proto_file:
            desc = reg.file(f.name)
            assert desc is not None, f"registry missing file {f.name}"  # noqa: S101
            all_files.append(desc)
        self._all_files = all_files
        self._file_to_generate = file_to_generate
        self._file_desc_to_generate = [
            d for d in all_files if d.name in file_to_generate
        ]

    @property
    def options(self) -> T_co:
        return self._options

    @property
    def files_to_generate(self) -> Sequence[DescFile]:
        return self._file_desc_to_generate

    @property
    def all_files(self) -> Sequence[DescFile]:
        return self._all_files

    def generate_file(
        self, path_or_desc: str | DescFile = "", suffix: str = ""
    ) -> _File:
        if isinstance(path_or_desc, DescFile):
            # Module represents a Python import path base, which generation uses
            # primarily for resolving relative imports. Because suffix can point to
            # arbitrary non-Python files, we always ensure the module is still a
            # standard Python module path.
            suffix, _, ext = suffix.partition(".")
            module = Module.for_desc(
                path_or_desc, suffix, escape_with_hash=self._escape_module_with_hash
            )
            path = _output_path_from_module(module)
            if ext:
                path += f".{ext}"
        else:
            path = path_or_desc
            module = _module_from_path(path_or_desc)
        f = _File(
            path,
            module,
            self._file_to_generate,
            self._name,
            self._version,
            self._parameter,
            escape_module_with_hash=self._escape_module_with_hash,
        )
        self._generated_files[path] = f
        return f


def _output_path_from_module(module: Module) -> str:
    """Compute the output path from a module."""
    module_path = module.path.removeprefix(".")
    if not module_path:
        return "__init__"
    return module_path.replace(".", "/")


def _module_from_path(path: str) -> Module:
    """Compute a Module from an arbitrary output path.

    `__init__.py` paths are mapped to their parent package because
    `foo/bar/__init__.py` is the Python package `foo.bar`, not the
    module `foo.bar.__init__`.  A bare `__init__.py` maps to the
    root package `.`.
    """
    parts = path.split("/")
    if not parts:
        return Module(".")
    base, _, _ = parts[-1].partition(".")
    parts[-1] = base
    if parts[-1] == "__init__":
        parts = parts[:-1]
    if not parts:
        return Module(".")
    return Module(f".{'.'.join(parts)}")
