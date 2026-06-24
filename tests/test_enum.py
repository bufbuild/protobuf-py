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

import pytest

from protobuf import enum_is_unknown
from tests.gen.enums_pb import ClosedColor, Color


def test_enum_base_class_str() -> None:
    """Test __str__ for the base Enum class with known values."""
    # Known values should show the Python member name (prefix stripped)
    assert str(Color.RED) == "RED"
    assert str(Color.GREEN) == "GREEN"
    assert str(Color.BLUE) == "BLUE"
    assert str(Color.UNSPECIFIED) == "UNSPECIFIED"


def test_enum_base_class_repr() -> None:
    """Test __repr__ for the base Enum class with known values."""
    # Known values should show the qualified Python name (prefix stripped)
    assert repr(Color.RED) == "Color.RED"
    assert repr(Color.GREEN) == "Color.GREEN"
    assert repr(Color.BLUE) == "Color.BLUE"
    assert repr(Color.UNSPECIFIED) == "Color.UNSPECIFIED"


def test_enum_base_class_unknown_value_str() -> None:
    """Test __str__ for the base Enum class with unknown values."""
    # Unknown values should show the integer value
    unknown = Color(99)
    assert str(unknown) == "99"


def test_enum_base_class_unknown_value_repr() -> None:
    """Test __repr__ for the base Enum class with unknown values."""
    # Unknown values should show the class name with integer
    unknown = Color(99)
    assert repr(unknown) == "Color(99)"


def test_enum_base_class_desc() -> None:
    """Test the desc() class method returns the descriptor."""
    desc = Color.desc()
    assert desc.name == "Color"
    assert desc.type_name == "Color"
    assert len(desc.values) == 4
    assert desc.values[0].name == "COLOR_UNSPECIFIED"
    assert desc.values[1].name == "COLOR_RED"
    assert desc.values[2].name == "COLOR_GREEN"
    assert desc.values[3].name == "COLOR_BLUE"


def test_enum_base_class_int_operations() -> None:
    """Test that Enum instances work as integers."""
    # Can use in arithmetic
    assert Color.RED + 1 == 2
    assert Color.BLUE - 1 == 2

    # Can compare with integers
    assert Color.RED == 1
    assert Color.GREEN == 2
    assert Color.BLUE == 3

    # Can convert to int
    assert int(Color.RED) == 1
    assert int(Color.GREEN) == 2


def test_enum_base_class_missing_with_non_int() -> None:
    """Test that _missing_ raises TypeError for non-integer values."""
    with pytest.raises(TypeError, match="value must be an int"):
        Color("not an int")  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="value must be an int"):
        Color(1.5)  # type: ignore[arg-type]


def test_enum_base_class_negative_value() -> None:
    """Test that negative enum values work correctly."""
    # Negative values are valid per the protobuf language spec (32-bit signed integer range)
    # See: https://protobuf.com/docs/language-spec
    negative = Color(-1)
    assert int(negative) == -1
    assert str(negative) == "-1"
    assert repr(negative) == "Color(-1)"


def test_enum_base_class_zero_value() -> None:
    """Test that zero enum values work correctly (common default case)."""
    # Zero is typically the default/unspecified value
    zero = Color.UNSPECIFIED
    assert int(zero) == 0
    assert zero == 0
    assert str(zero) == "UNSPECIFIED"  # Python member name
    assert repr(zero) == "Color.UNSPECIFIED"  # Python qualified name


def test_enum_base_class_equality() -> None:
    """Test enum value equality comparisons."""
    # Same enum values are equal
    assert Color.RED == Color.RED
    assert Color.GREEN == Color.GREEN

    # Different enum values are not equal
    assert Color.RED != Color.GREEN
    assert Color.BLUE != Color.RED

    # Enum values equal their integer counterparts
    assert Color.RED == 1
    assert Color.GREEN == 2


def test_enum_closed() -> None:
    """Test that closed enums raise ValueError for unknown values."""
    with pytest.raises(ValueError, match="`123` is not a valid ClosedColor"):
        ClosedColor(123)


def test_enum_is_unknown() -> None:
    # Known enum values should not be unknown
    assert not enum_is_unknown(Color.UNSPECIFIED)
    assert not enum_is_unknown(Color.RED)
    assert not enum_is_unknown(Color.GREEN)
    assert not enum_is_unknown(Color.BLUE)

    # Dynamically created values that match known values should not be unknown
    assert not enum_is_unknown(Color(0))  # UNSPECIFIED
    assert not enum_is_unknown(Color(1))  # RED

    # Unknown values (created via _missing_) should be unknown
    unknown_positive = Color(99)
    assert enum_is_unknown(unknown_positive)

    unknown_negative = Color(-1)
    assert enum_is_unknown(unknown_negative)
