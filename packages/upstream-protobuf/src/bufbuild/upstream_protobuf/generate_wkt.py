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
"""Generates well-known type Python code into the given output directory.

Usage: generate_wkt <output_dir>
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from license_header import apply_license_headers
from protoc import get_include_protos_path, get_protoc_path


def main() -> None:
    """Generate well-known type Python code."""
    if len(sys.argv) != 2:
        sys.stderr.write(f"usage: {sys.argv[0]} <output_dir>\n")
        sys.exit(2)

    output_dir = Path(sys.argv[1])
    include_dir = get_include_protos_path()

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        proc = subprocess.run(  # noqa: S603
            [
                get_protoc_path(),
                *[str(f) for f in include_dir.glob("google/protobuf/**/*.proto")],
                f"--py_out={tmp_path}",
                "--py_opt=no_fmt_off",
            ],
            check=False,
        )
        if proc.returncode:
            sys.exit(proc.returncode)

        shutil.rmtree(output_dir, ignore_errors=True)
        shutil.move(str(tmp_path / "google" / "protobuf"), str(output_dir))

    apply_license_headers(dirs=[output_dir])


if __name__ == "__main__":
    main()
