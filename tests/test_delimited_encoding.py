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

import pytest

from protobuf import Oneof
from protobuf._wire import BinaryReader, BinaryWriter, Tag, WireType

from .gen.delimited_encoding_pb import DelimitedEncoding

Msg = DelimitedEncoding.Msg


def test_singular() -> None:
    msg = DelimitedEncoding(singular=Msg(value=1))
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    assert r.tag() == Tag(2 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(1 << 3 | WireType.VARINT)
    assert r.int32() == 1
    assert r.tag() == Tag(2 << 3 | WireType.EGROUP)
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_nested() -> None:
    msg = DelimitedEncoding(singular=Msg(value=1, child=Msg(value=2)))
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    # outer: singular (field 2) SGROUP
    assert r.tag() == Tag(2 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(1 << 3 | WireType.VARINT)
    assert r.int32() == 1
    # inner: child (field 2 of Msg) SGROUP
    assert r.tag() == Tag(2 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(1 << 3 | WireType.VARINT)
    assert r.int32() == 2
    # closes child (field 2 of Msg)
    assert r.tag() == Tag(2 << 3 | WireType.EGROUP)
    # closes singular (field 2 of DelimitedEncoding)
    assert r.tag() == Tag(2 << 3 | WireType.EGROUP)
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_repeated() -> None:
    msg = DelimitedEncoding(repeated=[Msg(value=1), Msg(value=2)])
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    # first element
    assert r.tag() == Tag(3 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(1 << 3 | WireType.VARINT)
    assert r.int32() == 1
    assert r.tag() == Tag(3 << 3 | WireType.EGROUP)
    # second element
    assert r.tag() == Tag(3 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(1 << 3 | WireType.VARINT)
    assert r.int32() == 2
    assert r.tag() == Tag(3 << 3 | WireType.EGROUP)
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_oneof_message() -> None:
    msg = DelimitedEncoding(choice=Oneof(field="choice_message", value=Msg(value=1)))
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    assert r.tag() == Tag(8 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(1 << 3 | WireType.VARINT)
    assert r.int32() == 1
    assert r.tag() == Tag(8 << 3 | WireType.EGROUP)
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_length_prefixed_override() -> None:
    msg = DelimitedEncoding(length_prefixed=Msg(value=1))
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    # field 4 must use LENGTH_DELIMITED, not SGROUP
    assert r.tag() == Tag(4 << 3 | WireType.LENGTH_DELIMITED)
    length = r.varint()
    assert length == len(Msg(value=1).to_binary())
    r.read(length)
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_message_map() -> None:
    msg = DelimitedEncoding(message_map={"k": Msg(value=1)})
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    # map entry (field 5) is always LENGTH_DELIMITED
    assert r.tag() == Tag(5 << 3 | WireType.LENGTH_DELIMITED)
    entry_len = r.varint()
    entry_start = r.offset

    # key (field 1)
    assert r.tag() == Tag(1 << 3 | WireType.LENGTH_DELIMITED)
    assert r.string() == "k"

    # value (field 2) — message value inside map is also LENGTH_DELIMITED
    assert r.tag() == Tag(2 << 3 | WireType.LENGTH_DELIMITED)
    value_len = r.varint()
    assert value_len > 0
    r.read(value_len)

    assert r.offset == entry_start + entry_len
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_scalar_map() -> None:
    msg = DelimitedEncoding(scalar_map={"k": 42})
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    # map entry (field 6) is LENGTH_DELIMITED
    assert r.tag() == Tag(6 << 3 | WireType.LENGTH_DELIMITED)
    entry_len = r.varint()
    entry_start = r.offset

    # key (field 1)
    assert r.tag() == Tag(1 << 3 | WireType.LENGTH_DELIMITED)
    assert r.string() == "k"

    # value (field 2)
    assert r.tag() == Tag(2 << 3 | WireType.VARINT)
    assert r.int32() == 42

    assert r.offset == entry_start + entry_len
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_empty_delimited_message() -> None:
    msg = DelimitedEncoding(singular=Msg())
    data = msg.to_binary()
    r = BinaryReader(memoryview(data))

    # empty message: bare SGROUP/EGROUP with no content between them
    assert r.tag() == Tag(2 << 3 | WireType.SGROUP)
    assert r.tag() == Tag(2 << 3 | WireType.EGROUP)
    assert r.offset == len(data)

    assert DelimitedEncoding.from_binary(data) == msg


def test_mismatched_egroup() -> None:
    # Craft binary with SGROUP for field 2 but EGROUP for field 3
    w = BinaryWriter()
    w.tag(2, WireType.SGROUP)
    w.tag(3, WireType.EGROUP)
    data = w.finish()

    with pytest.raises(ValueError, match="mismatched group"):
        DelimitedEncoding.from_binary(data)


def test_all_fields_roundtrip() -> None:
    msg = DelimitedEncoding(
        name="a",
        singular=Msg(value=1),
        repeated=[Msg(value=2), Msg(value=3, child=Msg(value=4))],
        length_prefixed=Msg(value=5),
        message_map={"x": Msg(value=6)},
        scalar_map={"y": 7},
        choice=Oneof(field="choice_message", value=Msg(value=8)),
    )
    assert DelimitedEncoding.from_binary(msg.to_binary()) == msg
