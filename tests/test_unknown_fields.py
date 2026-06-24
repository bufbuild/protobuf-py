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

from protobuf import (
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescUnknownField,
    ScalarType,
)
from tests.gen.enums_pb import Color
from tests.gen.messages_pb import ExplicitFields, ExplicitFieldsWithUnknowns

desc_unknown_double_field = DescUnknownField(
    9990, DescFieldValueScalar(ScalarType.DOUBLE, default_value=0.0, oneof=None)
)
desc_unknown_enum_field = DescUnknownField(
    9991,
    DescFieldValueEnum(enum=Color.desc(), default_value=Color.UNSPECIFIED, oneof=None),
)
desc_unknown_repeated_field = DescUnknownField(
    9992,
    DescFieldValueList(
        element=ScalarType.STRING, packed=False, delimited_encoding=False
    ),
)
desc_unknown_map_field = DescUnknownField(
    9993, DescFieldValueMap(key=ScalarType.STRING, value=ScalarType.INT32)
)
desc_unknown_message_field = DescUnknownField(
    9994,
    DescFieldValueMessage(
        message=ExplicitFieldsWithUnknowns.Msg.desc(),
        delimited_encoding=False,
        oneof=None,
    ),
)

full_message = ExplicitFieldsWithUnknowns(
    int32_field=42,
    unknown_double_field=3.14,
    unknown_enum_field=Color.RED,
    unknown_repeated_field=["hello", "world"],
    unknown_map_field={"miles": 42},
    unknown_message_field=ExplicitFieldsWithUnknowns.Msg(value="hi"),
)


def test_unknown_fields_retained() -> None:
    msg = ExplicitFields.from_binary(full_message.to_binary())
    assert msg.int32_field == 42
    assert msg[desc_unknown_double_field] == 3.14
    assert msg[desc_unknown_enum_field] == Color.RED
    # If enum descriptor isn't available or a closed enum, can still access as an int
    assert (
        msg[
            DescUnknownField(
                9991,
                DescFieldValueScalar(ScalarType.INT32, default_value=0, oneof=None),
            )
        ]
        == 1
    )
    assert msg[desc_unknown_repeated_field] == ["hello", "world"]
    assert msg[desc_unknown_map_field] == {"miles": 42}
    assert msg[desc_unknown_message_field].value == "hi"

    recovered = ExplicitFieldsWithUnknowns.from_binary(msg.to_binary())
    assert recovered.int32_field == 42
    assert recovered.unknown_double_field == 3.14
    assert recovered.unknown_enum_field == Color.RED
    assert recovered.unknown_repeated_field == ["hello", "world"]
    assert recovered.unknown_map_field == {"miles": 42}
    assert recovered.unknown_message_field
    assert recovered.unknown_message_field.value == "hi"


def test_unknown_fields_dropped_on_write() -> None:
    msg = ExplicitFields.from_binary(full_message.to_binary())
    assert msg.int32_field == 42
    assert msg._unknown_fields
    msg = ExplicitFields.from_binary(msg.to_binary(write_unknown_fields=False))
    assert msg.int32_field == 42
    assert not msg._unknown_fields


def test_unknown_fields_dropped_on_read() -> None:
    msg = ExplicitFields.from_binary(
        full_message.to_binary(), ignore_unknown_fields=True
    )
    assert msg.int32_field == 42
    assert not msg._unknown_fields


def test_unknown_fields_access() -> None:
    msg = ExplicitFields()
    assert desc_unknown_double_field not in msg
    assert desc_unknown_enum_field not in msg
    assert desc_unknown_repeated_field not in msg
    assert desc_unknown_map_field not in msg
    assert desc_unknown_message_field not in msg

    msg[desc_unknown_double_field] = 2.718
    msg[desc_unknown_enum_field] = Color.GREEN
    msg[desc_unknown_repeated_field] = ["foo", "bar"]
    msg[desc_unknown_map_field] = {"key": 123}
    msg[desc_unknown_message_field] = ExplicitFieldsWithUnknowns.Msg(value="baz")

    assert msg[desc_unknown_double_field] == 2.718
    assert msg[desc_unknown_enum_field] == Color.GREEN
    assert msg[desc_unknown_repeated_field] == ["foo", "bar"]
    assert msg[desc_unknown_map_field] == {"key": 123}
    assert msg[desc_unknown_message_field].value == "baz"

    del msg[desc_unknown_double_field]
    del msg[desc_unknown_enum_field]
    del msg[desc_unknown_repeated_field]
    del msg[desc_unknown_map_field]
    del msg[desc_unknown_message_field]

    assert desc_unknown_double_field not in msg
    assert desc_unknown_enum_field not in msg
    assert desc_unknown_repeated_field not in msg
    assert desc_unknown_map_field not in msg
    assert desc_unknown_message_field not in msg
