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
import sys
from typing import Literal, cast, get_args

Implementation = Literal["native", "python"]

IMPLEMENTATION_ENV = "PROTOBUF_PY_TEST_IMPLEMENTATION"


def process_implementation() -> Implementation:
    implementation = os.environ.get(IMPLEMENTATION_ENV, "native")
    if implementation not in get_args(Implementation):
        msg = (
            f"{IMPLEMENTATION_ENV} must be one of {get_args(Implementation)}, "
            f"got {implementation!r}"
        )
        raise ValueError(msg)
    return cast("Implementation", implementation)


def hide_native_extension() -> None:
    """Make the extension unimportable when pinned to the python implementation.

    Must run before ``protobuf`` is imported.
    """
    if process_implementation() != "python":
        return
    if sys.modules.get("protobuf_ext") is not None:
        msg = "protobuf_ext was imported before it could be hidden"
        raise RuntimeError(msg)
    sys.modules["protobuf_ext"] = None  # pyright: ignore[reportArgumentType]  # ty: ignore[invalid-assignment]


def active_implementation() -> Implementation:
    """The implementation ``protobuf`` is actually using in this process."""
    from protobuf._native_message import NativeMessageClass  # noqa: PLC0415

    return "native" if NativeMessageClass is not None else "python"


def check_implementation(expected: Implementation | None = None) -> None:
    """Raise unless this process runs ``expected``, by default its pinned one."""
    if expected is None:
        expected = process_implementation()
    active = active_implementation()
    if active != expected:
        msg = (
            f"expected the {expected} implementation but this process has {active}; "
            f"run through xdist (the default) so each implementation gets its own "
            f"worker, or pin the process with {IMPLEMENTATION_ENV}"
        )
        raise RuntimeError(msg)
