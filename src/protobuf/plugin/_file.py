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

import sys
from collections import defaultdict
from contextlib import AbstractContextManager, contextmanager
from typing import TYPE_CHECKING, Any, Final, Protocol

from protobuf import DescEnum, DescExtension, DescFile, DescMessage, ScalarType
from protobuf._typing import assert_never
from protobuf.plugin._ident import Ident, Module

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable, Iterator

_INDENT = " " * 4

_TYPING = Module("typing")
_TYPE_CHECKING = _TYPING.ident("TYPE_CHECKING")

_WKT_MODULE = Module("protobuf.wkt")
_WKT_PROTO_PATHS: frozenset[str] = frozenset(
    {
        "google/protobuf/compiler/plugin.proto",
        "google/protobuf/any.proto",
        "google/protobuf/api.proto",
        "google/protobuf/cpp_features.proto",
        "google/protobuf/descriptor.proto",
        "google/protobuf/duration.proto",
        "google/protobuf/empty.proto",
        "google/protobuf/field_mask.proto",
        "google/protobuf/go_features.proto",
        "google/protobuf/java_features.proto",
        "google/protobuf/source_context.proto",
        "google/protobuf/struct.proto",
        "google/protobuf/timestamp.proto",
        "google/protobuf/type.proto",
        "google/protobuf/wrappers.proto",
    }
)


class File(Protocol):
    """A Python file that will have content generated based on the operations on this object."""

    path: str
    """The path of the file to generate, relative to the output directory."""

    def print(self, *args: object) -> None:
        """Add a line to the file.

        Args:
            *args: Elements to print on the line. Each argument is converted
                to a string element:

                - `str` values are printed verbatim.
                - `int`/`float`/`bool` as literals.
                - `bytes` as a bytes literal.
                - `Ident` as an imported name.
                - `ScalarType`, `DescMessage`, `DescEnum`, or
                  `DescExtension` as imported symbols.
                - `list` values are recursively flattened.
                - Other values are formatted with `f"{arg}"`.
        """

    def ident(self, name: str, *, type_only: bool = False) -> Ident:
        """Return an identifier scoped to this file's module.

        Args:
            name: The symbol name.
            type_only: If true, the import is emitted only inside an
                `if TYPE_CHECKING:` block.

        Returns:
            An `Ident` linked to this file's module.
        """
        ...

    def scope(self, *args: object) -> AbstractContextManager[None]:
        """Open an indented scope.

        Prints `args` as the scope header and indents all subsequent
        `print()` calls inside the context manager by one level.

        Args:
            *args: Elements to print as the scope header line.

        Examples:
            ```python
            with f.scope("class Foo:"):
                f.print("field: str")

            # Output:
            # class Foo:
            #     field: str
            ```
        """
        ...

    def type_checking(self) -> AbstractContextManager[None]:
        """Open an `if TYPE_CHECKING:` scope.

        Emits `if TYPE_CHECKING:` as a scope header and marks all
        identifiers printed inside the context manager as type-only
        imports.

        Raises:
            RuntimeError: If already inside a type-checking
                context.

        Examples:
            ```python
            with f.type_checking():
                f.print("x: ", f.ident("Foo"))

            # Output:
            # if TYPE_CHECKING:
            #     x: Foo
            #
            # The import for Foo is emitted under TYPE_CHECKING.
            ```
        """
        ...

    def preamble(self, desc: DescFile) -> None:
        """Add a `DO NOT EDIT` preamble derived from `desc`.

        Args:
            desc: The file descriptor whose proto name is used in the preamble.
        """
        ...

    def doc(self, *args: object) -> AbstractContextManager[None]:
        r'''Open a Python docstring.

        Prints opening `"""` (with `args` on the same line if
        provided) and closing `"""` on exit. If `args` are
        provided and nothing is printed inside the context manager, the
        docstring collapses to a single line. While the context is
        open, `print()` escapes `\` and `"""` in string
        elements so they cannot break the docstring. `scope()` works
        normally inside for indented sections.

        Args:
            *args: Optional elements to print on the opening line
                after the triple-quote.

        Examples:
            ```python
            with f.doc("A single-line docstring."):
                pass

            # Output:
            # """A single-line docstring."""
            ```

            ```python
            with f.doc("A short description."):
                f.print()
                f.print("Longer description.")

            # Output:
            # """A short description.
            #
            # Longer description.
            # """
            ```

            ```python
            with f.doc("Get a user by ID."):
                f.print()
                with f.scope("Args:"):
                    f.print("user_id: The unique identifier.")
                f.print()
                with f.scope("Returns:"):
                    f.print("The matching user.")

            # Output:
            # """Get a user by ID.
            #
            # Args:
            #     user_id: The unique identifier.
            #
            # Returns:
            #     The matching user.
            # """
            ```
        '''
        ...


class _File:
    if TYPE_CHECKING:
        module: Final[Module]

    def __init__(
        self,
        path: str,
        module: Module,
        file_to_generate: frozenset[str],
        plugin_name: str,
        plugin_version: str,
        parameter: str,
        *,
        escape_module_with_hash: bool = False,
    ) -> None:
        self.path = path
        self.module = module
        self._file_to_generate = file_to_generate
        self._plugin_name = plugin_name
        self._plugin_version = plugin_version
        self._parameter = parameter
        self._escape_module_with_hash = escape_module_with_hash
        self._indent = 0
        self._type_checking = False
        self._in_doc = False
        self._has_preamble = False
        self._preamble_proto_name: str | None = None
        self._elements: list[str | Ident] = []
        self._runtime_imports: dict[Module, set[Ident]] = defaultdict(set)
        self._type_imports: dict[Module, set[Ident]] = defaultdict(set)

    def print(self, *args: object) -> None:
        elements: list[str | Ident] = [self._to_el(arg) for arg in _flatten(args)]
        if all(element == "" for element in elements):
            self._elements.append("\n")
            return
        self._elements.extend([_INDENT * self._indent, *elements, "\n"])

    def ident(self, name: str, *, type_only: bool = False) -> Ident:
        return self.module.ident(name, type_only=type_only)

    @contextmanager
    def scope(self, *args: object) -> Generator[None, Any, None]:
        self.print(*args)
        self._indent += 1
        try:
            yield
        finally:
            self._indent -= 1

    @contextmanager
    def type_checking(self) -> Generator[None, Any, None]:
        if self._type_checking:
            msg = "already in a typechecking context"
            raise RuntimeError(msg)

        try:
            with self.scope("if ", _TYPE_CHECKING, ":"):
                self._type_checking = True
                yield
        finally:
            self._type_checking = False

    def preamble(self, desc: DescFile) -> None:
        self._has_preamble = True
        self._preamble_proto_name = desc.name

    @contextmanager
    def doc(self, *args: object) -> Generator[None, Any, None]:
        self._in_doc = True
        # Build the opening line manually: the '"""' prefix must not
        # be escaped, but user-provided args must be.
        self._elements.extend(
            [
                _INDENT * self._indent,
                '"""',
                *[self._to_el(arg) for arg in _flatten(args)],
                "\n",
            ]
        )
        count = len(self._elements)
        try:
            yield
        finally:
            self._in_doc = False
            if len(self._elements) == count:
                # Nothing was printed inside the block — collapse to
                # a single line: """Summary."""
                self._elements[-1] = '"""\n'
            else:
                self._elements.extend([_INDENT * self._indent, '"""', "\n"])

    def _to_el(self, v: object) -> str | Ident:
        ident: Ident
        match v:
            case ScalarType():  # This should be before int because this is an IntEnum
                return _scalar_type(v)
            case str():
                if self._in_doc:
                    # Escape backslashes and triple-quotes so they
                    # cannot break the enclosing docstring.
                    return v.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
                return v
            case DescMessage() | DescEnum() | DescExtension() | DescFile():
                ident = _desc_ident(
                    v,
                    self._file_to_generate,
                    type_only=False,
                    escape_module_with_hash=self._escape_module_with_hash,
                )
            case Ident():
                ident = (
                    _desc_ident(
                        v._desc,
                        self._file_to_generate,
                        type_only=v.type_only,
                        escape_module_with_hash=self._escape_module_with_hash,
                    )
                    if v._desc
                    else v
                )
            case _:
                return repr(v)
        ident = self._relativize(ident)
        if ident.type_only:
            self._type_imports[ident.module].add(ident)
        else:
            self._runtime_imports[ident.module].add(ident)
        return ident

    def _relativize(self, ident: Ident) -> Ident:
        if not _is_relative(ident.module):
            return Ident(
                ident.name,
                ident.module,
                type_only=ident.type_only or self._type_checking,
            )

        self_segments = _module_segments(self.module)
        import_segments = _module_segments(ident.module)
        if self_segments == import_segments:
            path = ""
        else:
            package_segments = (
                self_segments if _is_init_py(self.path) else self_segments[:-1]
            )
            shared = _shared_prefix_len(package_segments, import_segments)
            leading_dots = len(package_segments) - shared + 1
            path = "." * leading_dots + ".".join(import_segments[shared:])
        return Module(path).ident(
            ident.name, type_only=ident.type_only or self._type_checking
        )


def write(file: _File, path: str, *, no_fmt_off: bool = False) -> str:
    """Writes the file contents to string and returns that.

    We sort and group imports similar to ruff.
    """
    # Collect all the runtime imports with sorted identifier names
    runtime_imports: dict[Module, list[Ident]] = {
        module: sorted(idents)
        for module, idents in file._runtime_imports.items()
        if module.path != ""
    }
    # Type only imports that are not already in the runtime imports
    type_only_imports: dict[Module, list[Ident]] = {}
    for module, idents in file._type_imports.items():
        if module.path == "":
            continue
        unique = [
            ident for ident in idents if ident not in runtime_imports.get(module, [])
        ]
        if unique:
            type_only_imports[module] = sorted(unique)
    # If there are type only imports, add the TYPE_CHECKING identifier if not already added
    if type_only_imports:
        if _TYPING not in runtime_imports:
            runtime_imports[_TYPING] = []
        if _TYPE_CHECKING not in runtime_imports[_TYPING]:
            runtime_imports[_TYPING] = [
                _TYPE_CHECKING,
                *sorted(runtime_imports[_TYPING]),
            ]

    aliases = _AliasResolver(file)

    hdr: list[str] = []

    if file._has_preamble and file._preamble_proto_name is not None:
        hdr.extend(
            [
                _preamble(
                    file._preamble_proto_name,
                    file._plugin_name,
                    file._plugin_version,
                    file._parameter,
                    no_fmt_off=no_fmt_off,
                ),
                "",
            ]
        )

    if path.endswith(".py"):
        # Ruff doesn't complain even if this is in an empty file and always puts this at the top with a new line after
        hdr.extend(["from __future__ import annotations", ""])

    _write_imports(hdr, aliases, runtime_imports)

    if type_only_imports:
        hdr.extend([f"if {aliases.resolve(_TYPE_CHECKING)}:"])
        _write_imports(hdr, aliases, type_only_imports, indent=_INDENT)

    result = "".join(
        [
            "\n".join(hdr) + "\n\n" if hdr else "",
            *[
                el if isinstance(el, str) else aliases.resolve(el)
                for el in file._elements
            ],
        ]
    )
    return f"{result.rstrip()}\n" if result else ""


def _preamble(
    proto_name: str,
    plugin_name: str,
    plugin_version: str,
    parameter: str,
    *,
    no_fmt_off: bool,
) -> str:
    """Return the DO NOT EDIT file header for a generated proto file."""
    lines = [
        f"# Generated from {proto_name}. DO NOT EDIT.",
        f'# Generated by {plugin_name} v{plugin_version} with parameter "{parameter}".',
        "# ruff: noqa: PGH004",
        "# ruff: noqa",
    ]
    if not no_fmt_off:
        lines.append("# fmt: off")
    return "\n".join(lines)


def _desc_ident(
    desc: DescEnum | DescMessage | DescExtension | DescFile,
    file_to_generate: frozenset[str],
    *,
    type_only: bool = False,
    escape_module_with_hash: bool = False,
) -> Ident:
    """Return an importable identifier for a descriptor type."""
    ident = Ident.for_desc(
        desc, type_only=type_only, escape_module_with_hash=escape_module_with_hash
    )
    file = desc if isinstance(desc, DescFile) else desc.file
    if _use_wkt_module(file, file_to_generate):
        return Ident(ident.name, _WKT_MODULE, type_only=type_only)
    return ident


def _use_wkt_module(desc: DescFile, file_to_generate: frozenset[str]) -> bool:
    """Return True if the descriptor should be imported from protobuf.wkt."""
    # Well-known types are imported from protobuf.wkt unless the
    # WKT proto is itself being generated, in which case we use
    # a relative import to the generated file.
    return desc.name in _WKT_PROTO_PATHS and desc.name not in file_to_generate


def _write_imports(
    lines: list[str],
    aliases: _AliasResolver,
    imports: dict[Module, list[Ident]],
    indent: str = "",
) -> None:
    """Append grouped import lines to `lines`."""
    # Ruff splits the imports into groups of std, global, and relative. We also do the same:
    for group in _group_and_sort_imports(imports):
        for module, idents in group.items():
            deduped = sorted({aliases.resolve_import(ident) for ident in idents})
            lines.append(f"{indent}from {module.path} import {', '.join(deduped)}")

        lines.append("")


def _group_and_sort_imports(
    imports: dict[Module, list[Ident]],
) -> list[dict[Module, list[Ident]]]:
    """Split imports into stdlib, third-party, and relative groups."""
    std, gbl, rel = {}, {}, {}
    for module, idents in imports.items():
        if _is_relative(module):
            rel[module] = idents
        elif module.path.split(".", 1)[0] in sys.stdlib_module_names:
            std[module] = idents
        else:
            gbl[module] = idents
    return [dict(sorted(group.items())) for group in [std, gbl, rel] if group]


class _AliasResolver:
    """Keeps track of all the symbols (imported and self) and their aliases for a file.

    Aliases are created by adding `_` to the end. For every n conflicting symbols, each
    nth conflict's alias is (n-1) underscores appended.

    Symbols that belong to the file take precedence.
    """

    def __init__(self, file: _File) -> None:
        # Mark all identifiers of the current file as seen to avoid aliases.
        self._seen: dict[str, list[Ident]] = {
            ident.name: [ident] for ident in file._runtime_imports[Module("")]
        }
        # We must also mark type only ones of the current module
        for ident in file._type_imports[Module("")]:
            self._resolve(ident)

    def resolve(self, ident: Ident) -> str:
        """Returns the alias or name."""
        root, _, suffix = ident.name.partition(".")
        if suffix:
            resolved = self._resolve_name(Ident(root, ident.module))
            return f"{resolved}.{suffix}"
        return self._resolve_name(ident)

    def resolve_import(self, ident: Ident) -> str:
        """Returns the import statement for an alias or the name."""
        root, _, suffix = ident.name.partition(".")
        if suffix:
            ident = Ident(root, ident.module)
        al = self._resolve(ident)
        return f"{ident.name} as {al}" if al else ident.name

    def _resolve_name(self, ident: Ident) -> str:
        """Returns the alias or name for the ident."""
        return al if (al := self._resolve(ident)) else ident.name

    def _resolve(self, ident: Ident) -> str:
        if ident.name not in self._seen:
            self._seen[ident.name] = [ident]
        if ident not in self._seen[ident.name]:
            self._seen[ident.name].append(ident)

        i = self._seen[ident.name].index(ident)
        if i == 0:
            return ""
        candidate = f"{ident.name}{'_' * i}"
        return self._resolve(Ident(candidate, ident.module)) or candidate


def _scalar_type(scalar: ScalarType) -> str:  # noqa: RET503
    """Map a protobuf scalar type to its Python type name."""
    match scalar:
        case ScalarType.DOUBLE | ScalarType.FLOAT:
            return "float"
        case (
            ScalarType.INT64
            | ScalarType.UINT64
            | ScalarType.INT32
            | ScalarType.FIXED64
            | ScalarType.FIXED32
            | ScalarType.UINT32
            | ScalarType.SFIXED32
            | ScalarType.SFIXED64
            | ScalarType.SINT32
            | ScalarType.SINT64
        ):
            return "int"
        case ScalarType.BOOL:
            return "bool"
        case ScalarType.STRING:
            return "str"
        case ScalarType.BYTES:
            return "bytes"
        case _:
            assert_never(scalar)


def _flatten(args: Iterable[object]) -> Iterator[object]:
    """Recursively flatten nested lists into a single sequence."""
    for arg in args:
        if isinstance(arg, list):
            yield from _flatten(arg)
        else:
            yield arg


def _is_relative(module: Module) -> bool:
    """Return True if the module path is a relative import."""
    return module.path.startswith(".")


def _module_segments(module: Module) -> list[str]:
    path = module.path.removeprefix(".")
    return path.split(".") if path else []


def _is_init_py(path: str) -> bool:
    file_name = path.rsplit("/", maxsplit=1)[-1]
    return file_name == "__init__.py"


def _shared_prefix_len(left: list[str], right: list[str]) -> int:
    for i, (left_part, right_part) in enumerate(zip(left, right, strict=False)):
        if left_part != right_part:
            return i
    return min(len(left), len(right))
