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
"""Shim for the conformance_test_runner executable provided by protoc-runner."""

from __future__ import annotations

import os
import subprocess
import sys
from typing import TYPE_CHECKING

from protoc import get_conformance_test_runner_path

from protobuf import maximum_supported_edition

if TYPE_CHECKING:
    from pathlib import Path


def run(output_dir: Path, command: list[str], test: str = "") -> None:
    """Run the conformance test runner."""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    args = [
        get_conformance_test_runner_path(),
        "--output_dir",
        str(output_dir),
        "--enforce_recommended",
        "--maximum_edition",
        maximum_supported_edition.name.removeprefix("EDITION_"),
    ]
    if test:
        args.extend(["--test", test])
    subprocess.run(  # noqa: S603
        [*args, *command], env=env, check=True
    )
