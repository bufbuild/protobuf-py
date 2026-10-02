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

# ty: ignore[deprecated]

from __future__ import annotations

import warnings

from protobuf import Enum
from tests.gen.deprecated_pb import (
    DeprecatedEnum,
    DeprecatedMessage,
    EnumWithDeprecatedValue,
    MessageWithDeprecatedFields,
)


def test_deprecated_message() -> None:
    assert DeprecatedMessage.__dict__["__deprecated__"] == (
        "deprecated.DeprecatedMessage is deprecated."
    )
    assert DeprecatedMessage.NestedDeprecatedMessage.__dict__["__deprecated__"] == (
        "deprecated.DeprecatedMessage.NestedDeprecatedMessage is deprecated."
    )
    assert not hasattr(MessageWithDeprecatedFields, "__deprecated__")


def test_deprecated_enum() -> None:
    assert (
        DeprecatedEnum.__dict__["__deprecated__"]
        == "deprecated.DeprecatedEnum is deprecated."
    )


def test_deprecated_enum_value() -> None:
    # The deprecated member is only hidden from type checkers.
    assert list(EnumWithDeprecatedValue) == [
        EnumWithDeprecatedValue.UNSPECIFIED,
        EnumWithDeprecatedValue.OLD,
        EnumWithDeprecatedValue.NEW,
    ]
    assert EnumWithDeprecatedValue(1) is EnumWithDeprecatedValue.OLD
    assert type(EnumWithDeprecatedValue) is type(Enum)
    assert MessageWithDeprecatedFields.NestedEnum.OLD.value == 1


def test_deprecated_fields() -> None:
    assert MessageWithDeprecatedFields.__slots__ == (
        "message",
        "enum",
        "deprecated_field",
        "deprecated_list",
        "deprecated_map",
        "deprecated_message",
        "value",
        "deprecated",
        "property",
        "overload",
        "choice",
    )
    msg = MessageWithDeprecatedFields(
        deprecated_field=1,
        deprecated_list=[2],
        deprecated_map={"a": 3},
        deprecated=True,
        property=True,
        overload=True,
    )
    msg.deprecated_message = MessageWithDeprecatedFields(value=4)
    assert msg.deprecated_field == 1
    assert msg.deprecated_list == [2]
    assert msg.deprecated_map == {"a": 3}
    assert msg.deprecated_message.value == 4
    assert msg.deprecated
    assert msg.property
    assert msg.overload


def test_no_runtime_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        msg = MessageWithDeprecatedFields(
            message=DeprecatedMessage(value=1),
            enum=DeprecatedEnum.UNSPECIFIED,
            deprecated_field=2,
        )
        msg.deprecated_field = msg.deprecated_field + 1
        DeprecatedMessage.NestedDeprecatedMessage()
        MessageWithDeprecatedFields.NestedDeprecatedMessage()
        _ = EnumWithDeprecatedValue.OLD
        parsed = MessageWithDeprecatedFields.from_binary(msg.to_binary())
    assert parsed == msg
