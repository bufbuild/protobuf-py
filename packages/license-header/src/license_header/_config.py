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
"""Read license header configuration from pyproject.toml."""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import tomli as tomllib


@dataclasses.dataclass(frozen=True)
class Config:
    """License header configuration."""

    license_type: str
    copyright_holder: str
    year_range: str
    ignore_patterns: list[str]
    pyproject_dir: Path


def load_config(pyproject_path: Path | None = None) -> Config:
    """Load configuration from pyproject.toml.

    Args:
        pyproject_path: Explicit path to pyproject.toml. If None, searches
            upward from the current working directory.

    Returns:
        Parsed configuration.

    Raises:
        FileNotFoundError: If no pyproject.toml is found.
        ValueError: If required configuration is missing or invalid.
    """
    if pyproject_path is None:
        pyproject_path = _find_pyproject()
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    license_type: str | None = _get(data, "project", "license")
    if license_type is None:
        msg = "pyproject.toml: [project].license is required"
        raise ValueError(msg)
    if license_type != "Apache-2.0":
        msg = f"pyproject.toml: unsupported license {license_type!r}, only 'Apache-2.0' is supported"
        raise ValueError(msg)

    tool: dict[str, Any] | None = _get(data, "tool", "licenseheader")
    if tool is None:
        msg = "pyproject.toml: [tool.licenseheader] section is required"
        raise ValueError(msg)

    copyright_holder: str | None = tool.get("copyright-holder")
    if copyright_holder is None:
        msg = "pyproject.toml: [tool.licenseheader].copyright-holder is required"
        raise ValueError(msg)

    year_range: str | None = tool.get("year-range")
    if year_range is None:
        msg = "pyproject.toml: [tool.licenseheader].year-range is required"
        raise ValueError(msg)

    ignore_patterns: list[str] = tool.get("ignore", [])

    return Config(
        license_type=license_type,
        copyright_holder=copyright_holder,
        year_range=str(year_range),
        ignore_patterns=ignore_patterns,
        pyproject_dir=pyproject_path.parent,
    )


def _find_pyproject() -> Path:
    """Walk up from cwd to find pyproject.toml."""
    current = Path.cwd().resolve()
    for directory in (current, *current.parents):
        candidate = directory / "pyproject.toml"
        if candidate.is_file():
            return candidate
    msg = "could not find pyproject.toml"
    raise FileNotFoundError(msg)


def _get(data: dict[str, Any], *keys: str) -> Any:
    """Safely traverse nested dicts."""
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
        if current is None:
            return None
    return current
