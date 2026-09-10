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

import re

MapImports = tuple[tuple[re.Pattern[str], str], ...]

_OPTION_NAME = "map_imports"

_TARGET = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*")


def compile_map_imports(mappings: dict[str, str]) -> MapImports:
    compiled: list[tuple[re.Pattern[str], str]] = []
    for pattern, target in mappings.items():
        if not pattern:
            msg = f"option '{_OPTION_NAME}': pattern must not be empty"
            raise ValueError(msg)
        # An empty target (or ".") maps to the canonical module path.
        normalized = target.removesuffix(".")
        if normalized and not _TARGET.fullmatch(normalized):
            msg = f"option '{_OPTION_NAME}': target '{target}' must be a Python package path"
            raise ValueError(msg)
        compiled.append((_glob_to_regex(pattern), normalized))
    return tuple(compiled)


def map_import_target(proto_name: str, map_imports: MapImports) -> str | None:
    for pattern, target in map_imports:
        if pattern.fullmatch(proto_name):
            return target
    return None


def _glob_to_regex(pattern: str) -> re.Pattern[str]:
    parts: list[str] = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if pattern[i + 1 : i + 2] == "*":
                if pattern[i + 2 : i + 3] == "/":
                    parts.append(r"([^/]+/)*")
                    i += 3
                    continue
                parts.append(".*")
                i += 2
                continue
            parts.append(r"[^/]*")
        elif char == "/" and i == len(pattern) - 1:
            # A trailing slash matches everything in the directory.
            parts.append("/.*")
        else:
            parts.append(re.escape(char))
        i += 1
    return re.compile("".join(parts))
