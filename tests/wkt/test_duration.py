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

import pytest

from protobuf.wkt import Duration


def test_duration_to_from_seconds() -> None:
    assert Duration.from_seconds(123) == Duration(seconds=123)
    assert Duration.from_seconds(123.1) == Duration(seconds=123, nanos=100_000_000)
    # test round trip
    assert Duration.from_seconds(123.1).to_seconds() == 123.1
    # test negatives
    assert Duration.from_seconds(-123) == Duration(seconds=-123)
    assert Duration.from_seconds(-123.1) == Duration(seconds=-123, nanos=-100_000_000)
    assert Duration.from_seconds(-123.1).to_seconds() == -123.1
    # test floating point edge cases
    assert Duration.from_seconds(1.9999999996) == Duration(seconds=2)


def test_duration_to_from_nanos() -> None:
    assert Duration.from_nanos(123) == Duration(nanos=123)
    assert Duration.from_nanos(8_000_000_000) == Duration(seconds=8)
    assert Duration.from_nanos(8_000_000_001) == Duration(seconds=8, nanos=1)

    assert Duration.from_nanos(123).to_nanos() == 123
    assert Duration.from_nanos(8_000_000_000).to_nanos() == 8_000_000_000
    assert Duration.from_nanos(8_000_000_001).to_nanos() == 8_000_000_001


@pytest.mark.parametrize(
    ("duration", "expected"),
    [
        (Duration(), datetime.timedelta()),
        (
            Duration(seconds=818035920, nanos=123456789),
            datetime.timedelta(seconds=818035920, microseconds=123457),
        ),
    ],
)
def test_duration_to_delta(duration: Duration, expected: datetime.timedelta) -> None:
    assert duration.to_timedelta() == expected


@pytest.mark.parametrize(
    ("us", "expected"),
    [
        (1_800_000, Duration(seconds=1, nanos=800_000_000)),
        (1_000_020, Duration(seconds=1, nanos=20_000)),
        (1_000_000, Duration(seconds=1)),
        (70, Duration(nanos=70_000)),
        (0, Duration()),
        (-70, Duration(nanos=-70_000)),
        (-1_000_000, Duration(seconds=-1)),
        (-1_000_020, Duration(seconds=-1, nanos=-20_000)),
        (-1_800_000, Duration(seconds=-1, nanos=-800_000_000)),
    ],
)
def test_duration_from_delta_micro(us: int, expected: Duration) -> None:
    actual = Duration.from_timedelta(datetime.timedelta(microseconds=us))
    assert actual.seconds == expected.seconds
    assert actual.nanos == expected.nanos


@pytest.mark.parametrize(
    ("duration", "expected_json"),
    [
        (Duration(seconds=1234, nanos=123456789), '"1234.123456789s"'),
        (Duration(seconds=1234, nanos=123456000), '"1234.123456s"'),
        (Duration(seconds=1234, nanos=123000000), '"1234.123s"'),
        (Duration(seconds=1234, nanos=0), '"1234s"'),
        (Duration(seconds=0, nanos=1), '"0.000000001s"'),
        (Duration(seconds=0, nanos=10), '"0.000000010s"'),
        (Duration(seconds=0, nanos=100), '"0.000000100s"'),
        (Duration(seconds=0, nanos=1000), '"0.000001s"'),
        (Duration(seconds=0, nanos=10000), '"0.000010s"'),
        (Duration(seconds=-10, nanos=-5000000), '"-10.005s"'),
        (Duration(seconds=0, nanos=-5000000), '"-0.005s"'),
    ],
)
def test_duration_json(duration: Duration, expected_json: str) -> None:
    assert duration.to_json() == expected_json
    assert Duration.from_json(expected_json) == duration
