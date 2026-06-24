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

from protobuf._bootstrap import _EDITION_PROTO2, _EDITION_PROTO3
from tests.conftest import Plugin

if TYPE_CHECKING:
    from protobuf.plugin._schema import Schema
    from tests.conftest import Protoc

_PROTO3_FILES = {
    "input.proto": """
        syntax = "proto3";
        import "dep.proto";
        message Foo {
            Dep dep = 1;
        }
    """,
    "dep.proto": """
        syntax = "proto3";
        message Dep {}
    """,
}

_PROTO2_FILES = {
    "input.proto": """
        syntax = "proto2";
        message Foo {
            optional int32 id = 1;
        }
    """
}


class TestSchema:
    def test_basic_proto3(self, protoc: Protoc) -> None:
        received: list[object] = []

        def generate(schema: Schema[None]) -> None:
            received.append(schema.options)
            assert len(schema.files_to_generate) == 1
            assert schema.files_to_generate[0].name == "input.proto"

        resp = protoc.run_plugin(
            Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
        )
        assert resp.error == ""
        assert len(received) == 1
        assert received[0] is None

    def test_all_files_includes_deps(self, protoc: Protoc) -> None:
        def generate(schema: Schema[None]) -> None:
            all_names = [f.name for f in schema.all_files]
            assert "input.proto" in all_names
            assert "dep.proto" in all_names

        resp = protoc.run_plugin(
            Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
        )
        assert resp.error == ""

    class TestGenerateFileByPath:
        def test_py(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                schema.generate_file("my_package/utils.py")

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            assert any(f.name == "my_package/utils.py" for f in resp.file)

        def test_not_py(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                dep_file = next(f for f in schema.all_files if f.name == "dep.proto")
                f = schema.generate_file("my_package/utils.txt")
                f.print(dep_file.messages[0])

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            out_file = next(
                (f for f in resp.file if f.name == "my_package/utils.txt"), None
            )
            assert out_file is not None
            # Verify relative import is correct. Not handling the extension would
            # cause an extra level up.
            assert out_file.content.startswith("from ..dep_pb import Dep")

        def test_no_ext(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                schema.generate_file("my_package/utils")

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            assert any(f.name == "my_package/utils" for f in resp.file)

        def test_two_ext(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                schema.generate_file("my_package/utils.pb.txt")

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            assert any(f.name == "my_package/utils.pb.txt" for f in resp.file)

    class TestGenerateFileByDesc:
        def test_bare_suffix(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                schema.generate_file(schema.files_to_generate[0], "_pb")

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            # Not a Python file
            assert any(f.name == "input_pb" for f in resp.file)

        def test_py(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                schema.generate_file(schema.files_to_generate[0], "_pb.py")

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            assert any(f.name == "input_pb.py" for f in resp.file)

        def test_not_py(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                dep_file = next(f for f in schema.all_files if f.name == "dep.proto")
                f = schema.generate_file(schema.files_to_generate[0], "_pb.pyi")
                f.print(dep_file.messages[0])

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            out_file = next((f for f in resp.file if f.name == "input_pb.pyi"), None)
            assert out_file is not None
            # Verify relative import is correct. Not handling the extension would
            # cause an extra level up.
            assert out_file.content.startswith("from .dep_pb import Dep")

        def test_py_and_not_py(self, protoc: Protoc) -> None:
            def generate(schema: Schema[None]) -> None:
                schema.generate_file(schema.files_to_generate[0], "_pb.py")
                schema.generate_file(schema.files_to_generate[0], "_pb.txt")
                schema.generate_file(schema.files_to_generate[0], ".pb.bin")

            resp = protoc.run_plugin(
                Plugin(generate), _PROTO3_FILES, files_to_generate=["input.proto"]
            )
            assert resp.error == ""
            assert {f.name for f in resp.file} == {
                "input_pb.py",
                "input_pb.txt",
                "input.pb.bin",
            }


class TestEditionBounds:
    def test_proto3_within_range(self, protoc: Protoc) -> None:
        count: list[int] = []

        def generate(schema: Schema[None]) -> None:
            count.append(len(schema.files_to_generate))

        resp = protoc.run_plugin(
            Plugin(
                generate,
                minimum_edition=_EDITION_PROTO2,
                maximum_edition=_EDITION_PROTO3,
            ),
            _PROTO3_FILES,
            files_to_generate=["input.proto"],
        )
        assert resp.error == ""
        assert count == [1]

    def test_proto3_rejected_when_max_is_proto2(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(
                lambda _: None,
                minimum_edition=_EDITION_PROTO2,
                maximum_edition=_EDITION_PROTO2,
            ),
            _PROTO3_FILES,
            files_to_generate=["input.proto"],
        )
        assert "input.proto has edition 999" in resp.error

    def test_proto2_rejected_when_min_is_proto3(self, protoc: Protoc) -> None:
        resp = protoc.run_plugin(
            Plugin(
                lambda _: None,
                minimum_edition=_EDITION_PROTO3,
                maximum_edition=_EDITION_PROTO3,
            ),
            _PROTO2_FILES,
            files_to_generate=["input.proto"],
        )
        assert "input.proto has edition 998" in resp.error

    def test_dep_outside_range_is_not_checked(self, protoc: Protoc) -> None:
        """Only files_to_generate are checked, not transitive deps."""
        count: list[int] = []

        def generate(schema: Schema[None]) -> None:
            count.append(len(schema.files_to_generate))

        resp = protoc.run_plugin(
            Plugin(
                generate,
                minimum_edition=_EDITION_PROTO3,
                maximum_edition=_EDITION_PROTO3,
            ),
            _PROTO3_FILES,
            files_to_generate=["input.proto"],
        )
        assert resp.error == ""
        assert count == [1]
