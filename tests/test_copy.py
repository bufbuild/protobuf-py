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

# ruff: noqa: PGH003 # copy.replace uses a blanket type: ignore that works for both pyright and ty
import copy
import sys
from typing import TYPE_CHECKING, Any

import pytest

from protobuf import Oneof
from tests.gen.messages_pb import MixedFieldsWithRequired

if TYPE_CHECKING:
    from collections.abc import Callable

# copy.replace() is only available in Python 3.13+
PYTHON_3_13_PLUS = sys.version_info >= (3, 13)
requires_python_3_13 = pytest.mark.skipif(
    not PYTHON_3_13_PLUS, reason="Requires Python 3.13+ for copy.replace()"
)


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_creates_new_instance(copy_func: Callable[[Any], Any]) -> None:
    """Test that copy creates a new instance with same field values."""
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42
    msg.implicit_field = 100
    copied = copy_func(msg)

    # Should be a different instance
    assert copied is not msg
    # Should be the same type
    assert type(copied) is type(msg)
    # Should have the same field values
    assert copied.explicit_field == 42
    assert copied.implicit_field == 100


def test_shallow_copy_shares_mutable_references() -> None:
    """Test that shallow copy shares references to mutable objects."""
    # Create a message with mutable fields
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "nested"
    msg = MixedFieldsWithRequired()
    msg.repeated_field = ["a", "b", "c"]
    msg.map_field = {"key1": 1, "key2": 2}
    msg.message_field = bar
    copied = copy.copy(msg)

    # Shallow copy should share the same list reference
    assert copied.repeated_field is msg.repeated_field
    copied.repeated_field.append("d")
    assert msg.repeated_field == ["a", "b", "c", "d"]

    # Shallow copy should share the same dict reference
    assert copied.map_field is msg.map_field
    copied.map_field["key3"] = 3
    assert msg.map_field == {"key1": 1, "key2": 2, "key3": 3}

    # Shallow copy should share the same nested message reference
    assert copied.message_field is msg.message_field
    assert copied.message_field is bar

    # Modifying nested message in shallow copy affects original
    assert copied.message_field is not None
    copied.message_field.value = "modified"
    assert msg.message_field is not None
    assert msg.message_field.value == "modified"

    # Test with empty collections - shallow copy shares them
    msg2 = MixedFieldsWithRequired()
    msg2.repeated_field = []
    msg2.map_field = {}
    copied2 = copy.copy(msg2)
    assert copied2.repeated_field is msg2.repeated_field
    assert copied2.map_field is msg2.map_field


def test_deep_copy_creates_independent_copies() -> None:
    """Test that deep copy creates independent copies of mutable objects."""
    # Create a message with mutable fields
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "nested"
    msg = MixedFieldsWithRequired()
    msg.repeated_field = ["a", "b", "c"]
    msg.map_field = {"key1": 1, "key2": 2}
    msg.message_field = bar
    copied = copy.deepcopy(msg)

    # Deep copy should create a new list
    assert copied.repeated_field is not msg.repeated_field
    assert copied.repeated_field == ["a", "b", "c"]
    copied.repeated_field.append("d")
    assert msg.repeated_field == ["a", "b", "c"]  # Original unchanged
    assert copied.repeated_field == ["a", "b", "c", "d"]

    # Deep copy should create a new dict
    assert copied.map_field is not msg.map_field
    assert copied.map_field == {"key1": 1, "key2": 2}
    copied.map_field["key3"] = 3
    assert msg.map_field == {"key1": 1, "key2": 2}  # Original unchanged
    assert copied.map_field == {"key1": 1, "key2": 2, "key3": 3}

    # Deep copy should create a new nested message
    assert copied.message_field is not msg.message_field
    assert copied.message_field is not bar
    assert isinstance(copied.message_field, MixedFieldsWithRequired.Bar)
    assert copied.message_field.value == "nested"

    # Modifying nested message in deep copy does not affect original
    assert copied.message_field is not None
    copied.message_field.value = "modified"
    assert msg.message_field is not None
    assert msg.message_field.value == "nested"  # Original unchanged

    # Test with empty collections - deep copy creates new ones
    msg2 = MixedFieldsWithRequired()
    msg2.repeated_field = []
    msg2.map_field = {}
    copied2 = copy.deepcopy(msg2)
    assert copied2.repeated_field is not msg2.repeated_field
    assert copied2.repeated_field == []
    assert copied2.map_field is not msg2.map_field
    assert copied2.map_field == {}


def test_deep_copy_with_oneof() -> None:
    """Test that deep copy properly handles oneof fields."""
    msg = MixedFieldsWithRequired()
    msg.oneof_group = Oneof("oneof_field", "test_value")
    copied = copy.deepcopy(msg)

    # Should have the same value
    assert copied.oneof_group == msg.oneof_group


def test_deep_copy_with_all_field_types() -> None:
    """Test deep copy with all field types populated."""
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "nested"
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42
    msg.implicit_field = 100
    msg.legacy_required_field = "required"
    msg.repeated_field = ["a", "b", "c"]
    msg.message_field = bar
    msg.field_with_default = 99
    msg.map_field = {"key": 1}
    msg.oneof_group = Oneof("oneof_field", "oneof_value")
    copied = copy.deepcopy(msg)

    # All scalar fields should be equal
    assert copied.explicit_field == 42
    assert copied.implicit_field == 100
    assert copied.legacy_required_field == "required"
    assert copied.field_with_default == 99

    # All mutable fields should be independent copies
    assert copied.repeated_field is not msg.repeated_field
    assert copied.repeated_field == ["a", "b", "c"]

    assert copied.map_field is not msg.map_field
    assert copied.map_field == {"key": 1}

    assert copied.message_field is not msg.message_field
    assert copied.message_field is not None
    assert copied.message_field.value == "nested"

    assert copied.oneof_group == msg.oneof_group


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_with_none_fields(copy_func: Callable[[Any], Any]) -> None:
    """Test that copy works correctly with None fields."""
    msg = MixedFieldsWithRequired()
    msg.message_field = None
    msg.oneof_group = None
    copied = copy_func(msg)

    assert copied.message_field is None
    assert copied.oneof_group is None


def test_deep_copy_with_memo() -> None:
    """Test that deep copy uses the memo parameter correctly."""
    msg = MixedFieldsWithRequired(explicit_field=1)
    msg.repeated_field = ["a", "b"]

    # Test with explicit memo to ensure memo is used
    memo: dict[int, object] = {}
    copied = copy.deepcopy(msg, memo)

    # The memo should contain the original object
    assert id(msg) in memo
    assert memo[id(msg)] is copied


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_preserves_descriptor(copy_func: Callable[[Any], Any]) -> None:
    """Test that copy preserves the message descriptor reference."""
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42
    copied = copy_func(msg)

    # Both should reference the same descriptor (not copied)
    assert copied._desc is msg._desc
    assert copied._desc is MixedFieldsWithRequired._desc


def test_deepcopy_does_not_copy_desc() -> None:
    """Test that __deepcopy__ explicitly does not copy _desc.

    This is important because _desc is potentially a giant tree and should be
    shared between all instances of the same message type. We verify that
    _desc is the exact same object (by identity) after deep copy.
    """
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42
    msg.repeated_field = ["a", "b"]

    # Create a nested message
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "nested"
    msg.message_field = bar

    # Deep copy the message
    copied = copy.deepcopy(msg)

    # Verify that _desc is not copied (same object identity)
    assert copied._desc is msg._desc
    assert copied._desc is MixedFieldsWithRequired._desc
    assert id(copied._desc) == id(msg._desc)

    # Verify nested message's _desc is also not copied
    assert copied.message_field is not None
    assert copied.message_field._desc is bar._desc
    assert copied.message_field._desc is MixedFieldsWithRequired.Bar._desc
    assert id(copied.message_field._desc) == id(bar._desc)

    # But other fields should be independent copies
    assert copied.repeated_field is not msg.repeated_field
    assert copied.repeated_field == ["a", "b"]
    assert copied.message_field is not bar


@requires_python_3_13
def test_replace_creates_new_instance() -> None:
    """Test that copy.replace creates a new instance with updated fields."""
    # Test replacing a single field
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42
    msg.implicit_field = 100
    replaced = copy.replace(msg, explicit_field=99)  # type: ignore

    # Should be a different instance
    assert replaced is not msg
    # Original should be unchanged
    assert msg.explicit_field == 42
    assert msg.implicit_field == 100
    # Replaced should have new value for explicit_field
    assert replaced.explicit_field == 99
    # Other fields should be the same
    assert replaced.implicit_field == 100

    # Test replacing multiple fields
    msg2 = MixedFieldsWithRequired()
    msg2.explicit_field = 42
    msg2.implicit_field = 100
    msg2.legacy_required_field = "original"
    replaced2 = copy.replace(msg2, explicit_field=99, legacy_required_field="updated")  # type: ignore

    # Original should be unchanged
    assert msg2.explicit_field == 42
    assert msg2.legacy_required_field == "original"
    # Replaced should have new values
    assert replaced2.explicit_field == 99
    assert replaced2.legacy_required_field == "updated"
    # Unchanged fields should be the same
    assert replaced2.implicit_field == 100

    # Should preserve the descriptor
    assert replaced._desc is msg._desc
    assert replaced._desc is MixedFieldsWithRequired._desc


def test_shallow_copy_does_not_contaminate_original_presence() -> None:
    """Test that modifying a shallow copy does not mutate the original's presence tracking."""
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42
    copied = copy.copy(msg)

    # Set a new field on the copy that was not present on the original
    copied.legacy_required_field = "new"

    # The copy should have presence for the new field
    assert copied.has_field("legacy_required_field")
    # The original must NOT gain presence from the copy's mutation
    assert not msg.has_field("legacy_required_field")


@requires_python_3_13
def test_replace_does_not_contaminate_original_presence() -> None:
    """Test that copy.replace does not mutate the original's presence tracking."""
    msg = MixedFieldsWithRequired()
    assert not msg.has_field("explicit_field")

    replaced = copy.replace(msg, explicit_field=99)  # type: ignore

    # The replaced instance should have presence
    assert replaced.has_field("explicit_field")
    assert replaced.explicit_field == 99
    # The original must NOT gain presence from the replace call
    assert not msg.has_field("explicit_field")


@requires_python_3_13
def test_replace_mutable_field_behavior() -> None:
    """Test copy.replace behavior with mutable fields."""
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "nested"
    msg = MixedFieldsWithRequired()
    msg.repeated_field = ["a", "b", "c"]
    msg.map_field = {"key1": 1}
    msg.message_field = bar

    # When not replacing mutable fields, they should be shared (shallow copy)
    replaced = copy.replace(msg, explicit_field=99)  # type: ignore
    assert replaced.repeated_field is msg.repeated_field
    assert replaced.map_field is msg.map_field
    assert replaced.message_field is msg.message_field
    assert replaced.message_field is bar

    # When explicitly replacing mutable fields, new values should be used
    new_list = ["x", "y", "z"]
    new_map = {"key2": 2}
    replaced2 = copy.replace(msg, repeated_field=new_list, map_field=new_map)  # type: ignore

    # Original should be unchanged
    assert msg.repeated_field == ["a", "b", "c"]
    assert msg.map_field == {"key1": 1}
    # Replaced should have new values
    assert replaced2.repeated_field is new_list
    assert replaced2.map_field is new_map


@requires_python_3_13
def test_replace_with_none() -> None:
    """Test that copy.replace can set fields to None."""
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "test"
    msg = MixedFieldsWithRequired()
    msg.message_field = bar
    msg.oneof_group = Oneof("oneof_field", "value")
    replaced = copy.replace(msg, message_field=None, oneof_group=None)  # type: ignore

    # Original should be unchanged
    assert msg.message_field is bar
    assert msg.oneof_group is not None
    # Replaced should have None values
    assert replaced.message_field is None
    assert replaced.oneof_group is None


@requires_python_3_13
def test_replace_unknown_field() -> None:
    """Test that __replace__ raises AttributeError for unknown fields."""
    msg = MixedFieldsWithRequired(explicit_field=1)

    # Should raise AttributeError for unknown field, matching __setattr__ behavior
    with pytest.raises(
        AttributeError,
        match=r"'MixedFieldsWithRequired' object has no attribute 'nonexistent_field'",
    ):
        copy.replace(msg, nonexistent_field="should error")  # type: ignore


@requires_python_3_13
def test_replace_invalid_type() -> None:
    """Test copy.replace() behavior when setting a field to an invalid type.

    Currently, copy.replace() does not perform runtime type validation and will
    accept any value. Type mismatches will be caught at serialization time
    or by static type checkers.
    """
    msg = MixedFieldsWithRequired(legacy_required_field="valid string")

    # This should work - the type is correct
    result = copy.replace(msg, legacy_required_field="another string")  # type: ignore
    assert result.legacy_required_field == "another string"

    # Currently, this does NOT raise an error at assignment time.
    # Type validation happens at serialization or via static type checkers.
    result2 = copy.replace(msg, legacy_required_field=12345)  # type: ignore
    assert result2.legacy_required_field == 12345  # type: ignore[comparison-overlap]


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_preserves_presence_with_fields_set(
    copy_func: Callable[[Any], Any],
) -> None:
    """Test that copy preserves presence for various field types when fields are set."""
    bar = MixedFieldsWithRequired.Bar()
    bar.value = "nested"

    msg = MixedFieldsWithRequired()
    # Set various field types
    msg.explicit_field = 42
    msg.implicit_field = 100
    msg.legacy_required_field = "required"
    msg.repeated_field = ["a", "b"]
    msg.message_field = bar
    msg.field_with_default = 99
    msg.map_field = {"key": 1}
    msg.oneof_group = Oneof("oneof_field", "oneof_value")

    # All fields should be present
    assert msg.has_field("explicit_field")
    assert msg.has_field("implicit_field")
    assert msg.has_field("legacy_required_field")
    assert msg.has_field("repeated_field")
    assert msg.has_field("message_field")
    assert msg.has_field("field_with_default")
    assert msg.has_field("map_field")
    assert msg.oneof_group == Oneof("oneof_field", "oneof_value")
    assert msg.has_field("oneof_field")

    # Copy and verify presence is preserved
    copied = copy_func(msg)
    assert copied.has_field("explicit_field")
    assert copied.has_field("implicit_field")
    assert copied.has_field("legacy_required_field")
    assert copied.has_field("repeated_field")
    assert copied.has_field("message_field")
    assert copied.has_field("field_with_default")
    assert copied.has_field("map_field")
    assert copied.oneof_group == Oneof("oneof_field", "oneof_value")
    assert copied.has_field("oneof_field")


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_preserves_presence_with_fields_unset(
    copy_func: Callable[[Any], Any],
) -> None:
    """Test that copy preserves absence for various field types when fields are not set."""
    msg = MixedFieldsWithRequired()
    # Don't set any fields - they should all be absent

    # All fields should be absent
    assert not msg.has_field("explicit_field")
    assert not msg.has_field(
        "implicit_field"
    )  # Zero value means not present for implicit
    assert not msg.has_field("legacy_required_field")
    assert not msg.has_field("repeated_field")
    assert not msg.has_field("message_field")
    assert not msg.has_field("field_with_default")
    assert not msg.has_field("map_field")
    assert msg.oneof_group is None
    assert not msg.has_field("oneof_field")

    # Copy and verify absence is preserved
    copied = copy_func(msg)
    assert not copied.has_field("explicit_field")
    assert not copied.has_field("implicit_field")
    assert not copied.has_field("legacy_required_field")
    assert not copied.has_field("repeated_field")
    assert not copied.has_field("message_field")
    assert not copied.has_field("field_with_default")
    assert not copied.has_field("map_field")
    assert copied.oneof_group is None
    assert not copied.has_field("oneof_field")


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_message_subclass(copy_func: Callable[[Any], Any]) -> None:
    """Test that copy works with arbitrary subclasses."""

    class SubMessage(MixedFieldsWithRequired):
        __slots__ = ()

    msg = SubMessage()
    msg.explicit_field = 42
    msg.implicit_field = 100
    copied = copy_func(msg)

    # Should be a different instance
    assert copied is not msg
    # Should be the same type
    assert type(copied) is type(msg)
    # Should have the same field values
    assert copied.explicit_field == 42
    assert copied.implicit_field == 100


@pytest.mark.parametrize("copy_func", [copy.copy, copy.deepcopy])
def test_copy_with_unknown_fields(copy_func: Callable[[Any], Any]) -> None:
    """Test that copy creates independent unknown fields."""
    msg = MixedFieldsWithRequired()
    msg._get_or_init_unknown_fields()[999] = [b"bear"]

    copied = copy_func(msg)
    assert copied._get_or_init_unknown_fields() == {999: [b"bear"]}
    copied._get_or_init_unknown_fields()[999].append(b"cat")
    # Original should not be affected
    assert msg._get_or_init_unknown_fields() == {999: [b"bear"]}
