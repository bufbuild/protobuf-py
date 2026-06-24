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

from protobuf.wkt import FileOptions
from tests.gen.extensions_proto3_pb import (
    Proto3ExtMessage,
    ext_message_ext,
    ext_optional_uint32_ext,
    ext_packed_uint32_ext,
    ext_uint32_ext,
    ext_unpacked_uint32_ext,
)


def test_scalar_set_and_get() -> None:
    msg = FileOptions()
    msg[ext_uint32_ext] = 123
    assert ext_uint32_ext in msg
    assert msg[ext_uint32_ext] == 123


def test_scalar_default() -> None:
    msg = FileOptions()
    assert ext_uint32_ext not in msg
    assert msg[ext_uint32_ext] == 0


def test_optional_scalar_set_and_get() -> None:
    msg = FileOptions()
    msg[ext_optional_uint32_ext] = 0
    assert ext_optional_uint32_ext in msg
    assert msg[ext_optional_uint32_ext] == 0


def test_message_set_and_get() -> None:
    msg = FileOptions()
    msg[ext_message_ext] = Proto3ExtMessage(string_field="hello")
    assert ext_message_ext in msg
    assert msg[ext_message_ext] == Proto3ExtMessage(string_field="hello")


def test_packed_repeated() -> None:
    msg = FileOptions()
    msg[ext_packed_uint32_ext] = [1, 2, 3]
    assert msg[ext_packed_uint32_ext] == [1, 2, 3]


def test_unpacked_repeated() -> None:
    msg = FileOptions()
    msg[ext_unpacked_uint32_ext] = [4, 5, 6]
    assert msg[ext_unpacked_uint32_ext] == [4, 5, 6]


def test_round_trip() -> None:
    msg = FileOptions()
    msg[ext_uint32_ext] = 42
    msg[ext_optional_uint32_ext] = 99
    msg[ext_packed_uint32_ext] = [1, 2]
    msg[ext_message_ext] = Proto3ExtMessage(string_field="hi")
    msg2 = FileOptions.from_binary(msg.to_binary())
    assert msg2[ext_uint32_ext] == 42
    assert msg2[ext_optional_uint32_ext] == 99
    assert msg2[ext_packed_uint32_ext] == [1, 2]
    assert msg2[ext_message_ext] == Proto3ExtMessage(string_field="hi")


def test_clear() -> None:
    msg = FileOptions()
    msg[ext_uint32_ext] = 42
    del msg[ext_uint32_ext]
    assert ext_uint32_ext not in msg
    assert msg[ext_uint32_ext] == 0


def test_extensions_always_have_presence() -> None:
    # Unlike regular proto3 fields, extensions always have explicit presence.
    # Setting a zero value still creates presence for both implicit and
    # optional extensions.
    msg = FileOptions()
    msg[ext_uint32_ext] = 0
    assert ext_uint32_ext in msg
    assert msg[ext_uint32_ext] == 0
    msg[ext_optional_uint32_ext] = 0
    assert ext_optional_uint32_ext in msg
    assert msg[ext_optional_uint32_ext] == 0
    # Both survive round-trip
    msg2 = FileOptions.from_binary(msg.to_binary())
    assert ext_uint32_ext in msg2
    assert ext_optional_uint32_ext in msg2
