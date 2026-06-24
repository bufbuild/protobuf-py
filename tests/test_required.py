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

import copy

import pytest

from protobuf import DescField, merge_from_binary, merge_from_json

from .gen.enums_pb import Color
from .gen.messages_pb import LegacyRequiredFields

ALL_FIELDS = LegacyRequiredFields.desc().fields


@pytest.fixture
def populated_message() -> LegacyRequiredFields:
    return LegacyRequiredFields(
        double_field=1.0,
        float_field=2.0,
        int32_field=3,
        int64_field=4,
        uint32_field=5,
        uint64_field=6,
        sint32_field=7,
        sint64_field=8,
        fixed32_field=9,
        fixed64_field=10,
        sfixed32_field=11,
        sfixed64_field=12,
        bool_field=True,
        string_field="hello",
        bytes_field=b"world",
        enum_field=Color.RED,
    )


@pytest.fixture
def zero_value_message() -> LegacyRequiredFields:
    return LegacyRequiredFields(
        double_field=0.0,
        float_field=0.0,
        int32_field=0,
        int64_field=0,
        uint32_field=0,
        uint64_field=0,
        sint32_field=0,
        sint64_field=0,
        fixed32_field=0,
        fixed64_field=0,
        sfixed32_field=0,
        sfixed64_field=0,
        bool_field=False,
        string_field="",
        bytes_field=b"",
        enum_field=Color.UNSPECIFIED,
    )


def test_to_binary_all_set(populated_message: LegacyRequiredFields) -> None:
    populated_message.to_binary()


def test_to_json_all_set(populated_message: LegacyRequiredFields) -> None:
    populated_message.to_json()


@pytest.mark.parametrize("field", ALL_FIELDS, ids=lambda f: f.name)
def test_to_binary_missing_required_field(
    populated_message: LegacyRequiredFields, field: DescField
) -> None:
    msg = copy.copy(populated_message)
    del msg[field]
    with pytest.raises(ValueError, match="required field not set"):
        msg.to_binary()


@pytest.mark.parametrize("field", ALL_FIELDS, ids=lambda f: f.name)
def test_to_json_missing_required_field(
    populated_message: LegacyRequiredFields, field: DescField
) -> None:
    msg = copy.copy(populated_message)
    del msg[field]
    with pytest.raises(ValueError, match="required field not set"):
        msg.to_json()


def test_to_binary_zero_values(zero_value_message: LegacyRequiredFields) -> None:
    zero_value_message.to_binary()


def test_to_json_zero_values(zero_value_message: LegacyRequiredFields) -> None:
    zero_value_message.to_json()


def test_from_binary_missing_required() -> None:
    LegacyRequiredFields.from_binary(b"")


def test_merge_from_binary_missing_required() -> None:
    msg = LegacyRequiredFields()
    merge_from_binary(msg, b"")


def test_from_json_missing_required() -> None:
    LegacyRequiredFields.from_json("{}")


def test_merge_from_json_missing_required() -> None:
    msg = LegacyRequiredFields()
    merge_from_json(msg, "{}")
