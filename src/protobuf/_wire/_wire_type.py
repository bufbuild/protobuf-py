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

from enum import IntEnum
from typing import final


@final
class WireType(IntEnum):
    """Wire types as defined in the Protocol Buffers encoding."""

    VARINT = 0
    """Used for int32, int64, uint32, uint64, sint32, sint64, bool, enum."""

    BIT64 = 1
    """Used for fixed64, sfixed64, double. Always 8 bytes with little-endian byte order."""

    LENGTH_DELIMITED = 2
    """Used for string, bytes, embedded messages, packed repeated fields.

    Only repeated numeric types (types which use the varint, 32-bit,
    or 64-bit wire types) can be packed. In proto3, such fields are
    packed by default.
    """

    SGROUP = 3
    """Group start."""

    EGROUP = 4
    """Group end."""

    BIT32 = 5
    """Used for fixed32, sfixed32, float. Always 4 bytes with little-endian byte order."""
