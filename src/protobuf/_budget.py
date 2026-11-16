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

import re
from typing import TYPE_CHECKING, Protocol, cast

from ._descriptors import DescMessage, ScalarType

if TYPE_CHECKING:
    from collections.abc import Sized

# Approximate sizes of CPython heap allocations, measured with `sys.getsizeof`
# on 64-bit CPython 3.14. The budget guards against unbounded allocation from
# malicious payloads rather than providing exact accounting, so small
# inaccuracies across versions and builds are fine.

OBJECT_HEADER_SIZE = 16
"""Refcount and type pointer at the start of every object."""
SLOT_SIZE = 8
"""One `__slots__` entry: a pointer."""
GC_HEAD_SIZE = 16
"""GC header allocated in front of every GC-tracked object."""
FLOAT_SIZE = 24
"""A float object."""
INT_SIZE = 36
"""A 64-bit int object. Smaller ints are slightly smaller."""
STR_OVERHEAD = 41
"""Header of an ASCII str; the length is added on top."""
BYTES_OVERHEAD = 33
"""Header of a bytes object."""
EMPTY_LIST_SIZE = 56
"""An empty list."""
EMPTY_DICT_SIZE = 64
"""An empty dict."""
LIST_SLOT_SIZE = 8
"""One appended list element: an 8-byte pointer slot."""
DICT_ENTRY_SIZE = 40
"""One inserted dict entry: hash + key + value words plus growth slack."""
ONEOF_SIZE = 32
"""A Oneof wrapper object: object header plus two references."""

# A str stores every character at the width of its widest one, with a header
# (including the trailing NUL) that depends on that width.
_STR_LATIN1_OVERHEAD = 57
_STR_UCS2_OVERHEAD = 58
_STR_UCS4_OVERHEAD = 60
_UCS2_OR_WIDER = re.compile("[\u0100-\U0010ffff]")
_UCS4 = re.compile("[\U00010000-\U0010ffff]")


def str_size(value: str) -> int:
    """The size of a str."""
    length = len(value)
    if value.isascii():
        return STR_OVERHEAD + length
    if _UCS4.search(value):
        return _STR_UCS4_OVERHEAD + 4 * length
    if _UCS2_OR_WIDER.search(value):
        return _STR_UCS2_OVERHEAD + 2 * length
    return _STR_LATIN1_OVERHEAD + length


def _instance_size(message_type: type) -> int:
    """The fixed allocation size of an instance of a slots-only class."""
    basicsize = getattr(message_type, "__basicsize__", None)
    if basicsize is not None:
        return basicsize
    # PyPy doesn't provide basicsize so we approximate it based on slot count.
    slots = 0
    for cls in message_type.__mro__:
        names = cls.__dict__.get("__slots__", ())
        names = (names,) if isinstance(names, str) else names
        slots += sum(1 for name in names if name not in ("__dict__", "__weakref__"))
    return OBJECT_HEADER_SIZE + SLOT_SIZE * slots


def _message_alloc_size(desc: DescMessage) -> int:
    """Approximate heap size of a freshly-initialized message instance.

    The fixed instance size (all fields are slots) plus the empty containers
    created for repeated/map field defaults.
    """
    size = _instance_size(desc.type) + GC_HEAD_SIZE
    for _, default in desc._defaults:
        if isinstance(default, list):
            size += EMPTY_LIST_SIZE
        elif isinstance(default, dict):
            size += EMPTY_DICT_SIZE
    return size


# Allocation for each scalar type whose values have a fixed size, indexed by
# the type's number. Bools are shared singletons and allocate nothing.
_FIXED_SCALAR_SIZES = (
    None,  # 0: unused
    FLOAT_SIZE,  # 1: DOUBLE
    FLOAT_SIZE,  # 2: FLOAT
    INT_SIZE,  # 3: INT64
    INT_SIZE,  # 4: UINT64
    INT_SIZE,  # 5: INT32
    INT_SIZE,  # 6: FIXED64
    INT_SIZE,  # 7: FIXED32
    0,  # 8: BOOL
    None,  # 9: STRING
    None,  # 10: GROUP
    None,  # 11: MESSAGE
    None,  # 12: BYTES
    INT_SIZE,  # 13: UINT32
    None,  # 14: ENUM
    INT_SIZE,  # 15: SFIXED32
    INT_SIZE,  # 16: SFIXED64
    INT_SIZE,  # 17: SINT32
    INT_SIZE,  # 18: SINT64
)


class Budget(Protocol):
    """Accounts for the allocations made while parsing a message."""

    def charge_message(self, desc: DescMessage) -> None:
        """Charges for a new instance of the message type."""
        ...

    def charge_scalar(self, scalar_type: ScalarType, value: object) -> None:
        """Charges for a parsed scalar value of the given type."""
        ...

    def charge_fixed_scalar(self, scalar_type: ScalarType) -> None:
        """Charges for a scalar of a type whose values have a fixed size.

        These are all scalar types except strings and bytes.
        """
        ...

    def charge_str(self, value: str) -> None:
        """Charges for a str."""
        ...

    def charge_str_encoded(self, length: int) -> None:
        """Charges the least a str decoded from UTF-8 of the given length can be.

        A str is stored at the width of its widest character, which is only
        known once decoded. The least is where every character takes two bytes
        of UTF-8 and one in the str.
        """
        ...

    def charge_str_decoded(self, value: str, length: int) -> None:
        """Charges the rest of a str after charge_str_encoded for its UTF-8 length."""
        ...

    def charge_bytes(self, length: int) -> None:
        """Charges for a bytes of the given length."""
        ...

    def charge_int(self) -> None:
        """Charges for an int.

        Small ints are shared and larger ones vary a little in size, but a
        flat charge is close enough.
        """
        ...

    def charge_float(self) -> None:
        """Charges for a float."""
        ...

    def charge_enum(self) -> None:
        """Charges for a member of an enum type created for a number it does not define."""
        ...

    def charge_oneof(self) -> None:
        """Charges for a Oneof wrapper."""
        ...

    def charge_list(self) -> None:
        """Charges for a new list."""
        ...

    def charge_list_item(self) -> None:
        """Charges for appending an item to a list."""
        ...

    def charge_dict(self) -> None:
        """Charges for a new dict."""
        ...

    def charge_dict_entry(self) -> None:
        """Charges for inserting an entry into a dict."""
        ...


class TrackingBudget:
    """Tracks approximate allocations, raising an error once a limit is exceeded."""

    __slots__ = ("current", "max")

    def __init__(self, limit: int) -> None:
        self.current = 0
        self.max = limit

    def charge(self, amount: int) -> None:
        """Charges the given number of bytes."""
        self.current += amount
        if self.current > self.max:
            msg = f"allocation budget exceeded: needed {self.current} bytes, limit is {self.max}"
            raise ValueError(msg)

    def charge_message(self, desc: DescMessage) -> None:
        size = desc._alloc_size
        if size is None:
            size = _message_alloc_size(desc)
            object.__setattr__(desc, "_alloc_size", size)
        self.charge(size)

    def charge_scalar(self, scalar_type: ScalarType, value: object) -> None:
        if scalar_type == ScalarType.STRING:
            self.charge(str_size(cast("str", value)))
        elif scalar_type == ScalarType.BYTES:
            self.charge(BYTES_OVERHEAD + len(cast("Sized", value)))
        elif scalar_type == ScalarType.BOOL:
            # Bools are shared singletons; nothing is allocated.
            pass
        elif scalar_type in (ScalarType.DOUBLE, ScalarType.FLOAT):
            self.charge(FLOAT_SIZE)
        else:
            self.charge(INT_SIZE)

    def charge_fixed_scalar(self, scalar_type: ScalarType) -> None:
        size = _FIXED_SCALAR_SIZES[scalar_type.value]
        assert size is not None  # noqa: S101
        self.charge(size)

    def charge_str(self, value: str) -> None:
        self.charge(str_size(value))

    def charge_str_encoded(self, length: int) -> None:
        self.charge(STR_OVERHEAD + length // 2)

    def charge_str_decoded(self, value: str, length: int) -> None:
        self.charge(str_size(value) - (STR_OVERHEAD + length // 2))

    def charge_bytes(self, length: int) -> None:
        self.charge(BYTES_OVERHEAD + length)

    def charge_int(self) -> None:
        self.charge(INT_SIZE)

    def charge_float(self) -> None:
        self.charge(FLOAT_SIZE)

    def charge_enum(self) -> None:
        self.charge(INT_SIZE + GC_HEAD_SIZE)

    def charge_oneof(self) -> None:
        self.charge(ONEOF_SIZE)

    def charge_list(self) -> None:
        self.charge(EMPTY_LIST_SIZE)

    def charge_list_item(self) -> None:
        self.charge(LIST_SLOT_SIZE)

    def charge_dict(self) -> None:
        self.charge(EMPTY_DICT_SIZE)

    def charge_dict_entry(self) -> None:
        self.charge(DICT_ENTRY_SIZE)


class NoopBudget:
    """Does no accounting, for parsing without an allocation limit."""

    __slots__ = ()

    def charge_message(self, desc: DescMessage) -> None:
        pass

    def charge_scalar(self, scalar_type: ScalarType, value: object) -> None:
        pass

    def charge_fixed_scalar(self, scalar_type: ScalarType) -> None:
        pass

    def charge_str(self, value: str) -> None:
        pass

    def charge_str_encoded(self, length: int) -> None:
        pass

    def charge_str_decoded(self, value: str, length: int) -> None:
        pass

    def charge_bytes(self, length: int) -> None:
        pass

    def charge_int(self) -> None:
        pass

    def charge_float(self) -> None:
        pass

    def charge_enum(self) -> None:
        pass

    def charge_oneof(self) -> None:
        pass

    def charge_list(self) -> None:
        pass

    def charge_list_item(self) -> None:
        pass

    def charge_dict(self) -> None:
        pass

    def charge_dict_entry(self) -> None:
        pass


def new_budget(limit: int | None) -> Budget:
    """Returns the budget for an optional allocation limit."""
    return NoopBudget() if limit is None else TrackingBudget(limit)
