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

from typing import TYPE_CHECKING, Any

from ._descriptors import (
    DescEnum,
    DescFieldValue,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    ScalarType,
)
from ._enum import Enum
from ._from_binary import (
    FromBinaryOptions,
    read_enum,
    read_list,
    read_map_entry,
    read_message,
    read_scalar,
)
from ._to_binary import (
    ToBinaryOptions,
    write_list_field,
    write_map_field,
    write_message_field,
    write_scalar_field,
)
from ._typing import assert_never
from ._wire import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from ._message import Message


def has_unknown_field(
    message: Message, number: int, field_value: DescFieldValue
) -> bool:
    # For closed enums, we need to actually decode the value to know if it is
    # known or not. We special case it to keep the common case simpler.
    if not (uf := message._unknown_fields):
        return False
    match field_value:
        case (
            DescFieldValueEnum(enum=DescEnum(open=False))
            | DescFieldValueList(element=DescEnum(open=False))
        ):
            value = get_unknown_field(message, number, field_value)
            if value is None or value == []:
                return False
    return number in uf


def get_unknown_field(  # noqa: RET503
    message: Message, number: int, field_value: DescFieldValue
) -> Any:
    if not (uf := message._unknown_fields) or not (binary_fields := uf.get(number)):
        return None

    opts = FromBinaryOptions()
    match field_value:
        case DescFieldValueScalar():
            reader = BinaryReader(memoryview(binary_fields[-1]))
            reader.tag()
            return read_scalar(field_value.scalar, reader)
        case DescFieldValueEnum():
            reader = BinaryReader(memoryview(binary_fields[-1]))
            reader.tag()
            enum_value = read_enum(field_value.enum, reader)
            if isinstance(enum_value, Enum):
                return enum_value
            return None
        case DescFieldValueMessage():
            message = field_value.message.type()
            for binary_field in binary_fields:
                reader = BinaryReader(memoryview(binary_field))
                tag = reader.tag()
                if field_value.delimited_encoding:
                    read_message(
                        message, reader, opts, depth=0, group_number=tag.number
                    )
                else:
                    read_message(message, reader, opts, depth=0, length=reader.varint())
            return message
        case DescFieldValueList():
            list_value: list[Any] = []
            for binary_field in binary_fields:
                reader = BinaryReader(memoryview(binary_field))
                while reader.offset < len(binary_field):
                    tag = reader.tag()
                    read_list(
                        None,
                        list_value,
                        number,
                        field_value,
                        tag.wire_type,
                        reader,
                        opts,
                        depth=0,
                    )
            return list_value
        case DescFieldValueMap():
            map_value: dict[Any, Any] = {}
            for binary_field in binary_fields:
                reader = BinaryReader(memoryview(binary_field))
                while reader.offset < len(binary_field):
                    reader.tag()
                    if entry := read_map_entry(
                        None, number, field_value, reader, opts, depth=0
                    ):
                        key, value_ = entry
                        map_value[key] = value_
            return map_value
        case _:
            assert_never(field_value)


def set_unknown_field(
    message: Message, number: int, field_value: DescFieldValue, value: Any
) -> None:
    writer = BinaryWriter()
    match field_value:
        case DescFieldValueScalar():
            write_scalar_field(number, field_value.scalar, value, writer)
        case DescFieldValueEnum():
            write_scalar_field(number, ScalarType.INT32, value, writer)
        case DescFieldValueMessage():
            write_message_field(
                number,
                value,
                writer,
                ToBinaryOptions(write_unknown_fields=True),
                delimited_encoding=field_value.delimited_encoding,
            )
        case DescFieldValueList():
            write_list_field(
                number,
                field_value,
                value,
                writer,
                ToBinaryOptions(write_unknown_fields=True),
            )
        case DescFieldValueMap():
            write_map_field(
                number,
                field_value,
                value,
                writer,
                ToBinaryOptions(write_unknown_fields=True),
            )
        case _:
            assert_never(field_value)
    binary = writer.finish()
    message._get_or_init_unknown_fields()[number] = [binary]
