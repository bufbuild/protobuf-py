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

import pytest

from .gen.delimited_encoding_pb import DelimitedEncoding
from .gen.maps_pb import Maps
from .gen.messages_pb import Recursive
from .gen.scalars_pb import Scalars

RECURSION_ERROR = "exceeded maximum recursion depth 100 while serializing message"


def generate_recursive(depth: int) -> Recursive:
    if depth == 0:
        return Recursive()
    return Recursive(recursive=generate_recursive(depth - 1))


def generate_recursive_msg(depth: int) -> DelimitedEncoding.Msg:
    if depth == 0:
        return DelimitedEncoding.Msg()
    return DelimitedEncoding.Msg(child=generate_recursive_msg(depth - 1))


def test_equals_recursion_limit() -> None:
    msg = generate_recursive(100)
    assert Recursive.from_binary(msg.to_binary()) == msg


@pytest.mark.parametrize(
    "msg",
    [
        pytest.param(
            Recursive(recursive=generate_recursive(100)), id="recursive field"
        ),
        pytest.param(
            Recursive(repeated_recursive=[generate_recursive(100)]), id="repeated field"
        ),
        pytest.param(
            Recursive(map_recursive={"a": generate_recursive(100)}), id="map field"
        ),
        pytest.param(
            DelimitedEncoding(singular=generate_recursive_msg(100)), id="group field"
        ),
    ],
)
def test_exceed_recursion_limit(msg: Recursive | DelimitedEncoding) -> None:
    with pytest.raises(RecursionError, match=RECURSION_ERROR):
        msg.to_binary()


@pytest.mark.parametrize("field", ["recursive", "repeated_recursive", "map_recursive"])
def test_cyclic_message(field: str) -> None:
    msg = Recursive()
    match field:
        case "recursive":
            msg.recursive = msg
        case "repeated_recursive":
            msg.repeated_recursive = [msg]
        case _:
            msg.map_recursive = {"a": msg}
    with pytest.raises(RecursionError, match=RECURSION_ERROR):
        msg.to_binary()


def test_cyclic_group() -> None:
    msg = DelimitedEncoding.Msg()
    msg.child = msg
    with pytest.raises(RecursionError, match=RECURSION_ERROR):
        msg.to_binary()


def test_map_entries_last_to_first() -> None:
    msg = Maps(int32_to_int32={1: 2, 3: 4})
    assert msg.to_binary() == b"\x0a\x04\x08\x03\x10\x04\x0a\x04\x08\x01\x10\x02"


def test_float_signaling_nan_is_quiet() -> None:
    signaling_nan = struct.unpack("<d", struct.pack("<Q", 0x7FF4_0000_0000_0000))[0]
    msg = Scalars(float_field=signaling_nan)
    assert msg.to_binary() == b"\x15\x00\x00\xe0\x7f"
