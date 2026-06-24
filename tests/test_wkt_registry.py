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

from protobuf._wkt_registry import (
    WktAny,
    WktDuration,
    WktFieldMask,
    WktListValue,
    WktStruct,
    WktTimestamp,
    WktValue,
    WktWrapper,
    is_null_value_enum,
    is_wkt_value,
    match_wkt,
)
from protobuf.wkt import (
    Any,
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

from .gen.scalars_pb import Scalars

if TYPE_CHECKING:
    from protobuf import Message


class TestMatchWkt:
    def test_timestamp(self) -> None:
        assert isinstance(match_wkt(Timestamp._desc), WktTimestamp)

    def test_duration(self) -> None:
        assert isinstance(match_wkt(Duration._desc), WktDuration)

    def test_any(self) -> None:
        assert isinstance(match_wkt(Any._desc), WktAny)

    def test_field_mask(self) -> None:
        assert isinstance(match_wkt(FieldMask._desc), WktFieldMask)

    def test_struct(self) -> None:
        wkt = match_wkt(Struct._desc)
        assert isinstance(wkt, WktStruct)

    def test_list_value(self) -> None:
        wkt = match_wkt(ListValue._desc)
        assert isinstance(wkt, WktListValue)

    def test_value(self) -> None:
        wkt = match_wkt(Value._desc)
        assert isinstance(wkt, WktValue)

    @pytest.mark.parametrize(
        "msg_type",
        [
            DoubleValue,
            FloatValue,
            Int32Value,
            Int64Value,
            UInt32Value,
            UInt64Value,
            BoolValue,
            StringValue,
            BytesValue,
        ],
    )
    def test_wrapper(self, msg_type: type[Message]) -> None:
        wkt = match_wkt(msg_type._desc)
        assert isinstance(wkt, WktWrapper)

    def test_non_wkt_returns_none(self) -> None:
        assert match_wkt(Scalars._desc) is None


class TestIsWktValue:
    def test_value_desc(self) -> None:
        assert is_wkt_value(Value._desc) is True

    def test_non_value_wkt(self) -> None:
        assert is_wkt_value(Timestamp._desc) is False

    def test_non_wkt(self) -> None:
        assert is_wkt_value(Scalars._desc) is False


class TestIsNullValueEnum:
    def test_null_value_desc(self) -> None:
        assert is_null_value_enum(NullValue._desc) is True

    def test_non_null_value_enum(self) -> None:
        from .gen.enums_pb import Color  # noqa: PLC0415

        assert is_null_value_enum(Color._desc) is False
