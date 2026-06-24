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

import json
from typing import Any, cast

import pytest

from protobuf import (
    Message,
    Oneof,
    Registry,
    message_from_json_value,
    message_to_json_value,
)

from .gen.enums_pb import ClosedColor, Color, EnumMessage
from .gen.json_names_pb import JsonNames
from .gen.lists_pb import Lists
from .gen.maps_pb import Maps
from .gen.messages_pb import ExplicitFields, ImplicitFields, MixedFields
from .gen.oneofs_pb import Oneofs
from .gen.scalars_pb import Scalars


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            Scalars(
                double_field=1.5,
                float_field=2.5,
                int32_field=42,
                int64_field=123456789,
                uint32_field=100,
                uint64_field=9876543210,
                sint32_field=-7,
                sint64_field=-999,
                fixed32_field=300,
                fixed64_field=400,
                sfixed32_field=-50,
                sfixed64_field=-60,
                bool_field=True,
                string_field="hello",
                bytes_field=b"test",
            ),
            {
                "doubleField": 1.5,
                "floatField": 2.5,
                "int32Field": 42,
                "int64Field": "123456789",
                "uint32Field": 100,
                "uint64Field": "9876543210",
                "sint32Field": -7,
                "sint64Field": "-999",
                "fixed32Field": 300,
                "fixed64Field": "400",
                "sfixed32Field": -50,
                "sfixed64Field": "-60",
                "boolField": True,
                "stringField": "hello",
                "bytesField": "dGVzdA==",
            },
            id="Scalars",
        ),
        pytest.param(
            EnumMessage(
                color_field=Color.GREEN,
                closed_color_field=ClosedColor.RED,
                color_list=[Color.RED, Color.BLUE, Color(99)],
                closed_color_list=[ClosedColor.GREEN, ClosedColor.BLUE],
                string_to_color={"x": Color.GREEN},
                string_to_closed_color={"y": ClosedColor.RED},
            ),
            {
                "colorField": "COLOR_GREEN",
                "closedColorField": "CLOSED_COLOR_RED",
                "colorList": ["COLOR_RED", "COLOR_BLUE", 99],
                "closedColorList": ["CLOSED_COLOR_GREEN", "CLOSED_COLOR_BLUE"],
                "stringToColor": {"x": "COLOR_GREEN"},
                "stringToClosedColor": {"y": "CLOSED_COLOR_RED"},
            },
            id="EnumMessage",
        ),
        pytest.param(
            Lists(
                double_list=[1.5, 2.5],
                float_list=[3.5, 4.5],
                int32_list=[1, -2],
                int64_list=[3, -4],
                uint32_list=[5, 6],
                uint64_list=[7, 8],
                sint32_list=[-9, 10],
                sint64_list=[-11, 12],
                fixed32_list=[13, 14],
                fixed64_list=[15, 16],
                sfixed32_list=[-17, 18],
                sfixed64_list=[-19, 20],
                bool_list=[True, False],
                string_list=["a", "b"],
                bytes_list=[b"x", b"y"],
                enum_list=[Color.RED, Color.GREEN],
                msg_list=[Lists.Msg(value="one")],
                recursive_list=[Lists(int32_list=[99])],
            ),
            {
                "doubleList": [1.5, 2.5],
                "floatList": [3.5, 4.5],
                "int32List": [1, -2],
                "int64List": ["3", "-4"],
                "uint32List": [5, 6],
                "uint64List": ["7", "8"],
                "sint32List": [-9, 10],
                "sint64List": ["-11", "12"],
                "fixed32List": [13, 14],
                "fixed64List": ["15", "16"],
                "sfixed32List": [-17, 18],
                "sfixed64List": ["-19", "20"],
                "boolList": [True, False],
                "stringList": ["a", "b"],
                "bytesList": ["eA==", "eQ=="],
                "enumList": ["COLOR_RED", "COLOR_GREEN"],
                "msgList": [{"value": "one"}],
                "recursiveList": [{"int32List": [99]}],
            },
            id="Lists",
        ),
        pytest.param(
            Maps(
                int32_to_int32={1: 2},
                int64_to_int64={3: 4},
                uint32_to_uint32={5: 6},
                uint64_to_uint64={7: 8},
                sint32_to_sint32={-1: -2},
                sint64_to_sint64={-3: -4},
                fixed32_to_fixed32={9: 10},
                fixed64_to_fixed64={11: 12},
                sfixed32_to_sfixed32={-5: -6},
                sfixed64_to_sfixed64={-7: -8},
                bool_to_bool={True: False},
                string_to_string={"k": "v"},
                string_to_float={"f": 1.5},
                string_to_double={"d": 2.5},
                string_to_bytes={"b": b"hi"},
                string_to_enum={"e": Color.RED},
                string_to_msg={"m": Maps.Msg(value="nested")},
                int32_to_enum={1: Color.GREEN},
                int32_to_msg={2: Maps.Msg(value="by_int")},
                bool_to_msg={True: Maps.Msg(value="by_bool")},
                string_to_recursive={"r": Maps(string_to_string={"inner": "value"})},
            ),
            {
                "int32ToInt32": {"1": 2},
                "int64ToInt64": {"3": "4"},
                "uint32ToUint32": {"5": 6},
                "uint64ToUint64": {"7": "8"},
                "sint32ToSint32": {"-1": -2},
                "sint64ToSint64": {"-3": "-4"},
                "fixed32ToFixed32": {"9": 10},
                "fixed64ToFixed64": {"11": "12"},
                "sfixed32ToSfixed32": {"-5": -6},
                "sfixed64ToSfixed64": {"-7": "-8"},
                "boolToBool": {"true": False},
                "stringToString": {"k": "v"},
                "stringToFloat": {"f": 1.5},
                "stringToDouble": {"d": 2.5},
                "stringToBytes": {"b": "aGk="},
                "stringToEnum": {"e": "COLOR_RED"},
                "stringToMsg": {"m": {"value": "nested"}},
                "int32ToEnum": {"1": "COLOR_GREEN"},
                "int32ToMsg": {"2": {"value": "by_int"}},
                "boolToMsg": {"true": {"value": "by_bool"}},
                "stringToRecursive": {"r": {"stringToString": {"inner": "value"}}},
            },
            id="Maps",
        ),
        pytest.param(
            ExplicitFields(
                double_field=1.5,
                float_field=2.5,
                int32_field=42,
                int64_field=100,
                uint32_field=200,
                uint64_field=300,
                sint32_field=-10,
                sint64_field=-20,
                fixed32_field=400,
                fixed64_field=500,
                sfixed32_field=-30,
                sfixed64_field=-40,
                bool_field=True,
                string_field="hello",
                bytes_field=b"world",
                enum_field=Color.BLUE,
                message_field=ExplicitFields.Msg(value="nested"),
                oneof_group=Oneof(field="oneof_string", value="picked"),
            ),
            {
                "doubleField": 1.5,
                "floatField": 2.5,
                "int32Field": 42,
                "int64Field": "100",
                "uint32Field": 200,
                "uint64Field": "300",
                "sint32Field": -10,
                "sint64Field": "-20",
                "fixed32Field": 400,
                "fixed64Field": "500",
                "sfixed32Field": -30,
                "sfixed64Field": "-40",
                "boolField": True,
                "stringField": "hello",
                "bytesField": "d29ybGQ=",
                "enumField": "COLOR_BLUE",
                "messageField": {"value": "nested"},
                "oneofString": "picked",
            },
            id="ExplicitFields",
        ),
        pytest.param(
            ImplicitFields(
                double_field=1.5,
                float_field=2.5,
                int32_field=42,
                int64_field=100,
                uint32_field=200,
                uint64_field=300,
                sint32_field=-10,
                sint64_field=-20,
                fixed32_field=400,
                fixed64_field=500,
                sfixed32_field=-30,
                sfixed64_field=-40,
                bool_field=True,
                string_field="hello",
                bytes_field=b"world",
                enum_field=Color.RED,
                repeated_field=["a", "b"],
                map_field={"k": 1},
            ),
            {
                "doubleField": 1.5,
                "floatField": 2.5,
                "int32Field": 42,
                "int64Field": "100",
                "uint32Field": 200,
                "uint64Field": "300",
                "sint32Field": -10,
                "sint64Field": "-20",
                "fixed32Field": 400,
                "fixed64Field": "500",
                "sfixed32Field": -30,
                "sfixed64Field": "-40",
                "boolField": True,
                "stringField": "hello",
                "bytesField": "d29ybGQ=",
                "enumField": "COLOR_RED",
                "repeatedField": ["a", "b"],
                "mapField": {"k": 1},
            },
            id="ImplicitFields",
        ),
        pytest.param(
            MixedFields(
                explicit_field=1,
                implicit_field=2,
                repeated_field=["a"],
                message_field=MixedFields.Bar(value="bar"),
                field_with_default=99,
                map_field={"k": 42},
                oneof_group=Oneof(field="oneof_field", value="choice"),
                implicit_enum_field=MixedFields.E.ONE,
                explicit_enum_field=MixedFields.E.TWO,
            ),
            {
                "explicitField": 1,
                "implicitField": 2,
                "repeatedField": ["a"],
                "messageField": {"value": "bar"},
                "fieldWithDefault": 99,
                "mapField": {"k": 42},
                "oneofField": "choice",
                "implicitEnumField": "ONE",
                "explicitEnumField": "TWO",
            },
            id="MixedFields",
        ),
        pytest.param(
            Oneofs(
                scalars=Oneof(field="string_field", value="hello"),
                single=Oneof(field="only_field", value="only"),
                mixed=Oneof(field="msg_field", value=Oneofs.Msg(value="nested")),
            ),
            {
                "stringField": "hello",
                "onlyField": "only",
                "msgField": {"value": "nested"},
            },
            id="Oneofs",
        ),
        pytest.param(
            JsonNames(
                scalar_field=42,
                repeated_field=["a", "b"],
                map_field={"x": 1},
                enum_field=Color.RED,
                msg_field=JsonNames.Msg(value="hi"),
                value=Oneof(field="oneof_string", value="hello"),
            ),
            {
                "scalarFieldJsonName": 42,
                "repeatedFieldJsonName": ["a", "b"],
                "mapFieldJsonName": {"x": 1},
                "enumFieldJsonName": "COLOR_RED",
                "msgFieldJsonName": {"value": "hi"},
                "oneofStringJsonName": "hello",
            },
            id="JsonNames",
        ),
    ],
)
def test_json(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            ImplicitFields(),
            {
                "doubleField": 0.0,
                "floatField": 0.0,
                "int32Field": 0,
                "int64Field": "0",
                "uint32Field": 0,
                "uint64Field": "0",
                "sint32Field": 0,
                "sint64Field": "0",
                "fixed32Field": 0,
                "fixed64Field": "0",
                "sfixed32Field": 0,
                "sfixed64Field": "0",
                "boolField": False,
                "stringField": "",
                "bytesField": "",
                "enumField": "COLOR_UNSPECIFIED",
                "repeatedField": [],
                "mapField": {},
            },
            id="ImplicitFields",
        ),
        pytest.param(ExplicitFields(), {}, id="ExplicitFields"),
    ],
)
def test_always_emit_implicit(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected, always_emit_implicit=True)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            EnumMessage(
                color_field=Color.GREEN,
                color_list=[Color.RED, Color.GREEN],
                string_to_color={"a": Color.RED, "b": Color.GREEN},
            ),
            {"colorField": 2, "colorList": [1, 2], "stringToColor": {"a": 1, "b": 2}},
            id="known_values",
        ),
        pytest.param(
            EnumMessage(color_field=Color(99)), {"colorField": 99}, id="unknown_value"
        ),
    ],
)
def test_print_enums_as_ints(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected, print_enums_as_ints=True)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            JsonNames(
                scalar_field=42,
                repeated_field=["a", "b"],
                map_field={"x": 1},
                enum_field=Color.RED,
                msg_field=JsonNames.Msg(value="hi"),
                value=Oneof(field="oneof_string", value="hello"),
            ),
            {
                "scalar_field": 42,
                "repeated_field": ["a", "b"],
                "map_field": {"x": 1},
                "enum_field": "COLOR_RED",
                "msg_field": {"value": "hi"},
                "oneof_string": "hello",
            },
            id="JsonNames",
        ),
        pytest.param(
            MixedFields(
                explicit_field=1,
                repeated_field=["a"],
                message_field=MixedFields.Bar(value="bar"),
                map_field={"k": 42},
                oneof_group=Oneof(field="oneof_field", value="choice"),
            ),
            {
                "explicit_field": 1,
                "repeated_field": ["a"],
                "message_field": {"value": "bar"},
                "map_field": {"k": 42},
                "oneof_field": "choice",
            },
            id="MixedFields",
        ),
    ],
)
def test_use_proto_field_name(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected, use_proto_field_name=True)


@pytest.mark.parametrize(
    "json_str",
    [
        pytest.param("+/8=", id="std/padded"),
        pytest.param("+/8", id="std/unpadded"),
        pytest.param("-_8=", id="url/padded"),
        pytest.param("-_8", id="url/unpadded"),
    ],
)
def test_bytes_from_json(json_str: str) -> None:
    msg = Scalars.from_json(json.dumps({"bytesField": json_str}))
    assert msg.bytes_field == b"\xfb\xff"


def test_from_json_unknown_field() -> None:
    with pytest.raises(ValueError, match="is unknown"):
        Scalars.from_json(json.dumps({"notAKnownField": "abc"}))


def test_from_json_ignore_unknown_fields() -> None:
    msg = Scalars.from_json(
        json.dumps({"notAKnownField": "abc"}), ignore_unknown_fields=True
    )
    assert msg == Scalars()


# Range and overflow errors (e.g. int32 too large, float32 overflow) are
# covered by the conformance suite. These cases focus on type mismatches
# and parse failures.
@pytest.mark.parametrize(
    ("json_obj", "exc_type", "match"),
    [
        ({"doubleField": ""}, ValueError, "invalid float/double value"),
        (
            {"doubleField": "-1.89769e+308"},
            ValueError,
            "unexpected infinite/NaN number",
        ),
        ({"bytesField": "not base 64"}, ValueError, "invalid base64 data"),
        ({"int32Field": "abc"}, ValueError, "invalid integer value"),
        ({"int32Field": True}, TypeError, "unexpected json type"),
        ({"int32Field": {}}, TypeError, "unexpected json type"),
        ({"int32Field": []}, TypeError, "unexpected json type"),
    ],
)
def test_from_json_singular_scalar_error(
    json_obj: dict[str, Any], exc_type: type[Exception], match: str | None
) -> None:
    with pytest.raises(exc_type, match=match):
        Scalars.from_json(json.dumps(json_obj))


@pytest.mark.parametrize(
    ("json_obj", "exc_type", "match"),
    [
        ({"int32List": "abc"}, TypeError, "expected list got"),
        ({"int32List": 123}, TypeError, "expected list got"),
        ({"int32List": True}, TypeError, "expected list got"),
        ({"int32List": {"x": 1}}, TypeError, "expected list got"),
        ({"int32List": [1, None]}, ValueError, "unexpected null value for list item"),
        ({"int32List": ["abc"]}, ValueError, "invalid integer value"),
        ({"int32List": [True]}, TypeError, "unexpected json type"),
        ({"int32List": [{}]}, TypeError, "unexpected json type"),
        ({"int32List": [[]]}, TypeError, "unexpected json type"),
    ],
)
def test_from_json_repeated_scalar_error(
    json_obj: dict[str, Any], exc_type: type[Exception], match: str
) -> None:
    with pytest.raises(exc_type, match=match):
        Lists.from_json(json.dumps(json_obj))


@pytest.mark.parametrize("value", [True, "NONEXISTENT", {}, []])
def test_from_json_singular_enum_error(value: Any) -> None:
    with pytest.raises(ValueError, match="cannot decode"):
        EnumMessage.from_json(json.dumps({"colorField": value}))


@pytest.mark.parametrize(
    ("json_obj", "exc_type", "match"),
    [
        ({"colorList": "abc"}, TypeError, "expected list got"),
        ({"colorList": 123}, TypeError, "expected list got"),
        ({"colorList": True}, TypeError, "expected list got"),
        ({"colorList": {}}, TypeError, "expected list got"),
        ({"colorList": [1, None]}, ValueError, "unexpected null value"),
        ({"colorList": [True]}, ValueError, "cannot decode"),
        ({"colorList": ["NONEXISTENT"]}, ValueError, "cannot decode"),
        ({"colorList": [{}]}, ValueError, "cannot decode"),
        ({"colorList": [[]]}, ValueError, "cannot decode"),
    ],
)
def test_from_json_repeated_enum_error(
    json_obj: dict[str, Any], exc_type: type[Exception], match: str
) -> None:
    with pytest.raises(exc_type, match=match):
        EnumMessage.from_json(json.dumps(json_obj))


@pytest.mark.parametrize("value", ["abc", [], True, 123])
def test_from_json_singular_message_error(value: Any) -> None:
    with pytest.raises(TypeError, match="cannot decode"):
        ExplicitFields.from_json(json.dumps({"messageField": value}))


def test_from_json_singular_message_nested_error() -> None:
    with pytest.raises(TypeError, match="expected string got"):
        ExplicitFields.from_json(json.dumps({"messageField": {"value": 123}}))


@pytest.mark.parametrize(
    ("json_obj", "exc_type", "match"),
    [
        ({"msgList": "abc"}, TypeError, "expected list got"),
        ({"msgList": 123}, TypeError, "expected list got"),
        ({"msgList": {}}, TypeError, "expected list got"),
        ({"msgList": [None]}, ValueError, "unexpected null value"),
        ({"msgList": [{"value": 123}]}, TypeError, "expected string got"),
    ],
)
def test_from_json_repeated_message_error(
    json_obj: dict[str, Any], exc_type: type[Exception], match: str
) -> None:
    with pytest.raises(exc_type, match=match):
        Lists.from_json(json.dumps(json_obj))


@pytest.mark.parametrize(
    ("json_obj", "exc_type", "match"),
    [
        ({"int32ToInt32": "abc"}, TypeError, "expected dict got"),
        ({"int32ToInt32": []}, TypeError, "expected dict got"),
        ({"int32ToInt32": 123}, TypeError, "expected dict got"),
        ({"int32ToInt32": True}, TypeError, "expected dict got"),
        (
            {"int32ToInt32": {"123": None}},
            ValueError,
            "unexpected null value for map value",
        ),
        ({"int32ToInt32": {"not-an-int32": 123}}, ValueError, "invalid integer value"),
        (
            {"int32ToInt32": {"123": "not-an-int32"}},
            ValueError,
            "invalid integer value",
        ),
    ],
)
def test_from_json_map_error(
    json_obj: dict[str, Any], exc_type: type[Exception], match: str
) -> None:
    with pytest.raises(exc_type, match=match):
        Maps.from_json(json.dumps(json_obj))


def test_from_json_oneof_set_multiple_times() -> None:
    with pytest.raises(ValueError, match="oneof set multiple times"):
        MixedFields.from_json(json.dumps({"oneofField": "a", "oneofBaz": 1}))


def _test_roundtrip(
    message: Message,
    expected: Any,
    /,
    *,
    registry: Registry | None = None,
    always_emit_implicit: bool = False,
    print_enums_as_ints: bool = False,
    use_proto_field_name: bool = False,
    ignore_unknown_fields: bool = False,
) -> None:
    json_str = message.to_json(
        registry=registry,
        always_emit_implicit=always_emit_implicit,
        print_enums_as_ints=print_enums_as_ints,
        use_proto_field_name=use_proto_field_name,
    )
    assert json.loads(json_str) == expected

    roundtripped = type(message).from_json(
        json_str, registry=registry, ignore_unknown_fields=ignore_unknown_fields
    )
    assert roundtripped == message

    json_value = message_to_json_value(
        message,
        registry=registry,
        always_emit_implicit=always_emit_implicit,
        print_enums_as_ints=print_enums_as_ints,
        use_proto_field_name=use_proto_field_name,
    )
    assert json_value == expected

    decoded = message_from_json_value(type(message), json_value, registry=registry)
    assert decoded == message


def test_closed_enum_to_json() -> None:
    msg = EnumMessage(closed_color_field=cast("Any", 99))
    with pytest.raises(ValueError, match="invalid enum value 99 for enum ClosedColor"):
        msg.to_json()


def test_closed_enum_from_json() -> None:
    with pytest.raises(ValueError, match="`99` is not a valid ClosedColor"):
        EnumMessage.from_json(json.dumps({"closedColorField": 99}))


def test_closed_enum_from_json_ignoring_unknown_fields() -> None:
    msg = EnumMessage.from_json(
        json.dumps({"closedColorField": 99}), ignore_unknown_fields=True
    )
    assert msg.closed_color_field == ClosedColor.UNSPECIFIED
