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

import json
import sys
from typing import TYPE_CHECKING, Any, cast

import pytest

from protobuf._budget import (
    BYTES_OVERHEAD,
    DICT_ENTRY_SIZE,
    EMPTY_DICT_SIZE,
    EMPTY_LIST_SIZE,
    INT_SIZE,
    LIST_SLOT_SIZE,
    OBJECT_HEADER_SIZE,
    SLOT_SIZE,
    TrackingBudget,
    _instance_size,
    _message_alloc_size,
    str_size,
)
from protobuf._native_message import NativeMessageClass
from protobuf._wire import BinaryWriter, WireType
from protobuf.wkt import FileDescriptorSet, Struct, Timestamp, Value

from .gen.lists_pb import Lists
from .gen.maps_pb import Maps
from .gen.oneofs_pb import Oneofs
from .gen.scalars_pb import Scalars

if TYPE_CHECKING:
    from collections.abc import Callable

    from protobuf import Message

_IS_CPYTHON = sys.implementation.name == "cpython"
_GIL_ENABLED = getattr(sys, "_is_gil_enabled", lambda: True)()
# The str header shrank in 3.12 and is larger again without the GIL.
_STR_SIZES_MATCH = _IS_CPYTHON and sys.version_info >= (3, 12) and _GIL_ENABLED

_TEXTS = [
    pytest.param("", id="empty"),
    pytest.param("a" * 50, id="ascii"),
    pytest.param("é" * 50, id="latin1"),
    pytest.param("あ" * 50, id="cjk"),
    pytest.param("a" * 50 + "あ", id="ascii+cjk"),
    pytest.param("😀" * 50, id="emoji"),
    pytest.param("あ" * 50 + "😀", id="cjk+emoji"),
]


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
    budget = TrackingBudget(sys.maxsize)
    budget.charge_message(desc)
    assert desc._alloc_size is not None
    assert budget.current == desc._alloc_size
    budget.charge_message(desc)
    assert budget.current == 2 * desc._alloc_size


@pytest.mark.skipif(not _STR_SIZES_MATCH, reason="str layout differs")
@pytest.mark.parametrize("text", _TEXTS)
def test_str_size_matches_interpreter(text: str) -> None:
    assert str_size(text) == sys.getsizeof(text)


def _assert_charged(parse: Callable[[int], Message], expected: int) -> None:
    """Asserts that the parse charges exactly the expected amount."""
    parse(expected)
    with pytest.raises(ValueError, match="allocation budget exceeded"):
        parse(expected - 1)


def _parsers(message: Message) -> list[Callable[[int], Message]]:
    """Parses of the message from binary, JSON text, and a JSON tree."""
    cls = type(message)
    data = message.to_binary()
    text = message.to_json()
    tree = json.loads(text)
    return [
        lambda limit: cls.from_binary(data, allocation_limit=limit),
        lambda limit: cls.from_json(text, allocation_limit=limit),
        lambda limit: cls._from_json_value(tree, allocation_limit=limit),
    ]


@pytest.mark.parametrize("text", _TEXTS)
def test_repeated_string_charge(text: str) -> None:
    count = 3
    message = Lists(string_list=[text] * count)
    expected = _message_alloc_size(Lists._desc)
    expected += count * (str_size(text) + LIST_SLOT_SIZE)
    for parse in _parsers(message):
        _assert_charged(parse, expected)


def test_string_map_charge() -> None:
    entries = {f"キー{i}": f"value{i}😀" for i in range(3)}
    message = Maps(string_to_string=entries)
    expected = _message_alloc_size(Maps._desc)
    expected += sum(
        str_size(k) + str_size(v) + DICT_ENTRY_SIZE for k, v in entries.items()
    )
    for parse in _parsers(message):
        _assert_charged(parse, expected)


def test_unknown_field_charge() -> None:
    def field(number: int, payload: bytes) -> bytes:
        writer = BinaryWriter()
        writer.tag(number, WireType.LENGTH_DELIMITED)
        writer.bytes_(payload)
        return writer.finish()

    fields = [field(200, b"x"), field(1000, b"y" * 10), field(1000, b"z")]
    expected = _message_alloc_size(Scalars._desc) + EMPTY_DICT_SIZE
    # Each distinct number has a list and a dict entry, and a key if it is
    # above the small ints the interpreter shares.
    expected += 2 * (EMPTY_LIST_SIZE + DICT_ENTRY_SIZE) + INT_SIZE
    expected += sum(BYTES_OVERHEAD + len(f) + LIST_SLOT_SIZE for f in fields)

    data = b"".join(fields)
    _assert_charged(
        lambda limit: Scalars.from_binary(data, allocation_limit=limit), expected
    )
