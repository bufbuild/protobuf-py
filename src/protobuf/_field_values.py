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

from math import copysign
from typing import Any

from ._descriptors import (
    DescField,
    DescFieldValue,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescFieldValueSingular,
    DescOneof,
    ScalarType,
    SupportedFieldPresence,
)
from ._typing import assert_never


def scalar_zero_value(scalar_type: ScalarType) -> Any:  # noqa: RET503
    """Return the zero value for a scalar type."""
    match scalar_type:
        case ScalarType.BOOL:
            return False
        case (
            ScalarType.INT32
            | ScalarType.INT64
            | ScalarType.UINT32
            | ScalarType.UINT64
            | ScalarType.SINT32
            | ScalarType.SINT64
            | ScalarType.FIXED32
            | ScalarType.FIXED64
            | ScalarType.SFIXED32
            | ScalarType.SFIXED64
        ):
            return 0
        case ScalarType.FLOAT | ScalarType.DOUBLE:
            return 0.0
        case ScalarType.STRING:
            return ""
        case ScalarType.BYTES:
            return b""
        case _:
            assert_never(scalar_type)


def requires_presence(member: DescField) -> bool:
    """Returns whether this field needs separate presence tracking.

    Scalar and enum fields with explicit presence need separate
    tracking because their zero value (0, "", False, etc.) is a
    valid user-provided value, indistinguishable from "not set".
    Other field types carry presence in the value itself.
    """
    if (
        isinstance(member.value, DescFieldValueSingular)
        and member.value.oneof is None
        and not isinstance(member.value, DescFieldValueMessage)
    ):
        return member.presence != SupportedFieldPresence.IMPLICIT
    return False


def default_value(member: DescFieldValue | DescOneof) -> Any:  # noqa: RET503
    """Return the default value for the given field or oneof."""
    match member:
        case DescOneof() | DescFieldValueMessage():
            return None
        case DescFieldValueEnum(default_value=default):
            return member.enum.type(
                member.enum.values[0].number if default is None else default
            )
        case DescFieldValueScalar(default_value=default):
            if default is not None:
                return default
            return scalar_zero_value(member.scalar)
        case DescFieldValueList():
            return []
        case DescFieldValueMap():
            return {}
        case _:
            assert_never(member)


def is_zero_value(member: DescFieldValue | DescOneof, value: Any) -> bool:
    """Returns whether the given field or oneof value is a zero value.

    Only used for fields with implicit presence.
    """
    if isinstance(member, DescFieldValueEnum):
        return value == member.enum.values[0].number
    if isinstance(member, DescFieldValueScalar) and member.scalar == ScalarType.FLOAT:
        return value == 0.0 and copysign(1, value) == 1
    return not bool(value)
