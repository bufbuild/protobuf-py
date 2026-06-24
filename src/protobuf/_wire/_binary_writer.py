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
from typing import TYPE_CHECKING, final

if TYPE_CHECKING:
    from ._wire_type import WireType


def _append_varint(buf: bytearray, value: int) -> None:
    """Append varint-encoded bytes to buf."""
    while value > 0x7F:
        buf.append((value & 0x7F) | 0x80)
        value >>= 7
    buf.append(value & 0x7F)


@final
class BinaryWriter:
    """A writer for serializing Protocol Buffer wire format.

    Length-delimited message fields are handled with `fork()`/`join()` pairs.
    Each `fork()` opens a new scope — the writing context for one sub-message —
    and reserves a placeholder for the length varint whose value is not yet
    known. Each `join()` closes the scope, fills in the placeholder with the
    actual byte count, and returns to the enclosing scope.

    All scopes share a single flat chunk list. Each chunk is appended exactly
    once and never moved or copied, giving O(n) total work where n is the
    number of bytes serialized.
    """

    def __init__(self) -> None:
        # The output of the writer will be the concatenation of all chunks in this list.
        self._chunks: list[bytes | bytearray] = []

        # Accumulation buffer for small writes; flushed to _chunks at structural boundaries.
        self._buf: bytearray = bytearray()

        # Number of bytes written in the current scope (resets to 0 on fork()).
        self._size: int = 0

        # Stack of (placeholder_idx, parent_size): pushed by fork(), popped by join().
        self._stack: list[tuple[int, int]] = []

    def _flush(self) -> None:
        """Move the accumulation buffer into _chunks if non-empty, updating size."""
        if self._buf:
            self._size += len(self._buf)
            self._chunks.append(self._buf)
            self._buf = bytearray()

    def fork(self) -> None:
        """Open a new scope for a length-delimited sub-message field.

        Reserves a placeholder for the length varint and saves the current
        scope on the stack. Subsequent writes accumulate into the new scope.
        Must be paired with a call to join().
        """
        self._flush()
        placeholder_idx = len(self._chunks)
        self._chunks.append(b"")  # placeholder for the length varint
        self._stack.append((placeholder_idx, self._size))
        self._size = 0

    def join(self) -> None:
        """Close the current scope and finalize the sub-message length.

        Fills the placeholder reserved by `fork()` with the actual byte count of
        the scope, then restores the enclosing scope.
        """
        if not self._stack:
            msg = "join() called without a matching fork()"
            raise RuntimeError(msg)
        self._flush()
        placeholder_idx, parent_size = self._stack.pop()
        sub_size = self._size
        length_varint = bytearray()
        _append_varint(length_varint, sub_size)
        self._chunks[placeholder_idx] = length_varint
        self._size = parent_size + len(length_varint) + sub_size

    def finish(self) -> bytes:
        """Return the serialized bytes.

        Returns:
            The complete serialized message as bytes.
        """
        if self._stack:
            msg = f"finish() called with {len(self._stack)} unclosed fork()"
            raise RuntimeError(msg)
        self._flush()
        return b"".join(self._chunks)

    def _varint(self, value: int) -> None:
        _append_varint(self._buf, value)

    def tag(self, number: int, wire_type: WireType) -> None:
        """Write a field tag (field number + wire type).

        Args:
            number: The field number.
            wire_type: The wire type for the field.
        """
        self.uint32((number << 3) | wire_type)

    def bool_(self, value: bool) -> None:  # noqa: FBT001
        """Write a boolean as a varint.

        Args:
            value: The boolean to encode.
        """
        self._varint(int(value))

    def int32(self, value: int) -> None:
        """Write a signed 32-bit integer as a varint.

        Negative values are encoded using two's complement.

        Args:
            value: The signed 32-bit integer to encode.
        """
        if value < -(1 << 31) or value >= (1 << 31):
            msg = f"value out of range for int32: {value}"
            raise ValueError(msg)
        self._varint(value % (1 << 64))

    def int64(self, value: int) -> None:
        """Write a signed 64-bit integer as a varint.

        Negative values are encoded using two's complement.

        Args:
            value: The signed 64-bit integer to encode.
        """
        if value < -(1 << 63) or value >= (1 << 63):
            msg = f"value out of range for int64: {value}"
            raise ValueError(msg)
        self._varint(value % (1 << 64))

    def uint32(self, value: int) -> None:
        """Write an unsigned 32-bit integer as a varint.

        Args:
            value: The unsigned 32-bit integer to encode.
        """
        if value < 0 or value >= (1 << 32):
            msg = f"value out of range for uint32: {value}"
            raise ValueError(msg)
        self._varint(value)

    def uint64(self, value: int) -> None:
        """Write an unsigned 64-bit integer as a varint.

        Args:
            value: The unsigned 64-bit integer to encode.
        """
        if value < 0 or value >= (1 << 64):
            msg = f"value out of range for uint64: {value}"
            raise ValueError(msg)
        self._varint(value)

    def sint32(self, value: int) -> None:
        """Write a signed 32-bit integer as a zigzag-encoded varint.

        Args:
            value: The signed 32-bit integer to encode.
        """
        if value < -(1 << 31) or value >= (1 << 31):
            msg = f"value out of range for sint32: {value}"
            raise ValueError(msg)
        self._varint((value << 1) ^ (value >> 31))

    def sint64(self, value: int) -> None:
        """Write a signed 64-bit integer as a zigzag-encoded varint.

        Args:
            value: The signed 64-bit integer to encode.
        """
        if value < -(1 << 63) or value >= (1 << 63):
            msg = f"value out of range for sint64: {value}"
            raise ValueError(msg)
        self._varint((value << 1) ^ (value >> 63))

    def fixed32(self, value: int) -> None:
        """Write an unsigned 32-bit integer in fixed-width format.

        Args:
            value: The unsigned 32-bit integer to encode.
        """
        if value < 0 or value >= (1 << 32):
            msg = f"value out of range for fixed32: {value}"
            raise ValueError(msg)
        self._buf += struct.pack("<I", value)

    def sfixed32(self, value: int) -> None:
        """Write a signed 32-bit integer in fixed-width format.

        Args:
            value: The signed 32-bit integer to encode.
        """
        if value < -(1 << 31) or value >= (1 << 31):
            msg = f"value out of range for sfixed32: {value}"
            raise ValueError(msg)
        self._buf += struct.pack("<i", value)

    def fixed64(self, value: int) -> None:
        """Write an unsigned 64-bit integer in fixed-width format.

        Args:
            value: The unsigned 64-bit integer to encode.
        """
        if value < 0 or value >= (1 << 64):
            msg = f"value out of range for fixed64: {value}"
            raise ValueError(msg)
        self._buf += struct.pack("<Q", value)

    def sfixed64(self, value: int) -> None:
        """Write a signed 64-bit integer in fixed-width format.

        Args:
            value: The signed 64-bit integer to encode.
        """
        if value < -(1 << 63) or value >= (1 << 63):
            msg = f"value out of range for sfixed64: {value}"
            raise ValueError(msg)
        self._buf += struct.pack("<q", value)

    def float_(self, value: float) -> None:
        """Write a 32-bit floating point number.

        Args:
            value: The float to encode.
        """
        self._buf += struct.pack("<f", value)

    def double(self, value: float) -> None:
        """Write a 64-bit floating point number.

        Args:
            value: The float to encode.
        """
        self._buf += struct.pack("<d", value)

    def bytes_(self, value: bytes) -> None:
        """Write a length-delimited byte sequence.

        Args:
            value: The bytes to encode.
        """
        self._varint(len(value))
        self._flush()
        self._size += len(value)
        self._chunks.append(value)

    def raw(self, value: bytes) -> None:
        """Write raw bytes directly to the output without any encoding.

        Args:
            value: The raw bytes to write.
        """
        self._flush()
        self._size += len(value)
        self._chunks.append(value)

    def string(self, value: str) -> None:
        """Write a length-delimited UTF-8 string.

        Args:
            value: The string to encode.
        """
        self.bytes_(value.encode("utf-8"))
