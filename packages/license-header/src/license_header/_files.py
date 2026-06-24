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
"""File discovery using git ls-files."""

from __future__ import annotations

import fnmatch
import subprocess
from pathlib import Path


def list_files(
    dirs: list[Path], ignore_patterns: list[str], extensions: frozenset[str]
) -> list[Path]:
    """List supported files tracked by git, excluding ignored patterns.

    Args:
        dirs: Directories to search. Defaults to ["."] if empty.
        ignore_patterns: Glob patterns for files to skip (e.g. ``**/gen/**``).
        extensions: File extensions to include (e.g. ``{".py", ".sh"}``).

    Returns:
        Sorted list of file paths.
    """
    if not dirs:
        dirs = [Path()]

    dir_args = [str(d) for d in dirs]
    result = subprocess.run(  # noqa: S603
        [  # noqa: S607
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            *dir_args,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    files: list[Path] = []
    for line in result.stdout.splitlines():
        path = Path(line)
        if path.suffix not in extensions:
            continue
        if _is_ignored(str(path), ignore_patterns):
            continue
        if not path.exists():
            continue
        files.append(path)

    return sorted(files)


def _is_ignored(filepath: str, patterns: list[str]) -> bool:
    """Check if a filepath matches any ignore pattern.

    Patterns follow fnmatch semantics against the full path.
    Use ``**/`` prefix to match at any depth (e.g. ``**/gen/**``).
    """
    for pattern in patterns:
        if fnmatch.fnmatch(filepath, pattern):
            return True
        # Expand ** to match any number of path segments
        if pattern.startswith("**/"):
            suffix = pattern[3:]
            parts = filepath.split("/")
            for i in range(len(parts)):
                if fnmatch.fnmatch("/".join(parts[i:]), suffix):
                    return True
    return False
