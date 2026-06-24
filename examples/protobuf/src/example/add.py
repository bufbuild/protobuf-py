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
from pathlib import Path

from .gen.example_pb import User

if __name__ == "__main__":
    with Path("users.binpb").open("ab") as file:
        user = User(
            first_name=input("Enter first name: "),
            last_name=input("Enter last name: "),
            active=True,
        )
        while True:
            location = input("Enter a location (or leave blank to finish): ")
            if location == "":
                break
            user.locations.append(location)
        data = user.to_binary()
        file.write(struct.pack(">I", len(data)))
        file.write(data)
