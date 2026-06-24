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

import io
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from protobuf.plugin._run import run
from protobuf.wkt import CodeGeneratorResponse
from tests.conftest import Plugin

if TYPE_CHECKING:
    from protobuf.plugin._schema import Schema
    from tests.conftest import Protoc


def test_version(monkeypatch: pytest.MonkeyPatch) -> None:
    stdout_capture = io.StringIO()
    monkeypatch.setattr(sys, "argv", ["protoc-gen-test", "--version"])
    monkeypatch.setattr(sys, "stdout", stdout_capture)
    with pytest.raises(SystemExit):
        run("protoc-gen-test", "1.2.3", lambda _: None)
    assert stdout_capture.getvalue() == "protoc-gen-test v1.2.3\n"


class TestBasicRun:
    def test_generates_file(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            for desc in schema.files_to_generate:
                f = schema.generate_file(desc, "_pb.py")
                f.print("# hello")

        resp = protoc.run_plugin(Plugin(generate), {"test.proto": 'syntax = "proto3";'})
        assert resp.error == ""
        assert len(resp.file) == 1
        assert resp.file[0].name == "test_pb.py"
        assert "# hello" in resp.file[0].content

    def test_generates_non_python_file(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            f = schema.generate_file("output.txt")
            f.print("hello world")

        resp = protoc.run_plugin(Plugin(generate), {"test.proto": 'syntax = "proto3";'})
        assert resp.error == ""
        assert len(resp.file) == 1
        assert resp.file[0].name == "output.txt"
        assert resp.file[0].content == "hello world\n"

    def test_exception_written_to_response(self, protoc: Protoc) -> None:
        def generate(_: Schema[None]) -> None:
            msg = "something went wrong"
            raise RuntimeError(msg)

        resp = protoc.run_plugin(Plugin(generate), {"test.proto": 'syntax = "proto3";'})
        assert resp.error != ""
        assert "RuntimeError" in resp.error
        assert "something went wrong" in resp.error

    def test_response_features(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(lambda _: None), {"test.proto": 'syntax = "proto3";'}
        )
        assert resp.error == ""
        expected = int(CodeGeneratorResponse.Feature.PROTO3_OPTIONAL) | int(
            CodeGeneratorResponse.Feature.SUPPORTS_EDITIONS
        )
        assert resp.supported_features == expected

    def test_all_files_includes_dependencies(self, protoc: Protoc) -> None:
        seen_all: list[list[str]] = []
        seen_to_generate: list[list[str]] = []

        def generate(schema: Schema[None]) -> None:
            seen_all.append([d.name for d in schema.all_files])
            seen_to_generate.append([d.name for d in schema.files_to_generate])

        resp = protoc.run_plugin(
            Plugin(generate),
            {
                "dep.proto": 'syntax = "proto3"; message Dep {}',
                "main.proto": 'syntax = "proto3"; import "dep.proto"; message Main { Dep dep = 1; }',
            },
            files_to_generate=["main.proto"],
        )
        assert resp.error == ""
        assert seen_all == [["dep.proto", "main.proto"]]
        assert seen_to_generate == [["main.proto"]]


class TestOptions:
    def test_dataclass_options(self, protoc: Protoc) -> None:
        @dataclass
        class _Opts:
            suffix: str = "_connect"
            verbose: bool = False

        received: list[_Opts] = []

        def generate(schema: Schema[_Opts]) -> None:
            received.append(schema.options)

        resp = protoc.run_plugin(
            Plugin(generate, options=_Opts),
            {"test.proto": 'syntax = "proto3";'},
            parameter="suffix=_connect,verbose",
        )
        assert resp.error == ""
        assert len(received) == 1
        assert received[0].suffix == "_connect"
        assert received[0].verbose is True

    def test_callable_options(self, protoc: Protoc) -> None:
        received: list[str] = []

        def generate(schema: Schema[str]) -> None:
            received.append(schema.options)

        resp = protoc.run_plugin(
            Plugin(generate, options=str.upper),
            {"test.proto": 'syntax = "proto3";'},
            parameter="hello,world",
        )
        assert resp.error == ""
        assert received == ["HELLO,WORLD"]

    def test_nonempty_parameter_without_options_is_error(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(lambda _: None),
            {"test.proto": 'syntax = "proto3";'},
            parameter="foo=bar",
        )
        assert resp.error != ""
        assert "foo=bar" in resp.error

    def test_reserved_option_in_dataclass_raises(self) -> None:
        @dataclass
        class _BadOpts:
            no_fmt_off: bool = False

        with pytest.raises(ValueError, match="no_fmt_off"):
            run("protoc-gen-test", "1.0.0", _BadOpts, lambda _: None)  # type: ignore[arg-type]


class TestFrameworkOptions:
    def test_no_fmt_off_true(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            for desc in schema.files_to_generate:
                f = schema.generate_file(desc, "_pb.py")
                f.preamble(desc)

        resp = protoc.run_plugin(
            Plugin(generate),
            {"foo/bar/baz.proto": 'syntax = "proto3"; package foo.bar;'},
            parameter="no_fmt_off",
        )
        assert resp.error == ""
        assert "# fmt: off" not in resp.file[0].content

    def test_no_fmt_off_false(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            for desc in schema.files_to_generate:
                f = schema.generate_file(desc, "_pb.py")
                f.preamble(desc)

        resp = protoc.run_plugin(
            Plugin(generate),
            {"foo/bar/baz.proto": 'syntax = "proto3"; package foo.bar;'},
            parameter="no_fmt_off=false",
        )
        assert resp.error == ""
        assert "# fmt: off" in resp.file[0].content

    def test_escape_module_with_hash_true(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            for desc in schema.files_to_generate:
                f = schema.generate_file(desc, "_pb.py")
                f.preamble(desc)

        resp = protoc.run_plugin(
            Plugin(generate),
            {"foo/bar-module/baz-service.proto": 'syntax = "proto3"; package foo.bar;'},
            parameter="escape_module_with_hash",
        )
        assert resp.error == ""
        assert len(resp.file) == 1
        assert resp.file[0].name == "foo/bar_module_c243e363/baz_service_2fcc6f38_pb.py"

    def test_escape_module_with_hash_false(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            for desc in schema.files_to_generate:
                f = schema.generate_file(desc, "_pb.py")
                f.preamble(desc)

        resp = protoc.run_plugin(
            Plugin(generate),
            {"foo/bar-module/baz-service.proto": 'syntax = "proto3"; package foo.bar;'},
            parameter="escape_module_with_hash=false",
        )
        assert resp.error == ""
        assert len(resp.file) == 1
        assert resp.file[0].name == "foo/bar_module/baz_service_pb.py"

    def test_invalid_framework_option_value_is_error(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(lambda _: None),
            {"test.proto": 'syntax = "proto3";'},
            parameter="no_fmt_off=maybe",
        )
        assert resp.error != ""
        assert "no_fmt_off" in resp.error
