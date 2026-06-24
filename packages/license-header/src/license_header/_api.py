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
"""Public API and CLI entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

from license_header._config import Config, load_config
from license_header._files import list_files
from license_header._header import STYLES, make_header, modify


def _iter_modifications(
    dirs: list[Path] | None, config: Config | None
) -> Iterator[tuple[Path, str]]:
    """Yield ``(path, new_content)`` for every file that needs a header update."""
    if config is None:
        config = load_config()
    headers = {
        ext: (make_header(config.copyright_holder, config.year_range, style), style)
        for ext, style in STYLES.items()
    }
    for path in list_files(dirs or [], config.ignore_patterns, frozenset(headers)):
        header, style = headers[path.suffix]
        content = path.read_text(encoding="utf-8")
        result = modify(content, header, style)
        if result != content:
            yield path, result


def apply_license_headers(
    dirs: list[Path] | None = None, config: Config | None = None
) -> list[Path]:
    """Apply license headers to files.

    Args:
        dirs: Directories to process. Defaults to the pyproject.toml directory.
        config: Configuration. Loaded from pyproject.toml if not provided.

    Returns:
        List of files that were modified.
    """
    modified: list[Path] = []
    for path, result in _iter_modifications(dirs, config):
        path.write_text(result, encoding="utf-8")
        modified.append(path)
    return modified


def check_license_headers(
    dirs: list[Path] | None = None, config: Config | None = None
) -> list[Path]:
    """Check that files have correct license headers.

    Args:
        dirs: Directories to process. Defaults to the pyproject.toml directory.
        config: Configuration. Loaded from pyproject.toml if not provided.

    Returns:
        List of files with missing or incorrect headers.
    """
    return [path for path, _ in _iter_modifications(dirs, config)]


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="license-header",
        description="Add or check license headers in source files.",
    )
    parser.add_argument(
        "dirs",
        nargs="*",
        type=Path,
        help="Directories to process (default: project root)",
    )
    parser.add_argument(
        "--check", action="store_true", help="Check mode: exit 1 if headers are missing"
    )
    args = parser.parse_args()

    dirs: list[Path] = args.dirs or []

    if args.check:
        missing = check_license_headers(dirs=dirs)
        if missing:
            sys.stderr.write(f"missing license header in {len(missing)} files:\n")
            for path in missing:
                sys.stderr.write(f"  {path}\n")
            sys.exit(1)
        sys.exit(0)

    modified = apply_license_headers(dirs=dirs)
    print(f"updated {len(modified)} license headers.")  # noqa: T201
