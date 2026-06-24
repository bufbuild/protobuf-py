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

from typing import Final

from ._bootstrap import _MAXIMUM_EDITION, _MINIMUM_EDITION
from .wkt._gen.descriptor_pb import Edition

minimum_supported_edition: Final[Edition] = Edition(_MINIMUM_EDITION)
"""The minimum protobuf edition supported by this implementation."""

maximum_supported_edition: Final[Edition] = Edition(_MAXIMUM_EDITION)
"""The maximum protobuf edition supported by this implementation."""
