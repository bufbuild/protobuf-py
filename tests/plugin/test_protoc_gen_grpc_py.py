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

from protoc_gen_grpc_py import _generate, _Options

from tests.conftest import Plugin

if TYPE_CHECKING:
    from tests.conftest import Protoc


# We test protoc-gen-py within the protobuf plugin's unit test to reuse test harnesses.
# In the future, if we provide a public protoc plugin testing API, we can use it to
# move these to protoc-gen-py itself.


SERVICE_PROTO = dedent(
    """\
    syntax = "proto3";
    package foo.bar;
    service FooService {
        rpc FooMethod (FooRequest) returns (FooResponse);
    }
    message FooRequest {}
    message FooResponse {}
    """
)


class TestOptions:
    def test_io_default(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(_generate, options=_Options), {"foo/bar/baz.proto": SERVICE_PROTO}
        )
        assert resp.error == ""
        file = next(f for f in resp.file if f.name == "foo/bar/baz_pb_grpc.py")
        assert "class FooServiceServicer:" in file.content
        assert "class FooServiceClient:" in file.content
        assert "class FooServiceServicerSync:" in file.content
        assert "class FooServiceClientSync:" in file.content

    def test_io_async(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(_generate, options=_Options),
            {"foo/bar/baz.proto": SERVICE_PROTO},
            parameter="io=async",
        )
        assert resp.error == ""
        file = next(f for f in resp.file if f.name == "foo/bar/baz_pb_grpc.py")
        assert "class FooServiceServicer:" in file.content
        assert "class FooServiceClient:" in file.content
        assert "class FooServiceServicerSync:" not in file.content
        assert "class FooServiceClientSync:" not in file.content

    def test_io_sync(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(_generate, options=_Options),
            {"foo/bar/baz.proto": SERVICE_PROTO},
            parameter="io=sync",
        )
        assert resp.error == ""
        file = next(f for f in resp.file if f.name == "foo/bar/baz_pb_grpc.py")
        assert "class FooServiceServicer:" not in file.content
        assert "class FooServiceClient:" not in file.content
        assert "class FooServiceServicerSync:" in file.content
        assert "class FooServiceClientSync:" in file.content
