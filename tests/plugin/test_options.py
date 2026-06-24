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

import enum
import sys
from dataclasses import dataclass, field
from typing import Literal

import pytest

from protobuf.plugin._options import parse_options


class TestScalar:
    @dataclass
    class Options:
        name: str = "default"
        verbose: bool = False
        count: int = 0
        ratio: float = 1.0

    def test_defaults_empty_string(self) -> None:
        result, unparsed = parse_options(TestScalar.Options, "")
        assert unparsed == ""
        assert result == TestScalar.Options()

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("name=hello", Options(name="hello")),
            ("name=foo=bar", Options(name="foo=bar")),
            ("verbose", Options(verbose=True)),
            ("verbose=true", Options(verbose=True)),
            ("verbose=True", Options(verbose=True)),
            ("verbose=false", Options(verbose=False)),
            ("verbose=False", Options(verbose=False)),
            ("count=42", Options(count=42)),
            ("count=-1", Options(count=-1)),
            ("ratio=0.75", Options(ratio=0.75)),
            ("ratio=2", Options(ratio=2.0)),
            (
                "name=world,verbose=true,count=5,ratio=3.14",
                Options(name="world", verbose=True, count=5, ratio=3.14),
            ),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestScalar.Options, parameter)
        assert unknown == ""
        assert result == expected

    @pytest.mark.parametrize(
        ("parameter", "match"),
        [
            ("verbose=maybe", "cannot parse 'maybe' as bool"),
            ("verbose=1", "cannot parse '1' as bool"),
            ("verbose=yes", "cannot parse 'yes' as bool"),
            ("count=abc", "cannot parse 'abc' as int"),
            ("ratio=nan_bad", "cannot parse 'nan_bad' as float"),
            ("name", "requires a value"),
            ("count", "requires a value"),
            ("name=a,name=b", "specified 2 times"),
        ],
    )
    def test_invalid(self, parameter: str, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            parse_options(TestScalar.Options, parameter)


class TestList:
    @dataclass
    class Options:
        imports: list[str] = field(default_factory=list)
        counts: list[int] = field(default_factory=list)

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("", Options()),
            ("imports=foo", Options(imports=["foo"])),
            (
                "imports=foo,imports=bar,imports=baz",
                Options(imports=["foo", "bar", "baz"]),
            ),
            ("counts=1,counts=2,counts=3", Options(counts=[1, 2, 3])),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestList.Options, parameter)
        assert unknown == ""
        assert result == expected

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="cannot parse 'abc' as int"):
            parse_options(TestList.Options, "counts=abc")


class TestDict:
    @dataclass
    class Options:
        rewrites: dict[str, str] = field(default_factory=dict)

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("", Options()),
            ("rewrites=foo.proto:pkg/foo", Options(rewrites={"foo.proto": "pkg/foo"})),
            (
                "rewrites=a.proto:pkg/a,rewrites=b.proto:pkg/b",
                Options(rewrites={"a.proto": "pkg/a", "b.proto": "pkg/b"}),
            ),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestDict.Options, parameter)
        assert unknown == ""
        assert result == expected

    @pytest.mark.parametrize(
        ("parameter", "match"),
        [
            ("rewrites=nocolon", r"must contain ':'"),
            (
                "rewrites=a.proto:pkg/a,rewrites=a.proto:pkg/b",
                "duplicate key 'a.proto'",
            ),
            ("rewrites", "requires a value"),
        ],
    )
    def test_invalid(self, parameter: str, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            parse_options(TestDict.Options, parameter)


class TestLiteral:
    @dataclass
    class Options:
        target: Literal["js", "ts", "py"] = "py"

    def test_valid(self) -> None:
        result, unknown = parse_options(TestLiteral.Options, "target=js")
        assert unknown == ""
        assert result == TestLiteral.Options(target="js")

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="not a valid value"):
            parse_options(TestLiteral.Options, "target=rust")


if sys.version_info >= (3, 11):

    class TestStrEnum:
        @dataclass
        class Options:
            class Color(enum.StrEnum):
                RED = "crimson"
                GREEN = "lime"
                BLUE = "azure"

            color: Color = Color.RED

        @pytest.mark.parametrize(
            ("parameter", "expected"),
            [
                ("color=red", Options(color=Options.Color.RED)),
                ("color=RED", Options(color=Options.Color.RED)),
                ("color=crimson", Options(color=Options.Color.RED)),
                ("color=CRIMSON", Options(color=Options.Color.RED)),
                ("color=GREEN", Options(color=Options.Color.GREEN)),
                ("color=lime", Options(color=Options.Color.GREEN)),
            ],
        )
        def test_valid(self, parameter: str, expected: Options) -> None:
            result, unknown = parse_options(TestStrEnum.Options, parameter)
            assert unknown == ""
            assert result == expected

        def test_invalid(self) -> None:
            with pytest.raises(ValueError, match="not a valid Color"):
                parse_options(TestStrEnum.Options, "color=yellow")


class TestLegacyStrEnum:
    @dataclass
    class Options:
        class Color(str, enum.Enum):
            RED = "crimson"
            GREEN = "lime"
            BLUE = "azure"

        color: Color = Color.RED

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("color=red", Options(color=Options.Color.RED)),
            ("color=RED", Options(color=Options.Color.RED)),
            ("color=crimson", Options(color=Options.Color.RED)),
            ("color=CRIMSON", Options(color=Options.Color.RED)),
            ("color=GREEN", Options(color=Options.Color.GREEN)),
            ("color=lime", Options(color=Options.Color.GREEN)),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestLegacyStrEnum.Options, parameter)
        assert unknown == ""
        assert result == expected

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="not a valid Color"):
            parse_options(TestLegacyStrEnum.Options, "color=yellow")


class TestIntEnum:
    @dataclass
    class Options:
        class Level(enum.IntEnum):
            DEBUG = 0
            INFO = 1
            WARNING = 2
            ERROR = 3

        level: Level = Level.INFO

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("level=debug", Options(level=Options.Level.DEBUG)),
            ("level=WARNING", Options(level=Options.Level.WARNING)),
            ("level=3", Options(level=Options.Level.ERROR)),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestIntEnum.Options, parameter)
        assert unknown == ""
        assert result == expected

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="not a valid Level"):
            parse_options(TestIntEnum.Options, "level=verbose")


class TestOptional:
    @dataclass
    class Options:
        flag: bool | None = None
        count: int | None = None

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("", Options()),
            ("flag", Options(flag=True)),
            ("flag=true", Options(flag=True)),
            ("flag=false", Options(flag=False)),
            ("count=5", Options(count=5)),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestOptional.Options, parameter)
        assert unknown == ""
        assert result == expected

    def test_invalid(self) -> None:
        with pytest.raises(ValueError, match="cannot parse 'maybe' as bool"):
            parse_options(TestOptional.Options, "flag=maybe")


class TestMetadataNameAlias:
    @dataclass
    class Options:
        async_: bool | None = field(default=None, metadata={"name": "async"})

    @pytest.mark.parametrize(
        ("parameter", "expected"),
        [
            ("", Options()),
            ("async=true", Options(async_=True)),
            ("async=false", Options(async_=False)),
            ("async", Options(async_=True)),
        ],
    )
    def test_valid(self, parameter: str, expected: Options) -> None:
        result, unknown = parse_options(TestMetadataNameAlias.Options, parameter)
        assert unknown == ""
        assert result == expected

    def test_field_name_is_not_a_key(self) -> None:
        result, unknown = parse_options(TestMetadataNameAlias.Options, "async_=true")
        assert unknown == "async_=true"
        assert result == TestMetadataNameAlias.Options(async_=None)

    def test_error_uses_option_key(self) -> None:
        with pytest.raises(ValueError, match="option 'async'"):
            parse_options(TestMetadataNameAlias.Options, "async=maybe")


class TestUnknownKeys:
    @dataclass
    class Options:
        name: str = "default"

    @pytest.mark.parametrize(
        ("parameter", "expected_unparsed"),
        [
            ("name=hello,oops=value", "oops=value"),
            ("name=hello,oops", "oops"),
            ("name=hello,foo=bar,baz=qux", "foo=bar,baz=qux"),
        ],
    )
    def test_unparsed(self, parameter: str, expected_unparsed: str) -> None:
        result, unparsed = parse_options(TestUnknownKeys.Options, parameter)
        assert result.name == "hello"
        assert unparsed == expected_unparsed


class TestRequired:
    @dataclass
    class Options:
        name: str

    def test_missing_raises(self) -> None:
        with pytest.raises(ValueError, match="missing required option 'name'"):
            parse_options(TestRequired.Options, "")
