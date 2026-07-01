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

from datetime import datetime, timedelta, timezone, tzinfo
from time import time_ns
from typing import TYPE_CHECKING, TypeVar

from ._const import (
    EPOCH_DATETIME_AWARE,
    EPOCH_DATETIME_NAIVE,
    MAX_NANOS,
    MICROSECOND_DELTA,
    MIN_NANOS,
    SECOND_AS_NANOS,
)

Self = TypeVar("Self", bound="TimestampMixin")


class TimestampMixin:
    __slots__ = ()

    if TYPE_CHECKING:

        def __init__(self, *, seconds: int = 0, nanos: int = 0) -> None: ...

        seconds: int
        nanos: int

    @classmethod
    def now(cls: type[Self]) -> Self:
        """Create for the current time."""
        return cls.from_nanos(time_ns())

    @classmethod
    def from_nanos(cls: type[Self], nanos: int, /) -> Self:
        """Create from a Unix timestamp in nanoseconds."""
        if nanos > MAX_NANOS or nanos < MIN_NANOS:
            msg = "seconds out of range"
            raise OverflowError(msg)
        return cls(seconds=nanos // SECOND_AS_NANOS, nanos=nanos % SECOND_AS_NANOS)

    @classmethod
    def from_datetime(cls: type[Self], dt: datetime, /) -> Self:
        """Create from the given datetime."""
        return cls.from_nanos(
            ((dt.astimezone(timezone.utc) - EPOCH_DATETIME_AWARE) // MICROSECOND_DELTA) * 1000
        )

    def to_datetime(self, tzinfo: tzinfo | None = None) -> datetime:
        """Convert to a datetime.

        Args:
            tzinfo: A datetime.tzinfo subclass; defaults to None.

        Returns:
            If tzinfo is None, returns a timezone-naive UTC datetime (with no timezone
            information, i.e. not aware that it's UTC).

            Otherwise, returns a timezone-aware datetime in the input timezone.
        """
        delta = timedelta(seconds=self.seconds, microseconds=round(self.nanos / 1000)

        if tzinfo is None:
            return EPOCH_DATETIME_NAIVE + delta
        else:
            return (EPOCH_DATETIME_AWARE + delta).astimezone(tzinfo)

    def to_nanos(self) -> int:
        """Convert to the number of nanoseconds since Unix epoch 1970-01-01T00:00:00Z.

        Examples:
            >>> from protobuf.wkt import Timestamp
            >>> Timestamp(nanos=1_000).to_nanos()
            1000
            >>> Timestamp(seconds=10, nanos=100).to_nanos()
            10000000100
        """
        return self.seconds * SECOND_AS_NANOS + self.nanos

    def to_seconds(self) -> float:
        """Convert to a number of seconds since Unix epoch 1970-01-01T00:00:00Z.

        Parts of a second are expressed as fractional values.

        Examples:
            >>> from protobuf.wkt import Timestamp
            >>> Timestamp(seconds=10).to_seconds()
            10.0
            >>> Timestamp(nanos=100).to_seconds()
            1e-07
            >>> Timestamp(seconds=10, nanos=100).to_seconds()
            10.0000001
        """
        return self.seconds + self.nanos / SECOND_AS_NANOS

    @classmethod
    def from_seconds(cls: type[Self], seconds: float, /) -> Self:
        """Create a new Timestamp from a timestamp expressed in seconds since Unix epoch 1970-01-01T00:00:00Z.

        Parts of a second are expressed as fractional values.

        Examples:
            >>> from protobuf.wkt import Timestamp
            >>> Timestamp.from_seconds(10)
            Timestamp(seconds=10)
            >>> Timestamp.from_seconds(10.1)
            Timestamp(seconds=10, nanos=100000000)
            >>> Timestamp.from_seconds(-10.1)
            Timestamp(seconds=-11, nanos=900000000)
        """
        nanos = round(seconds * SECOND_AS_NANOS)
        return cls.from_nanos(nanos)
        # OverflowError: date value out of range
