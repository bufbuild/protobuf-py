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
from typing import TYPE_CHECKING

import pytest

from protobuf.plugin import Ident, Module

if TYPE_CHECKING:
    from tests.conftest import Protoc


def test_ident() -> None:
    m = Module("protobuf")
    i = m.ident("Message")
    assert i == Ident("Message", m)
    assert i.type_only is False


def test_ident_type_only() -> None:
    m = Module("protobuf")
    i = m.ident("Message", type_only=True)
    assert i == Ident("Message", m, type_only=True)
    assert i.type_only is True


@pytest.mark.parametrize(
    ("parent", "child", "expected"),
    [
        ("protobuf", "wkt", "protobuf.wkt"),
        (".foo", "bar", ".foo.bar"),
        (".foo", "class", ".foo.class_"),
    ],
)
def test_module(parent: str, child: str, expected: str) -> None:
    assert Module(parent).module(child).path == expected


@pytest.mark.parametrize(
    ("proto_name", "suffix", "expected"),
    [
        ("foo/bar.proto", "_pb", ".foo.bar_pb"),
        ("foo/bar.proto", "_connect", ".foo.bar_connect"),
        ("foo.proto", "_pb", ".foo_pb"),
        ("a/b/c.proto", "_grpc", ".a.b.c_grpc"),
        ("class/foo.proto", "_pb", ".class_.foo_pb"),
        ("bar_pb/foo.proto", "_pb", ".bar_pb_.foo_pb"),
    ],
)
def test_for_desc(protoc: Protoc, proto_name: str, suffix: str, expected: str) -> None:
    desc = protoc.compile_file('syntax = "proto3";', name=proto_name)
    assert Module.for_desc(desc, suffix).path == expected


class TestIdentForDesc:
    class TestFile:
        def test_standard(self, protoc: Protoc) -> None:
            desc = protoc.compile_file(
                'syntax = "proto3"; package foo.bar;', name="foo/bar/baz.proto"
            )
            ident = Ident.for_desc(desc)
            assert ident.name == "baz_pb"
            assert ident.module == Module(".foo.bar")
            assert ident.type_only is False

        def test_hyphens(self, protoc: Protoc) -> None:
            desc = protoc.compile_file(
                'syntax = "proto3"; package foo.bar;',
                name="foo/bar-module/baz-service.proto",
            )
            ident = Ident.for_desc(desc)
            assert ident.name == "baz_service_pb"
            assert ident.module == Module(".foo.bar_module")
            assert ident.type_only is False

        def test_hyphens_hash(self, protoc: Protoc) -> None:
            desc = protoc.compile_file(
                'syntax = "proto3"; package foo.bar;',
                name="foo/bar-module/baz-service.proto",
            )
            ident = Ident.for_desc(desc, escape_module_with_hash=True)
            assert ident.name == "baz_service_2fcc6f38_pb"
            assert ident.module == Module(".foo.bar_module_c243e363")
            assert ident.type_only is False

        def test_dots(self, protoc: Protoc) -> None:
            desc = protoc.compile_file(
                'syntax = "proto3"; package foo.bar;',
                name="foo/bar.module/baz.service.proto",
            )
            ident = Ident.for_desc(desc)
            assert ident.name == "baz_service_pb"
            assert ident.module == Module(".foo.bar_module")
            assert ident.type_only is False

        @pytest.mark.skipif(
            sys.platform == "win32",
            reason="Windows does not support unicode in file paths at least in CI",
        )
        def test_unicode(self, protoc: Protoc) -> None:
            desc = protoc.compile_file(
                'syntax = "proto3"; package foo.bar;',
                name="foo/bar🐻module/baz-service.proto",
            )
            ident = Ident.for_desc(desc)
            assert ident.name == "baz_service_pb"
            assert ident.module == Module(".foo.bar_module")
            assert ident.type_only is False

        def test_pb_reserved(self, protoc: Protoc) -> None:
            desc = protoc.compile_file(
                'syntax = "proto3"; package foo.bar;', name="foo/bar_pb/cat.proto"
            )
            ident = Ident.for_desc(desc)
            assert ident.name == "cat_pb"
            assert ident.module == Module(".foo.bar_pb_")
            assert ident.type_only is False

    def test_message(self, protoc: Protoc) -> None:
        desc = protoc.compile_message(
            'syntax = "proto3"; package foo.bar; message MyMessage {}'
        )
        ident = Ident.for_desc(desc)
        assert ident.name == "MyMessage"
        assert ident.module == Module(".input_pb")

    def test_enum(self, protoc: Protoc) -> None:
        desc = protoc.compile_enum(
            'syntax = "proto3"; package pkg; enum Status { STATUS_UNSPECIFIED = 0; }'
        )
        ident = Ident.for_desc(desc)
        assert ident.name == "Status"
        assert ident.module == Module(".input_pb")

    def test_extension(self, protoc: Protoc) -> None:
        desc = protoc.compile_extension(
            """
            syntax = "proto2";
            import "google/protobuf/descriptor.proto";
            extend google.protobuf.MessageOptions {
                optional string my_opt = 50000;
            }
            """
        )
        ident = Ident.for_desc(desc)
        assert ident.name == "ext_my_opt"
        assert ident.module == Module(".input_pb")

    def test_nested_message(self, protoc: Protoc) -> None:
        desc = protoc.compile_file(
            'syntax = "proto3"; package pkg; message Outer { message Inner {} }'
        )
        inner = desc.messages[0].nested_messages[0]
        ident = Ident.for_desc(inner)
        assert ident.name == "Outer.Inner"

    def test_no_package(self, protoc: Protoc) -> None:
        desc = protoc.compile_message('syntax = "proto3"; message Msg {}')
        ident = Ident.for_desc(desc)
        assert ident.name == "Msg"


def test_ident_equality_ignores_type_only() -> None:
    m = Module("protobuf")
    a = Ident("Message", m, type_only=False)
    b = Ident("Message", m, type_only=True)
    assert a == b
    assert hash(a) == hash(b)
