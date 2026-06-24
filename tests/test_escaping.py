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

import ast
import keyword
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from protobuf.plugin._file import _desc_ident
from protobuf.plugin._ident import Module

if TYPE_CHECKING:
    from tests.conftest import Protoc


@pytest.mark.parametrize(
    "proto_file_path",
    [
        "foo/bar.proto",
        pytest.param(
            "bär.proto",
            marks=pytest.mark.xfail(
                sys.platform == "win32",
                reason="protoc cannot handle non-ASCII filenames on Windows",
            ),
        ),
        "foo.proto",
        "foo1/bar_baz.proto",
        "list/bar.proto",
        "class/bar.proto",
        "match/bar.proto",
        pytest.param("0x.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a b.bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a-b/bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a+b/bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a.b/bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param(
            "__init__/foo.proto", marks=pytest.mark.xfail(reason="not escaped")
        ),
        pytest.param("_foo.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param(
            "__pycache__/foo.proto", marks=pytest.mark.xfail(reason="not escaped")
        ),
        pytest.param("__init__.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("café☕.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param(
            "!\"#$%&'()*,;=?@[\\]^`{|}~.proto",
            marks=pytest.mark.xfail(reason="not escaped"),
        ),
        pytest.param(
            "__main__/foo.proto", marks=pytest.mark.xfail(reason="not escaped")
        ),
    ],
)
def test_module_name(generated_names: _Generated, proto_file_path: str) -> None:
    """Verify each proto file path produces an importable Python module name.

    Each component of the name must:
    - Be a valid Python identifier.
    - Not be a Python keyword.
    - Not be a reserved import system name.

    A dot in the proto path must not introduce an extra module name component.
    """
    name = generated_names.module_name(proto_file_path)
    components = name.split(".")
    expected_depth = proto_file_path.count("/") + 1
    assert len(components) == expected_depth, (
        f"expected {expected_depth} components, got {len(components)}: {name}"
    )
    reserved_import_system_names = frozenset({"__init__", "__pycache__", "__main__"})
    for component in components:
        assert component.isidentifier(), (
            f"module name {name} has invalid identifier in {component!r}"
        )
        assert not keyword.iskeyword(component), (
            f"module name {name} has keyword in {component!r}"
        )
        assert component not in reserved_import_system_names, (
            f"module name {name} has reserved name in {component!r}"
        )
        assert not component.startswith("_"), (
            f"module name {name} has private component in {component!r}"
        )


@pytest.mark.parametrize(
    ("proto_a", "proto_b"),
    [
        ("foo.proto", "foo_pb/bar.proto"),
        ("x/foo.proto", "x/foo_pb/bar.proto"),
        ("x/foo_pb/bar.proto", "x/foo.proto"),
        ("x/a.proto", "x/b.proto"),
    ],
)
def test_module_name_collision(
    generated_names: _Generated, proto_a: str, proto_b: str
) -> None:
    """Verify different proto file paths produce distinct, non-overlapping module names."""
    path_a = generated_names.module_name(proto_a)
    path_b = generated_names.module_name(proto_b)
    assert path_a != path_b, f"{proto_a!r} and {proto_b!r} both map to {path_a!r}"
    assert not path_b.startswith(path_a + "."), (
        f"{proto_b!r} module {path_b!r} is a submodule of {proto_a!r} module {path_a!r}"
    )
    assert not path_a.startswith(path_b + "."), (
        f"{proto_a!r} module {path_a!r} is a submodule of {proto_b!r} module {path_b!r}"
    )


@pytest.mark.parametrize(
    "proto_file_path",
    [
        "example.proto",
        "foo/bar.proto",
        "__init__.proto",
        pytest.param("a-b/bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a+b/bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a b.bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("a.b/bar.proto", marks=pytest.mark.xfail(reason="not escaped")),
        pytest.param("café☕.proto", marks=pytest.mark.xfail(reason="not escaped")),
    ],
)
def test_file_descriptor_var_name(
    generated_names: _Generated, proto_file_path: str
) -> None:
    """The file descriptor variable name must be a valid Python identifier."""
    name = generated_names.file_descriptor_var_name(proto_file_path)
    assert name.isidentifier(), (
        f"file descriptor var {name!r} is not a valid identifier"
    )
    assert not keyword.iskeyword(name), f"file descriptor var {name!r} is a keyword"


@pytest.mark.xfail(reason="not escaped")
def test_generated_escaping_is_valid_python() -> None:
    """The generated escaping_pb.py must be valid Python syntax."""
    # TODO #322: once escaping is implemented, remove this test and let pyright catch regressions
    source = (Path(__file__).parent / "gen" / "escaping_pb.py").read_text(
        encoding="utf-8"
    )
    ast.parse(source)


def test_escaping_importable() -> None:
    from .gen import escaping_pb  # noqa: F401, PLC0415


class _Generated:
    def __init__(self, protoc: Protoc) -> None:
        self.protoc = protoc

    def module_name(self, proto_file_path: str) -> str:
        """Compile a proto file path and return its Python module name: foo/bar.proto -> foo.bar_pb."""
        desc = self.protoc.compile_file('syntax = "proto3";', name=proto_file_path)
        mod = Module.for_desc(desc, "_pb")
        assert mod.path.startswith(".")
        return mod.path.lstrip(".")

    def file_descriptor_var_name(self, proto_file_path: str) -> str:
        """Return the file descriptor variable name the codegen produces."""
        desc = self.protoc.compile_file('syntax = "proto3";', name=proto_file_path)
        return _desc_ident(desc, frozenset()).name


@pytest.fixture
def generated_names(protoc: Protoc) -> _Generated:
    return _Generated(protoc)
