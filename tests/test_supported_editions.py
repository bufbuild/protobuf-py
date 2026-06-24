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

import protobuf
from protobuf._bootstrap import _feature_defaults
from protobuf.wkt import Edition


def test_minimum_supported_edition() -> None:
    assert protobuf.minimum_supported_edition == Edition.PROTO2


def test_maximum_supported_edition() -> None:
    assert protobuf.maximum_supported_edition == Edition.EDITION_2024


def test_min_max_match_feature_defaults() -> None:
    # The minimum supported edition must have coverage via at-or-before lookup.
    assert min(_feature_defaults) <= protobuf.minimum_supported_edition
    # The maximum supported edition must have an explicit entry (no extrapolation beyond it).
    assert protobuf.maximum_supported_edition == max(_feature_defaults)
