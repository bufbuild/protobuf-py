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
"""Tests for Message initialization with and without arguments."""

from __future__ import annotations

import re
import typing
from typing import Any, cast

import pytest

from protobuf import DescFieldValueEnum, Oneof
from tests.gen.messages_pb import MixedFieldsWithRequired

if typing.TYPE_CHECKING:
    from tests.conftest import Protoc


def test_message_init() -> None:
    """Test that messages initialize all attributes to their default values."""
    msg = MixedFieldsWithRequired()
    assert msg.explicit_field == 0
    assert msg.implicit_field == 0
    assert msg.legacy_required_field == ""
    assert msg.repeated_field == []
    assert msg.message_field is None
    assert msg.field_with_default == 42
    assert msg.map_field == {}
    assert msg.oneof_group is None
    assert msg.explicit_enum_field == MixedFieldsWithRequired.E.UNSPECIFIED
    assert isinstance(msg.explicit_enum_field, MixedFieldsWithRequired.E)

    assert not msg.has_field("explicit_field")
    assert not msg.has_field("implicit_field")
    assert not msg.has_field("legacy_required_field")
    assert not msg.has_field("repeated_field")
    assert not msg.has_field("message_field")
    assert not msg.has_field("field_with_default")
    assert not msg.has_field("map_field")
    assert not msg.has_field("oneof_field")
    assert not msg.has_field("oneof_baz")
    assert not msg.has_field("explicit_enum_field")


def test_message_init_default_args() -> None:
    """Test that messages init accepts default field values, leaving all fields unset."""
    msg = MixedFieldsWithRequired(
        explicit_field=None,
        implicit_field=0,
        legacy_required_field=None,
        repeated_field=None,
        message_field=None,
        field_with_default=None,
        map_field=None,
        oneof_group=None,
    )
    assert msg.explicit_field == 0
    assert msg.implicit_field == 0
    assert msg.legacy_required_field == ""
    assert msg.repeated_field == []
    assert msg.message_field is None
    assert msg.field_with_default == 42
    assert msg.map_field == {}
    assert msg.oneof_group is None
    assert not msg.has_field("explicit_field")
    assert not msg.has_field("implicit_field")
    assert not msg.has_field("legacy_required_field")
    assert not msg.has_field("repeated_field")
    assert not msg.has_field("message_field")
    assert not msg.has_field("field_with_default")
    assert not msg.has_field("map_field")
    assert not msg.has_field("oneof_field")
    assert not msg.has_field("oneof_baz")


def test_message_init_arg_zeroish_values() -> None:
    """Test that messages init accepts zero-ish field values, making all fields present."""
    bar = MixedFieldsWithRequired.Bar()
    msg = MixedFieldsWithRequired(
        explicit_field=0,
        implicit_field=1,
        legacy_required_field="",
        repeated_field=[""],
        message_field=bar,
        field_with_default=0,
        map_field={"": 0},
        oneof_group=Oneof(field="oneof_field", value=""),
    )
    assert msg.explicit_field == 0
    assert msg.implicit_field == 1
    assert msg.legacy_required_field == ""
    assert msg.repeated_field == [""]
    assert msg.message_field is bar
    assert msg.field_with_default == 0
    assert msg.map_field == {"": 0}
    assert msg.oneof_group == Oneof(field="oneof_field", value="")
    assert msg.has_field("explicit_field")
    assert msg.has_field("implicit_field")
    assert msg.has_field("legacy_required_field")
    assert msg.has_field("repeated_field")
    assert msg.has_field("message_field")
    assert msg.has_field("field_with_default")
    assert msg.has_field("map_field")
    assert msg.has_field("oneof_field")
    assert not msg.has_field("oneof_baz")


def test_message_init_arg_values() -> None:
    """Test that messages init accepts field values, making all fields present."""
    bar = MixedFieldsWithRequired.Bar()
    msg = MixedFieldsWithRequired(
        explicit_field=1,
        implicit_field=2,
        legacy_required_field="3",
        repeated_field=["4"],
        message_field=bar,
        field_with_default=6,
        map_field={"": 7},
        oneof_group=Oneof(field="oneof_field", value="8"),
    )
    assert msg.explicit_field == 1
    assert msg.implicit_field == 2
    assert msg.legacy_required_field == "3"
    assert msg.repeated_field == ["4"]
    assert msg.message_field is bar
    assert msg.field_with_default == 6
    assert msg.map_field == {"": 7}
    assert msg.oneof_group == Oneof(field="oneof_field", value="8")
    assert msg.has_field("explicit_field")
    assert msg.has_field("implicit_field")
    assert msg.has_field("legacy_required_field")
    assert msg.has_field("repeated_field")
    assert msg.has_field("message_field")
    assert msg.has_field("field_with_default")
    assert msg.has_field("map_field")
    assert msg.has_field("oneof_field")


def test_message_unknown_arg() -> None:
    """Test that messages init raises error when unknown field is passed."""
    with pytest.raises(
        TypeError,
        match=re.escape(
            r"MixedFieldsWithRequired.__init__() got an unexpected keyword argument 'nonexistent_field'"
        ),
    ):
        _ = cast("Any", MixedFieldsWithRequired)(nonexistent_field="should error")
    with pytest.raises(
        TypeError,
        match=re.escape(
            r"MixedFieldsWithRequired.Bar.__init__() got an unexpected keyword argument 'nonexistent_field'"
        ),
    ):
        _ = cast("Any", MixedFieldsWithRequired.Bar)(nonexistent_field="should error")


UNKNOWN_FIELDS_PROTO = """\
edition = "2023";

message UnknownFields {
  string hello = 1;
  oneof choice {
    string foo = 3;
    int32 bar = 4;
  }
}
"""


def test_message_setattr_unknown_field(protoc: Protoc) -> None:
    """Test that setting an unknown field via attribute assignment raises an error."""
    msg_class = protoc.compile_message(UNKNOWN_FIELDS_PROTO).type
    msg = cast("Any", msg_class())

    with pytest.raises(AttributeError, match="has no attribute 'foo'"):
        msg.foo = "hello"

    with pytest.raises(AttributeError, match="has no attribute 'bar'"):
        msg.bar = 400

    with pytest.raises(AttributeError, match="has no attribute 'foo'"):
        _ = msg.foo

    with pytest.raises(AttributeError, match="has no attribute 'nonexistent_field'"):
        msg.nonexistent_field = "should error"


def test_message_init_invalid_type() -> None:
    """Test __init__ behavior when setting a field to an invalid type.

    Currently, __init__ does not perform runtime type validation and will
    accept any value. Type mismatches will be caught at serialization time
    or by static type checkers.
    """
    # This should work - the type is correct
    msg1 = MixedFieldsWithRequired(legacy_required_field="valid string")
    assert msg1.legacy_required_field == "valid string"

    # Currently, this does NOT raise an error at initialization time.
    # Type validation happens at serialization or via static type checkers.
    msg2: Any = MixedFieldsWithRequired(legacy_required_field=cast("str", 12345))
    assert msg2.legacy_required_field == 12345


def test_enum_default_value_zero(protoc: Protoc) -> None:
    """Regression: default_value(field) must not treat integer 0 as 'no default'.

    When a proto2 enum field has [default = X] where X has number 0
    but is NOT the first declared enum value, the default must be X (0),
    not the first value.
    """
    desc = protoc.compile_message("""
        syntax="proto2";
        enum E { ONE = 1; TWO = 2; ZERO = 0; }
        message M { optional E e = 1 [default = ZERO]; }
    """)
    field = desc.fields[0]
    assert isinstance(field.value, DescFieldValueEnum)
    assert field.value.default_value == 0

    msg = desc.type()
    assert msg[field] == 0
