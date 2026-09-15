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

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar

from typing_extensions import Buffer, assert_never

from ._budget import (
    BYTES_OVERHEAD,
    DICT_ENTRY_SIZE,
    FLOAT_SIZE,
    GC_HEAD_SIZE,
    INT_SIZE,
    LIST_SLOT_SIZE,
    ONEOF_SIZE,
    STR_OVERHEAD,
    Budget,
)
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
        budget: Tracks approximate allocations during the parse and raises
            once the configured limit is exceeded. Unlimited by default.
    """

    ignore_unknown_fields: bool = False
    budget: Budget = field(default_factory=Budget)


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
    None,  # 9: STRING (length-delimited, handled in read_scalar)
    None,  # 10: GROUP
    None,  # 11: MESSAGE
    None,  # 12: BYTES (length-delimited, handled in read_scalar)
    BinaryReader.uint32,  # 13: UINT32
    None,  # 14: ENUM
    BinaryReader.sfixed32,  # 15: SFIXED32
    BinaryReader.sfixed64,  # 16: SFIXED64
    BinaryReader.sint32,  # 17: SINT32
    BinaryReader.sint64,  # 18: SINT64
)

# Allocation charged for each fixed-size scalar before it is read, indexed like
# _SCALAR_READERS. Bools are shared singletons and allocate nothing.
_SCALAR_CHARGES = (
    None,  # 0: unused
    FLOAT_SIZE,  # 1: DOUBLE
    FLOAT_SIZE,  # 2: FLOAT
    INT_SIZE,  # 3: INT64
    INT_SIZE,  # 4: UINT64
    INT_SIZE,  # 5: INT32
    INT_SIZE,  # 6: FIXED64
    INT_SIZE,  # 7: FIXED32
    0,  # 8: BOOL
    None,  # 9: STRING
    None,  # 10: GROUP
    None,  # 11: MESSAGE
    None,  # 12: BYTES
    INT_SIZE,  # 13: UINT32
    None,  # 14: ENUM
    INT_SIZE,  # 15: SFIXED32
    INT_SIZE,  # 16: SFIXED64
    INT_SIZE,  # 17: SINT32
    INT_SIZE,  # 18: SINT64
)


def read_scalar(scalar_type: ScalarType, reader: BinaryReader, budget: Budget) -> Any:
    if scalar_type == ScalarType.STRING:
        length = reader.varint()
        budget.charge(STR_OVERHEAD + length)
        return str(reader.read(length), "utf-8")
    if scalar_type == ScalarType.BYTES:
        length = reader.varint()
        budget.charge(BYTES_OVERHEAD + length)
        return bytes(reader.read(length))
    charge = _SCALAR_CHARGES[scalar_type.value]
    reader_method = _SCALAR_READERS[scalar_type.value]
    assert charge is not None and reader_method is not None  # noqa: S101, PT018
    budget.charge(charge)
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
                budget = opts.budget
                budget.charge(
                    BYTES_OVERHEAD + len(key_raw) + len(field_raw) + LIST_SLOT_SIZE
                )
                message._get_or_init_unknown_fields().setdefault(tag.number, []).append(
                    key_raw + bytes(field_raw)
                )
            continue

        budget = opts.budget
        match field_value := desc_field.value:
            case DescFieldValueScalar():
                value = read_scalar(field_value.scalar, reader, budget)
                if field_value.oneof is not None:
                    budget.charge(ONEOF_SIZE)
                message._set_member(desc_field, value)
            case DescFieldValueMessage(
                message=desc_nested_message, delimited_encoding=delimited_encoding
            ):
                existing: Message | None = message._get_member(desc_field)
                if existing is None:
                    budget.charge_message(desc_nested_message)
                    if field_value.oneof is not None:
                        budget.charge(ONEOF_SIZE)
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
                value = read_enum(field_value.enum, reader, budget)
                if isinstance(value, Enum):
                    if field_value.oneof is not None:
                        budget.charge(ONEOF_SIZE)
                    message._set_member(desc_field, value)
                elif not opts.ignore_unknown_fields:
                    _write_unknown_enum_field(message, desc_field.number, value, budget)
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
                    budget.charge(DICT_ENTRY_SIZE)
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
            budget = opts.budget
            budget.charge(
                BYTES_OVERHEAD + len(key_raw) + len(field_bytes) + LIST_SLOT_SIZE
            )
            message._get_or_init_unknown_fields().setdefault(field_number, []).append(
                key_raw + bytes(field_bytes)
            )
        return

    budget = opts.budget
    match element_type:
        case ScalarType():
            value = read_scalar(element_type, reader, budget)
        case DescMessage():
            budget.charge_message(element_type)
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
            value = read_enum(element_type, reader, budget)
            if not isinstance(value, Enum):
                if not opts.ignore_unknown_fields:
                    _write_unknown_enum_field(message, field_number, value, budget)
                return
        case _:
            assert_never(element_type)
    budget.charge(LIST_SLOT_SIZE)
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
    budget = opts.budget
    while reader.offset < end:
        match element_type:
            case ScalarType():
                value = read_scalar(element_type, reader, budget)
                budget.charge(LIST_SLOT_SIZE)
                list_.append(value)
            case DescEnum():
                value = read_enum(element_type, reader, budget)
                if isinstance(value, Enum):
                    budget.charge(LIST_SLOT_SIZE)
                    list_.append(value)
                elif not opts.ignore_unknown_fields:
                    # Even for packed fields we write unknown enum values as unpacked.
                    _write_unknown_enum_field(message, field_number, value, budget)
            case _:
                assert_never(element_type)


def read_enum(desc_enum: DescEnum, reader: BinaryReader, budget: Budget) -> Enum | int:
    value = reader.int32()
    if not desc_enum._values_by_number.get(value):
        if not desc_enum.open:
            return value
        budget.charge(INT_SIZE + GC_HEAD_SIZE)
    return desc_enum.type(value)


def _write_unknown_enum_field(
    message: Message | None, field_number: int, value: int, budget: Budget
) -> None:
    if message is None:
        return
    writer = BinaryWriter()
    writer.tag(field_number, WireType.VARINT)
    writer.int32(value)
    field_bytes = writer.finish()
    budget.charge(BYTES_OVERHEAD + len(field_bytes) + LIST_SLOT_SIZE)
    message._get_or_init_unknown_fields().setdefault(field_number, []).append(
        field_bytes
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

    budget = opts.budget
    while reader.offset < end:
        tag = reader.tag()
        if tag.number == 1:  # key
            if tag.wire_type != field_value._key_wire_type:
                _read_unknown_map_entry(
                    message, field_number, reader, start_offset, opts, depth
                )
                return None
            key = read_scalar(field_value.key, reader, budget)
        elif tag.number == 2:  # value
            if tag.wire_type != field_value._value_wire_type:
                _read_unknown_map_entry(
                    message, field_number, reader, start_offset, opts, depth
                )
                return None
            match field_value.value:
                case ScalarType() as scalar_type:
                    value = read_scalar(scalar_type, reader, budget)
                case DescEnum() as desc_enum:
                    value = read_enum(desc_enum, reader, budget)
                    if not isinstance(value, Enum):
                        _read_unknown_map_entry(
                            message, field_number, reader, start_offset, opts, depth
                        )
                        return None
                case DescMessage():
                    budget.charge_message(field_value.value)
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
                budget.charge_message(field_value.value)
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
        budget = opts.budget
        budget.charge(BYTES_OVERHEAD + len(key_raw) + len(entry_bytes) + LIST_SLOT_SIZE)
        message._get_or_init_unknown_fields().setdefault(field_number, []).append(
            key_raw + bytes(entry_bytes)
        )


def merge_from_binary(
    message: Message,
    data: Buffer,
    *,
    ignore_unknown_fields: bool = False,
    allocation_limit: int | None = None,
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
        data: Serialized binary protobuf data. Must not be mutated during parsing.
        ignore_unknown_fields: If `True`, unknown fields in the binary data are silently discarded.
        allocation_limit: If set, the approximate number of bytes of Python
            objects the parse may allocate before raising a ValueError.
    """
    message._merge_from_binary(
        data, ignore_unknown_fields, allocation_limit=allocation_limit
    )
