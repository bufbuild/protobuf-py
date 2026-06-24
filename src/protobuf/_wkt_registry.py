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

"""Central registry for matching well-known type descriptors.

Consolidates WKT identification and field extraction into a single source
of truth, replacing scattered string comparisons and cast chains.
"""

from __future__ import annotations

import re
from copy import copy
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, TypeAlias, cast

from ._descriptors import (
    DescEnum,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    ScalarType,
)

if TYPE_CHECKING:
    from types import NotImplementedType

    from ._from_json import FromJsonOptions
    from ._message import Message
    from ._to_json import ToJsonOptions
    from ._typing import JsonValue
    from .wkt import Any, Duration, FieldMask, ListValue, Struct, Timestamp, Value
    from .wkt._gen.any_pb import Any as GenAny


_TS_MIN = datetime(1, 1, 1, tzinfo=timezone.utc)
_TS_MAX = datetime(9999, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

# Strict RFC 3339 validation — datetime.fromisoformat is too permissive
# (accepts lowercase 't', space separator, offsets without colons).
_TIMESTAMP_RE = re.compile(
    r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2})"
    r"(?:\.([0-9]{1,9}))?"
    r"(Z|(?:[+-][0-9]{2}:[0-9]{2}))$"
)

_DURATION_RE = re.compile(r"^(-?[0-9]+)(?:\.([0-9]{1,9}))?s$")


@dataclass(frozen=True, slots=True)
class WktTimestamp:
    def to_json_value(self, msg: Message, _opts: ToJsonOptions) -> JsonValue:
        from .wkt import Timestamp  # noqa: PLC0415
        from .wkt._mixin._const import (  # noqa: PLC0415
            DURATION_SECONDS_MAX,
            NANOS_PER_SECOND_MAX,
        )

        value = cast("Timestamp", msg)
        if not (-DURATION_SECONDS_MAX <= value.seconds <= DURATION_SECONDS_MAX):
            err = "timestamp seconds out of range"
            raise ValueError(err)
        if not (0 <= value.nanos <= NANOS_PER_SECOND_MAX):
            err = "timestamp nanos out of range"
            raise ValueError(err)
        # Use nanos=0 for datetime conversion — we append nanos separately
        # to preserve nanosecond precision.
        iso_secs = (
            Timestamp(seconds=value.seconds)
            .to_datetime()
            .isoformat(timespec="seconds")
            .removesuffix("+00:00")
        )
        if value.nanos == 0:
            return iso_secs + "Z"
        nanos_str = f"{value.nanos:09d}"
        if nanos_str[3:] == "000000":
            nanos_str = nanos_str[:3]
        elif nanos_str[6:] == "000":
            nanos_str = nanos_str[:6]
        return f"{iso_secs}.{nanos_str}Z"

    def from_json(self, msg: Message, json: JsonValue, _opts: FromJsonOptions) -> bool:
        from .wkt import Timestamp  # noqa: PLC0415

        value = cast("Timestamp", msg)
        if not isinstance(json, str):
            err = f"cannot decode {value._desc.type_name} from JSON: {json}"
            raise TypeError(err)
        matches = _TIMESTAMP_RE.match(json)
        if not matches:
            err = f"cannot decode {value._desc.type_name} from JSON: invalid RFC 3339 string"
            raise ValueError(err)
        nanos = 0
        if matches[2]:
            frac = matches[2]
            nanos = int("1" + frac + "0" * (9 - len(frac))) - 1_000_000_000
        # Reconstruct without fractional seconds for datetime parsing.
        # TODO: Remove this normalization when the Python floor is 3.11+.
        # Python 3.10's datetime.fromisoformat does not accept a trailing "Z".
        offset = "+00:00" if matches[3] == "Z" else matches[3]
        try:
            dt = datetime.fromisoformat(matches[1] + offset)
        except ValueError:
            err = f"cannot decode {value._desc.type_name} from JSON: invalid RFC 3339 string"
            raise ValueError(err) from None
        if dt < _TS_MIN or dt > _TS_MAX:
            err = (
                f"cannot decode {value._desc.type_name} from JSON: must be from"
                " 0001-01-01T00:00:00Z to 9999-12-31T23:59:59Z inclusive"
            )
            raise ValueError(err)
        value.seconds = Timestamp.from_datetime(dt).seconds
        value.nanos = nanos
        return True

    def mixin(self) -> type | None:
        from .wkt._mixin import TimestampMixin  # noqa: PLC0415

        return TimestampMixin


@dataclass(frozen=True, slots=True)
class WktDuration:
    def to_json_value(self, msg: Message, _opts: ToJsonOptions) -> JsonValue:
        from .wkt._mixin._const import (  # noqa: PLC0415
            DURATION_SECONDS_MAX,
            NANOS_PER_SECOND_MAX,
        )

        value = cast("Duration", msg)
        if not (-DURATION_SECONDS_MAX <= value.seconds <= DURATION_SECONDS_MAX):
            err = "duration seconds out of range"
            raise ValueError(err)
        if not (-NANOS_PER_SECOND_MAX <= value.nanos <= NANOS_PER_SECOND_MAX):
            err = "duration nanos out of range"
            raise ValueError(err)
        if (value.seconds > 0 and value.nanos < 0) or (
            value.seconds < 0 and value.nanos > 0
        ):
            err = "duration seconds and nanos have different signs"
            raise ValueError(err)
        if value.nanos == 0:
            return f"{value.seconds}s"
        nanos_str = f"{abs(value.nanos):09d}"
        if nanos_str[3:] == "000000":
            nanos_str = nanos_str[:3]
        elif nanos_str[6:] == "000":
            nanos_str = nanos_str[:6]
        text = f"{value.seconds}.{nanos_str}"
        if value.nanos < 0 and value.seconds == 0:
            text = "-" + text
        return text + "s"

    def from_json(self, msg: Message, json: JsonValue, _opts: FromJsonOptions) -> bool:
        from .wkt._mixin._const import DURATION_SECONDS_MAX  # noqa: PLC0415

        value = cast("Duration", msg)
        if not isinstance(json, str):
            err = f"cannot decode {value._desc.type_name} from JSON: {json}"
            raise TypeError(err)
        duration_match = _DURATION_RE.match(json)
        if not duration_match:
            err = f"cannot decode {value._desc.type_name} from JSON: {json}"
            raise ValueError(err)
        seconds = int(duration_match[1])
        if seconds > DURATION_SECONDS_MAX or seconds < -DURATION_SECONDS_MAX:
            err = f"cannot decode {value._desc.type_name} from JSON: {json}"
            raise ValueError(err)
        nanos = 0
        if duration_match[2]:
            nanos = int(duration_match[2] + "0" * (9 - len(duration_match[2])))
            if seconds < 0 or duration_match[1] == "-0":
                nanos = -nanos
        value.seconds = seconds
        value.nanos = nanos
        return True

    def mixin(self) -> type | None:
        from .wkt._mixin import DurationMixin  # noqa: PLC0415

        return DurationMixin


@dataclass(frozen=True, slots=True)
class WktAny:
    def to_json_value(self, msg: Message, opts: ToJsonOptions) -> JsonValue:
        from ._to_json import _message_to_json_value  # noqa: PLC0415
        from .wkt._mixin._any import type_url_to_name  # noqa: PLC0415

        message = cast("GenAny", msg)
        if message.type_url == "":
            return {}
        if not opts.registry:
            err = f'any "{message.type_url}" is not in the type registry'
            raise ValueError(err)
        type_name = type_url_to_name(message.type_url)
        desc = opts.registry.message(type_name)
        if not desc:
            err = f'any: "{message.type_url}" is not in the type registry'
            raise ValueError(err)
        unpacked = message.unpack(desc)
        assert unpacked is not None  # noqa: S101
        json_value = _message_to_json_value(unpacked, opts)
        # WKTs have custom JSON representations (strings, arrays, null, etc.)
        # that must be wrapped in a "value" field. Regular messages produce
        # dicts whose fields are merged alongside "@type".
        if not isinstance(json_value, dict) or match_wkt(desc) is not None:
            return {"@type": message.type_url, "value": json_value}
        json_value["@type"] = message.type_url
        return json_value

    def from_json(self, msg: Message, json: JsonValue, opts: FromJsonOptions) -> bool:
        from ._from_json import _read_message  # noqa: PLC0415
        from .wkt import Any  # noqa: PLC0415

        value = cast("Any", msg)
        if not isinstance(json, dict):
            err = f"cannot decode {Any._desc.type_name} from JSON: {json}"
            raise TypeError(err)
        if not json:
            return True
        type_url = json.get("@type")
        if not isinstance(type_url, str) or not type_url:
            err = f"cannot decode {Any._desc.type_name} from JSON: {json}, @type is invalid: {type_url}"
            raise ValueError(err)
        type_name = (
            type_url[type_url.rindex("/") + 1 :] if "/" in type_url else type_url
        )
        desc = opts.registry.message(type_name) if opts.registry else None
        if not desc:
            err = f"cannot decode {Any._desc.type_name} from JSON: {type_url} is not in the type registry"
            raise ValueError(err)
        message = desc.type()
        if match_wkt(desc) is not None and "value" in json:
            _read_message(message, json["value"], opts)
        else:
            json = copy(json)
            del json["@type"]
            _read_message(message, json, opts)
        any_ = Any.pack(message)
        value.type_url = any_.type_url
        value.value = any_.value
        return True

    def mixin(self) -> type | None:
        from .wkt._mixin import AnyMixin  # noqa: PLC0415

        return AnyMixin


@dataclass(frozen=True, slots=True)
class WktFieldMask:
    def to_json_value(self, msg: Message, _opts: ToJsonOptions) -> JsonValue:
        from ._names import proto_camel_case, proto_snake_case  # noqa: PLC0415

        value = cast("FieldMask", msg)
        parts: list[str] = []
        for path in value.paths:
            proto_camel_path = proto_camel_case(path)
            if proto_snake_case(proto_camel_path) != path:
                err = (
                    f"invalid FieldMask path: lowerCamelCase of {path} is irreversible"
                )
                raise ValueError(err)
            parts.append(proto_camel_path)
        return ",".join(parts)

    def from_json(self, msg: Message, json: JsonValue, _opts: FromJsonOptions) -> bool:
        from ._names import proto_snake_case  # noqa: PLC0415

        value = cast("FieldMask", msg)
        if not isinstance(json, str):
            err = f"cannot decode {value._desc.type_name} from JSON: {json}"
            raise TypeError(err)
        if not json:
            return True
        for path in json.split(","):
            if "_" in path:
                err = f"cannot decode {value._desc.type_name} from JSON: path names must be lowerCamelCase"
                raise ValueError(err)
            value.paths.append(proto_snake_case(path))
        return True

    def mixin(self) -> type | None:
        return None


@dataclass(frozen=True, slots=True)
class WktStruct:
    fields: DescFieldValueMap

    def to_json_value(self, msg: Message, opts: ToJsonOptions) -> JsonValue:
        from ._to_json import _struct_to_json_value  # noqa: PLC0415

        return _struct_to_json_value(cast("Struct", msg), opts)

    def from_json(self, msg: Message, json: JsonValue, opts: FromJsonOptions) -> bool:
        from ._from_json import _struct_from_json  # noqa: PLC0415

        _struct_from_json(cast("Struct", msg), json, opts, self.fields)
        return True

    def mixin(self) -> type | None:
        return None


@dataclass(frozen=True, slots=True)
class WktListValue:
    values: DescFieldValueList

    def to_json_value(self, msg: Message, opts: ToJsonOptions) -> JsonValue:
        from ._to_json import _value_to_json_value  # noqa: PLC0415

        return [
            _value_to_json_value(element, opts)
            for element in cast("ListValue", msg).values
        ]

    def from_json(self, msg: Message, json: JsonValue, opts: FromJsonOptions) -> bool:
        from ._from_json import _list_value_from_json  # noqa: PLC0415

        _list_value_from_json(cast("ListValue", msg), json, opts, self.values)
        return True

    def mixin(self) -> type | None:
        return None


@dataclass(frozen=True, slots=True)
class WktValue:
    null_value: DescFieldValueEnum
    number_value: DescFieldValueScalar
    string_value: DescFieldValueScalar
    bool_value: DescFieldValueScalar
    struct_value: DescFieldValueMessage
    list_value: DescFieldValueMessage

    def to_json_value(self, msg: Message, opts: ToJsonOptions) -> JsonValue:
        from ._to_json import _value_to_json_value  # noqa: PLC0415

        return _value_to_json_value(cast("Value", msg), opts)

    def from_json(self, msg: Message, json: JsonValue, opts: FromJsonOptions) -> bool:
        from ._from_json import _value_from_json  # noqa: PLC0415

        _value_from_json(cast("Value", msg), json, opts, self)
        return True

    def mixin(self) -> type | None:
        return None


@dataclass(frozen=True, slots=True)
class WktWrapper:
    field: DescField
    value: DescFieldValueScalar

    def to_json_value(self, msg: Message, _opts: ToJsonOptions) -> JsonValue:
        from ._to_json import _scalar_to_json_value  # noqa: PLC0415

        return _scalar_to_json_value(self.value.scalar, msg[self.field])

    def from_json(self, msg: Message, json: JsonValue, _opts: FromJsonOptions) -> bool:
        from ._from_json import _read_scalar  # noqa: PLC0415

        if json is None:
            del msg[self.field]
        else:
            msg[self.field] = _read_scalar(self.field, self.value.scalar, json)
        return True

    def mixin(self) -> type | None:
        return None


@dataclass(frozen=True, slots=True)
class WktFileDescriptorSet:
    def to_json_value(self, _msg: Message, _opts: ToJsonOptions) -> NotImplementedType:
        return NotImplemented

    def from_json(
        self, _msg: Message, _json: JsonValue, _opts: FromJsonOptions
    ) -> bool:
        return False

    def mixin(self) -> type | None:
        from .wkt._mixin import FileDescriptorSetMixin  # noqa: PLC0415

        return FileDescriptorSetMixin


WktMatch: TypeAlias = (
    WktTimestamp
    | WktDuration
    | WktAny
    | WktFieldMask
    | WktStruct
    | WktListValue
    | WktValue
    | WktWrapper
    | WktFileDescriptorSet
)


def match_wkt(desc: DescMessage) -> WktMatch | None:
    """Match a message descriptor against known well-known types.

    Returns a typed match object with pre-extracted field descriptors if the
    descriptor's file name, type name, and fields match a known WKT. Returns
    None otherwise.
    """
    if not desc.type_name.startswith("google.protobuf."):
        return None
    if not desc.file.name.startswith("google/protobuf/"):
        return None
    match desc.type_name:
        case "google.protobuf.Timestamp":
            return _match_timestamp(desc)
        case "google.protobuf.Duration":
            return _match_duration(desc)
        case "google.protobuf.Any":
            return _match_any(desc)
        case "google.protobuf.FieldMask":
            return _match_field_mask(desc)
        case "google.protobuf.Struct":
            return _match_struct(desc)
        case "google.protobuf.ListValue":
            return _match_list_value(desc)
        case "google.protobuf.Value":
            return _match_value(desc)
        case "google.protobuf.FileDescriptorSet":
            return _match_file_descriptor_set(desc)
        case _:
            return _match_wrapper(desc)


def is_wkt_value(desc: DescMessage) -> bool:
    """Check if a message descriptor is google.protobuf.Value."""
    return desc.type_name == "google.protobuf.Value" and desc.file.name.startswith(
        "google/protobuf/"
    )


def is_null_value_enum(desc: DescEnum) -> bool:
    """Check if an enum descriptor is google.protobuf.NullValue."""
    return desc.type_name == "google.protobuf.NullValue" and desc.file.name.startswith(
        "google/protobuf/"
    )


# The type name in the outer match of match_wkt already discriminates
# Timestamp from Duration. The field checks below are a defensive guard
# to reject descriptors whose fields don't match the expected schema.


def _match_timestamp(desc: DescMessage) -> WktTimestamp | None:
    fields = desc._fields_by_name
    if (
        (seconds := fields.get("seconds"))
        and isinstance(seconds.value, DescFieldValueScalar)
        and seconds.value.scalar == ScalarType.INT64
        and (nanos := fields.get("nanos"))
        and isinstance(nanos.value, DescFieldValueScalar)
        and nanos.value.scalar == ScalarType.INT32
    ):
        return WktTimestamp()
    return None


def _match_duration(desc: DescMessage) -> WktDuration | None:
    fields = desc._fields_by_name
    if (
        (seconds := fields.get("seconds"))
        and isinstance(seconds.value, DescFieldValueScalar)
        and seconds.value.scalar == ScalarType.INT64
        and (nanos := fields.get("nanos"))
        and isinstance(nanos.value, DescFieldValueScalar)
        and nanos.value.scalar == ScalarType.INT32
    ):
        return WktDuration()
    return None


def _match_any(desc: DescMessage) -> WktAny | None:
    fields = desc._fields_by_name
    if (
        (type_url := fields.get("type_url"))
        and isinstance(type_url.value, DescFieldValueScalar)
        and type_url.value.scalar == ScalarType.STRING
        and (value := fields.get("value"))
        and isinstance(value.value, DescFieldValueScalar)
        and value.value.scalar == ScalarType.BYTES
    ):
        return WktAny()
    return None


def _match_field_mask(desc: DescMessage) -> WktFieldMask | None:
    fields = desc._fields_by_name
    if (
        (paths := fields.get("paths"))
        and isinstance(paths.value, DescFieldValueList)
        and paths.value.element == ScalarType.STRING
    ):
        return WktFieldMask()
    return None


def _match_struct(desc: DescMessage) -> WktStruct | None:
    fields = desc._fields_by_name
    if (
        (f := fields.get("fields"))
        and isinstance(f.value, DescFieldValueMap)
        and f.value.key == ScalarType.STRING
    ):
        return WktStruct(fields=f.value)
    return None


def _match_list_value(desc: DescMessage) -> WktListValue | None:
    fields = desc._fields_by_name
    if (
        (values := fields.get("values"))
        and isinstance(values.value, DescFieldValueList)
        and isinstance(values.value.element, DescMessage)
    ):
        return WktListValue(values=values.value)
    return None


def _match_value(desc: DescMessage) -> WktValue | None:
    fields = desc._fields_by_name
    if (
        (null_value := fields.get("null_value"))
        and isinstance(null_value.value, DescFieldValueEnum)
        and (number_value := fields.get("number_value"))
        and isinstance(number_value.value, DescFieldValueScalar)
        and number_value.value.scalar == ScalarType.DOUBLE
        and (string_value := fields.get("string_value"))
        and isinstance(string_value.value, DescFieldValueScalar)
        and string_value.value.scalar == ScalarType.STRING
        and (bool_value := fields.get("bool_value"))
        and isinstance(bool_value.value, DescFieldValueScalar)
        and bool_value.value.scalar == ScalarType.BOOL
        and (struct_value := fields.get("struct_value"))
        and isinstance(struct_value.value, DescFieldValueMessage)
        and (list_value := fields.get("list_value"))
        and isinstance(list_value.value, DescFieldValueMessage)
    ):
        return WktValue(
            null_value=null_value.value,
            number_value=number_value.value,
            string_value=string_value.value,
            bool_value=bool_value.value,
            struct_value=struct_value.value,
            list_value=list_value.value,
        )
    return None


def _match_file_descriptor_set(desc: DescMessage) -> WktFileDescriptorSet | None:
    fields = desc._fields_by_name
    if (
        (file := fields.get("file"))
        and isinstance(file.value, DescFieldValueList)
        and isinstance(file.value.element, DescMessage)
    ):
        return WktFileDescriptorSet()
    return None


def _match_wrapper(desc: DescMessage) -> WktWrapper | None:
    # Uses structural matching rather than an explicit allowlist of wrapper
    # type names. Any google.protobuf.* message with exactly one scalar field
    # named "value" is treated as a wrapper type. This is safe because all
    # other known WKT types are matched explicitly above in match_wkt.
    if len(desc.fields) != 1:
        return None
    field = desc.fields[0]
    if not isinstance(field.value, DescFieldValueScalar) or field.name != "value":
        return None
    return WktWrapper(field=field, value=field.value)
