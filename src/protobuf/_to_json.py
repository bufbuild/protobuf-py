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
import math
from base64 import b64encode
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from ._descriptors import (
    DescEnum,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    ScalarType,
    SupportedFieldPresence,
)
from ._oneof import Oneof
from ._typing import JsonPrimitive, JsonValue, assert_never
from ._validate import validate
from ._wkt_registry import is_null_value_enum, match_wkt

if TYPE_CHECKING:
    from types import NotImplementedType

    from ._message import Message
    from ._registry import Registry
    from .wkt import Struct, Value


@dataclass(slots=True, frozen=True)
class ToJsonOptions:
    always_emit_implicit: bool
    print_enums_as_ints: bool
    use_proto_field_name: bool
    registry: Registry | None = None


def _struct_to_json_value(value: Struct, opts: ToJsonOptions) -> JsonValue:
    return {key: _value_to_json_value(val, opts) for key, val in value.fields.items()}


def _value_to_json_value(value: Value, opts: ToJsonOptions) -> JsonValue:
    match value.kind:
        case Oneof(field="null_value"):
            return None
        case Oneof(field="number_value", value=v):
            # Value does not allow non-finite numbers.
            if not math.isfinite(v):
                msg = "value cannot be NaN or Infinity"
                raise ValueError(msg)
            return _scalar_to_json_value(ScalarType.DOUBLE, v)
        case Oneof(field="string_value", value=v) | Oneof(field="bool_value", value=v):
            return v
        case Oneof(field="struct_value", value=v):
            return _struct_to_json_value(v, opts)
        case Oneof(field="list_value", value=v):
            return [_value_to_json_value(element, opts) for element in v.values]
        case _:
            msg = "value must have exactly one field set"
            raise ValueError(msg)


def _scalar_to_json_value(scalar_type: ScalarType, value: Any) -> JsonPrimitive:
    match scalar_type:
        case (
            ScalarType.INT64
            | ScalarType.UINT64
            | ScalarType.SINT64
            | ScalarType.FIXED64
            | ScalarType.SFIXED64
        ):
            return str(value)
        case ScalarType.FLOAT | ScalarType.DOUBLE:
            if math.isnan(value):
                return "NaN"
            if math.isinf(value):
                return "Infinity" if value > 0 else "-Infinity"
            return value
        case ScalarType.BYTES:
            return b64encode(value).decode()
        case _:
            return value


def _enum_to_json_value(
    desc_enum: DescEnum, value: int, opts: ToJsonOptions
) -> JsonValue:
    if is_null_value_enum(desc_enum):
        return None
    if opts.print_enums_as_ints:
        return int(value)
    if enum_value := desc_enum._values_by_number.get(value):
        return enum_value.name
    if not desc_enum.open:
        msg = f"invalid enum value {value} for enum {desc_enum.type_name}"
        raise ValueError(msg)
    # If the enum is open but value is unknown, print the integer value.
    return value


def _container_value_to_json_value(  # noqa: RET503
    desc_element: ScalarType | DescEnum | DescMessage, value: Any, opts: ToJsonOptions
) -> JsonValue:
    match desc_element:
        case ScalarType():
            return _scalar_to_json_value(desc_element, value)
        case DescEnum():
            return _enum_to_json_value(desc_element, value, opts)
        case DescMessage():
            return _message_to_json_value(value, opts)
        case _:
            assert_never(desc_element)


def _try_wkt_to_json(
    msg: Message, opts: ToJsonOptions
) -> JsonValue | NotImplementedType:
    """Encode a well-known type to its special JSON representation.

    Returns the JSON value if the message was handled, NotImplemented if
    generic encoding should proceed.
    """
    wkt = match_wkt(type(msg)._desc)
    if wkt is None:
        return NotImplemented
    return wkt.to_json_value(msg, opts)


def _message_to_json_value(message: Message, opts: ToJsonOptions) -> JsonValue:
    if (json_value := _try_wkt_to_json(message, opts)) is not NotImplemented:
        return json_value

    # Regular fields
    result: dict[str, JsonValue] = {}
    for desc_field in message._desc.fields:
        if not message._contains_member(desc_field) and (
            not opts.always_emit_implicit
            or desc_field.presence != SupportedFieldPresence.IMPLICIT
        ):
            continue
        value = message._get_member(desc_field)
        match field_value := desc_field.value:
            case DescFieldValueScalar():
                json_value = _scalar_to_json_value(field_value.scalar, value)
            case DescFieldValueEnum():
                json_value = _enum_to_json_value(field_value.enum, value, opts)
            case DescFieldValueMessage():
                json_value = _message_to_json_value(value, opts)
            case DescFieldValueList():
                json_value = [
                    _container_value_to_json_value(field_value.element, element, opts)
                    for element in value
                ]
            case DescFieldValueMap():
                json_value = {
                    (
                        key if isinstance(key, str) else json.dumps(key)
                    ): _container_value_to_json_value(field_value.value, val, opts)
                    for key, val in value.items()
                }
            case _:
                assert_never(field_value)
        json_key = (
            desc_field.name if opts.use_proto_field_name else desc_field.json_name
        )
        result[json_key] = json_value

    # Extension fields
    if opts.registry and (uf := message._unknown_fields):
        for field_number in uf:
            ext_desc = opts.registry.extension_for(message._desc, field_number)
            if not ext_desc:
                continue
            value = message[ext_desc.type]
            match field_value := ext_desc.value:
                case DescFieldValueScalar():
                    json_value = _scalar_to_json_value(field_value.scalar, value)
                case DescFieldValueEnum():
                    json_value = _enum_to_json_value(field_value.enum, value, opts)
                case DescFieldValueMessage():
                    json_value = _message_to_json_value(value, opts)
                case DescFieldValueList():
                    json_value = [
                        _container_value_to_json_value(
                            field_value.element, element, opts
                        )
                        for element in value
                    ]
                case _:
                    assert_never(field_value)
            result[f"[{ext_desc.type_name}]"] = json_value
    return result


def to_json(message: Message, opts: ToJsonOptions) -> str:
    return json.dumps(_message_to_json_value(message, opts))


def message_to_json_value(
    message: Message,
    /,
    *,
    registry: Registry | None = None,
    always_emit_implicit: bool = False,
    print_enums_as_ints: bool = False,
    use_proto_field_name: bool = False,
) -> JsonValue:
    """Converts a protobuf message to a Python value that can be encoded as JSON.

    This can be useful when embedding a message within a larger structure encoded as JSON.
    The message content is converted using ProtoJSON semantics, including support for
    well-known-types and extensions if a registry is provided.

    See [`message_from_json_value`][] for the inverse operation.

    Examples:
        ```python
        user = User(
            name="Alice", created_at=Timestamp.from_datetime(datetime(2024, 1, 1))
        )
        # For example, a request to a task runner
        request = {"task": "save_user", "user": message_to_json_value(user)}
        assert (
            json.dumps(request)
            == '{"task": "save_user", "user": {"name": "Alice", "createdAt": "2024-01-01T00:00:00Z"}}'
        )
        ```
    """
    validate(message)
    opts = ToJsonOptions(
        always_emit_implicit=always_emit_implicit,
        print_enums_as_ints=print_enums_as_ints,
        use_proto_field_name=use_proto_field_name,
        registry=registry,
    )
    return _message_to_json_value(message, opts)
