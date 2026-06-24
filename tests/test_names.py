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

import pytest

from protobuf._names import proto_camel_case, proto_snake_case

if TYPE_CHECKING:
    from tests.conftest import Protoc


@pytest.mark.parametrize(
    ("camel", "snake"),
    [
        ("", ""),
        ("fooBar", "foo_bar"),
        ("fooBarBaz", "foo_bar_baz"),
        ("foo", "foo"),
        ("ID", "_i_d"),
        ("fooID", "foo_i_d"),
        ("HTMLParser", "_h_t_m_l_parser"),
        ("a", "a"),
        ("aB", "a_b"),
        ("alreadysnake", "alreadysnake"),
    ],
)
def test_camel_to_snake(camel: str, snake: str) -> None:
    assert proto_snake_case(camel) == snake


@pytest.mark.parametrize(
    "name",
    [
        "foo_bar",
        "__proto__",
        "fieldname1",
        "field_name2",
        "_field_name3",
        "field__name4_",
        "field0name5",
        "field_0_name6",
        "fieldName7",
        "FieldName8",
        "field_Name9",
        "Field_Name10",
        "FIELD_NAME11",
        "FIELD_name12",
        "__field_name13",
        "__Field_name14",
        "field__name15",
        "field__Name16",
        "field_name17__",
        "Field_name18__",
    ],
)
def test_proto_camel_case_matches_protoc(protoc: Protoc, name: str) -> None:
    """proto_camel_case must agree with the json_name assigned by protoc."""
    desc = protoc.compile_field(
        f"""\
edition = "2023";
message M {{
    int32 {name} = 1;
}}
"""
    )
    assert proto_camel_case(name) == desc.proto.json_name


@pytest.mark.parametrize(
    "name", ["foo_bar", "foo_bar_baz", "foo", "a_b", "a", "single", "already_camel"]
)
def test_roundtrip(name: str) -> None:
    assert proto_snake_case(proto_camel_case(name)) == name


@pytest.mark.parametrize(
    ("snake", "camel"),
    [("foo_", "foo"), ("foo__", "foo"), ("foo__bar", "fooBar"), ("foo_1", "foo1")],
)
def test_irreversible(snake: str, camel: str) -> None:
    """Some snake_case names produce a camelCase that cannot round-trip back."""
    assert proto_camel_case(snake) == camel
    assert proto_snake_case(camel) != snake
