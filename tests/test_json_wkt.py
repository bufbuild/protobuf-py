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
from typing import Any

import pytest

from protobuf import Message, Oneof, Registry
from protobuf.wkt import (
    Any as AnyMsg,
    BoolValue,
    BytesValue,
    DoubleValue,
    Duration,
    FieldMask,
    FloatValue,
    Int32Value,
    Int64Value,
    ListValue,
    NullValue,
    StringValue,
    Struct,
    Timestamp,
    UInt32Value,
    UInt64Value,
    Value,
)
from tests.gen.scalars_pb import Scalars


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        (DoubleValue(value=1.5), 1.5),
        (FloatValue(value=1.5), 1.5),
        (Int32Value(value=42), 42),
        (Int64Value(value=42), "42"),
        (UInt32Value(value=42), 42),
        (UInt64Value(value=42), "42"),
        (BoolValue(value=True), True),
        (StringValue(value="hi"), "hi"),
        (BytesValue(value=b"\xab\xcd"), "q80="),
    ],
)
def test_wrappers(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        (DoubleValue(), 0.0),
        (FloatValue(), 0.0),
        (Int32Value(), 0),
        (Int64Value(), "0"),
        (UInt32Value(), 0),
        (UInt64Value(), "0"),
        (BoolValue(), False),
        (StringValue(), ""),
        (BytesValue(), ""),
    ],
)
def test_wrappers_zero(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected)


@pytest.mark.parametrize(
    ("seconds", "nanos", "expected"),
    [
        pytest.param(0, 0, "1970-01-01T00:00:00Z", id="zero"),
        pytest.param(
            1625079042, 123456789, "2021-06-30T18:50:42.123456789Z", id="with_nanos"
        ),
    ],
)
def test_timestamp(seconds: int, nanos: int, expected: str) -> None:
    _test_roundtrip(Timestamp(seconds=seconds, nanos=nanos), expected)


@pytest.mark.parametrize(
    ("json_str", "seconds", "nanos"),
    [
        pytest.param(
            "2025-01-27T11:42:15.689823456+01:00",
            1737974535,
            689823456,
            id="9 frac digits +offset",
        ),
        pytest.param(
            "2025-01-27T11:42:15.6898+01:00",
            1737974535,
            689800000,
            id="4 frac digits +offset",
        ),
        pytest.param(
            "2025-01-27T11:42:15.6+01:00",
            1737974535,
            600000000,
            id="1 frac digit +offset",
        ),
        pytest.param("2025-01-27T11:42:15.0+01:00", 1737974535, 0, id="0 frac +offset"),
        pytest.param("2025-01-27T11:42:15+01:00", 1737974535, 0, id="no frac +offset"),
        pytest.param(
            "2025-01-27T11:42:15.689823456Z",
            1737978135,
            689823456,
            id="9 frac digits Z",
        ),
        pytest.param(
            "2025-01-27T11:42:15.689800Z", 1737978135, 689800000, id="6 frac digits Z"
        ),
        pytest.param(
            "2025-01-27T11:42:15.6898Z", 1737978135, 689800000, id="4 frac digits Z"
        ),
        pytest.param(
            "2025-01-27T11:42:15.6Z", 1737978135, 600000000, id="1 frac digit Z"
        ),
        pytest.param("2025-01-27T11:42:15.0Z", 1737978135, 0, id="0 frac Z"),
        pytest.param("2025-01-27T11:42:15Z", 1737978135, 0, id="no frac Z"),
    ],
)
def test_timestamp_from_json(json_str: str, seconds: int, nanos: int) -> None:
    msg = Timestamp.from_json(json.dumps(json_str))
    assert msg.seconds == seconds
    assert msg.nanos == nanos


@pytest.mark.parametrize(
    ("seconds", "nanos", "expected"),
    [
        pytest.param(3, 0, "3s", id="3s"),
        pytest.param(3, 1000, "3.000001s", id="3s 1ms"),
        pytest.param(3, 1, "3.000000001s", id="3s 1ns"),
        pytest.param(-3, -1, "-3.000000001s", id="-3s 1ns"),
        pytest.param(0, 5, "0.000000005s", id="0s 5ns"),
        pytest.param(0, -5, "-0.000000005s", id="0s -5ns"),
        pytest.param(0, 0, "0s", id="0s 0ns"),
    ],
)
def test_duration(seconds: int, nanos: int, expected: str) -> None:
    _test_roundtrip(Duration(seconds=seconds, nanos=nanos), expected)


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        pytest.param(
            ["user.display_name", "photo"], "user.displayName,photo", id="with_paths"
        ),
        pytest.param([], "", id="empty"),
    ],
)
def test_field_mask(paths: list[str], expected: str) -> None:
    _test_roundtrip(FieldMask(paths=paths), expected)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            Struct(
                fields={
                    "a": Value(kind=Oneof(field="number_value", value=123)),
                    "b": Value(kind=Oneof(field="string_value", value="abc")),
                }
            ),
            {"a": 123, "b": "abc"},
            id="with_fields",
        ),
        pytest.param(Struct(), {}, id="empty"),
    ],
)
def test_struct(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            Value(kind=Oneof(field="bool_value", value=True)), True, id="bool_value"
        ),
        pytest.param(
            Value(kind=Oneof(field="number_value", value=42.0)), 42.0, id="number_value"
        ),
        pytest.param(
            Value(kind=Oneof(field="string_value", value="hello")),
            "hello",
            id="string_value",
        ),
        pytest.param(
            Value(kind=Oneof(field="null_value", value=NullValue.NULL_VALUE)),
            None,
            id="null_value",
        ),
        pytest.param(
            Value(
                kind=Oneof(
                    field="struct_value",
                    value=Struct(
                        fields={"foo": Value(kind=Oneof(field="number_value", value=1))}
                    ),
                )
            ),
            {"foo": 1},
            id="struct_value",
        ),
        pytest.param(
            Value(
                kind=Oneof(
                    field="list_value",
                    value=ListValue(
                        values=[
                            Value(kind=Oneof(field="number_value", value=1)),
                            Value(kind=Oneof(field="string_value", value="two")),
                        ]
                    ),
                )
            ),
            [1, "two"],
            id="list_value",
        ),
    ],
)
def test_value(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            ListValue(
                values=[
                    Value(kind=Oneof(field="number_value", value=1)),
                    Value(kind=Oneof(field="string_value", value="two")),
                    Value(kind=Oneof(field="bool_value", value=False)),
                ]
            ),
            [1, "two", False],
            id="with_values",
        ),
        pytest.param(ListValue(), [], id="empty"),
    ],
)
def test_list_value(message: Message, expected: Any) -> None:
    _test_roundtrip(message, expected)


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        pytest.param(
            Scalars(int32_field=42, string_field="hello"),
            {
                "@type": "type.googleapis.com/Scalars",
                "int32Field": 42,
                "stringField": "hello",
            },
            id="Scalars",
        ),
        pytest.param(
            Timestamp(seconds=1625079042, nanos=123456789),
            {
                "@type": "type.googleapis.com/google.protobuf.Timestamp",
                "value": "2021-06-30T18:50:42.123456789Z",
            },
            id="Timestamp",
        ),
        pytest.param(
            Duration(seconds=1, nanos=212000000),
            {
                "@type": "type.googleapis.com/google.protobuf.Duration",
                "value": "1.212s",
            },
            id="Duration",
        ),
        pytest.param(
            Struct(
                fields={"key": Value(kind=Oneof(field="string_value", value="val"))}
            ),
            {
                "@type": "type.googleapis.com/google.protobuf.Struct",
                "value": {"key": "val"},
            },
            id="Struct",
        ),
        pytest.param(
            BoolValue(value=True),
            {"@type": "type.googleapis.com/google.protobuf.BoolValue", "value": True},
            id="BoolValue",
        ),
    ],
)
def test_any(message: Message, expected: dict[str, Any]) -> None:
    registry = Registry(type(message))
    any_msg = AnyMsg.pack(message)
    json_str = any_msg.to_json(registry=registry)
    assert json.loads(json_str) == expected

    roundtripped = AnyMsg.from_json(json_str, registry=registry)
    assert roundtripped == any_msg


def test_any_empty() -> None:
    _test_roundtrip(AnyMsg(), {})


def test_any_no_registry() -> None:
    any_msg = AnyMsg.pack(Scalars(int32_field=1))
    with pytest.raises(ValueError, match="is not in the type registry"):
        any_msg.to_json()


def test_any_type_not_in_registry() -> None:
    any_msg = AnyMsg.pack(Scalars(int32_field=1))
    with pytest.raises(ValueError, match="is not in the type registry"):
        any_msg.to_json(registry=Registry())


@pytest.mark.parametrize(
    ("seconds", "nanos", "match"),
    [
        (315_576_000_001, 0, "duration seconds out of range"),
        (-315_576_000_001, 0, "duration seconds out of range"),
        (-1, 1, "duration seconds and nanos have different signs"),
        (1, -1, "duration seconds and nanos have different signs"),
        (0, 1_000_000_000, "duration nanos out of range"),
    ],
)
def test_duration_to_json_error(seconds: int, nanos: int, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        Duration(seconds=seconds, nanos=nanos).to_json()


@pytest.mark.parametrize(
    ("json_str", "error_type"),
    [("123", TypeError), ('"3.5"', ValueError), ('"315576000001s"', ValueError)],
)
def test_duration_from_json_error(json_str: str, error_type: type[Exception]) -> None:
    with pytest.raises(error_type, match="cannot decode"):
        Duration.from_json(json_str)


@pytest.mark.parametrize(
    ("seconds", "nanos", "match"),
    [
        (315_576_000_001, 0, "timestamp seconds out of range"),
        (-315_576_000_001, 0, "timestamp seconds out of range"),
        (5000, 1_000_000_000, "timestamp nanos out of range"),
    ],
)
def test_timestamp_to_json_error(seconds: int, nanos: int, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        Timestamp(seconds=seconds, nanos=nanos).to_json()


@pytest.mark.parametrize(
    ("json_str", "error_type", "match"),
    [
        ("123", TypeError, "cannot decode"),
        ('"not-a-timestamp"', ValueError, "invalid RFC 3339"),
        ('"2025-01-27t11:42:15Z"', ValueError, "invalid RFC 3339"),
        ('"2025-01-27 11:42:15Z"', ValueError, "invalid RFC 3339"),
        ('"2025-13-01T00:00:00Z"', ValueError, "invalid RFC 3339"),
    ],
)
def test_timestamp_from_json_error(
    json_str: str, error_type: type[Exception], match: str
) -> None:
    with pytest.raises(error_type, match=match):
        Timestamp.from_json(json_str)


def test_field_mask_to_json_irreversible() -> None:
    with pytest.raises(ValueError, match="irreversible"):
        FieldMask(paths=["user.displayName"]).to_json()


@pytest.mark.parametrize(
    ("json_str", "error_type", "match"),
    [
        ("123", TypeError, "cannot decode"),
        ('"user.display_name,photo"', ValueError, "path names must be lowerCamelCase"),
    ],
)
def test_field_mask_from_json_error(
    json_str: str, error_type: type[Exception], match: str
) -> None:
    with pytest.raises(error_type, match=match):
        FieldMask.from_json(json_str)


@pytest.mark.parametrize(
    ("message", "match"),
    [
        (Value(), "value must have exactly one field set"),
        (
            Value(kind=Oneof(field="number_value", value=float("nan"))),
            "value cannot be NaN or Infinity",
        ),
        (
            Value(kind=Oneof(field="number_value", value=float("inf"))),
            "value cannot be NaN or Infinity",
        ),
        (
            Value(kind=Oneof(field="number_value", value=float("-inf"))),
            "value cannot be NaN or Infinity",
        ),
    ],
)
def test_value_to_json_error(message: Message, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        message.to_json()


@pytest.mark.parametrize("json_str", ['"abc"', "[1, 2]"])
def test_struct_from_json_error(json_str: str) -> None:
    with pytest.raises(TypeError, match="cannot decode"):
        Struct.from_json(json_str)


@pytest.mark.parametrize("json_str", ['"abc"', '{"a": 1}'])
def test_list_value_from_json_error(json_str: str) -> None:
    with pytest.raises(TypeError, match="cannot decode"):
        ListValue.from_json(json_str)


@pytest.mark.parametrize(
    ("json_str", "error_type", "match"),
    [
        ('{"value": 123}', ValueError, r"@type is invalid"),
        ('{"@type": ""}', ValueError, r"@type is invalid"),
        ('{"@type": "/"}', ValueError, "is not in the type registry"),
        (
            '{"@type": "type.googleapis.com/Unknown"}',
            ValueError,
            "is not in the type registry",
        ),
        ('"abc"', TypeError, "cannot decode"),
    ],
)
def test_any_from_json_error(
    json_str: str, error_type: type[Exception], match: str
) -> None:
    with pytest.raises(error_type, match=match):
        AnyMsg.from_json(json_str, registry=Registry(Scalars))


def _test_roundtrip(message: Message, expected: Any) -> None:
    json_str = message.to_json()
    assert json.loads(json_str) == expected

    roundtripped = type(message).from_json(json_str)
    assert roundtripped == message
