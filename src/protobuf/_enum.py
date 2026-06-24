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

from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._descriptors import DescEnum


class Enum(IntEnum):
    """Base class for protobuf enumeration types.

    Protobuf enumerations are integer-based. This class inherits from `IntEnum`
    so enum values work as integers while maintaining a link to the protobuf
    descriptor.

    Generated enum classes inherit from this base class and define their enum
    values as class attributes.

    Examples:
        ```python
        from protobuf import Enum


        # Generated from:
        # enum Color {
        #   COLOR_UNSPECIFIED = 0;
        #   COLOR_RED = 1;
        #   COLOR_GREEN = 2;
        # }
        class Color(Enum):
            UNSPECIFIED = 0  # Python name (prefix stripped)
            RED = 1
            GREEN = 2


        # Use like a regular int
        color = Color.RED
        print(color)  # Prints: RED (Python member name)
        print(repr(color))  # Color.RED (Python qualified name)
        print(int(color))  # 1
        print(color + 1)  # 2
        print(color == 1)  # True

        # Access the descriptor
        desc = Color.desc()
        print(desc.name)  # "Color"
        ```
    """

    if TYPE_CHECKING:
        _desc: DescEnum

    @classmethod
    def _missing_(cls, value: object) -> Enum:
        """Handle unknown enum values.

        Called by the enum metaclass for undefined values. Open enums must
        support unknown values, so this creates a pseudo-member.

        Args:
            value: The integer value to create an enum instance for.

        Returns:
            A new enum instance with the given value.

        Raises:
            TypeError: If the value is not an integer.
        """
        if not isinstance(value, int):
            msg = f"value must be an int, not {type(value).__name__}"
            raise TypeError(msg)

        if not cls._desc.open:
            msg = f"`{value}` is not a valid {cls.__name__}"
            raise ValueError(msg)

        # Create a pseudo-member for unknown values
        pseudo_member = int.__new__(cls, value)
        pseudo_member._name_ = None  # type: ignore[attr-defined]
        pseudo_member._value_ = value  # type: ignore[attr-defined]
        return pseudo_member  # type: ignore[return-value]

    def __str__(self) -> str:
        """Return a string representation of the enum value.

        Returns the Python member name (e.g., "RED") for known values,
        or the integer as a string for unknown values.

        Returns:
            The Python member name if known, otherwise the integer as a string.

        Examples:
            ```python
            str(Color.RED)  # 'RED'
            str(Color(99))  # '99'
            ```
        """
        if self._name_ is not None:
            return self._name_
        return str(int(self))

    def __repr__(self) -> str:
        """Return a detailed string representation of the enum value.

        Returns the qualified Python name (e.g., "Color.RED") for known values,
        or "Color(99)" format for unknown values.

        Returns:
            The qualified Python name if known, otherwise the class name with integer.

        Examples:
            ```python
            repr(Color.RED)  # 'Color.RED'
            repr(Color(99))  # 'Color(99)'
            ```
        """
        if self._name_ is not None:
            return f"{self.__class__.__qualname__}.{self._name_}"
        return f"{self.__class__.__qualname__}({int(self)})"

    @classmethod
    def desc(cls) -> DescEnum:
        """Get the descriptor for this enumeration type.

        Returns:
            The DescEnum descriptor for this enum.

        Examples:
            ```python
            desc = Color.desc()
            desc.type_name  # 'my.package.Color'
            desc.values[0].name  # 'COLOR_UNSPECIFIED'
            ```
        """
        return cls._desc


def enum_is_unknown(value: Enum, /) -> bool:
    """Check if an enum value is unknown (i.e., not defined in the protobuf schema)."""
    return value.name is None
