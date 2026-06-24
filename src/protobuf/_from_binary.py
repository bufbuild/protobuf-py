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

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar

from ._descriptors import (
    DescEnum,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    ScalarType,
)
from ._enum import Enum
from ._field_values import scalar_zero_value
from ._typing import assert_never
from ._wire._binary_reader import DEPTH_LIMIT, BinaryReader
from ._wire._binary_writer import BinaryWriter
from ._wire._wire_type import WireType

if TYPE_CHECKING:
    from ._message import Message

    T = TypeVar("T", bound=Message)


@dataclass(slots=True, frozen=True)
class FromBinaryOptions:
    """Options to control the behavior of from_binary.

    Args:
        ignore_unknown_fields: If `True`, unknown fields are ignored instead of being added to the message.
    """

    ignore_unknown_fields: bool = False


# Dispatch table for reading scalar values. CPython currently does not generate
# jump tables for ``match`` statements, and it is still fairly simple to use this
# table instead.
# https://github.com/python/cpython/issues/88449
_SCALAR_READERS = (
    None,  # 0: unused
    BinaryReader.double,  # 1: DOUBLE
    BinaryReader.float_,  # 2: FLOAT
    BinaryReader.int64,  # 3: INT64
    BinaryReader.uint64,  # 4: UINT64
    BinaryReader.int32,  # 5: INT32
    BinaryReader.fixed64,  # 6: FIXED64
    BinaryReader.fixed32,  # 7: FIXED32
    BinaryReader.bool_,  # 8: BOOL
    BinaryReader.string,  # 9: STRING
    None,  # 10: GROUP
    None,  # 11: MESSAGE
    BinaryReader.bytes_,  # 12: BYTES
    BinaryReader.uint32,  # 13: UINT32
    None,  # 14: ENUM
    BinaryReader.sfixed32,  # 15: SFIXED32
    BinaryReader.sfixed64,  # 16: SFIXED64
    BinaryReader.sint32,  # 17: SINT32
    BinaryReader.sint64,  # 18: SINT64
)


def read_scalar(scalar_type: ScalarType, reader: BinaryReader) -> Any:
    reader_method = _SCALAR_READERS[scalar_type.value]
    assert reader_method is not None  # noqa: S101
    return reader_method(reader)


# TODO delete this, and either:
#  - call the method from to_binary once implemented
#  - use a different representation for unknown fields
def _encode_varint(value: int) -> bytes:
    """Encode an integer as a varint."""
    result = bytearray()
    while value > 0x7F:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value)
    return bytes(result)


def read_message(
    message: Message,
    reader: BinaryReader,
    opts: FromBinaryOptions,
    depth: int,
    *,
    length: int = 0,
    group_number: int | None = None,
) -> Message:
    if depth > DEPTH_LIMIT:
        msg = f"exceeded maximum recursion depth {DEPTH_LIMIT} while parsing message"
        raise RecursionError(msg)
    desc_message = message._desc
    end = reader.offset + length  # Only used for length-delimited messages

    while group_number is not None or reader.offset < end:
        tag = reader.tag()

        if group_number is not None and tag.wire_type == WireType.EGROUP:
            if tag.number != group_number:
                msg = f"mismatched group end tag: expected {group_number}, got {tag.number}"
                raise ValueError(msg)
            break

        desc_field = desc_message._fields_by_tag.get(tag.raw)

        if desc_field is None:  # Unknown field
            field_raw = reader.skip(tag.wire_type, depth + 1, field_number=tag.number)
            if not opts.ignore_unknown_fields:
                key_raw = _encode_varint((tag.number << 3) | tag.wire_type)
                message._get_or_init_unknown_fields().setdefault(tag.number, []).append(
                    key_raw + bytes(field_raw)
                )
            continue

        match field_value := desc_field.value:
            case DescFieldValueScalar():
                message._set_member(desc_field, read_scalar(field_value.scalar, reader))
            case DescFieldValueMessage(
                message=desc_nested_message, delimited_encoding=delimited_encoding
            ):
                existing: Message | None = message._get_member(desc_field)
                if existing is None:
                    existing = desc_nested_message.type()
                    message._set_member(desc_field, existing)
                if delimited_encoding:
                    read_message(
                        existing, reader, opts, depth + 1, group_number=tag.number
                    )
                else:
                    read_message(
                        existing, reader, opts, depth + 1, length=reader.varint()
                    )
            case DescFieldValueEnum():
                value = read_enum(field_value.enum, reader)
                if isinstance(value, Enum):
                    message._set_member(desc_field, value)
                elif not opts.ignore_unknown_fields:
                    _write_unknown_enum_field(message, desc_field.number, value)
            case DescFieldValueList():
                read_list(
                    message,
                    message._get_member(desc_field),
                    desc_field.number,
                    field_value,
                    tag.wire_type,
                    reader,
                    opts,
                    depth,
                )
            case DescFieldValueMap():
                entry = read_map_entry(
                    message, desc_field.number, field_value, reader, opts, depth
                )
                if entry:
                    key, value = entry
                    message._get_member(desc_field)[key] = value
            case _:
                assert_never(desc_field)

    return message


def read_list(
    message: Message | None,
    list_: list,
    field_number: int,
    field_value: DescFieldValueList,
    wire_type: WireType,
    reader: BinaryReader,
    opts: FromBinaryOptions,
    depth: int,
) -> None:
    element_type = field_value.element

    # Packed repeated field
    if wire_type == WireType.LENGTH_DELIMITED and field_value._packable:
        assert isinstance(element_type, (ScalarType, DescEnum))  # noqa: S101
        _read_packed_list(message, list_, field_number, element_type, reader, opts)
        return

    if wire_type != field_value._unpacked_wire_type:
        # Wire type doesn't match expected unpacked type, skip the field.
        field_bytes = reader.skip(wire_type, depth + 1, field_number=field_number)
        if not opts.ignore_unknown_fields and message:
            key_raw = _encode_varint((field_number << 3) | wire_type)
            message._get_or_init_unknown_fields().setdefault(field_number, []).append(
                key_raw + bytes(field_bytes)
            )
        return

    match element_type:
        case ScalarType():
            value = read_scalar(element_type, reader)
        case DescMessage():
            if field_value.delimited_encoding:
                value = read_message(
                    element_type.type(),
                    reader,
                    opts,
                    depth + 1,
                    group_number=field_number,
                )
            else:
                value = read_message(
                    element_type.type(), reader, opts, depth + 1, length=reader.varint()
                )
        case DescEnum():
            value = read_enum(element_type, reader)
            if not isinstance(value, Enum):
                if not opts.ignore_unknown_fields:
                    _write_unknown_enum_field(message, field_number, value)
                return
        case _:
            assert_never(element_type)
    list_.append(value)


def _read_packed_list(
    message: Message | None,
    list_: list,
    field_number: int,
    element_type: ScalarType | DescEnum,
    reader: BinaryReader,
    opts: FromBinaryOptions,
) -> None:
    length = reader.varint()
    end = reader.offset + length
    while reader.offset < end:
        match element_type:
            case ScalarType():
                list_.append(read_scalar(element_type, reader))
            case DescEnum():
                value = read_enum(element_type, reader)
                if isinstance(value, Enum):
                    list_.append(value)
                elif not opts.ignore_unknown_fields:
                    # Even for packed fields we write unknown enum values as unpacked.
                    _write_unknown_enum_field(message, field_number, value)
            case _:
                assert_never(element_type)


def read_enum(desc_enum: DescEnum, reader: BinaryReader) -> Enum | int:
    value = reader.int32()
    if not desc_enum.open and not desc_enum._values_by_number.get(value):
        return value
    return desc_enum.type(value)


def _write_unknown_enum_field(
    message: Message | None, field_number: int, value: int
) -> None:
    if message is None:
        return
    writer = BinaryWriter()
    writer.tag(field_number, WireType.VARINT)
    writer.int32(value)
    message._get_or_init_unknown_fields().setdefault(field_number, []).append(
        writer.finish()
    )


def read_map_entry(
    message: Message | None,
    field_number: int,
    field_value: DescFieldValueMap,
    reader: BinaryReader,
    opts: FromBinaryOptions,
    depth: int,
) -> tuple[Any, Any] | None:
    start_offset = reader.offset
    length = reader.varint()
    end = reader.offset + length

    key: Any = None
    value: Any = None

    while reader.offset < end:
        tag = reader.tag()
        if tag.number == 1:  # key
            if tag.wire_type != field_value._key_wire_type:
                _read_unknown_map_entry(
                    message, field_number, reader, start_offset, opts, depth
                )
                return None
            key = read_scalar(field_value.key, reader)
        elif tag.number == 2:  # value
            if tag.wire_type != field_value._value_wire_type:
                _read_unknown_map_entry(
                    message, field_number, reader, start_offset, opts, depth
                )
                return None
            match field_value.value:
                case ScalarType() as scalar_type:
                    value = read_scalar(scalar_type, reader)
                case DescEnum() as desc_enum:
                    value = read_enum(desc_enum, reader)
                    if not isinstance(value, Enum):
                        _read_unknown_map_entry(
                            message, field_number, reader, start_offset, opts, depth
                        )
                        return None
                case DescMessage():
                    value = field_value.value.type()
                    read_message(value, reader, opts, depth + 1, length=reader.varint())
                case _:
                    assert_never(field_value.value)
        else:
            reader.skip(tag.wire_type, depth + 1, field_number=tag.number)

    if key is None:
        key = scalar_zero_value(field_value.key)
    if value is None:
        match field_value.value:
            case ScalarType() as scalar_type:
                value = scalar_zero_value(scalar_type)
            case DescEnum() as desc_enum:
                value = desc_enum.type(desc_enum.values[0].number)
            case DescMessage():
                value = field_value.value.type()
            case _:
                assert_never(field_value.value)

    return key, value


def _read_unknown_map_entry(
    message: Message | None,
    field_number: int,
    reader: BinaryReader,
    start_offset: int,
    opts: FromBinaryOptions,
    depth: int,
) -> None:
    # The entire map entry must be recorded to unknown fields. Simplest way
    # is to reset the reader and skip.
    reader.seek(start_offset)
    entry_bytes = reader.skip(
        WireType.LENGTH_DELIMITED, depth, field_number=field_number
    )
    if not opts.ignore_unknown_fields and message:
        key_raw = _encode_varint((field_number << 3) | WireType.LENGTH_DELIMITED)
        message._get_or_init_unknown_fields().setdefault(field_number, []).append(
            key_raw + bytes(entry_bytes)
        )


def merge_from_binary(
    message: Message, data: bytes, *, ignore_unknown_fields: bool = False
) -> None:
    """Parse serialized binary data, merging fields into an existing message.

    Merge rules by field kind:

    - Scalar and enum: the existing value is overwritten.
    - Message: recursively merged if already present, otherwise set.
    - Repeated: elements are appended.
    - Map: entries are added; existing keys are overwritten. Message-valued map entries are not merged.
    - Unknown fields: retained unless `ignore_unknown_fields` is `True`.

    Args:
        message: The message instance to merge into.
        data: Serialized binary protobuf data.
        ignore_unknown_fields: If `True`, unknown fields in the binary data are silently discarded.
    """
    message._merge_from_binary(data, ignore_unknown_fields)
