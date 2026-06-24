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
)
from ._typing import assert_never
from ._wire._binary_writer import BinaryWriter
from ._wire._wire_type import WireType

if TYPE_CHECKING:
    from ._message import Message


@dataclass(slots=True, frozen=True)
class ToBinaryOptions:
    """Options to control the behavior of to_binary.

    Args:
        write_unknown_fields: If `True`, unknown fields are written to the output.
    """

    write_unknown_fields: bool


def _scalar_wire_type(scalar_type: ScalarType) -> WireType:
    match scalar_type:
        case ScalarType.FIXED64 | ScalarType.SFIXED64 | ScalarType.DOUBLE:
            return WireType.BIT64
        case ScalarType.FIXED32 | ScalarType.SFIXED32 | ScalarType.FLOAT:
            return WireType.BIT32
        case ScalarType.STRING | ScalarType.BYTES:
            return WireType.LENGTH_DELIMITED
        case _:
            return WireType.VARINT


# Dispatch table for writing scalar values. CPython currently does not generate
# jump tables for ``match`` statements, and it is still fairly simple to use this
# table instead.
# https://github.com/python/cpython/issues/88449
_SCALAR_WRITERS = (
    None,  # 0: unused
    BinaryWriter.double,  # 1: DOUBLE
    BinaryWriter.float_,  # 2: FLOAT
    BinaryWriter.int64,  # 3: INT64
    BinaryWriter.uint64,  # 4: UINT64
    BinaryWriter.int32,  # 5: INT32
    BinaryWriter.fixed64,  # 6: FIXED64
    BinaryWriter.fixed32,  # 7: FIXED32
    BinaryWriter.bool_,  # 8: BOOL
    BinaryWriter.string,  # 9: STRING
    None,  # 10: GROUP
    None,  # 11: MESSAGE
    BinaryWriter.bytes_,  # 12: BYTES
    BinaryWriter.uint32,  # 13: UINT32
    None,  # 14: ENUM
    BinaryWriter.sfixed32,  # 15: SFIXED32
    BinaryWriter.sfixed64,  # 16: SFIXED64
    BinaryWriter.sint32,  # 17: SINT32
    BinaryWriter.sint64,  # 18: SINT64
)


def _write_scalar(scalar_type: ScalarType, value: Any, writer: BinaryWriter) -> None:
    writer_method = _SCALAR_WRITERS[scalar_type.value]
    assert writer_method is not None  # noqa: S101
    writer_method(writer, value)


def write_scalar_field(
    number: int, scalar_type: ScalarType, value: Any, writer: BinaryWriter
) -> None:
    writer.tag(number, _scalar_wire_type(scalar_type))
    _write_scalar(scalar_type, value, writer)


def write_message_field(
    number: int,
    value: Message,
    writer: BinaryWriter,
    opts: ToBinaryOptions,
    *,
    delimited_encoding: bool,
) -> None:
    if delimited_encoding:
        writer.tag(number, WireType.SGROUP)
        write_message(value, writer, opts)
        writer.tag(number, WireType.EGROUP)
    else:
        writer.tag(number, WireType.LENGTH_DELIMITED)
        writer.fork()
        write_message(value, writer, opts)
        writer.join()


def write_list_field(
    field_number: int,
    field_value: DescFieldValueList,
    value: list,
    writer: BinaryWriter,
    opts: ToBinaryOptions,
) -> None:
    element_type = field_value.element

    if field_value.packed:
        element_type = (
            element_type if isinstance(element_type, ScalarType) else ScalarType.INT32
        )
        writer.tag(field_number, WireType.LENGTH_DELIMITED)
        writer.fork()
        for v in value:
            _write_scalar(element_type, v, writer)
        writer.join()
        return

    for v in value:
        match element_type:
            case ScalarType():
                write_scalar_field(field_number, element_type, v, writer)
            case DescEnum():
                write_scalar_field(field_number, ScalarType.INT32, v, writer)
            case DescMessage():
                write_message_field(
                    field_number,
                    v,
                    writer,
                    opts,
                    delimited_encoding=field_value.delimited_encoding,
                )
            case _:
                assert_never(element_type)


def write_map_field(
    number: int,
    field_value: DescFieldValueMap,
    map_: dict,
    writer: BinaryWriter,
    opts: ToBinaryOptions,
) -> None:
    for key, value in map_.items():
        writer.tag(number, WireType.LENGTH_DELIMITED)
        writer.fork()

        write_scalar_field(1, field_value.key, key, writer)

        match field_value.value:
            case ScalarType() as scalar_type:
                write_scalar_field(2, scalar_type, value, writer)
            case DescEnum():
                write_scalar_field(2, ScalarType.INT32, value, writer)
            case DescMessage():
                write_message_field(2, value, writer, opts, delimited_encoding=False)
            case _:
                assert_never(field_value.value)

        writer.join()


def write_message(
    message: Message, writer: BinaryWriter, opts: ToBinaryOptions
) -> None:
    for desc_field in message:
        value = message._get_member(desc_field)
        match field_value := desc_field.value:
            case DescFieldValueScalar():
                write_scalar_field(desc_field.number, field_value.scalar, value, writer)
            case DescFieldValueMessage():
                write_message_field(
                    desc_field.number,
                    value,
                    writer,
                    opts,
                    delimited_encoding=field_value.delimited_encoding,
                )
            case DescFieldValueEnum():
                write_scalar_field(desc_field.number, ScalarType.INT32, value, writer)
            case DescFieldValueList():
                write_list_field(desc_field.number, field_value, value, writer, opts)
            case DescFieldValueMap():
                write_map_field(desc_field.number, field_value, value, writer, opts)
            case _:
                assert_never(field_value)

    # Add unknown fields
    if (uf := message._unknown_fields) and opts.write_unknown_fields:
        for field_bytes_list in uf.values():
            for field_bytes in field_bytes_list:
                writer.raw(field_bytes)
