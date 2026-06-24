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

import datetime
import time
from datetime import timezone

import pytest

from protobuf.wkt import Timestamp


def test_timestamp_to_from_seconds() -> None:
    assert Timestamp.from_seconds(123) == Timestamp(seconds=123)
    assert Timestamp.from_seconds(123.1) == Timestamp(seconds=123, nanos=100_000_000)
    # test round trip
    assert Timestamp.from_seconds(123.1).to_seconds() == 123.1
    # test negatives
    assert Timestamp.from_seconds(-123) == Timestamp(seconds=-123)
    assert Timestamp.from_seconds(-123.1) == Timestamp(seconds=-124, nanos=900_000_000)
    assert Timestamp.from_seconds(-123.1).to_seconds() == -123.1
    # test floating point edge cases
    assert Timestamp.from_seconds(1.9999999996) == Timestamp(seconds=2)
    # test the biggest legal value (floating point inaccuracy doesn't let you get a larger fractional value)
    assert (
        Timestamp.from_seconds(253402300799.9999).to_datetime().isoformat()
        == "9999-12-31T23:59:59.999902+00:00"
    )
    # test the smallest legal value
    # 0001-01-01 00:00:00 +0000 UTC -62135596800
    assert (
        Timestamp.from_seconds(-62135596800).to_datetime().isoformat()
        == "0001-01-01T00:00:00+00:00"
    )
    # test out of bounds
    try:
        Timestamp.from_seconds(253402300799.99999)
        pytest.fail("Timestamp.from_seconds should fail")
    except OverflowError:
        pass
    try:
        Timestamp.from_seconds(-62135596800.1)
        pytest.fail("Timestamp.from_seconds should fail")
    except OverflowError:
        pass


def test_timestamp_to_from_nanos() -> None:
    assert Timestamp.from_nanos(123) == Timestamp(nanos=123)
    assert Timestamp.from_nanos(8_000_000_000) == Timestamp(seconds=8)
    assert Timestamp.from_nanos(8_000_000_001) == Timestamp(seconds=8, nanos=1)

    assert Timestamp.from_nanos(123).to_nanos() == 123
    assert Timestamp.from_nanos(8_000_000_000).to_nanos() == 8_000_000_000
    assert Timestamp.from_nanos(8_000_000_001).to_nanos() == 8_000_000_001
    # test the biggest legal value (datetime won't allow a bigger value)
    assert (
        Timestamp.from_nanos(253_402_300_799_999_999_000).to_datetime().isoformat()
        == "9999-12-31T23:59:59.999999+00:00"
    )
    # test the smallest legal value
    # 0001-01-01 00:00:00 +0000 UTC -62135596800
    assert (
        Timestamp.from_nanos(-62_135_596_800_000_000_000).to_datetime().isoformat()
        == "0001-01-01T00:00:00+00:00"
    )
    # test out of bounds
    try:
        Timestamp.from_nanos(253_402_300_799_999_999_001)
        pytest.fail("Timestamp.from_seconds should fail")
    except OverflowError:
        pass
    try:
        Timestamp.from_nanos(-62_135_596_800_000_000_001)
        pytest.fail("Timestamp.from_seconds should fail")
    except OverflowError:
        pass


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        (Timestamp(), datetime.datetime(1970, 1, 1, tzinfo=timezone.utc)),
        (
            Timestamp(seconds=818035920, nanos=123456789),
            datetime.datetime(1970, 1, 1, tzinfo=timezone.utc)
            + datetime.timedelta(seconds=818035920, microseconds=123457),
        ),
    ],
)
def test_timestamp_to_datetime(
    timestamp: Timestamp, expected: datetime.datetime
) -> None:
    assert timestamp.to_datetime() == expected


@pytest.mark.parametrize(
    ("nanos", "expected"),
    [
        (0, Timestamp()),
        (818_035_920_123_000_000, Timestamp(seconds=818035920, nanos=123_000_000)),
        (1_000_000_000, Timestamp(seconds=1)),
        (1_020_000_000, Timestamp(seconds=1, nanos=20_000_000)),
        (-1_070_000_000, Timestamp(seconds=-2, nanos=930_000_000)),
        (-1_000_000_000, Timestamp(seconds=-1)),
    ],
)
def test_timestamp_from_unix_nanos(nanos: int, expected: Timestamp) -> None:
    actual = Timestamp.from_nanos(nanos)
    assert actual.seconds == expected.seconds
    assert actual.nanos == expected.nanos


def test_timestamp_now() -> None:
    lower_limit = time.time_ns()
    ts = Timestamp.now()
    upper_limit = time.time_ns()
    assert ts.seconds * 1_000_000_000 + ts.nanos <= upper_limit
    assert ts.seconds * 1_000_000_000 + ts.nanos >= lower_limit


@pytest.mark.parametrize(
    ("timestamp", "expected_json"),
    [
        (
            Timestamp(seconds=1765894940, nanos=123456789),
            '"2025-12-16T14:22:20.123456789Z"',
        ),
        (
            Timestamp(seconds=1765894940, nanos=123456000),
            '"2025-12-16T14:22:20.123456Z"',
        ),
        (Timestamp(seconds=1765894940, nanos=123000000), '"2025-12-16T14:22:20.123Z"'),
        (Timestamp(seconds=1765894940, nanos=0), '"2025-12-16T14:22:20Z"'),
        (
            Timestamp(seconds=-30607358094, nanos=789123456),
            '"1000-02-03T04:05:06.789123456Z"',
        ),
        (Timestamp(seconds=1, nanos=100), '"1970-01-01T00:00:01.000000100Z"'),
    ],
)
def test_timestamp_json(timestamp: Timestamp, expected_json: str) -> None:
    assert timestamp.to_json() == expected_json
    assert Timestamp.from_json(expected_json) == timestamp
