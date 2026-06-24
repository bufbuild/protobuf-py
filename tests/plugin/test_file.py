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

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from protobuf import ScalarType
from protobuf.plugin import File, Ident, Module
from protobuf.plugin._file import _File, write as gen_write
from protobuf.wkt import any_pb, timestamp_pb

if TYPE_CHECKING:
    from collections.abc import Callable

    from protobuf import DescFile
    from tests.conftest import Protoc


@pytest.mark.parametrize(
    ("value", "literal"),
    [
        (42, "42"),
        (3.14, "3.14"),
        (True, "True"),
        (False, "False"),
        (b"\x00\x01", "b'\\x00\\x01'"),
        (b'"', "b'\"'"),
    ],
)
def test_literals(value: object, literal: str) -> None:
    _test_generated_file(
        lambda f: f.print("v = ", value),
        f"""\
        from __future__ import annotations


        v = {literal}
        """,
    )


@pytest.mark.parametrize(
    ("scalar", "expected_type"),
    [
        (ScalarType.DOUBLE, "float"),
        (ScalarType.FLOAT, "float"),
        (ScalarType.INT64, "int"),
        (ScalarType.UINT64, "int"),
        (ScalarType.INT32, "int"),
        (ScalarType.FIXED64, "int"),
        (ScalarType.FIXED32, "int"),
        (ScalarType.UINT32, "int"),
        (ScalarType.SFIXED32, "int"),
        (ScalarType.SFIXED64, "int"),
        (ScalarType.SINT32, "int"),
        (ScalarType.SINT64, "int"),
        (ScalarType.BOOL, "bool"),
        (ScalarType.STRING, "str"),
        (ScalarType.BYTES, "bytes"),
    ],
)
def test_scalar_types(scalar: ScalarType, expected_type: str) -> None:
    _test_generated_file(
        lambda f: f.print("v: ", scalar),
        f"""\
        from __future__ import annotations


        v: {expected_type}
        """,
    )


def test_list_flattening() -> None:
    _test_generated_file(
        lambda f: f.print("v: ", ["list[", ["dict[", ["str", ", ", "int"], "]"], "]"]),
        """\
        from __future__ import annotations


        v: list[dict[str, int]]
        """,
    )


def test_empty_lines() -> None:
    def write(f: File) -> None:
        f.print("v = ", 1)
        f.print()
        f.print("x = v")

    _test_generated_file(
        write,
        """\
        from __future__ import annotations


        v = 1

        x = v
        """,
    )


def test_scope() -> None:
    def write(f: File) -> None:
        with f.scope("class Foo:"):
            f.print("x: str")
            f.print()  # Just like ruff empty lines are not indented
            f.print("y: str")
        f.print("Bar = Foo")

    _test_generated_file(
        write,
        """\
        from __future__ import annotations


        class Foo:
            x: str

            y: str
        Bar = Foo
        """,
    )


def test_nested_scope() -> None:
    def write(f: File) -> None:
        with f.scope("class Foo:"):
            f.print("x: str")
            f.print("y: str")
            with f.scope("class Bar:"):
                f.print("x: str")

    _test_generated_file(
        write,
        """\
        from __future__ import annotations


        class Foo:
            x: str
            y: str
            class Bar:
                x: str
        """,
    )


def test_global_import() -> None:
    def write(f: File) -> None:
        with f.scope("class Foo(", Module("protobuf").ident("Message"), "):"):
            f.print("pass")

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from protobuf import Message


        class Foo(Message):
            pass
        """,
    )


def test_relative_import() -> None:
    def write(f: File) -> None:
        with f.scope("class Foo(", Module(".protobuf").ident("Message"), "):"):
            f.print("pass")

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from .protobuf import Message


        class Foo(Message):
            pass
        """,
    )


@pytest.mark.parametrize(
    ("path", "self_mod", "dep_mod", "expected_import"),
    [
        pytest.param(
            "__init__.py",
            Module("."),
            Module(".bar"),
            "from .bar import Baz",
            id="sibling-module-at-base",
        ),
        pytest.param(
            "foo/__init__.py",
            Module(".foo"),
            Module(".foo.bar"),
            "from .bar import Baz",
            id="sibling-module-in-subpackage",
        ),
        pytest.param(
            "foo/bar/__init__.py",
            Module(".foo.bar"),
            Module(".foo.baz"),
            "from ..baz import Baz",
            id="sibling-package",
        ),
    ],
)
def test_relative_overlapping_package(
    path: str, self_mod: Module, dep_mod: Module, expected_import: str
) -> None:
    def write(f: File) -> None:
        f.print("x: ", dep_mod.ident("Baz"))

    _test_generated_file(
        write,
        f"""\
        from __future__ import annotations

        {expected_import}


        x: Baz
        """,
        _File(
            path=path,
            module=self_mod,
            file_to_generate=frozenset(),
            plugin_name="test",
            plugin_version="0.0.0",
            parameter="",
        ),
    )


def test_import_conflicts() -> None:
    protobuf = Module("protobuf")
    other = Module(".other")
    another = Module(".another")

    def write(f: File) -> None:
        f.print("other = ", other.ident("Foo"), "()")

        with f.scope("class ", f.ident("Foo"), "(", protobuf.ident("Message"), "):"):
            f.print("other: ", other.ident("Foo"))
            f.print("another: ", another.ident("Foo"))
            f.print("others: list[", other.ident("Foo"), "]")

    # Even if an import is seen first, identifiers within the file must come first.
    # Also, the import sorting determines which symbol is aliased first.
    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from protobuf import Message

        from .another import Foo as Foo_
        from .other import Foo as Foo__


        other = Foo__()
        class Foo(Message):
            other: Foo__
            another: Foo_
            others: list[Foo__]
        """,
    )


def test_nested_ident_import() -> None:
    """Dotted ident names import only the root symbol."""
    other = Module(".other")

    def write(f: File) -> None:
        f.print("x: ", other.ident("Outer.Inner"))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from .other import Outer


        x: Outer.Inner
        """,
    )


def test_nested_ident_import_with_conflict() -> None:
    """Dotted ident root is aliased when it conflicts with a local name."""
    other = Module(".other")

    def write(f: File) -> None:
        with f.scope("class ", f.ident("Outer"), ":"):
            f.print("x: ", other.ident("Outer.Inner"))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from .other import Outer as Outer_


        class Outer:
            x: Outer_.Inner
        """,
    )


def test_nested_ident_import_dedup() -> None:
    """Multiple dotted idents with the same root produce a single import."""
    other = Module(".other")

    def write(f: File) -> None:
        f.print("x: ", other.ident("Outer.Inner"))
        f.print("y: ", other.ident("Outer.Other"))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from .other import Outer


        x: Outer.Inner
        y: Outer.Other
        """,
    )


def test_nested_ident_import_cross_module_conflict() -> None:
    """Dotted idents with the same root from different modules are aliased."""
    a = Module(".a")
    b = Module(".b")

    def write(f: File) -> None:
        f.print("x: ", a.ident("Outer.Inner"))
        f.print("y: ", b.ident("Outer.Inner"))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from .a import Outer
        from .b import Outer as Outer_


        x: Outer.Inner
        y: Outer_.Inner
        """,
    )


def test_type_checking_scope() -> None:
    def write(f: File) -> None:
        with f.type_checking():
            f.print(
                "x: ", Module("protobuf").ident("Message")
            )  # Scope will ensure this is type-only
            f.print("y: ", Module("protobuf").ident("Message", type_only=True))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING

        if TYPE_CHECKING:
            from protobuf import Message


        if TYPE_CHECKING:
            x: Message
            y: Message
        """,
    )


def test_type_only_imports() -> None:
    def write(f: File) -> None:
        f.print("y: ", Module("protobuf").ident("Message"))
        with f.type_checking():
            f.print("x: ", Module("protobuf").ident("Message", type_only=True))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING

        from protobuf import Message


        y: Message
        if TYPE_CHECKING:
            x: Message
        """,
    )


def test_type_checking_nested_raises() -> None:
    g = _File(
        path="test_pb.py",
        module=Module(".test_pb"),
        file_to_generate=frozenset(),
        plugin_name="test",
        plugin_version="0.0.0",
        parameter="",
    )
    with (
        g.type_checking(),
        pytest.raises(RuntimeError, match="already in a typechecking context"),
        g.type_checking(),
    ):
        pass


def test_write_without_preamble() -> None:
    _test_generated_file(
        lambda f: f.print("x = 1"),
        """\
        from __future__ import annotations


        x = 1
        """,
    )


def test_type_checking_alias() -> None:
    def write(f: File) -> None:
        with f.scope("class ", f.ident("TYPE_CHECKING"), ":"):
            f.print("pass")
        f.print()
        with f.type_checking():
            f.print(
                "x: ", Module("protobuf").ident("Message")
            )  # Scope will ensure this is type-only
            f.print("y: ", Module("protobuf").ident("Message", type_only=True))

    _test_generated_file(
        write,
        """\
        from __future__ import annotations

        from typing import TYPE_CHECKING as TYPE_CHECKING_

        if TYPE_CHECKING_:
            from protobuf import Message


        class TYPE_CHECKING:
            pass

        if TYPE_CHECKING_:
            x: Message
            y: Message
        """,
    )


class TestDoc:
    def test_single_line(self) -> None:
        def write(f: File) -> None:
            with f.doc("A single-line docstring."):
                pass

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """A single-line docstring."""
            ''',
        )

    def test_basic(self) -> None:
        def write(f: File) -> None:
            with f.doc("A short description."):
                f.print("Longer description.")

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """A short description.
            Longer description.
            """
            ''',
        )

    def test_no_args(self) -> None:
        def write(f: File) -> None:
            with f.doc():
                f.print("Just a description.")

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """
            Just a description.
            """
            ''',
        )

    def test_escapes_backslash(self) -> None:
        def write(f: File) -> None:
            with f.doc():
                f.print("A path: C:\\Users\\foo")

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """
            A path: C:\\\\Users\\\\foo
            """
            ''',
        )

    def test_escapes_triple_quotes(self) -> None:
        def write(f: File) -> None:
            with f.doc():
                f.print('Some text with """ triple quotes.')

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """
            Some text with \\"\\"\\" triple quotes.
            """
            ''',
        )

    def test_escapes_args(self) -> None:
        """Escaping also applies to args passed to doc() on the opening line."""

        def write(f: File) -> None:
            with f.doc('Has a backslash \\ and triple quotes """ here.'):
                pass

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """Has a backslash \\\\ and triple quotes \\"\\"\\" here."""
            ''',
        )

    def test_with_scope(self) -> None:
        def write(f: File) -> None:
            with f.doc("Get a user by ID."):
                f.print()
                with f.scope("Args:"):
                    f.print("user_id: The unique identifier.")
                f.print()
                with f.scope("Returns:"):
                    f.print("The matching user.")

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            """Get a user by ID.

            Args:
                user_id: The unique identifier.

            Returns:
                The matching user.
            """
            ''',
        )

    def test_nested_in_scope(self) -> None:
        def write(f: File) -> None:
            with f.scope("class Foo:"), f.doc("A class docstring."):
                f.print("Details here.")

        _test_generated_file(
            write,
            '''\
            from __future__ import annotations


            class Foo:
                """A class docstring.
                Details here.
                """
            ''',
        )


class TestDescriptorImports:
    def test_imports(self, desc: DescFile) -> None:
        protobuf = Module("protobuf")

        def write(f: File) -> None:
            with f.scope(
                "class ", desc.messages[0], "(", protobuf.ident("Message"), "):"
            ):
                f.print("pass")
            with f.scope("class ", desc.enums[0], "(", protobuf.ident("Enum"), "):"):
                f.print("pass")
            f.print()
            with f.scope(
                "_DESC = ", protobuf.module("_codegen").ident("file_desc"), "("
            ):
                with f.scope("["):
                    for dep in desc.dependencies:
                        f.print(dep, ".desc(),")
                f.print("]")
            f.print(")")
            with f.scope("def desc():"):
                f.print("return _DESC")

        _test_generated_file(
            write,
            """\
            from __future__ import annotations

            from protobuf import Enum, Message
            from protobuf._codegen import file_desc
            from protobuf.wkt import any_pb, timestamp_pb

            from . import b_pb
            from .pkg import b_pb as b_pb_


            class Foo(Message):
                pass
            class Enu(Enum):
                pass

            _DESC = file_desc(
                [
                    b_pb.desc(),
                    b_pb_.desc(),
                    timestamp_pb.desc(),
                    any_pb.desc(),
                ]
            )
            def desc():
                return _DESC
            """,
            file=_File(
                path="test_pb.py",
                module=Module.for_desc(desc, "_pb"),
                file_to_generate=frozenset(),
                plugin_name="test",
                plugin_version="0.0.0",
                parameter="",
            ),
        )

    def test_wkt_import_not_generated(self, desc: DescFile) -> None:
        """WKT references use protobuf.wkt when the WKT is not being generated."""
        protobuf = Module("protobuf")
        timestamp_msg = timestamp_pb.desc().messages[0]
        any_msg = any_pb.desc().messages[0]

        def write(f: File) -> None:
            with f.scope(
                "class ", desc.messages[2], "(", protobuf.ident("Message"), "):"
            ):
                f.print("ts: ", timestamp_msg)
                f.print("any: ", any_msg)

        _test_generated_file(
            write,
            """\
            from __future__ import annotations

            from protobuf import Message
            from protobuf.wkt import Any, Timestamp


            class Bar(Message):
                ts: Timestamp
                any: Any
            """,
            file=_File(
                path="test_pb.py",
                module=Module.for_desc(desc, "_pb"),
                file_to_generate=frozenset(),
                plugin_name="test",
                plugin_version="0.0.0",
                parameter="",
            ),
        )

    def test_wkt_import_when_generated(self, desc: DescFile) -> None:
        """WKT references use relative imports when the WKT is being generated."""
        protobuf = Module("protobuf")
        timestamp_msg = timestamp_pb.desc().messages[0]

        def write(f: File) -> None:
            with f.scope(
                "class ", desc.messages[2], "(", protobuf.ident("Message"), "):"
            ):
                f.print("ts: ", timestamp_msg)

        _test_generated_file(
            write,
            """\
            from __future__ import annotations

            from protobuf import Message

            from .google.protobuf.timestamp_pb import Timestamp


            class Bar(Message):
                ts: Timestamp
            """,
            file=_File(
                path="test_pb.py",
                module=Module.for_desc(desc, "_pb"),
                file_to_generate=frozenset(["google/protobuf/timestamp.proto"]),
                plugin_name="test",
                plugin_version="0.0.0",
                parameter="",
            ),
        )

    def test_wkt_import_type_only(self, desc: DescFile) -> None:
        """WKT references use protobuf.wkt when the WKT is not being generated."""
        protobuf = Module("protobuf")
        timestamp_msg = timestamp_pb.desc().messages[0]
        any_msg = any_pb.desc().messages[0]

        def write(f: File) -> None:
            with f.scope(
                "class ", desc.messages[2], "(", protobuf.ident("Message"), "):"
            ):
                f.print("ts: ", Ident.for_desc(timestamp_msg, type_only=True))
                f.print("any: ", Ident.for_desc(any_msg, type_only=True))

        _test_generated_file(
            write,
            """\
            from __future__ import annotations

            from typing import TYPE_CHECKING

            from protobuf import Message

            if TYPE_CHECKING:
                from protobuf.wkt import Any, Timestamp


            class Bar(Message):
                ts: Timestamp
                any: Any
            """,
            file=_File(
                path="test_pb.py",
                module=Module.for_desc(desc, "_pb"),
                file_to_generate=frozenset(),
                plugin_name="test",
                plugin_version="0.0.0",
                parameter="",
            ),
        )

    def test_preamble(self, protoc: Protoc) -> None:
        desc = protoc.compile_file('syntax = "proto3";')

        def write(f: File) -> None:
            f.preamble(desc)
            f.print("x = 1")

        _test_generated_file(
            write,
            """\
            # Generated from input.proto. DO NOT EDIT.
            # Generated by test-plugin v1.2.3 with parameter "target=pypy".
            # ruff: noqa: PGH004
            # ruff: noqa
            # fmt: off

            from __future__ import annotations


            x = 1
            """,
            file=_File(
                path="test_pb.py",
                module=Module.for_desc(desc, "_pb"),
                file_to_generate=frozenset(),
                plugin_name="test-plugin",
                plugin_version="1.2.3",
                parameter="target=pypy",
            ),
        )

    @pytest.fixture
    def desc(self, protoc: Protoc) -> DescFile:
        return protoc.compile(
            {
                "input.proto": """
                syntax = "proto3";
                import "b.proto";
                import "pkg/b.proto";
                import "google/protobuf/timestamp.proto";
                import "google/protobuf/any.proto";
                message Foo {}
                message M {
                    B local_b = 1;
                    E local_e = 2;
                    pkg.B pkg_b = 3;
                    pkg.Foo other_foo = 4;
                }
                message Bar {
                    google.protobuf.Timestamp ts = 1;
                    google.protobuf.Any any = 2;
                }
                enum Enu { ENU_ZERO = 0; }
            """,
                "b.proto": """
                syntax = "proto3";
                message B {}
                enum E { ZERO = 0; }
            """,
                "pkg/b.proto": """
                syntax = "proto3";
                package pkg;
                message B {}
                message Foo {}
            """,
            },
            "include_imports",
            "retain_options",
            "experimental_editions",
            "include_source_info",
        )["input.proto"]


def _test_generated_file(
    build: Callable[[File], None], expected: str, file: _File | None = None
) -> None:
    g = file or _File(
        path="test_pb.py",
        module=Module(".test_pb"),
        file_to_generate=frozenset(),
        plugin_name="test",
        plugin_version="0.0.0",
        parameter="",
    )
    build(g)
    output = gen_write(g, "test_pb.py")
    assert output == dedent(expected)
