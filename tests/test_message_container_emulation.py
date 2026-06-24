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
"""Tests for Message container emulation methods (__getitem__, __setitem__, __contains__, __delitem__)."""

from __future__ import annotations

import re
import typing
from typing import Any, cast

import pytest

import protobuf
from protobuf import Oneof
from tests.gen.messages_pb import MixedFieldsWithRequired

if typing.TYPE_CHECKING:
    from tests.conftest import Protoc


desc_explicit_field = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "explicit_field"
]
desc_implicit_field = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "implicit_field"
]
desc_legacy_required_field = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "legacy_required_field"
]
desc_repeated_field = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "repeated_field"
]
desc_message_field = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "message_field"
]
desc_field_with_default = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "field_with_default"
]
desc_map_field = MixedFieldsWithRequired.desc()._fields_by_local_name["map_field"]
desc_implicit_enum_field = MixedFieldsWithRequired.desc()._fields_by_local_name[
    "implicit_enum_field"
]
desc_oneof_group = MixedFieldsWithRequired.desc()._oneofs_by_local_name["oneof_group"]
desc_oneof_field = desc_oneof_group._fields_by_name["oneof_field"]
desc_oneof_baz = desc_oneof_group._fields_by_name["oneof_baz"]


def test_basic_container_operations() -> None:
    """Test basic __getitem__, __setitem__, and __contains__ operations."""
    msg = MixedFieldsWithRequired()

    # Set and get fields using actual field names from the descriptor
    msg[desc_explicit_field] = 42
    msg[desc_implicit_field] = 100
    assert msg[desc_explicit_field] == 42
    assert msg[desc_implicit_field] == 100

    # Check presence
    assert desc_explicit_field in msg
    assert desc_implicit_field in msg
    assert desc_legacy_required_field not in msg
    assert desc_implicit_enum_field not in msg

    # Update existing value
    msg[desc_explicit_field] = 200
    assert msg[desc_explicit_field] == 200

    msg[desc_implicit_enum_field] = MixedFieldsWithRequired.E.UNSPECIFIED
    assert desc_implicit_enum_field not in msg
    msg[desc_implicit_enum_field] = MixedFieldsWithRequired.E.ONE
    assert desc_implicit_enum_field in msg
    assert msg[desc_implicit_enum_field] == MixedFieldsWithRequired.E.ONE


def test_delitem_operations() -> None:
    """Test __delitem__ clears fields to their default values."""
    msg = MixedFieldsWithRequired()

    # Delete a non-existent field (should not raise)
    del msg[desc_legacy_required_field]
    assert desc_legacy_required_field not in msg

    # int32 explicit_field = 1;
    msg.explicit_field = 101
    assert desc_explicit_field in msg
    del msg[desc_explicit_field]
    assert desc_explicit_field not in msg

    # int32 implicit_field = 2 [features.field_presence = IMPLICIT];
    msg.implicit_field = 102
    assert desc_implicit_field in msg
    del msg[desc_implicit_field]
    assert desc_implicit_field not in msg

    # string legacy_required_field = 3 [features.field_presence = LEGACY_REQUIRED];
    msg.legacy_required_field = "value legacy required"
    assert desc_legacy_required_field in msg
    del msg[desc_legacy_required_field]
    assert desc_legacy_required_field not in msg

    # repeated string repeated_field = 4;
    msg.repeated_field = ["a", "b", "c"]
    assert desc_repeated_field in msg
    del msg[desc_repeated_field]
    assert desc_repeated_field not in msg

    # Bar message_field = 5;
    msg.message_field = MixedFieldsWithRequired.Bar()
    assert desc_message_field in msg
    del msg[desc_message_field]
    assert desc_message_field not in msg

    # int32 field_with_default = 6 [default = 42];
    msg.field_with_default = 0
    assert desc_field_with_default in msg
    del msg[desc_field_with_default]
    assert desc_field_with_default not in msg

    # map<string, int32> map_field = 7;
    msg.map_field = {"a": 1, "b": 2}
    assert desc_map_field in msg
    del msg[desc_map_field]
    assert desc_map_field not in msg

    # string oneof_field = 8;
    msg.oneof_group = protobuf.Oneof(field="oneof_field", value="")
    assert desc_oneof_field in msg
    del msg[desc_oneof_field]
    assert desc_oneof_field not in msg
    assert msg.oneof_group is None


def test_oneof_operations() -> None:
    """Test operations with oneofs, and oneof member fields."""
    msg = MixedFieldsWithRequired()

    # Assign by oneof member field
    msg[desc_oneof_field] = "abc"
    assert msg.oneof_group == Oneof(field="oneof_field", value="abc")
    assert msg[desc_oneof_field] == "abc"
    assert msg[desc_oneof_baz] == 0
    assert desc_oneof_field in msg
    assert desc_oneof_baz not in msg

    # Re-assign by oneof member field
    msg[desc_oneof_baz] = 123
    assert msg.oneof_group == Oneof(field="oneof_baz", value=123)
    assert msg[desc_oneof_field] == ""
    assert msg[desc_oneof_baz] == 123
    assert desc_oneof_field not in msg
    assert desc_oneof_baz in msg

    # Clear by unassigned oneof member field
    del msg[desc_oneof_field]
    assert msg.oneof_group == Oneof(field="oneof_baz", value=123)
    assert desc_oneof_field not in msg
    assert desc_oneof_baz in msg


def test_iter() -> None:
    """Test that __iter__ iterates over set message fields."""
    msg = MixedFieldsWithRequired()

    assert len(list(msg)) == 0
    for field in msg:
        assert field in msg

    msg.implicit_field = 100
    for field in msg:
        assert field in msg
    assert len(list(msg)) == 1
    assert next(iter(msg)).name == "implicit_field"


def test_getitem_type_error() -> None:
    """Test that __getitem__ raises TypeError for unsupported types.

    See https://docs.python.org/3/reference/datamodel.html#object.__getitem__
    """
    msg = MixedFieldsWithRequired.Bar()
    invalid_key = cast("Any", "explicit_field")
    with pytest.raises(TypeError, match="key must be a DescField, not str"):
        _ = msg[invalid_key]


def test_getitem_key_error() -> None:
    """Test that __getitem__ raises KeyError for non-existent field, foreign oneof and foreign field.

    See https://docs.python.org/3/reference/datamodel.html#object.__getitem__
    """
    msg = MixedFieldsWithRequired.Bar()
    field_presence_field = MixedFieldsWithRequired.desc().fields[0]
    with pytest.raises(
        KeyError,
        match=re.escape(
            "field MixedFieldsWithRequired.explicit_field cannot be used with message MixedFieldsWithRequired.Bar"
        ),
    ):
        _ = msg[field_presence_field]


def test_delitem_type_error() -> None:
    """Test that __delitem__ raises TypeError for unsupported types.

    See https://docs.python.org/3/reference/datamodel.html#object.__delitem__
    """
    msg = MixedFieldsWithRequired.Bar()
    invalid_key = cast("Any", "explicit_field")
    with pytest.raises(TypeError, match=re.escape("key must be a DescField, not str")):
        del msg[invalid_key]


def test_delitem_key_error() -> None:
    """Test that __delitem__ raises KeyError for non-existent field, foreign oneof and foreign field.

    See https://docs.python.org/3/reference/datamodel.html#object.__delitem__
    """
    msg = MixedFieldsWithRequired.Bar()
    field_presence_field = MixedFieldsWithRequired.desc().fields[0]
    with pytest.raises(
        KeyError,
        match=re.escape(
            "field MixedFieldsWithRequired.explicit_field cannot be used with message MixedFieldsWithRequired.Bar"
        ),
    ):
        del msg[field_presence_field]


def test_setitem_type_error() -> None:
    """Test that __setitem__ raises TypeError for unsupported types.

    See https://docs.python.org/3/reference/datamodel.html#object.__setitem__
    """
    msg = MixedFieldsWithRequired.Bar()
    invalid_key = cast("Any", "explicit_field")
    with pytest.raises(TypeError, match="key must be a DescField, not str"):
        msg[invalid_key] = 123


def test_setitem_key_error() -> None:
    """Test __setitem__ raises KeyError for non-existent field, foreign oneof and foreign field.

    See https://docs.python.org/3/reference/datamodel.html#object.__setitem__
    """
    msg = MixedFieldsWithRequired.Bar()
    field_presence_field = MixedFieldsWithRequired.desc().fields[0]
    with pytest.raises(
        KeyError,
        match=re.escape(
            "field MixedFieldsWithRequired.explicit_field cannot be used with message MixedFieldsWithRequired.Bar"
        ),
    ):
        msg[field_presence_field] = 123


def test_nested_and_list_fields() -> None:
    """Test container methods work with nested messages and lists."""
    msg = MixedFieldsWithRequired()

    # Message field
    nested = MixedFieldsWithRequired()
    nested.explicit_field = 5
    msg[desc_message_field] = nested
    assert msg[desc_message_field].explicit_field == 5

    # List field (repeated_field is a repeated string in the descriptor)
    msg[desc_repeated_field] = ["a", "b", "c"]
    assert msg[desc_repeated_field] == ["a", "b", "c"]
    msg[desc_repeated_field].append("d")
    assert msg[desc_repeated_field] == ["a", "b", "c", "d"]


def test_unset_field_presence() -> None:
    """Test that cleared fields are not considered set."""
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42

    # Initially set
    assert desc_explicit_field in msg

    # Clear the field
    del msg[desc_explicit_field]
    assert desc_explicit_field not in msg
    # __getitem__ returns default value for unset fields
    assert msg[desc_explicit_field] == 0

    # Delete clears to default
    msg.implicit_field = 100
    del msg[desc_implicit_field]
    assert msg[desc_explicit_field] == 0


def test_descriptor_based_access() -> None:
    """Test container operations using DescField descriptors."""
    msg = MixedFieldsWithRequired()

    # Get DescField objects from the descriptor
    explicit_field_desc = msg.desc()._fields_by_local_name["explicit_field"]
    implicit_field_desc = msg.desc()._fields_by_local_name["implicit_field"]
    repeated_field_desc = msg.desc()._fields_by_local_name["repeated_field"]

    # Set using DescField
    msg[explicit_field_desc] = 42
    msg[implicit_field_desc] = 100

    # Get using DescField
    assert msg[explicit_field_desc] == 42
    assert msg[implicit_field_desc] == 100

    # Check presence using DescField
    assert explicit_field_desc in msg
    assert implicit_field_desc in msg
    assert repeated_field_desc not in msg

    # Delete using DescField
    del msg[explicit_field_desc]
    assert explicit_field_desc not in msg
    assert msg[explicit_field_desc] == 0


KEYWORD_FIELD_PROTO = """\
edition = "2023";

message KeywordFields {
  string from = 1;
  bool class = 2 [features.field_presence = IMPLICIT];
  oneof import {
    string foo = 3;
    int32 def = 4;
  }
}
"""


def test_container_bool_keyword_field(protoc: Protoc) -> None:
    """Bool field with keyword proto name works via container emulation."""
    msg_class = protoc.compile_message(KEYWORD_FIELD_PROTO).type
    msg = msg_class()
    desc_class = msg_class.desc()._fields_by_local_name["class_"]

    msg[desc_class] = True
    assert msg[desc_class] is True
    assert desc_class in msg

    # Attribute access still uses local name
    assert cast("Any", msg).class_ is True
