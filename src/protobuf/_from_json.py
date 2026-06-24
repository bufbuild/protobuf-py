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
from base64 import b64decode
from dataclasses import dataclass
from json import loads as parse_json
from typing import TYPE_CHECKING, Literal, TypeVar, cast

from ._descriptors import (
    DescEnum,
    DescExtension,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescFieldValueSingular,
    DescMessage,
    DescOneof,
    ScalarType,
)
from ._oneof import Oneof
from ._typing import JsonValue, assert_never
from ._validate import (
    FLOAT32_MAX,
    FLOAT32_MIN,
    INT32_MAX,
    INT32_MIN,
    INT64_MAX,
    INT64_MIN,
    UINT32_MAX,
    UINT64_MAX,
)
from ._wkt_registry import (
    WktListValue,
    WktStruct,
    WktValue,
    is_null_value_enum,
    is_wkt_value,
    match_wkt,
)

if TYPE_CHECKING:
    from ._enum import Enum
    from ._message import Message
    from ._registry import Registry
    from .wkt import ListValue, NullValue, Struct, Value

    T = TypeVar("T", bound=Message)


@dataclass(slots=True, frozen=True)
class FromJsonOptions:
    ignore_unknown_fields: bool
    registry: Registry | None


def merge_from_json(
    message: Message,
    json: str | bytes | bytearray,
    *,
    ignore_unknown_fields: bool = False,
    registry: Registry | None = None,
) -> None:
    """Parse a ProtoJSON string, merging fields into an existing message.

    Merge rules by field kind:

    - Scalar and enum: the existing value is overwritten.
    - Message: recursively merged if already present, otherwise set.
    - Repeated: elements are appended.
    - Map: entries are added; existing keys are overwritten. Message-valued map entries are not merged.

    Args:
        message: The message instance to merge into.
        json: A str, bytes, or bytearray instance containing the ProtoJSON.
        ignore_unknown_fields: If `True`, unknown fields in the JSON data are
            silently discarded instead of raising an error.
        registry: Required to read google.protobuf.Any and extensions from
            JSON format.

    Raises:
        json.JSONDecodeError: If json_source is not valid JSON.
        TypeError: If the JSON structure does not match expected types.
        ValueError: If a google.protobuf.Any or an extension cannot be resolved
            through the registry.
    """
    json_value = parse_json(json, object_pairs_hook=_no_duplicates)
    opts = FromJsonOptions(
        ignore_unknown_fields=ignore_unknown_fields, registry=registry
    )
    _read_message(message, json_value, opts)


def _read_message(msg: Message, json: JsonValue, opts: FromJsonOptions) -> None:
    if _try_wkt_from_json(msg, json, opts):
        return
    if not isinstance(json, dict):
        err = f"cannot decode {msg.__class__.__qualname__} from JSON: {json}"
        raise TypeError(err)

    desc = msg.__class__._desc
    seen_oneofs = dict[DescOneof, DescField]()
    seen_fields = dict[DescField, str]()
    for key, value in json.items():
        field = desc._fields_by_json_name.get(key)
        if field:
            if seen := seen_fields.get(field):
                err = f"field set multiple times by {seen} and {key}"
                raise ValueError(err)
            seen_fields[field] = key
            field_value = field.value
            if isinstance(field_value, DescFieldValueSingular) and field_value.oneof:
                if value is None and isinstance(field_value, DescFieldValueScalar):
                    continue
                seen = seen_oneofs.get(field_value.oneof)
                if seen:
                    err = f"oneof set multiple times by {seen.name} and {field.name}"
                    raise ValueError(err)
                seen_oneofs[field_value.oneof] = field
            _read_field(msg, field, value, opts)
        else:
            extension = None
            if (
                key.startswith("[")
                and key.endswith("]")
                and opts.registry
                and (extension := opts.registry.extension(key[1:-1]))
                and extension.extendee.type_name == desc.type_name
            ):
                _read_extension(msg, extension, value, opts)
            if not extension and not opts.ignore_unknown_fields:
                err = (
                    f"cannot decode {desc.type_name} from JSON: key: '{key}' is unknown"
                )
                raise ValueError(err)


def _read_field(
    msg: Message, field: DescField, json: JsonValue, opts: FromJsonOptions
) -> None:
    match field_value := field.value:
        case DescFieldValueScalar():
            _read_scalar_field(msg, field, field_value, json)
        case DescFieldValueEnum():
            _read_enum_field(msg, field, field_value, json, opts)
        case DescFieldValueMessage():
            _read_message_field(msg, field, field_value, json, opts)
        case DescFieldValueList():
            _read_list_field(msg._get_member(field), field, field_value, json, opts)
        case DescFieldValueMap():
            _read_map_field(msg._get_member(field), field, field_value, json, opts)
        case _:
            assert_never(field_value)


def _read_extension(
    msg: Message, ext: DescExtension, json: JsonValue, opts: FromJsonOptions
) -> None:
    match field_value := ext.value:
        case DescFieldValueScalar():
            _read_scalar_extension(msg, ext, field_value, json)
        case DescFieldValueEnum():
            _read_enum_extension(msg, ext, field_value, json, opts)
        case DescFieldValueMessage():
            _read_message_extension(msg, ext, field_value, json, opts)
        case DescFieldValueList():
            _read_list_extension(msg, ext, field_value, json, opts)
        case _:
            assert_never(field_value)


def _read_scalar_extension(
    msg: Message, ext: DescExtension, field_value: DescFieldValueScalar, json: JsonValue
) -> None:
    if json is None:
        del msg[ext.type]
    else:
        msg[ext.type] = _read_scalar(ext, field_value.scalar, json)


def _read_enum_extension(
    msg: Message,
    ext: DescExtension,
    field_value: DescFieldValueEnum,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if _is_resetting_null(field_value.enum, json):
        del msg[ext.type]
    else:
        value = _read_enum(field_value.enum, json, opts.ignore_unknown_fields)
        if value is not None:
            msg[ext.type] = value


def _read_message_extension(
    msg: Message,
    ext: DescExtension,
    field_value: DescFieldValueMessage,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if _is_resetting_null(field_value.message, json):
        del msg[ext.type]
    else:
        value = field_value.message.type()
        _read_message(value, json, opts)
        msg[ext.type] = value


def _read_list_extension(
    msg: Message,
    ext: DescExtension,
    field_value: DescFieldValueList,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if json is None:
        return
    if not isinstance(json, list):
        raise _field_error(ext, f"expected list got {type(json)}", TypeError)
    msg[ext.type] = [
        v
        for element in json
        if (v := _read_container_item(ext, field_value.element, element, opts))
        is not None
    ]


def _read_scalar_field(
    msg: Message, field: DescField, field_value: DescFieldValueScalar, json: JsonValue
) -> None:
    if json is None:
        msg._del_member(field)
        return
    msg._set_member(field, _read_scalar(field, field_value.scalar, json))


def _read_enum_field(
    msg: Message,
    field: DescField,
    field_value: DescFieldValueEnum,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if _is_resetting_null(field_value.enum, json):
        msg._del_member(field)
        return
    value = _read_enum(field_value.enum, json, opts.ignore_unknown_fields)
    if value is not None:
        msg._set_member(field, value)


def _read_list_field(
    list_: list[object],
    field: DescField,
    field_value: DescFieldValueList,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if json is None:
        return
    if not isinstance(json, list):
        raise _field_error(field, f"expected list got {type(json)}", TypeError)
    list_.extend(
        value
        for element in json
        if (value := _read_container_item(field, field_value.element, element, opts))
        is not None
    )


def _read_map_field(
    dict_: dict[str | bool | int, object],
    field: DescField,
    field_value: DescFieldValueMap,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if json is None:
        return
    if not isinstance(json, dict):
        raise _field_error(field, f"expected dict got {type(json)}", TypeError)
    for json_key, json_value in json.items():
        key = _read_map_key(field, field_value, json_key)
        value = _read_container_item(field, field_value.value, json_value, opts)
        if value is not None:
            dict_[key] = value


def _read_message_field(
    msg: Message,
    field: DescField,
    field_value: DescFieldValueMessage,
    json: JsonValue,
    opts: FromJsonOptions,
) -> None:
    if _is_resetting_null(field_value.message, json):
        msg._del_member(field)
        return
    value = (
        msg._get_member(field)
        if msg._contains_member(field)
        else field_value.message.type()
    )
    _read_message(value, json, opts)
    msg._set_member(field, value)


def _read_map_key(
    field: DescField, field_value: DescFieldValueMap, json: JsonValue
) -> bool | int | str:
    match field_value.key:
        case ScalarType.BOOL:
            if json == "true":
                return True
            if json == "false":
                return False
            raise _field_error(field, f"unexpected bool map key value {json}")
        case ScalarType.STRING:
            return _read_string(field, json)
        case (
            ScalarType.DOUBLE | ScalarType.FLOAT | ScalarType.BYTES
        ):  # This is because the Map key is not narrow enough
            msg = f"invalid map key type: {field_value.key}"
            raise AssertionError(msg)
        case _:
            return _read_int(field, field_value.key, json)


def _read_container_item(
    field: DescField | DescExtension,
    element: ScalarType | DescMessage | DescEnum,
    json: JsonValue,
    opts: FromJsonOptions,
) -> bool | int | float | str | bytes | Message | Enum | None:
    if isinstance(element, ScalarType) and json is not None:
        return _read_scalar(field, element, json)
    if isinstance(element, DescMessage) and not _is_resetting_null(element, json):
        msg = element.type()
        _read_message(msg, json, opts)
        return msg
    if isinstance(element, DescEnum) and not _is_resetting_null(element, json):
        return _read_enum(element, json, opts.ignore_unknown_fields)
    raise _field_error(
        field,
        f"unexpected null value for {'map value' if isinstance(field, DescField) and isinstance(field.value, DescFieldValueMap) else 'list item'}",
    )


def _read_enum(
    desc: DescEnum,
    json: JsonValue,
    ignore_unknown_fields: bool,  # noqa: FBT001
) -> Enum | None:
    if json is None:
        return desc.type(desc.values[0].number)
    if not isinstance(json, bool) and isinstance(
        json, int
    ):  # isinstance(bool_value, int) is True
        if value := desc._values_by_number.get(json):
            return desc.type(value.number)
        if ignore_unknown_fields:
            return None
        # Succeeds for open enum, raises an error for closed
        return desc.type(json)
    if isinstance(json, str):
        if value := desc._values_by_name.get(json):
            return desc.type(value.number)
        if ignore_unknown_fields:
            return None

    msg = f"cannot decode {desc.type_name} from JSON: {json}"
    raise ValueError(msg)


def _read_scalar(
    desc: DescField | DescExtension, scalar_type: ScalarType, json: JsonValue
) -> bool | int | float | str | bytes:
    match scalar_type:
        case ScalarType.BOOL:
            if not isinstance(json, bool):
                raise _field_error(
                    desc, f"unexpected json type: {type(json)}", TypeError
                )
            return json
        case ScalarType.FLOAT:
            v = _parse_float(desc, json)
            if math.isfinite(v) and not FLOAT32_MIN <= v <= FLOAT32_MAX:
                raise _field_error(
                    desc, f"float value out of range: {json}", OverflowError
                )
            return v
        case ScalarType.DOUBLE:
            return _parse_float(desc, json)
        case ScalarType.STRING:
            return _read_string(desc, json)
        case ScalarType.BYTES:
            if not isinstance(json, str):
                raise _field_error(
                    desc, f"expected base64-encoded string got: {type(json)}", TypeError
                )
            # Accept standard and URL-safe base64, adding padding if necessary
            altchars = "-_" if "-" in json or "_" in json else None
            if padding := len(json) % 4:
                json = json + (4 - padding) * "="
            try:
                return b64decode(json, altchars=altchars, validate=True)
            except ValueError:
                raise _field_error(desc, "invalid base64 data", ValueError) from None
        case _:
            return _read_int(desc, scalar_type, json)


def _read_int(
    desc: DescField | DescExtension,
    int_type: Literal[
        ScalarType.INT32,
        ScalarType.SINT32,
        ScalarType.SFIXED32,
        ScalarType.INT64,
        ScalarType.SINT64,
        ScalarType.SFIXED64,
        ScalarType.UINT32,
        ScalarType.FIXED32,
        ScalarType.UINT64,
        ScalarType.FIXED64,
    ],
    json: JsonValue,
) -> int:
    v = _parse_int(desc, json)
    match int_type:
        case ScalarType.INT32 | ScalarType.SINT32 | ScalarType.SFIXED32:
            if not INT32_MIN <= v < INT32_MAX:
                raise _field_error(
                    desc, f"value {v} out of range for int32", OverflowError
                )
        case ScalarType.INT64 | ScalarType.SINT64 | ScalarType.SFIXED64:
            if not INT64_MIN <= v < INT64_MAX:
                raise _field_error(
                    desc, f"value {v} out of range for int64", OverflowError
                )
        case ScalarType.UINT32 | ScalarType.FIXED32:
            if not 0 <= v < UINT32_MAX:
                raise _field_error(
                    desc, f"value {v} out of range for uint32", OverflowError
                )
        case ScalarType.UINT64 | ScalarType.FIXED64:
            if not 0 <= v < UINT64_MAX:
                raise _field_error(
                    desc, f"value {v} out of range for uint64", OverflowError
                )
        case _:
            assert_never(int_type)
    return v


def _read_string(desc: DescField | DescExtension, json: JsonValue) -> str:
    if not isinstance(json, str):
        raise _field_error(desc, f"expected string got: {type(json)}", TypeError)
    try:
        # Raises UnicodeEncodeError for lone surrogates - they are not permitted in Protobuf strings
        json.encode("utf-8")
    except UnicodeEncodeError:
        raise _field_error(desc, f"invalid utf-8 string in field {desc}") from None
    return json


def _parse_int(desc: DescField | DescExtension, json: JsonValue) -> int:
    if not isinstance(json, bool) and isinstance(
        json, int
    ):  # isinstance(bool_value, int) is True
        return json

    if isinstance(json, float):
        f = json
    elif isinstance(json, str):
        if not json or json.strip() != json:
            raise _field_error(desc, f"invalid integer value: {json}")
        try:
            return int(json, 10)  # Default base parses any valid Python literal
        except ValueError:
            try:
                f = float(json)  # For strings that are "x.0"
            except ValueError:
                raise _field_error(desc, f"invalid integer value: '{json}'") from None
    else:
        raise _field_error(desc, f"unexpected json type: {type(json)}", TypeError)

    if not f.is_integer():
        raise _field_error(desc, f"expected integer, got non-integer float: {json}")

    return int(f)


def _parse_float(desc: DescField | DescExtension, json: JsonValue) -> float:
    if not isinstance(json, bool) and isinstance(
        json, int
    ):  # isinstance(bool_value, int) is True
        return float(json)

    if isinstance(json, float):
        f = json
    elif isinstance(json, str):
        if json in ("Infinity", "-Infinity", "NaN"):
            return float(json)
        if not json or json.strip() != json:
            raise _field_error(desc, f"invalid float/double value: {json}")
        try:
            f = float(json)
        except ValueError:
            raise _field_error(desc, f"invalid float/double value: {json}") from None
    else:
        raise _field_error(desc, f"unexpected json type: {type(json)}", TypeError)

    if not math.isfinite(f):
        raise _field_error(desc, "unexpected infinite/NaN number")

    return f


def _field_error(
    desc: DescField | DescExtension, msg: str, typ: type[Exception] = ValueError
) -> Exception:
    return (
        typ(f"{msg} for extension {desc.type_name}")
        if isinstance(desc, DescExtension)
        else typ(f"{msg} for field {desc.parent.type_name}.{desc.name}")
    )


def _is_resetting_null(element: DescMessage | DescEnum, json: JsonValue) -> bool:
    """Whether a JSON null should clear the field rather than set a value.

    All message and enum fields treat null as "clear", except
    google.protobuf.Value (where null represents NullValue) and
    google.protobuf.NullValue (where null is the literal enum value).
    """
    if json is not None:
        return False
    if isinstance(element, DescMessage):
        return not is_wkt_value(element)
    return not is_null_value_enum(element)


def _try_wkt_from_json(msg: Message, json: JsonValue, opts: FromJsonOptions) -> bool:
    """Decode a well-known type from its special JSON representation.

    Returns True if the message was handled, False if generic parsing should proceed.
    """
    wkt = match_wkt(msg.__class__._desc)
    if wkt is None:
        return False
    return wkt.from_json(msg, json, opts)


def _struct_from_json(
    msg: Struct, json: JsonValue, opts: FromJsonOptions, fields_desc: DescFieldValueMap
) -> None:
    if not isinstance(json, dict):
        err = f"cannot decode {msg._desc.type_name} from JSON: {json}"
        raise TypeError(err)
    value_desc = fields_desc.value
    assert isinstance(value_desc, DescMessage)  # noqa: S101
    value_wkt = match_wkt(value_desc)
    assert isinstance(value_wkt, WktValue)  # noqa: S101
    for k, v in json.items():
        val = cast("Value", value_desc.type())
        _value_from_json(val, v, opts, value_wkt)
        msg.fields[k] = val


def _list_value_from_json(
    msg: ListValue,
    json: JsonValue,
    opts: FromJsonOptions,
    values_desc: DescFieldValueList,
) -> None:
    if not isinstance(json, list):
        err = f"cannot decode {msg._desc.type_name} from JSON: {json}"
        raise TypeError(err)
    element_desc = values_desc.element
    assert isinstance(element_desc, DescMessage)  # noqa: S101
    element_wkt = match_wkt(element_desc)
    assert isinstance(element_wkt, WktValue)  # noqa: S101
    for e in json:
        val = cast("Value", element_desc.type())
        _value_from_json(val, e, opts, element_wkt)
        msg.values.append(val)


def _value_from_json(
    msg: Value, json: JsonValue, opts: FromJsonOptions, wkt: WktValue
) -> None:
    match json:
        case None:
            msg.kind = Oneof(
                "null_value", cast("NullValue", wkt.null_value.enum.type(0))
            )
        case bool():
            msg.kind = Oneof("bool_value", json)
        case int() | float():
            msg.kind = Oneof("number_value", float(json))
        case str():
            msg.kind = Oneof("string_value", json)
        case list():
            lv_desc = wkt.list_value.message
            lv_wkt = match_wkt(lv_desc)
            assert isinstance(lv_wkt, WktListValue)  # noqa: S101
            lv = cast("ListValue", lv_desc.type())
            _list_value_from_json(lv, json, opts, lv_wkt.values)
            msg.kind = Oneof("list_value", lv)
        case dict():
            struct_desc = wkt.struct_value.message
            struct_wkt = match_wkt(struct_desc)
            assert isinstance(struct_wkt, WktStruct)  # noqa: S101
            struct = cast("Struct", struct_desc.type())
            _struct_from_json(struct, json, opts, struct_wkt.fields)
            msg.kind = Oneof("struct_value", struct)
        case _:
            assert_never(json)


def _no_duplicates(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    """Reject duplicate JSON keys at parse time via json.loads object_pairs_hook.

    This is needed in addition to the seen_fields check in _read_message
    because a single proto field can have two distinct JSON keys (its proto
    name and its json_name). seen_fields catches that case, but it cannot
    catch two identical JSON keys that map to the same dict entry, since
    Python's default JSON parser silently keeps only the last value.
    """
    obj: dict[str, JsonValue] = {}
    for k, v in pairs:
        if k in obj:
            msg = f"duplicate key: {k}"
            raise ValueError(msg)
        obj[k] = v
    return obj


def message_from_json_value(
    message_type: type[T],
    data: JsonValue,
    *,
    ignore_unknown_fields: bool = False,
    registry: Registry | None = None,
) -> T:
    """Converts the Python value parsed from JSON data to a new Message of the given type.

    This can be useful when embedding a message within a larger structure encoded as JSON.
    The JSON data will be read using ProtoJSON semantics, including support for
    well-known-types and extensions if a registry is provided.

    See [`message_to_json_value`][] for the inverse operation.

    Examples:
        ```python
        # For example, a request to a task runner
        data = json.loads(
            '{"task": "save_user", "user": {"name": "Alice", "created_at": "2024-01-01T00:00:00Z"}}'
        )
        user = message_from_json_value(User, data["user"])
        assert user.name == "Alice"
        assert user.created_at == Timestamp.from_datetime(
            datetime(2024, 1, 1, tzinfo=timezone.utc)
        )
        ```
    """
    message = message_type()
    opts = FromJsonOptions(
        ignore_unknown_fields=ignore_unknown_fields, registry=registry
    )
    _read_message(message, data, opts)
    return message
