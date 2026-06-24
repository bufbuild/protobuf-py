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
"""Proto field name case conversion utilities."""

from __future__ import annotations


def proto_snake_case(name: str) -> str:
    """Convert lowerCamelCase to proto snake_case."""
    return "".join(f"_{c.lower()}" if c.isupper() else c for c in name)


def proto_camel_case(snake: str) -> str:
    """Convert proto snake_case to lowerCamelCase."""
    return "".join(
        (word[0].upper() + word[1:] if word else "") if i > 0 else word
        for i, word in enumerate(snake.split("_"))
    )
