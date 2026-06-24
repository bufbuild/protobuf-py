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

import struct
from dataclasses import dataclass
from typing import final

from ._wire_type import WireType

DEPTH_LIMIT = 100


@dataclass(frozen=True, slots=True, init=False)
class Tag:
    """Tag of a protobuf field, consisting of a field number and a wire type."""

    number: int
    wire_type: WireType
    raw: int

    def __init__(self, key: int) -> None:
        number = key >> 3
        wire_type = WireType(key & 0x07)

        if number == 0:
            msg = "invalid tag with field number 0"
            raise ValueError(msg)

        object.__setattr__(self, "number", number)
        object.__setattr__(self, "wire_type", wire_type)
        object.__setattr__(self, "raw", key)


@final
class BinaryReader:
    """A reader for deserializing Protocol Buffer wire format."""

    def __init__(self, data: memoryview) -> None:
        """Initialize a BinaryReader.

        Args:
            data: The underlying memoryview to read from.
        """
        self._data = data
        self._offset = 0

    @property
    def offset(self) -> int:
        """The current read position within the buffer."""
        return self._offset

    def read(self, size: int) -> memoryview:
        """Read a given number of bytes from the buffer."""
        if self._offset + size > len(self._data):
            msg = "unexpected end of buffer"
            raise EOFError(msg)
        result = self._data[self._offset : self._offset + size]
        self._offset += size
        return result

    def seek(self, offset: int) -> None:
        """Move the buffer position to the given offset."""
        if offset < 0 or offset > len(self._data):
            msg = "invalid seek offset"
            raise ValueError(msg)
        self._offset = offset

    def varint(self, limit: int = 10, last_byte_limit: int = 1) -> int:
        """Read a varint from the buffer."""
        result = 0
        shift = 0

        data = self._data
        offset = self._offset
        end = len(data)

        # protobuf guarantees varints are at most 10 bytes
        for i in range(limit):
            if offset >= end:
                msg = "unexpected end of buffer while reading varint"
                raise EOFError(msg)
            byte = data[offset]
            offset += 1

            result |= (byte & 0x7F) << shift
            shift += 7
            if byte < 0x80:
                if i == limit - 1 and byte > last_byte_limit:
                    msg = "invalid varint"
                    raise ValueError(msg)
                self._offset = offset
                return result
        msg = "invalid varint"
        raise ValueError(msg)

    def tag(self) -> Tag:
        """Read a varint and interpret it as a protobuf field tag, consisting of a field number and a wire type."""
        # Protobuf tags are limited to 5-byte varints
        key = self.varint(5, 0x0F)
        return Tag(key)

    def bool_(self) -> bool:
        """Read a varint and interpret it as a boolean."""
        return bool(self.varint())

    def int32(self) -> int:
        """Read a varint and interpret it as a signed 32-bit integer."""
        value = self.varint()
        value %= 1 << 32
        return value if value < (1 << 31) else value - (1 << 32)

    def int64(self) -> int:
        """Read a varint and interpret it as a signed 64-bit integer."""
        value = self.varint()
        return value if value < (1 << 63) else value - (1 << 64)

    def uint32(self) -> int:
        """Read a varint and interpret it as an unsigned 32-bit integer."""
        value = self.varint()
        return value % (1 << 32)

    def uint64(self) -> int:
        """Read a varint and interpret it as an unsigned 64-bit integer."""
        return self.varint()

    def sint32(self) -> int:
        """Read a varint and interpret it as a signed 32-bit integer with zigzag encoding."""
        value = self.varint()
        value = value % (1 << 32)
        return ((value + 1) >> 1) * (-1 if value & 1 else 1)

    def sint64(self) -> int:
        """Read a varint and interpret it as a signed 64-bit integer with zigzag encoding."""
        value = self.varint()
        return ((value + 1) >> 1) * (-1 if value & 1 else 1)

    def float_(self) -> float:
        """Read 4 bytes and interpret them as a 32-bit floating point number."""
        return struct.unpack("<f", self.read(4))[0]

    def double(self) -> float:
        """Read 8 bytes and interpret them as a 64-bit floating point number."""
        return struct.unpack("<d", self.read(8))[0]

    def fixed32(self) -> int:
        """Read 4 bytes and interpret them as an unsigned 32-bit integer."""
        return struct.unpack("<I", self.read(4))[0]

    def sfixed32(self) -> int:
        """Read 4 bytes and interpret them as a signed 32-bit integer."""
        return struct.unpack("<i", self.read(4))[0]

    def fixed64(self) -> int:
        """Read 8 bytes and interpret them as an unsigned 64-bit integer."""
        return struct.unpack("<Q", self.read(8))[0]

    def sfixed64(self) -> int:
        """Read 8 bytes and interpret them as a signed 64-bit integer."""
        return struct.unpack("<q", self.read(8))[0]

    def skip(self, wire_type: WireType, depth: int, *, field_number: int) -> memoryview:
        """Skip a field value and return a memoryview on the skipped bytes.

        Args:
            wire_type: The wire type of the field to skip.
            depth: The current recursion depth of the message tree.
            field_number: The field number. Used for delimited encoding.

        Returns:
            A [`memoryview`][] over the skipped bytes.
        """
        if depth > DEPTH_LIMIT:
            msg = f"exceeded maximum recursion depth {DEPTH_LIMIT} while skipping field {field_number}"
            raise RecursionError(msg)
        start = self._offset
        match wire_type:
            case WireType.VARINT:
                self.varint()
            case WireType.BIT64:
                self.read(8)
            case WireType.LENGTH_DELIMITED:
                length = self.varint()
                self.read(length)
            case WireType.BIT32:
                self.read(4)
            case WireType.SGROUP:
                while True:
                    inner_tag = self.tag()
                    if inner_tag.wire_type == WireType.EGROUP:
                        if inner_tag.number != field_number:
                            msg = f"mismatched group tag: expected {field_number}, got {inner_tag.number}"
                            raise ValueError(msg)
                        break
                    nested_depth = (
                        depth + 1 if inner_tag.wire_type == WireType.SGROUP else depth
                    )
                    self.skip(
                        inner_tag.wire_type,
                        depth=nested_depth,
                        field_number=inner_tag.number,
                    )
            case WireType.EGROUP:
                msg = "unexpected end group tag outside of group"
                raise ValueError(msg)
        return self._data[start : self._offset]

    def bytes_(self) -> bytes:
        """Read a length-delimited byte sequence."""
        length = self.varint()
        return bytes(self.read(length))

    def string(self) -> str:
        """Read a length-delimited byte sequence and decode it as UTF-8."""
        length = self.varint()
        view = self.read(length)
        return str(view, "utf-8")
