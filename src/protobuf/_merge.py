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

from typing import TypeVar

from ._message import Message

T = TypeVar("T", bound=Message)


def merge_from(target: T, source: T, *, ignore_unknown_fields: bool = False) -> None:
    """Merges the fields from source into target.

    Merge rules by field kind:

    - Scalar and enum: the existing value is overwritten.
    - Message: recursively merged if already present, otherwise set.
    - Repeated: elements are appended.
    - Map: entries are added; existing keys are overwritten. Message-valued map entries are not merged.
    - Unknown fields: retained unless `ignore_unknown_fields` is `True`.

    Args:
        target: The message instance to merge into.
        source: The message instance to merge from.
        ignore_unknown_fields: Whether to ignore unknown fields during the merge.
    """
    target._merge_from(source, ignore_unknown_fields)
