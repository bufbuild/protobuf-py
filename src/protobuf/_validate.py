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

import math
from typing import TYPE_CHECKING, Any

from ._descriptors import (
    DescEnum,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    DescOneof,
    ScalarType,
    SupportedFieldPresence,
)
from ._oneof import Oneof
from ._typing import assert_never

if TYPE_CHECKING:
    from ._message import Message

# Integer type limits (MIN is inclusive, MAX is exclusive upper bound)
INT32_MIN = -(2**31)
INT32_MAX = 2**31
INT64_MIN = -(2**63)
INT64_MAX = 2**63
UINT32_MAX = 2**32
UINT64_MAX = 2**64

# Range of finite values representable as float32
FLOAT32_MAX = 3.4028234663852886e38
FLOAT32_MIN = -3.4028234663852886e38


def validate(message: Message, /) -> None:
    """Validate a message for correctness before serialization.

    Checks that all field values have the correct types and that
    numeric values are within their valid ranges.

    Args:
        message: The message to validate.

    Raises:
        TypeError: If a field value has the wrong type.
        OverflowError: If a numeric value is out of range.
        ValueError: If an enum or oneof field has an invalid value.
    """
    # Iterate over members instead of fields to validate oneofs instead of
    # silently skipping them.
    for member in message._desc.members:
        if isinstance(member, DescOneof):
            if (value := getattr(message, member.local_name)) is not None:
                _validate_oneof(member, value)
            continue
        if not message._contains_member(member):
            if member.presence == SupportedFieldPresence.LEGACY_REQUIRED:
                msg = f"cannot encode {member}: required field not set"
                raise ValueError(msg)
            continue
        value: object = message._get_member(member)
        match member:
            case DescField():
                match field_value := member.value:
                    case DescFieldValueScalar():
                        _validate_scalar_type(field_value.scalar, value)
                    case DescFieldValueMessage():
                        _validate_message_value(field_value.message, value)
                    case DescFieldValueEnum():
                        _validate_enum(field_value.enum, value)
                    case DescFieldValueList():
                        if not isinstance(value, list):
                            msg = f"expected list, got {type(value)}"
                            raise TypeError(msg)
                        for element in value:
                            _validate_container_element(field_value.element, element)
                    case DescFieldValueMap():
                        if not isinstance(value, dict):
                            msg = f"expected dict, got {type(value)}"
                            raise TypeError(msg)
                        for k, v in value.items():
                            _validate_scalar_type(field_value.key, k)
                            _validate_container_element(field_value.value, v)
                    case _:
                        assert_never(field_value)
            case _:
                assert_never(member)


def _validate_oneof(desc: DescOneof, value: object) -> None:
    if not isinstance(value, Oneof):
        msg = f"{desc.parent.type_name}.{desc.name}: expected Oneof, got {type(value)}"
        raise TypeError(msg)
    if value.field not in desc._fields_by_name:
        msg = (
            f"{desc.parent.type_name}.{desc.name}: unknown oneof field '{value.field}'"
        )
        raise ValueError(msg)
    field = desc._fields_by_name[value.field]  # ty: ignore[invalid-argument-type] # fails to narrow this to str.
    value = value.value
    match field.value:
        case DescFieldValueScalar(scalar=scalar):
            _validate_scalar_type(scalar, value)
        case DescFieldValueMessage(message=message):
            _validate_message_value(message, value)
        case DescFieldValueEnum(enum=enum):
            _validate_enum(enum, value)
        case _:
            msg = f"invalid oneof field type: {field}"
            raise TypeError(msg)


def _validate_container_element(
    element_type: ScalarType | DescEnum | DescMessage, value: object
) -> None:
    match element_type:
        case ScalarType():
            _validate_scalar_type(element_type, value)
        case DescEnum():
            _validate_enum(element_type, value)
        case DescMessage():
            _validate_message_value(element_type, value)
        case _:
            assert_never(element_type)


def _validate_message_value(desc: DescMessage, value: object) -> None:
    from ._message import Message  # noqa: PLC0415

    if not isinstance(value, Message):
        msg = f"expected {desc.type_name!r}, got {type(value)}"
        raise TypeError(msg)
    if value._desc.type_name != desc.type_name:
        msg = f"expected {desc.type_name!r}, got {value._desc.type_name!r}"
        raise TypeError(msg)
    validate(value)


def _validate_enum(desc: DescEnum, value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        msg = f"expected int for enum {desc.type_name}, got {type(value)}"
        raise TypeError(msg)
    if not desc.open and value not in desc._values_by_number:
        msg = f"invalid enum value {value} for enum {desc.type_name}"
        raise ValueError(msg)


def _validate_scalar_type(scalar_type: ScalarType, value: Any) -> None:
    match scalar_type:
        case ScalarType.BOOL:
            _validate_bool(value)
        case ScalarType.INT32 | ScalarType.SINT32 | ScalarType.SFIXED32:
            _validate_int32(value)
        case ScalarType.UINT32 | ScalarType.FIXED32:
            _validate_uint32(value)
        case ScalarType.INT64 | ScalarType.SINT64 | ScalarType.SFIXED64:
            _validate_int64(value)
        case ScalarType.UINT64 | ScalarType.FIXED64:
            _validate_uint64(value)
        case ScalarType.FLOAT:
            _validate_float32(value)
        case ScalarType.DOUBLE:
            _validate_float64(value)
        case ScalarType.STRING:
            _validate_string(value)
        case ScalarType.BYTES:
            _validate_bytes(value)
        case _:
            assert_never(scalar_type)


def _validate_bool(value: object) -> None:
    if not isinstance(value, bool):
        msg = f"expected bool, got {type(value)}"
        raise TypeError(msg)


def _validate_int32(value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        msg = f"expected int, got {type(value)}"
        raise TypeError(msg)
    if not (INT32_MIN <= value < INT32_MAX):
        msg = f"value {value} out of range for int32"
        raise OverflowError(msg)


def _validate_uint32(value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        msg = f"expected int, got {type(value)}"
        raise TypeError(msg)
    if not (0 <= value < UINT32_MAX):
        msg = f"value {value} out of range for uint32"
        raise OverflowError(msg)


def _validate_int64(value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        msg = f"expected int, got {type(value)}"
        raise TypeError(msg)
    if not (INT64_MIN <= value < INT64_MAX):
        msg = f"value {value} out of range for int64"
        raise OverflowError(msg)


def _validate_uint64(value: object) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        msg = f"expected int, got {type(value)}"
        raise TypeError(msg)
    if not (0 <= value < UINT64_MAX):
        msg = f"value {value} out of range for uint64"
        raise OverflowError(msg)


def _validate_float32(value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        msg = f"expected float, got {type(value)}"
        raise TypeError(msg)
    f = float(value)
    if math.isfinite(f) and not (FLOAT32_MIN <= f <= FLOAT32_MAX):
        msg = f"value {value} out of range for float"
        raise OverflowError(msg)


def _validate_float64(value: object) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        msg = f"expected float, got {type(value)}"
        raise TypeError(msg)


def _validate_string(value: object) -> None:
    if not isinstance(value, str):
        msg = f"expected str, got {type(value)}"
        raise TypeError(msg)


def _validate_bytes(value: object) -> None:
    if not isinstance(value, (bytes, bytearray)):
        msg = f"expected bytes, got {type(value)}"
        raise TypeError(msg)
