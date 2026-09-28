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
from typing import Any, cast

import pytest

from protobuf._budget import OBJECT_HEADER_SIZE, SLOT_SIZE, Budget, _instance_size
from protobuf._native_message import NativeMessageClass
from protobuf.wkt import FileDescriptorSet, Struct, Timestamp, Value

from .gen.lists_pb import Lists
from .gen.maps_pb import Maps
from .gen.oneofs_pb import Oneofs
from .gen.scalars_pb import Scalars


class _NoBasicsize:
    """Simulates a PyPy type, by being an instantiated object that includes the mro of a type."""

    def __init__(self, real: type) -> None:
        self.__mro__ = real.__mro__


def _slot_count(message_type: type) -> int:
    slots = 0
    for cls in message_type.__mro__:
        names = cls.__dict__.get("__slots__", ())
        names = (names,) if isinstance(names, str) else names
        slots += sum(1 for n in names if n not in ("__dict__", "__weakref__"))
    return slots


@pytest.mark.skipif(
    NativeMessageClass is not None, reason="fallback only needed for pure Python"
)
@pytest.mark.skipif(
    sys.implementation.name != "cpython", reason="no __basicsize__ to compare against"
)
@pytest.mark.parametrize(
    "message_type",
    [Scalars, Lists, Maps, Oneofs, Struct, Value, Timestamp, FileDescriptorSet],
)
def test_instance_size_fallback_matches_basicsize(message_type: type[Any]) -> None:
    # Ensure the type (and its __slots__) exists before inspecting it.
    message_type()
    expected = message_type.__basicsize__
    if sys.version_info < (3, 12):
        # Before managed weakrefs, the __weakref__ slot occupied a pointer
        # inside the instance, which the fallback deliberately excludes.
        expected -= SLOT_SIZE
    if not getattr(sys, "_is_gil_enabled", lambda: True)():
        # Free-threaded builds fold the GC header into a 32-byte object
        # header, which basicsize includes and the formula does not.
        expected -= 16
    mt = _NoBasicsize(message_type)
    assert not hasattr(mt, "__basicsize__")
    assert _instance_size(cast("type", mt)) == expected


@pytest.mark.skipif(
    sys.implementation.name != "pypy", reason="exercises the real fallback path"
)
def test_instance_size_fallback_on_pypy() -> None:
    Scalars()
    assert not hasattr(Scalars, "__basicsize__")
    assert _instance_size(Scalars) == OBJECT_HEADER_SIZE + SLOT_SIZE * _slot_count(
        Scalars
    )


def test_alloc_size_cached_on_descriptor() -> None:
    desc = Scalars._desc
    object.__setattr__(desc, "_alloc_size", None)
    budget = Budget()
    budget.charge_message(desc)
    assert desc._alloc_size is not None
    assert budget.current == desc._alloc_size
    budget.charge_message(desc)
    assert budget.current == 2 * desc._alloc_size
