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

from typing import TYPE_CHECKING, Any, cast

import pytest

from protobuf._wire import BinaryWriter, WireType
from tests.gen.example_pb import User
from tests.gen.extensions_proto2_pb import (
    GroupExt,
    Proto2ExtContainer,
    Proto2Extendee,
    Proto2ExtEnum,
    Proto2ExtMessage,
    RepeatedGroupExt,
    ext_bytes_ext,
    ext_bytes_ext_with_default,
    ext_enum_ext,
    ext_enum_ext_with_default,
    ext_groupext,
    ext_inner_ext,
    ext_message_ext,
    ext_message_ext_proto3,
    ext_packed_uint32_ext,
    ext_repeated_enum_ext,
    ext_repeated_message_ext,
    ext_repeated_string_ext,
    ext_repeatedgroupext,
    ext_string_ext,
    ext_string_ext_with_default,
    ext_uint32_ext,
    ext_uint32_ext_with_default,
    ext_uint64_ext,
    ext_unpacked_uint32_ext,
)

if TYPE_CHECKING:
    from protobuf import Extension

EXTENSIONS: list[tuple[str, Extension[Proto2Extendee, Any], Any]] = [
    ("uint32", ext_uint32_ext, 123),
    ("uint32_with_default", ext_uint32_ext_with_default, 456),
    ("string", ext_string_ext, "abc"),
    ("string_with_default", ext_string_ext_with_default, "def"),
    ("uint64", ext_uint64_ext, 999),
    ("bytes", ext_bytes_ext, b"\x00\x01\x02"),
    ("bytes_with_default", ext_bytes_ext_with_default, b"\xab\xcd"),
    ("enum", ext_enum_ext, Proto2ExtEnum.NO),
    ("enum_with_default", ext_enum_ext_with_default, Proto2ExtEnum.YES),
    ("message", ext_message_ext, Proto2ExtMessage(string_field="hello")),
    ("message_proto3", ext_message_ext_proto3, User(first_name="John")),
    ("group", ext_groupext, GroupExt(a=1, b=2)),
    (
        "repeated_message",
        ext_repeated_message_ext,
        [Proto2ExtMessage(string_field="a")],
    ),
    ("repeated_enum", ext_repeated_enum_ext, [Proto2ExtEnum.YES, Proto2ExtEnum.NO]),
    ("repeated_string", ext_repeated_string_ext, ["a", "b", "c"]),
    ("packed_uint32", ext_packed_uint32_ext, [1, 2, 3]),
    ("unpacked_uint32", ext_unpacked_uint32_ext, [4, 5, 6]),
    ("repeated_group", ext_repeatedgroupext, [RepeatedGroupExt(a=1, b=2)]),
]


@pytest.mark.parametrize(
    ("_id", "ext", "value"), EXTENSIONS, ids=[g[0] for g in EXTENSIONS]
)
def test_set_and_get(_id: str, ext: Extension[Proto2Extendee, Any], value: Any) -> None:
    msg = Proto2Extendee()
    msg[ext] = value
    assert msg[ext] == value


@pytest.mark.parametrize(
    ("_id", "ext", "value"), EXTENSIONS, ids=[g[0] for g in EXTENSIONS]
)
def test_has(_id: str, ext: Extension[Proto2Extendee, Any], value: Any) -> None:
    msg = Proto2Extendee()
    assert ext not in msg
    msg[ext] = value
    assert ext in msg


@pytest.mark.parametrize(
    ("_id", "ext", "value"), EXTENSIONS, ids=[g[0] for g in EXTENSIONS]
)
def test_clear(_id: str, ext: Extension[Proto2Extendee, Any], value: Any) -> None:
    msg = Proto2Extendee()
    msg[ext] = value
    del msg[ext]
    assert ext not in msg


@pytest.mark.parametrize(
    ("_id", "ext", "value"), EXTENSIONS, ids=[g[0] for g in EXTENSIONS]
)
def test_round_trip(_id: str, ext: Extension[Proto2Extendee, Any], value: Any) -> None:
    msg = Proto2Extendee()
    msg[ext] = value
    msg2 = Proto2Extendee.from_binary(msg.to_binary())
    assert msg2[ext] == value


def test_clear_is_idempotent() -> None:
    msg = Proto2Extendee()
    del msg[ext_uint32_ext]


def test_wrong_extendee() -> None:
    """Using an extension on the wrong message type raises TypeError."""
    msg = cast("Any", Proto2ExtMessage())
    assert ext_uint32_ext not in msg  # type: ignore[arg-type]
    with pytest.raises(TypeError, match=r"extends.*but got message of type"):
        _ = msg[ext_uint32_ext]  # type: ignore[arg-type]
    with pytest.raises(TypeError, match=r"extends.*but got message of type"):
        msg[ext_uint32_ext] = 123  # type: ignore[arg-type]
    with pytest.raises(TypeError, match=r"extends.*but got message of type"):
        del msg[ext_uint32_ext]  # type: ignore[arg-type]


class TestGetDefault:
    """Getting an unset extension returns its default value."""

    def test_scalar_zero_values(self) -> None:
        msg = Proto2Extendee()
        assert msg[ext_uint32_ext] == 0
        assert msg[ext_string_ext] == ""
        assert msg[ext_uint64_ext] == 0
        assert msg[ext_bytes_ext] == b""

    def test_proto2_custom_defaults(self) -> None:
        msg = Proto2Extendee()
        assert msg[ext_uint32_ext_with_default] == 999
        assert msg[ext_string_ext_with_default] == "hello"
        assert msg[ext_bytes_ext_with_default] == b"\xab\xcd"

    def test_enum_first_value(self) -> None:
        msg = Proto2Extendee()
        assert msg[ext_enum_ext] == Proto2ExtEnum.YES

    def test_enum_custom_default(self) -> None:
        msg = Proto2Extendee()
        assert msg[ext_enum_ext_with_default] == Proto2ExtEnum.ZERO

    def test_message_is_none(self) -> None:
        msg = Proto2Extendee()
        assert msg[ext_message_ext] is None

    def test_repeated_is_empty_list(self) -> None:
        msg = Proto2Extendee()
        assert msg[ext_repeated_string_ext] == []
        assert msg[ext_repeated_message_ext] == []
        assert msg[ext_packed_uint32_ext] == []


class TestRepeated:
    """Repeated extension edge cases."""

    def test_set_replaces(self) -> None:
        msg = Proto2Extendee()
        msg[ext_repeated_string_ext] = ["a", "b"]
        msg[ext_repeated_string_ext] = ["c"]
        assert msg[ext_repeated_string_ext] == ["c"]

    def test_get_returns_a_copy(self) -> None:
        msg = Proto2Extendee()
        msg[ext_repeated_string_ext] = ["a"]
        got = msg[ext_repeated_string_ext]
        got.append("b")
        assert msg[ext_repeated_string_ext] == ["a"]


def test_nested_extension() -> None:
    """Extensions defined inside a message class."""
    msg = Proto2Extendee()
    msg[Proto2ExtContainer.ext_uint32_ext] = 42
    msg[Proto2ExtContainer.Child.ext_uint32_ext] = 99
    assert msg[Proto2ExtContainer.ext_uint32_ext] == 42
    assert msg[Proto2ExtContainer.Child.ext_uint32_ext] == 99
    msg2 = Proto2Extendee.from_binary(msg.to_binary())
    assert msg2[Proto2ExtContainer.ext_uint32_ext] == 42
    assert msg2[Proto2ExtContainer.Child.ext_uint32_ext] == 99


def test_extension_on_extension_message() -> None:
    """Extensions set on an extension message value survive round-trip."""
    inner = Proto2ExtMessage(string_field="hello")
    inner[ext_inner_ext] = 42

    msg = Proto2Extendee()
    msg[ext_message_ext] = inner

    result = msg[ext_message_ext]
    assert result.string_field == "hello"
    assert result[ext_inner_ext] == 42


class TestMerge:
    """Parsing concatenated binary merges extensions per protobuf spec."""

    def test_singular_last_wins(self) -> None:
        msg1 = Proto2Extendee()
        msg1[ext_uint32_ext] = 111
        msg2 = Proto2Extendee()
        msg2[ext_uint32_ext] = 222
        merged = Proto2Extendee.from_binary(msg1.to_binary() + msg2.to_binary())
        assert merged[ext_uint32_ext] == 222

    def test_message_fields_merge(self) -> None:
        msg1 = Proto2Extendee()
        msg1[ext_message_ext_proto3] = User(first_name="Alice")
        msg2 = Proto2Extendee()
        msg2[ext_message_ext_proto3] = User(last_name="Smith")
        merged = Proto2Extendee.from_binary(msg1.to_binary() + msg2.to_binary())
        assert merged[ext_message_ext_proto3] == User(
            first_name="Alice", last_name="Smith"
        )

    def test_repeated_appends(self) -> None:
        msg1 = Proto2Extendee()
        msg1[ext_repeated_string_ext] = ["a", "b"]
        msg2 = Proto2Extendee()
        msg2[ext_repeated_string_ext] = ["c"]
        merged = Proto2Extendee.from_binary(msg1.to_binary() + msg2.to_binary())
        assert merged[ext_repeated_string_ext] == ["a", "b", "c"]


def encode_enum_field(field_number: int, *values: int, packed: bool = False) -> bytes:
    w = BinaryWriter()
    if packed:
        w.tag(field_number, WireType.LENGTH_DELIMITED)
        w.fork()
        for value in values:
            w.int32(value)
        w.join()
        return w.finish()

    for value in values:
        w.tag(field_number, WireType.VARINT)
        w.int32(value)
    return w.finish()


def test_closed_enum_unknown_value() -> None:
    data = encode_enum_field(5001, 99)

    msg = Proto2Extendee.from_binary(data)
    assert ext_enum_ext not in msg
    assert msg[ext_enum_ext] == Proto2ExtEnum.YES


def test_closed_repeated_enum_only_unknown_values() -> None:
    data = encode_enum_field(7005, 99, 100, packed=True)

    msg = Proto2Extendee.from_binary(data)
    assert ext_repeated_enum_ext not in msg
    assert msg[ext_repeated_enum_ext] == []


def test_closed_repeated_enum_known_and_unknown_values() -> None:
    data = encode_enum_field(7005, 2, 99, 100, packed=True)

    msg = Proto2Extendee.from_binary(data)
    assert ext_repeated_enum_ext in msg
    assert msg[ext_repeated_enum_ext] == [Proto2ExtEnum.NO]
