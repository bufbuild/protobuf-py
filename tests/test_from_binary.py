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

from typing import TYPE_CHECKING, Any

import pytest

from protobuf import (
    DescEnum,
    DescField,
    DescFieldValueMap,
    DescMessage,
    Message,
    ScalarType,
)
from protobuf._typing import assert_never
from protobuf._wire import BinaryWriter, WireType

from .gen.delimited_encoding_pb import DelimitedEncoding
from .gen.enums_pb import ClosedColor, EnumMessage
from .gen.lists_pb import Lists
from .gen.maps_pb import Maps
from .gen.messages_pb import Recursive
from .gen.scalars_pb import Scalars

if TYPE_CHECKING:
    from .conftest import Protoc


def encode_map_entry(desc_field: DescField, *, key: Any, value: Any) -> bytes:
    """Build a single binary map entry for the types used in MapsMessage."""
    assert isinstance(desc_field.value, DescFieldValueMap)
    w = BinaryWriter()
    w.tag(desc_field.number, WireType.LENGTH_DELIMITED)
    w.fork()
    if key is not None:
        w.tag(1, WireType.LENGTH_DELIMITED)
        w.string(key)
    if value is not None:
        match desc_field.value.value:
            case ScalarType() | DescEnum():
                w.tag(2, WireType.VARINT)
                w.int32(value)
            case DescMessage():
                w.tag(2, WireType.LENGTH_DELIMITED)
                w.fork()
                w.raw(value.to_binary())
                w.join()
            case _:
                assert_never(desc_field.value.value)
    w.join()
    return w.finish()


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


@pytest.fixture
def maps_message_desc(protoc: Protoc) -> DescMessage:
    return protoc.compile_message("""\
        edition = "2023";
        message MapsMessage {
          message Nested { int32 a = 1; }
          enum Color {
            COLOR_UNSPECIFIED = 0;
            COLOR_RED = 1;
          }
          map<string, int32> scalar_map = 1;
          map<string, Color> enum_map = 2;
          map<string, Nested> message_map = 3;
        }
    """)


def test_map_missing_scalar_value(maps_message_desc: DescMessage) -> None:
    map_field = maps_message_desc._fields_by_local_name["scalar_map"]
    data = encode_map_entry(map_field, key="k", value=None)
    msg = maps_message_desc.type.from_binary(data)
    assert msg[map_field]["k"] == 0


def test_map_missing_enum_value(maps_message_desc: DescMessage) -> None:
    map_field = maps_message_desc._fields_by_local_name["enum_map"]
    data = encode_map_entry(map_field, key="k", value=None)
    msg = maps_message_desc.type.from_binary(data)
    assert msg[map_field]["k"] == 0


def test_map_missing_message_value(maps_message_desc: DescMessage) -> None:
    map_field = maps_message_desc._fields_by_local_name["message_map"]
    data = encode_map_entry(map_field, key="k", value=None)
    msg = maps_message_desc.type.from_binary(data)
    nested_type = maps_message_desc.nested_messages[0].type
    assert msg[map_field]["k"] is not None
    assert isinstance(msg[map_field]["k"], nested_type)


def test_map_missing_key(maps_message_desc: DescMessage) -> None:
    map_field = maps_message_desc._fields_by_local_name["scalar_map"]
    data = encode_map_entry(map_field, key=None, value=42)
    msg = maps_message_desc.type.from_binary(data)
    assert msg[map_field][""] == 42


@pytest.mark.parametrize("ignore_unknown_fields", [True, False])
def test_unknown_closed_enum_singular(ignore_unknown_fields: bool) -> None:
    data = encode_enum_field(2, 99)

    msg = EnumMessage.from_binary(data, ignore_unknown_fields=ignore_unknown_fields)

    assert not msg.has_field("closed_color_field")
    if ignore_unknown_fields:
        assert not msg._unknown_fields
    else:
        assert msg._unknown_fields == {2: [data]}


@pytest.mark.parametrize("ignore_unknown_fields", [True, False])
def test_unknown_closed_enum_packed_list(ignore_unknown_fields: bool) -> None:
    data = encode_enum_field(4, 1, 99, 2, packed=True)

    msg = EnumMessage.from_binary(data, ignore_unknown_fields=ignore_unknown_fields)

    assert msg.closed_color_list == [ClosedColor.RED, ClosedColor.GREEN]
    if ignore_unknown_fields:
        assert not msg._unknown_fields
    else:
        assert msg._unknown_fields == {4: [encode_enum_field(4, 99)]}


@pytest.mark.parametrize("ignore_unknown_fields", [True, False])
def test_unknown_closed_enum_unpacked_list(ignore_unknown_fields: bool) -> None:
    data = encode_enum_field(4, 1, 99, 2, packed=False)

    msg = EnumMessage.from_binary(data, ignore_unknown_fields=ignore_unknown_fields)

    assert msg.closed_color_list == [ClosedColor.RED, ClosedColor.GREEN]
    if ignore_unknown_fields:
        assert not msg._unknown_fields
    else:
        assert msg._unknown_fields == {4: [encode_enum_field(4, 99)]}


@pytest.mark.parametrize("ignore_unknown_fields", [True, False])
def test_unknown_closed_enum_map_value(ignore_unknown_fields: bool) -> None:
    map_field = EnumMessage._desc._fields_by_local_name["string_to_closed_color"]
    entry1 = encode_map_entry(map_field, key="a", value=2)
    entry2 = encode_map_entry(map_field, key="b", value=99)
    data = entry1 + entry2

    msg = EnumMessage.from_binary(data, ignore_unknown_fields=ignore_unknown_fields)

    assert msg.string_to_closed_color == {"a": ClosedColor.GREEN}
    if ignore_unknown_fields:
        assert not msg._unknown_fields
    else:
        assert msg._unknown_fields == {map_field.number: [entry2]}


def generate_recursive(depth: int) -> Recursive:
    if depth == 0:
        return Recursive()
    return Recursive(recursive=generate_recursive(depth - 1))


def test_equals_recursion_limit() -> None:
    msg = Recursive()
    msg.recursive = generate_recursive(99)
    msg.repeated_recursive = [generate_recursive(99) for _ in range(10)]
    msg.map_recursive = {str(i): generate_recursive(99) for i in range(10)}
    data = msg.to_binary()
    msg2 = Recursive.from_binary(data)
    assert msg == msg2


@pytest.mark.parametrize(
    "msg",
    [
        pytest.param(
            Recursive(recursive=generate_recursive(100)), id="recursive field"
        ),
        pytest.param(
            Recursive(repeated_recursive=[generate_recursive(100) for _ in range(10)]),
            id="repeated field",
        ),
        pytest.param(
            Recursive(
                map_recursive={str(i): generate_recursive(100) for i in range(10)}
            ),
            id="map field",
        ),
    ],
)
def test_exceed_recursion_limit(msg: Recursive) -> None:
    data = msg.to_binary()
    with pytest.raises(
        RecursionError,
        match="exceeded maximum recursion depth 100 while parsing message",
    ):
        Recursive.from_binary(data)


def generate_recursive_msg(depth: int) -> DelimitedEncoding.Msg:
    if depth == 0:
        return DelimitedEncoding.Msg()
    return DelimitedEncoding.Msg(child=generate_recursive_msg(depth - 1))


def test_known_group_recursion_limit() -> None:
    data = DelimitedEncoding(singular=generate_recursive_msg(100)).to_binary()

    with pytest.raises(
        RecursionError,
        match="exceeded maximum recursion depth 100 while parsing message",
    ):
        DelimitedEncoding.from_binary(data)


def test_unknown_skipped_group_equals_recursion_limit() -> None:
    start_group_tag = bytes([4 << 3 | WireType.SGROUP.value])
    end_group_tag = bytes([4 << 3 | WireType.EGROUP.value])

    data = start_group_tag * 100 + end_group_tag * 100
    msg = Recursive.from_binary(data)
    assert msg._unknown_fields == {4: [data]}


def test_unknown_skipped_group_exceeds_recursion_limit() -> None:
    start_group_tag = bytes([4 << 3 | WireType.SGROUP.value])
    end_group_tag = bytes([4 << 3 | WireType.EGROUP.value])

    data = start_group_tag * 101 + end_group_tag * 101
    with pytest.raises(
        RecursionError,
        match="exceeded maximum recursion depth 100 while skipping field 4",
    ):
        Recursive.from_binary(data)


def test_varint_matches_limit() -> None:
    data = bytes([5 << 3 | WireType.VARINT.value]) + b"\x81" + b"\x80" * 8 + b"\x00"
    msg = Scalars.from_binary(data)
    assert msg.uint32_field == 1


def test_varint_exceeds_limit_last_byte() -> None:
    data = bytes([5 << 3 | WireType.VARINT.value]) + b"\x81" + b"\x80" * 8 + b"\x02"
    with pytest.raises(ValueError, match="invalid varint"):
        Scalars.from_binary(data)


def test_varint_exceeds_limit_more_bytes() -> None:
    data = bytes([5 << 3 | WireType.VARINT.value]) + b"\x81" + b"\x80" * 8 + b"\x81"
    with pytest.raises(ValueError, match="invalid varint"):
        Scalars.from_binary(data)


class TestWireTypeMismatch:
    @pytest.mark.parametrize("msg_class", [Scalars, EnumMessage, Lists, Maps])
    def test_basic(self, msg_class: type[Message]) -> None:
        num_fields = 30
        w = BinaryWriter()
        # Groups conveniently don't match any field since these protos don't use them.
        for number in range(1, num_fields):
            w.tag(number, WireType.SGROUP)
            w.tag(number, WireType.EGROUP)
        data = w.finish()
        msg = msg_class.from_binary(data)
        assert msg == msg_class()
        # Should be enough to check every field is there without asserting the content.
        assert msg._unknown_fields is not None
        assert set(msg._unknown_fields.keys()) == set(range(1, num_fields))

    def test_map_key(self) -> None:
        w = BinaryWriter()
        for number in range(1, 22):
            w.tag(number, WireType.LENGTH_DELIMITED)
            w.fork()
            # Groups can't be used in maps
            w.tag(1, WireType.SGROUP)
            w.tag(1, WireType.EGROUP)
            w.join()
        data = w.finish()
        msg = Maps.from_binary(data)
        assert msg == Maps()
        # Should be enough to check every field is there without asserting the content.
        assert msg._unknown_fields is not None
        assert set(msg._unknown_fields.keys()) == set(range(1, 22))

    def test_map_value(self) -> None:
        w = BinaryWriter()
        for number in range(1, 22):
            w.tag(number, WireType.LENGTH_DELIMITED)
            w.fork()
            # Groups can't be used in maps
            w.tag(2, WireType.SGROUP)
            w.tag(2, WireType.EGROUP)
            w.join()
        data = w.finish()
        msg = Maps.from_binary(data)
        assert msg == Maps()
        # Should be enough to check every field is there without asserting the content.
        assert msg._unknown_fields is not None
        assert set(msg._unknown_fields.keys()) == set(range(1, 22))

    def test_delimited_encoding(self) -> None:
        w = BinaryWriter()
        w.tag(2, WireType.LENGTH_DELIMITED)
        w.uint32(0)
        w.tag(3, WireType.LENGTH_DELIMITED)
        w.uint32(0)
        w.tag(4, WireType.LENGTH_DELIMITED)  # Valid, explicitly length prefixed
        w.uint32(0)
        w.tag(5, WireType.LENGTH_DELIMITED)  # Valid, maps are never delimited
        w.fork()
        w.tag(2, WireType.LENGTH_DELIMITED)
        w.uint32(0)
        w.join()
        data = w.finish()
        msg = DelimitedEncoding.from_binary(data)
        assert msg == DelimitedEncoding(
            length_prefixed=DelimitedEncoding.Msg(),
            message_map={"": DelimitedEncoding.Msg()},
        )
        # Should be enough to check every field is there without asserting the content.
        assert msg._unknown_fields is not None
        assert {2, 3} == set(msg._unknown_fields.keys())
