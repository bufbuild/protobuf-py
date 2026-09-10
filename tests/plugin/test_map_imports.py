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

from protobuf.plugin import Ident, Module
from protobuf.plugin._file import _File, write as gen_write
from protobuf.plugin._map_imports import compile_map_imports, map_import_target

if TYPE_CHECKING:
    from protobuf import DescFile
    from tests.conftest import Protoc


class TestMapImportTarget:
    @pytest.mark.parametrize(
        ("pattern", "matches"),
        [
            pytest.param("google/rpc/status.proto", True, id="exact"),
            pytest.param("google/rpc/", True, id="trailing_slash"),
            pytest.param("google/", True, id="trailing_slash_parent"),
            pytest.param("google/rpc/*", True, id="star"),
            pytest.param("google/rpc/*.proto", True, id="star_suffix"),
            pytest.param("google/rpc/**", True, id="trailing_globstar"),
            pytest.param("google/**", True, id="trailing_globstar_parent"),
            pytest.param("**", True, id="globstar_only"),
            pytest.param("**/status.proto", True, id="leading_globstar"),
            pytest.param("google/**/status.proto", True, id="globstar_zero_elements"),
            pytest.param("**/*.proto", True, id="globstar_star"),
            pytest.param("google/rpc", False, id="directory_without_slash"),
            pytest.param("google/*", False, id="star_does_not_cross_separator"),
            pytest.param("google/*.proto", False, id="star_suffix_wrong_depth"),
            pytest.param("google/rpc/status", False, id="missing_extension"),
            pytest.param("google/rpc/s.atus.proto", False, id="dot_is_literal"),
            pytest.param("rpc/", False, id="not_anchored"),
            pytest.param("google/rpc/status.proto/", False, id="file_with_slash"),
        ],
    )
    def test_pattern(self, pattern: str, *, matches: bool) -> None:
        mappings = compile_map_imports({pattern: "pkg"})
        expected = "pkg" if matches else None
        assert map_import_target("google/rpc/status.proto", mappings) == expected

    def test_first_match_wins(self) -> None:
        mappings = compile_map_imports({"google/rpc/": "first", "google/": "second"})
        assert map_import_target("google/rpc/status.proto", mappings) == "first"
        assert map_import_target("google/type/date.proto", mappings) == "second"

    def test_target_trailing_dot_stripped(self) -> None:
        mappings = compile_map_imports({"**": "pkg."})
        assert map_import_target("foo.proto", mappings) == "pkg"

    @pytest.mark.parametrize("target", ["", "."])
    def test_empty_target_is_canonical(self, target: str) -> None:
        mappings = compile_map_imports({"**": target})
        assert map_import_target("foo.proto", mappings) == ""

    @pytest.mark.parametrize(
        "target", ["my-pkg", ".pkg", "..", "a..b", "pkg/sub", "1pkg", "pkg:x"]
    )
    def test_invalid_target_raises(self, target: str) -> None:
        with pytest.raises(ValueError, match="map_imports"):
            compile_map_imports({"**": target})

    def test_empty_pattern_raises(self) -> None:
        with pytest.raises(ValueError, match="map_imports"):
            compile_map_imports({"": "pkg"})


class TestFileMaps:
    def test_symbol_import(self, desc: DescFile) -> None:
        f = _file(desc, {"dep.proto": "mypkg.gen"})
        f.print("x: ", desc.dependencies[0].messages[0])
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from mypkg.gen.dep_pb import Dep


            x: Dep
            """
        )

    def test_module_import(self, desc: DescFile) -> None:
        f = _file(desc, {"pkg/": "mypkg.gen"})
        f.print("d = ", desc.dependencies[1], ".desc()")
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from mypkg.gen.pkg import nested_pb


            d = nested_pb.desc()
            """
        )

    def test_own_symbols_not_mapped(self, desc: DescFile) -> None:
        f = _file(desc, {"**": "mypkg.gen"})
        f.print("x: ", desc.messages[0])
        f.print("y: ", desc.dependencies[0].messages[0])
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from mypkg.gen.dep_pb import Dep


            x: Foo
            y: Dep
            """
        )

    def test_unmatched_import_stays_relative(self, desc: DescFile) -> None:
        f = _file(desc, {"pkg/": "mypkg.gen"})
        f.print("x: ", desc.dependencies[0].messages[0])
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from .dep_pb import Dep


            x: Dep
            """
        )

    def test_type_only_import(self, desc: DescFile) -> None:
        f = _file(desc, {"dep.proto": "mypkg.gen"})
        f.print("x: ", Ident.for_desc(desc.dependencies[0].messages[0], type_only=True))
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from typing import TYPE_CHECKING

            if TYPE_CHECKING:
                from mypkg.gen.dep_pb import Dep


            x: Dep
            """
        )

    def test_plain_ident_not_mapped(self, desc: DescFile) -> None:
        f = _file(desc, {"**": "mypkg.gen"})
        f.print("x: ", Module(".dep_pb").ident("Dep"))
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from .dep_pb import Dep


            x: Dep
            """
        )

    def test_wkt_not_mapped(self, protoc: Protoc) -> None:
        desc = protoc.compile_file(
            """
            syntax = "proto3";
            import "google/protobuf/timestamp.proto";
            message Foo { google.protobuf.Timestamp ts = 1; }
            """
        )
        f = _file(desc, {"google/": "mypkg.gen"})
        f.print("x: ", desc.dependencies[0].messages[0])
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from protobuf.wkt import Timestamp


            x: Timestamp
            """
        )

    def test_canonical_external_dependency(self, protoc: Protoc) -> None:
        files = protoc.compile(
            {
                "app/main.proto": """
                syntax = "proto3";
                package app;
                import "buf/validate/validate.proto";
                message Main {
                    buf.validate.Rule rule = 1;
                }
                """,
                "buf/validate/validate.proto": """
                syntax = "proto3";
                package buf.validate;
                message Rule {}
                """,
            },
            "include_imports",
        )
        dep = files["buf/validate/validate.proto"]
        f = _file(files["app/main.proto"], {"buf/validate/": ""})
        f.print(dep, ".desc()")
        f.print("rule: ", dep.messages[0])
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            from buf.validate import validate_pb
            from buf.validate.validate_pb import Rule


            validate_pb.desc()
            rule: Rule
            """
        )

    def test_canonical_root_external_dependency(self, protoc: Protoc) -> None:
        """A root-level external dependency becomes a plain `import X`."""
        files = protoc.compile(
            {
                "main.proto": """
                syntax = "proto3";
                import "dep.proto";
                message Main {
                    Dep dep = 1;
                }
                """,
                "dep.proto": """
                syntax = "proto3";
                message Dep {}
                """,
            },
            "include_imports",
        )
        dep = files["dep.proto"]
        f = _file(files["main.proto"], {"dep.proto": ""})
        f.print(dep, ".desc()")
        f.print("dep: ", dep.messages[0])
        assert gen_write(f, f.path) == dedent(
            """\
            from __future__ import annotations

            import dep_pb
            from dep_pb import Dep


            dep_pb.desc()
            dep: Dep
            """
        )

    @pytest.fixture
    def desc(self, protoc: Protoc) -> DescFile:
        return protoc.compile(
            {
                "input.proto": """
                syntax = "proto3";
                import "dep.proto";
                import "pkg/nested.proto";
                message Foo {
                    Dep dep = 1;
                    pkg.Nested nested = 2;
                }
            """,
                "dep.proto": 'syntax = "proto3"; message Dep {}',
                "pkg/nested.proto": 'syntax = "proto3"; package pkg; message Nested {}',
            },
            "include_imports",
        )["input.proto"]


def _file(desc: DescFile, mappings: dict[str, str]) -> _File:
    module = Module.for_desc(desc, "_pb")
    return _File(
        path=f"{module.path.removeprefix('.').replace('.', '/')}.py",
        module=module,
        file_to_generate=frozenset(),
        plugin_name="test",
        plugin_version="0.0.0",
        parameter="",
        map_imports=compile_map_imports(mappings),
    )
