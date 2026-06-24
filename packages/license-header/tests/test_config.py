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

from typing import TYPE_CHECKING

import pytest
from license_header._config import Config, load_config

if TYPE_CHECKING:
    from pathlib import Path


def test_load_config_valid(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
license = "Apache-2.0"

[tool.licenseheader]
copyright-holder = "Acme Corp."
year-range = "2025"
ignore = ["**/gen/**"]
""")
    config = load_config(pyproject)
    assert config == Config(
        license_type="Apache-2.0",
        copyright_holder="Acme Corp.",
        year_range="2025",
        ignore_patterns=["**/gen/**"],
        pyproject_dir=tmp_path,
    )


def test_load_config_missing_license(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
name = "test"

[tool.licenseheader]
copyright-holder = "Acme"
year-range = "2025"
""")
    with pytest.raises(ValueError, match="license is required"):
        load_config(pyproject)


def test_load_config_unsupported_license(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
license = "MIT"

[tool.licenseheader]
copyright-holder = "Acme"
year-range = "2025"
""")
    with pytest.raises(ValueError, match="unsupported license"):
        load_config(pyproject)


def test_load_config_missing_section(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
license = "Apache-2.0"
""")
    with pytest.raises(ValueError, match="section is required"):
        load_config(pyproject)


def test_load_config_missing_copyright_holder(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
license = "Apache-2.0"

[tool.licenseheader]
year-range = "2025"
""")
    with pytest.raises(ValueError, match="copyright-holder is required"):
        load_config(pyproject)


def test_load_config_missing_year_range(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
license = "Apache-2.0"

[tool.licenseheader]
copyright-holder = "Acme"
""")
    with pytest.raises(ValueError, match="year-range is required"):
        load_config(pyproject)


def test_load_config_ignore_defaults_empty(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""\
[project]
license = "Apache-2.0"

[tool.licenseheader]
copyright-holder = "Acme"
year-range = "2025"
""")
    config = load_config(pyproject)
    assert config.ignore_patterns == []
