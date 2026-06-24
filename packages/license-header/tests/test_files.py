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

import os
import subprocess
from pathlib import Path

from license_header._files import _is_ignored, list_files
from license_header._header import STYLES


def test_is_ignored_gen_pattern() -> None:
    assert _is_ignored("tests/gen/foo.py", ["**/gen/**"])
    assert _is_ignored("src/protobuf/wkt/_gen/any_pb.py", ["**/_gen/**"])
    assert not _is_ignored("src/protobuf/message.py", ["**/gen/**"])


def test_is_ignored_exact() -> None:
    assert _is_ignored("README.md", ["README.md"])
    # Without **, pattern only matches exact path
    assert not _is_ignored("src/README.md", ["README.md"])
    # Use **/ prefix to match at any depth
    assert _is_ignored("src/README.md", ["**/README.md"])
    assert not _is_ignored("src/main.py", ["README.md"])


def test_list_files_in_git_repo(tmp_path: Path) -> None:
    # Set up a minimal git repo
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)  # noqa: S607
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],  # noqa: S607
        cwd=tmp_path,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],  # noqa: S607
        cwd=tmp_path,
        capture_output=True,
        check=True,
    )

    # Create files
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "good.py").write_text("x = 1\n")
    (tmp_path / "src" / "run.sh").write_text("#!/bin/bash\necho hi\n")
    (tmp_path / "src" / "schema.proto").write_text('syntax = "proto3";\n')
    (tmp_path / "src" / "readme.md").write_text("hi\n")
    (tmp_path / "gen").mkdir()
    (tmp_path / "gen" / "generated.py").write_text("x = 2\n")

    subprocess.run(["git", "add", "."], cwd=tmp_path, capture_output=True, check=True)  # noqa: S607

    old_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        files = list_files([Path()], ["**/gen/**"], frozenset(STYLES))
    finally:
        os.chdir(old_cwd)

    names = [f.name for f in files]
    assert "good.py" in names
    assert "run.sh" in names
    assert "schema.proto" in names
    assert "readme.md" not in names  # unsupported extension
    assert "generated.py" not in names  # ignored
