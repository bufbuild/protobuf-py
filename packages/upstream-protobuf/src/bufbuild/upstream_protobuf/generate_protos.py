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
"""Generates Python code from .proto files in a directory.

Usage: generate_protos <proto_path> <output_dir>
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from protoc import get_protoc_path


def main() -> None:
    """Generate Python code from .proto files."""
    if len(sys.argv) != 3:
        sys.stderr.write(f"usage: {sys.argv[0]} <proto_path> <output_dir>\n")
        sys.exit(2)

    proto_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(proto_path.rglob("*.proto"))

    proc = subprocess.run(  # noqa: S603
        [
            get_protoc_path(),
            "--proto_path",
            proto_path,
            *[str(f) for f in files],
            f"--py_out={output_dir}",
        ],
        check=False,
    )
    if proc.returncode:
        sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
