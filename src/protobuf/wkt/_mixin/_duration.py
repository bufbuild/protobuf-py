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

from datetime import timedelta
from typing import TYPE_CHECKING, TypeVar

from ._const import MICROSECOND_DELTA, SECOND_AS_NANOS

Self = TypeVar("Self", bound="DurationMixin")


class DurationMixin:
    __slots__ = ()

    if TYPE_CHECKING:

        def __init__(self, *, seconds: int = 0, nanos: int = 0) -> None: ...

        seconds: int
        nanos: int

    @classmethod
    def from_nanos(cls: type[Self], nanos: int, /) -> Self:
        """Create from a duration in nanoseconds."""
        sign = -1 if nanos < 0 else 1
        nanos = abs(nanos)
        return cls(
            seconds=(nanos // SECOND_AS_NANOS) * sign,
            nanos=(nanos % SECOND_AS_NANOS) * sign,
        )

    @classmethod
    def from_timedelta(cls: type[Self], td: timedelta, /) -> Self:
        """Create from the given timedelta."""
        return cls.from_nanos((td // MICROSECOND_DELTA) * 1000)

    def to_timedelta(self) -> timedelta:
        """Convert to a timedelta."""
        return timedelta(seconds=self.seconds, microseconds=round(self.nanos / 1000))

    def to_nanos(self) -> int:
        """Convert to the number of nanoseconds.

        Examples:
            >>> from protobuf.wkt import Duration
            >>> Duration(nanos=1_000).to_nanos()
            1000
            >>> Duration(seconds=10, nanos=100).to_nanos()
            10000000100
        """
        return self.seconds * SECOND_AS_NANOS + self.nanos

    def to_seconds(self) -> float:
        """Convert to a number of seconds.

        Parts of a second are expressed as fractional values.

        Examples:
            >>> from protobuf.wkt import Duration
            >>> Duration(seconds=10).to_seconds()
            10.0
            >>> Duration(nanos=100).to_seconds()
            1e-07
            >>> Duration(seconds=10, nanos=100).to_seconds()
            10.0000001
        """
        return self.seconds + self.nanos / SECOND_AS_NANOS

    @classmethod
    def from_seconds(cls: type[Self], seconds: float, /) -> Self:
        """Create a new Duration from a duration in seconds.

        Parts of a second are expressed as fractional values.

        Examples:
            >>> from protobuf.wkt import Duration
            >>> Duration.from_seconds(10)
            Duration(seconds=10)
            >>> Duration.from_seconds(10.1)
            Duration(seconds=10, nanos=100000000)
        """
        nanos = round(seconds * SECOND_AS_NANOS)
        return cls.from_nanos(nanos)
