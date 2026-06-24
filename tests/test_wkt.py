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

from protobuf.wkt import Any, Duration, Timestamp

from .gen.scalars_pb import Scalars
from .gen.wkt_pb import WellKnownTypes


def test_wkt_roundtrip() -> None:
    s = Scalars(uint32_field=124)
    wkt = WellKnownTypes(
        any=Any.pack(s),
        duration=Duration(seconds=1234, nanos=123),
        timestamp=Timestamp(seconds=1234, nanos=123456789),
    )
    res = WellKnownTypes.from_binary(wkt.to_binary())
    assert res == wkt

    # Confirm special methods available on parsed message
    assert res.any is not None
    assert res.any.is_type(s.__class__)
    assert res.any.unpack(s.__class__) == s

    assert res.duration is not None
    assert res.duration.to_seconds() == 1234.000000123
    assert res.timestamp is not None
    assert res.timestamp.to_seconds() == 1234.123456789
