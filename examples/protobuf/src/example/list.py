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

import struct
import sys
from pathlib import Path

from .gen.example_pb import User

if __name__ == "__main__":
    try:
        with Path("users.binpb").open("rb") as file:
            while header := file.read(4):
                (length,) = struct.unpack(">I", header)
                data = file.read(length)
                user = User.from_binary(data)
                print(user)  # noqa: T201
    except FileNotFoundError as err:
        print(  # noqa: T201
            f"File {err.filename} not found. Create users first with add.py.",
            file=sys.stderr,
        )
        sys.exit(1)
