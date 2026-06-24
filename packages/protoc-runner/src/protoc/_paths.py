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

import sys
from pathlib import Path


def get_conformance_test_runner_path() -> Path:
    """Returns the path to the conformance test runner."""
    if sys.platform == "win32":
        msg = "conformance test runner is not supported on Windows"
        raise RuntimeError(msg)
    return Path(__file__).parent / "_bin" / "conformance_test_runner"


def get_protoc_path() -> Path:
    """Returns the path to the protoc binary."""
    protoc_exe = "protoc.exe" if sys.platform == "win32" else "protoc"
    return Path(__file__).parent / "_bin" / protoc_exe


def get_include_protos_path() -> Path:
    """Returns the path to the included protos."""
    return Path(__file__).parent / "include"
