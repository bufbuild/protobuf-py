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
import struct

import pytest

from protobuf._wire import BinaryReader, BinaryWriter, Tag, WireType


@pytest.mark.parametrize(
    ("field_number", "wire_type", "expected"),
    [
        (1, WireType.VARINT, b"\x08"),
        (2, WireType.LENGTH_DELIMITED, b"\x12"),
        (536870911, WireType.VARINT, b"\xf8\xff\xff\xff\x0f"),
    ],
)
def test_tag(field_number: int, wire_type: WireType, expected: bytes) -> None:
    w = BinaryWriter()
    w.tag(field_number, wire_type)
    data = w.finish()
    assert data == expected

    r = BinaryReader(memoryview(data))
    assert r.tag() == Tag(field_number << 3 | wire_type)
    assert r.offset == len(data)


def test_fork_join_nested() -> None:
    w = BinaryWriter()
    w.tag(1, WireType.LENGTH_DELIMITED)
    w.fork()
    w.tag(1, WireType.LENGTH_DELIMITED)
    w.fork()
    w.uint64(7)
    w.join()
    w.join()
    data = w.finish()
    assert data == b"\x0a\x03\x0a\x01\x07"

    r = BinaryReader(memoryview(data))
    assert r.tag() == Tag(1 << 3 | WireType.LENGTH_DELIMITED)
    assert r.varint() == 3  # outer length
    assert r.tag() == Tag(1 << 3 | WireType.LENGTH_DELIMITED)
    assert r.varint() == 1  # inner length
    assert r.uint64() == 7
    assert r.offset == len(data)


def test_join_without_fork_raises() -> None:
    w = BinaryWriter()
    with pytest.raises(
        RuntimeError, match="join\\(\\) called without a matching fork\\(\\)"
    ):
        w.join()


def test_finish_with_unclosed_fork_raises() -> None:
    w = BinaryWriter()
    w.fork()
    with pytest.raises(
        RuntimeError, match="finish\\(\\) called with 1 unclosed fork\\(\\)"
    ):
        w.finish()


def test_int32() -> None:
    w = BinaryWriter()
    w.int32(0)
    w.int32(1)
    w.int32(-1)
    w.int32(-(1 << 31))
    data = w.finish()
    assert (
        data
        == b"\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x80\x80\x80\x80\xf8\xff\xff\xff\xff\x01"
    )

    r = BinaryReader(memoryview(data))
    assert r.int32() == 0
    assert r.int32() == 1
    assert r.int32() == -1
    assert r.int32() == -(1 << 31)
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="int32"):
        BinaryWriter().int32(-(1 << 31) - 1)
    with pytest.raises(ValueError, match="int32"):
        BinaryWriter().int32(1 << 31)


def test_int64() -> None:
    w = BinaryWriter()
    w.int64(0)
    w.int64(1)
    w.int64(-1)
    w.int64(-(1 << 63))
    data = w.finish()
    assert (
        data
        == b"\x00\x01\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x80\x80\x80\x80\x80\x80\x80\x80\x80\x01"
    )

    r = BinaryReader(memoryview(data))
    assert r.int64() == 0
    assert r.int64() == 1
    assert r.int64() == -1
    assert r.int64() == -(1 << 63)
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="int64"):
        BinaryWriter().int64(-(1 << 63) - 1)
    with pytest.raises(ValueError, match="int64"):
        BinaryWriter().int64(1 << 63)


def test_uint32() -> None:
    w = BinaryWriter()
    w.uint32(0)
    w.uint32((1 << 32) - 1)
    data = w.finish()
    assert data == b"\x00\xff\xff\xff\xff\x0f"

    r = BinaryReader(memoryview(data))
    assert r.uint32() == 0
    assert r.uint32() == (1 << 32) - 1
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="uint32"):
        BinaryWriter().uint32(-1)
    with pytest.raises(ValueError, match="uint32"):
        BinaryWriter().uint32(1 << 32)


def test_uint64() -> None:
    w = BinaryWriter()
    w.uint64(0)
    w.uint64((1 << 64) - 1)
    data = w.finish()
    assert data == b"\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01"

    r = BinaryReader(memoryview(data))
    assert r.uint64() == 0
    assert r.uint64() == (1 << 64) - 1
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="uint64"):
        BinaryWriter().uint64(-1)
    with pytest.raises(ValueError, match="uint64"):
        BinaryWriter().uint64(1 << 64)


def test_sint32() -> None:
    w = BinaryWriter()
    w.sint32(0)
    w.sint32(-1)
    w.sint32(1)
    w.sint32(-(1 << 31))
    w.sint32((1 << 31) - 1)
    data = w.finish()
    assert data == b"\x00\x01\x02\xff\xff\xff\xff\x0f\xfe\xff\xff\xff\x0f"

    r = BinaryReader(memoryview(data))
    assert r.sint32() == 0
    assert r.sint32() == -1
    assert r.sint32() == 1
    assert r.sint32() == -(1 << 31)
    assert r.sint32() == (1 << 31) - 1
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="sint32"):
        BinaryWriter().sint32(-(1 << 31) - 1)
    with pytest.raises(ValueError, match="sint32"):
        BinaryWriter().sint32(1 << 31)


def test_sint64() -> None:
    w = BinaryWriter()
    w.sint64(0)
    w.sint64(-1)
    w.sint64(1)
    w.sint64(-(1 << 63))
    w.sint64((1 << 63) - 1)
    data = w.finish()
    assert (
        data
        == b"\x00\x01\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\xfe\xff\xff\xff\xff\xff\xff\xff\xff\x01"
    )

    r = BinaryReader(memoryview(data))
    assert r.sint64() == 0
    assert r.sint64() == -1
    assert r.sint64() == 1
    assert r.sint64() == -(1 << 63)
    assert r.sint64() == (1 << 63) - 1
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="sint64"):
        BinaryWriter().sint64(-(1 << 63) - 1)
    with pytest.raises(ValueError, match="sint64"):
        BinaryWriter().sint64(1 << 63)


def test_float() -> None:
    w = BinaryWriter()
    w.float_(0.0)
    w.float_(1.5)
    w.float_(float("inf"))
    w.float_(float("nan"))
    data = w.finish()
    assert data[:4] == struct.pack("<f", 0.0)
    assert data[4:8] == struct.pack("<f", 1.5)
    assert data[8:12] == struct.pack("<f", float("inf"))
    assert data[12:16] == struct.pack("<f", float("nan"))

    r = BinaryReader(memoryview(data))
    assert r.float_() == 0.0
    assert r.float_() == 1.5
    assert r.float_() == float("inf")
    assert math.isnan(r.float_())
    assert r.offset == len(data)


def test_double() -> None:
    w = BinaryWriter()
    w.double(0.0)
    w.double(1.5)
    w.double(float("-inf"))
    w.double(float("nan"))
    data = w.finish()
    assert data[:8] == struct.pack("<d", 0.0)
    assert data[8:16] == struct.pack("<d", 1.5)
    assert data[16:24] == struct.pack("<d", float("-inf"))
    assert data[24:32] == struct.pack("<d", float("nan"))

    r = BinaryReader(memoryview(data))
    assert r.double() == 0.0
    assert r.double() == 1.5
    assert r.double() == float("-inf")
    assert math.isnan(r.double())
    assert r.offset == len(data)


def test_fixed32() -> None:
    w = BinaryWriter()
    w.fixed32(0)
    w.fixed32((1 << 32) - 1)
    data = w.finish()
    assert data == struct.pack("<I", 0) + struct.pack("<I", (1 << 32) - 1)

    r = BinaryReader(memoryview(data))
    assert r.fixed32() == 0
    assert r.fixed32() == (1 << 32) - 1
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="fixed32"):
        BinaryWriter().fixed32(-1)
    with pytest.raises(ValueError, match="fixed32"):
        BinaryWriter().fixed32(1 << 32)


def test_sfixed32() -> None:
    w = BinaryWriter()
    w.sfixed32(0)
    w.sfixed32(-1)
    w.sfixed32(-(1 << 31))
    data = w.finish()
    assert data == struct.pack("<i", 0) + struct.pack("<i", -1) + struct.pack(
        "<i", -(1 << 31)
    )

    r = BinaryReader(memoryview(data))
    assert r.sfixed32() == 0
    assert r.sfixed32() == -1
    assert r.sfixed32() == -(1 << 31)
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="sfixed32"):
        BinaryWriter().sfixed32(-(1 << 31) - 1)
    with pytest.raises(ValueError, match="sfixed32"):
        BinaryWriter().sfixed32(1 << 31)


def test_fixed64() -> None:
    w = BinaryWriter()
    w.fixed64(0)
    w.fixed64((1 << 64) - 1)
    data = w.finish()
    assert data == struct.pack("<Q", 0) + struct.pack("<Q", (1 << 64) - 1)

    r = BinaryReader(memoryview(data))
    assert r.fixed64() == 0
    assert r.fixed64() == (1 << 64) - 1
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="fixed64"):
        BinaryWriter().fixed64(-1)
    with pytest.raises(ValueError, match="fixed64"):
        BinaryWriter().fixed64(1 << 64)


def test_sfixed64() -> None:
    w = BinaryWriter()
    w.sfixed64(0)
    w.sfixed64(-1)
    w.sfixed64(-(1 << 63))
    data = w.finish()
    assert data == struct.pack("<q", 0) + struct.pack("<q", -1) + struct.pack(
        "<q", -(1 << 63)
    )

    r = BinaryReader(memoryview(data))
    assert r.sfixed64() == 0
    assert r.sfixed64() == -1
    assert r.sfixed64() == -(1 << 63)
    assert r.offset == len(data)

    with pytest.raises(ValueError, match="sfixed64"):
        BinaryWriter().sfixed64(-(1 << 63) - 1)
    with pytest.raises(ValueError, match="sfixed64"):
        BinaryWriter().sfixed64(1 << 63)


def test_bool() -> None:
    w = BinaryWriter()
    w.bool_(False)
    w.bool_(True)
    data = w.finish()
    assert data == b"\x00\x01"

    r = BinaryReader(memoryview(data))
    assert r.bool_() is False
    assert r.bool_() is True
    assert r.offset == len(data)


def test_string() -> None:
    w = BinaryWriter()
    w.string("")
    w.string("hello")
    data = w.finish()
    assert data == b"\x00\x05hello"

    r = BinaryReader(memoryview(data))
    assert r.string() == ""
    assert r.string() == "hello"
    assert r.offset == len(data)


def test_bytes() -> None:
    w = BinaryWriter()
    w.bytes_(b"")
    w.bytes_(b"hello")
    data = w.finish()
    assert data == b"\x00\x05hello"

    r = BinaryReader(memoryview(data))
    assert r.bytes_() == b""
    assert r.bytes_() == b"hello"
    assert r.offset == len(data)
