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

from protobuf import Message, Oneof, message_to_json_value

from .gen.enums_pb import EnumMessage
from .gen.lists_pb import Lists
from .gen.maps_pb import Maps
from .gen.messages_pb import MixedFields
from .gen.oneofs_pb import Oneofs
from .gen.scalars_pb import Scalars

if TYPE_CHECKING:
    from re import Pattern


def _any(value: object) -> Any:
    return cast("Any", value)


@pytest.mark.parametrize(
    ("message", "match"),
    [
        pytest.param(Scalars(double_field=_any("x")), "float", id="double"),
        pytest.param(Scalars(float_field=_any("x")), "float", id="float"),
        pytest.param(Scalars(int32_field=_any("x")), "int", id="int32"),
        pytest.param(Scalars(int64_field=_any("x")), "int", id="int64"),
        pytest.param(Scalars(uint32_field=_any("x")), "int", id="uint32"),
        pytest.param(Scalars(uint64_field=_any("x")), "int", id="uint64"),
        pytest.param(Scalars(sint32_field=_any("x")), "int", id="sint32"),
        pytest.param(Scalars(sint64_field=_any("x")), "int", id="sint64"),
        pytest.param(Scalars(fixed32_field=_any("x")), "int", id="fixed32"),
        pytest.param(Scalars(fixed64_field=_any("x")), "int", id="fixed64"),
        pytest.param(Scalars(sfixed32_field=_any("x")), "int", id="sfixed32"),
        pytest.param(Scalars(sfixed64_field=_any("x")), "int", id="sfixed64"),
        pytest.param(Scalars(bool_field=_any(1)), "bool", id="bool"),
        pytest.param(Scalars(string_field=_any(123)), "str", id="string"),
        pytest.param(Scalars(bytes_field=_any("x")), "bytes", id="bytes"),
        pytest.param(Scalars(int32_field=_any(True)), "int", id="int_rejects_bool"),
        pytest.param(Scalars(bool_field=_any(0)), "bool", id="bool_rejects_int"),
        pytest.param(Lists(int32_list=_any((1, 2, 3))), "list", id="list"),
        pytest.param(Maps(int32_to_int32=_any([(0, 1), (1, 2)])), "dict", id="dict"),
    ],
)
def test_wrong_field_type(message: Message, match: str) -> None:
    _test_validation(message, TypeError, match=f"{match}")


@pytest.mark.parametrize(
    "message",
    [
        pytest.param(Scalars(int32_field=2**31), id="int32_overflow"),
        pytest.param(Scalars(uint32_field=-1), id="uint32_negative"),
        pytest.param(Scalars(int64_field=2**63), id="int64_overflow"),
        pytest.param(Scalars(uint64_field=-1), id="uint64_negative"),
        pytest.param(Scalars(float_field=3.4028234663852886e39), id="float_postive"),
        pytest.param(Scalars(float_field=-3.4028234663852886e39), id="float_nagative"),
    ],
)
def test_numeric_out_of_range(message: Message) -> None:
    _test_validation(message, OverflowError, match="out of range")


def test_wrong_message_type_singular() -> None:
    _test_validation(MixedFields(message_field=_any(Scalars())), TypeError)


def test_wrong_message_type_repeated() -> None:
    _test_validation(Lists(msg_list=_any([Scalars()])), TypeError)


def test_wrong_message_type_map_value() -> None:
    _test_validation(Maps(string_to_msg=_any({"key": Scalars()})), TypeError)


def test_not_a_message_in_message_field() -> None:
    _test_validation(MixedFields(message_field=_any("not_a_message")), TypeError)


def test_wrong_type_in_repeated_scalar() -> None:
    _test_validation(Lists(string_list=_any(["ok", 123])), TypeError)


def test_wrong_type_map_key() -> None:
    _test_validation(Maps(string_to_string=_any({123: "v"})), TypeError)


def test_wrong_type_map_value_scalar() -> None:
    _test_validation(Maps(string_to_string=_any({"a": 123})), TypeError)


def test_enum_wrong_type() -> None:
    _test_validation(EnumMessage(color_field=_any("RED")), TypeError)


def test_closed_enum_invalid_value() -> None:
    _test_validation(
        EnumMessage(closed_color_field=_any(99)),
        ValueError,
        match="invalid enum value 99 for enum",
    )


def test_oneof_wrong_type() -> None:
    _test_validation(
        Oneofs(scalars=_any(Oneof(field="string_field", value=123))), TypeError
    )


def test_oneof_invalid_value() -> None:
    _test_validation(Oneofs(scalars=_any("bad")), TypeError)


def test_oneof_unknown_field() -> None:
    _test_validation(
        Oneofs(scalars=_any(Oneof(field="nonexistent", value=123))),
        ValueError,
        match="unknown oneof field 'nonexistent'",
    )


def test_nested_message_validated() -> None:
    _test_validation(
        MixedFields(message_field=MixedFields.Bar(value=_any(123))), TypeError
    )


def _test_validation(
    msg: Message,
    expected_exception: type[Exception],
    *,
    match: str | Pattern[str] | None = None,
) -> None:
    with pytest.raises(expected_exception, match=match):
        msg.to_binary()
    with pytest.raises(expected_exception, match=match):
        msg.to_json()
    with pytest.raises(expected_exception, match=match):
        message_to_json_value(msg)
