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
"""Tests for Message methods has_field and clear_field."""

from __future__ import annotations

import re
import typing
from typing import Any, cast

import pytest

import protobuf
from tests.gen.messages_pb import MixedFieldsWithRequired

if typing.TYPE_CHECKING:
    from tests.conftest import Protoc


def test_basic_presence() -> None:
    msg = MixedFieldsWithRequired()

    msg.explicit_field = 42
    msg.implicit_field = 100

    assert msg.has_field("explicit_field")
    assert msg.has_field("implicit_field")
    assert not msg.has_field("legacy_required_field")
    assert not msg.has_field("implicit_enum_field")

    # Update existing value
    msg.explicit_field = 200
    msg.implicit_enum_field = MixedFieldsWithRequired.E.UNSPECIFIED
    assert not msg.has_field("implicit_enum_field")
    msg.implicit_enum_field = MixedFieldsWithRequired.E.ONE
    assert msg.has_field("implicit_enum_field")
    assert msg.implicit_enum_field == MixedFieldsWithRequired.E.ONE


def test_clear_field() -> None:
    """Test __delitem__ clears fields to their default values."""
    msg = MixedFieldsWithRequired()

    # Delete a non-existent field (should not raise)
    msg.clear_field("legacy_required_field")
    assert not msg.has_field("legacy_required_field")

    # int32 explicit_field = 1;
    msg.explicit_field = 101
    assert msg.has_field("explicit_field")
    msg.clear_field("explicit_field")
    assert not msg.has_field("explicit_field")

    # int32 implicit_field = 2 [features.field_presence = IMPLICIT];
    msg.implicit_field = 102
    assert msg.has_field("implicit_field")
    msg.clear_field("implicit_field")
    assert not msg.has_field("implicit_field")

    # string legacy_required_field = 3 [features.field_presence = LEGACY_REQUIRED];
    msg.legacy_required_field = "value legacy required"
    assert msg.has_field("legacy_required_field")
    msg.clear_field("legacy_required_field")
    assert not msg.has_field("legacy_required_field")

    # repeated string repeated_field = 4;
    msg.repeated_field = ["a", "b", "c"]
    assert msg.has_field("repeated_field")
    msg.clear_field("repeated_field")
    assert not msg.has_field("repeated_field")

    # Bar message_field = 5;
    msg.message_field = MixedFieldsWithRequired.Bar()
    assert msg.has_field("message_field")
    msg.clear_field("message_field")
    assert not msg.has_field("message_field")

    # int32 field_with_default = 6 [default = 42];
    msg.field_with_default = 0
    assert msg.has_field("field_with_default")
    msg.clear_field("field_with_default")
    assert not msg.has_field("field_with_default")

    # map<string, int32> map_field = 7;
    msg.map_field = {"a": 1, "b": 2}
    assert msg.has_field("map_field")
    msg.clear_field("map_field")
    assert not msg.has_field("map_field")

    # string oneof_field = 8;
    msg.oneof_group = protobuf.Oneof(field="oneof_field", value="")
    assert msg.has_field("oneof_field")
    msg.clear_field("oneof_field")
    assert not msg.has_field("oneof_field")
    assert msg.oneof_group is None


def test_has_field_type_error() -> None:
    msg = MixedFieldsWithRequired.Bar()
    invalid_key = cast("Any", 10)
    with pytest.raises(TypeError, match="key must be a str, not int"):
        _ = msg.has_field(invalid_key)


def test_has_field_key_error() -> None:
    msg = MixedFieldsWithRequired.Bar()
    with pytest.raises(
        KeyError,
        match=re.escape(
            "unknown key for message MixedFieldsWithRequired.Bar: 'nonexistent_field'"
        ),
    ):
        _ = msg.has_field(cast("Any", "nonexistent_field"))


def test_clear_field_type_error() -> None:
    msg = MixedFieldsWithRequired.Bar()
    invalid_key = cast("Any", 10)
    with pytest.raises(TypeError, match="key must be a str, not int"):
        _ = msg.clear_field(invalid_key)


def test_clear_field_key_error() -> None:
    msg = MixedFieldsWithRequired.Bar()
    with pytest.raises(
        KeyError,
        match=re.escape(
            "unknown key for message MixedFieldsWithRequired.Bar: 'nonexistent_field'"
        ),
    ):
        msg.clear_field(cast("Any", "nonexistent_field"))


def test_unset_field_presence() -> None:
    msg = MixedFieldsWithRequired()
    msg.explicit_field = 42

    assert msg.has_field("explicit_field")

    msg.clear_field("explicit_field")
    assert not msg.has_field("explicit_field")
    assert msg.explicit_field == 0

    msg.implicit_field = 100
    msg.clear_field("implicit_field")
    assert msg.explicit_field == 0


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


def test_presence_uses_proto_name_not_local_name(protoc: Protoc) -> None:
    msg_class = protoc.compile_message(KEYWORD_FIELD_PROTO).type
    msg = cast("Any", msg_class())

    msg.from_ = "hello"
    assert msg.from_ == "hello"
    assert msg.has_field("from")
    msg.clear_field("from")
    assert not msg.has_field("from")

    # Local name (escaped) does not work, but suggests proto name
    with pytest.raises(KeyError, match=re.escape("did you mean 'from'?")):
        _ = msg.has_field("from_")
    with pytest.raises(KeyError, match=re.escape("did you mean 'from'?")):
        msg.clear_field("from_")

    with pytest.raises(KeyError, match="unknown key for message KeywordFields: 'def_'"):
        msg.has_field("def_")
