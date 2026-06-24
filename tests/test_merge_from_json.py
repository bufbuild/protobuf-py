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

from protobuf import merge_from_json
from tests.gen.lists_pb import Lists
from tests.gen.maps_pb import Maps
from tests.gen.messages_pb import ExplicitFields
from tests.gen.scalars_pb import Scalars


def test_scalar_overwrite() -> None:
    msg = Scalars(int32_field=10)

    merge_from_json(msg, '{"int32Field": 42}')
    assert msg.int32_field == 42


def test_nested_message_merge() -> None:
    msg = ExplicitFields(message_field=ExplicitFields.Msg(value="hello"))

    merge_from_json(msg, '{"messageField": {"value": "world"}}')
    assert msg.message_field is not None
    assert msg.message_field.value == "world"


def test_repeated_append() -> None:
    msg = Lists(string_list=["a", "b"])

    merge_from_json(msg, '{"stringList": ["c", "d"]}')
    assert msg.string_list == ["a", "b", "c", "d"]


def test_map_merge() -> None:
    msg = Maps(string_to_string={"a": "1", "b": "2"})

    merge_from_json(msg, '{"stringToString": {"b": "99", "c": "3"}}')
    assert dict(msg.string_to_string) == {"a": "1", "b": "99", "c": "3"}


def test_merge_empty_data() -> None:
    msg = Scalars(int32_field=42)

    merge_from_json(msg, "{}")
    assert msg.int32_field == 42


def test_unknown_fields_raises() -> None:
    msg = Scalars()
    with pytest.raises(ValueError, match="unknown"):
        merge_from_json(msg, '{"noSuchField": 1}')


def test_unknown_fields_ignored() -> None:
    msg = Scalars(int32_field=42)

    merge_from_json(msg, '{"noSuchField": 1}', ignore_unknown_fields=True)
    assert msg.int32_field == 42
