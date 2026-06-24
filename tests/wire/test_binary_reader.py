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

from protobuf._wire import BinaryReader, Tag, WireType


def test_tag_accepts_uint32_max_encoding() -> None:
    data = b"\xfd\xff\xff\xff\x0f"
    reader = BinaryReader(memoryview(data))

    assert reader.tag() == Tag(((1 << 29) - 1) << 3 | WireType.BIT32)


def test_tag_rejects_value_above_uint32() -> None:
    data = b"\x88\x80\x80\x80\x40"
    reader = BinaryReader(memoryview(data))

    with pytest.raises(ValueError, match="invalid varint"):
        reader.tag()
