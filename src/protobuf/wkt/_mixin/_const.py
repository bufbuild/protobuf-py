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

from datetime import datetime, timedelta, timezone

SECOND_AS_NANOS = 1_000_000_000
"""One second as nano seconds."""

NANOS_PER_SECOND_MAX = 999_999_999
"""Maximum nanosecond value within a second."""

DURATION_SECONDS_MAX = 315_576_000_000
"""Maximum/minimum seconds for Duration (representing +/-10,000 years)."""

TIMESTAMP_SECONDS_MIN = -62_135_596_800
"""Minimum seconds for Timestamp (0001-01-01T00:00:00Z)."""

TIMESTAMP_SECONDS_MAX = 253_402_300_799
"""Maximum seconds for Timestamp (9999-12-31T23:59:59Z)."""

TIMESTAMP_NANOS_MIN = TIMESTAMP_SECONDS_MIN * SECOND_AS_NANOS
"""Smallest legal value for nanoseconds"""

TIMESTAMP_NANOS_MAX = TIMESTAMP_SECONDS_MAX * SECOND_AS_NANOS + NANOS_PER_SECOND_MAX
"""Largest legal value for nanoseconds"""

EPOCH_DATETIME = datetime(1970, 1, 1, tzinfo=timezone.utc)
"""Epoch represented in datetime."""

MICROSECOND_DELTA = timedelta(microseconds=1)
"""One microsecond represented in timedelta."""
