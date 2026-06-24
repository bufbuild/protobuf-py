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

import subprocess
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def _run(
    module: str, *, input_text: str = "", cwd: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [sys.executable, "-m", module],
        input=input_text,
        capture_output=True,
        text=True,
        cwd=cwd,
        check=False,
    )


def test_add_and_list(tmp_path: Path) -> None:
    """Test add.py and list.py."""
    # Add two users
    result = _run(
        "example.add", input_text="Alice\nSmith\nNYC\nParis\n\n", cwd=tmp_path
    )
    assert result.returncode == 0, result.stderr
    result = _run("example.add", input_text="Bob\nJones\n\n", cwd=tmp_path)
    assert result.returncode == 0, result.stderr

    # List both users
    result = _run("example.list", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert "Alice" in result.stdout
    assert "Smith" in result.stdout
    assert "NYC" in result.stdout
    assert "Paris" in result.stdout
    assert "Bob" in result.stdout
    assert "Jones" in result.stdout
