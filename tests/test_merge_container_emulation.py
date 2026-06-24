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

from typing import Protocol, TypeVar

import pytest

from protobuf import Message, merge_from, merge_from_binary as do_merge_from_binary
from protobuf._wire import BinaryWriter, WireType
from tests.gen.messages_pb import MixedFields

T = TypeVar("T", bound=Message)


def merge_from_binary(
    target: T, source: T, *, ignore_unknown_fields: bool = False
) -> None:
    do_merge_from_binary(
        target, source.to_binary(), ignore_unknown_fields=ignore_unknown_fields
    )


MERGE = [merge_from, merge_from_binary]


class MergeFunc(Protocol):
    def __call__(
        self, target: T, source: T, *, ignore_unknown_fields: bool = False
    ) -> None: ...


@pytest.mark.parametrize("merge", MERGE)
def test_scalar_overwrite(merge: MergeFunc) -> None:
    msg = MixedFields(explicit_field=10)
    other = MixedFields(explicit_field=42)

    merge(msg, other)
    assert msg.explicit_field == 42


@pytest.mark.parametrize("merge", MERGE)
def test_nested_message_merge(merge: MergeFunc) -> None:
    msg = MixedFields(message_field=MixedFields.Bar(value="hello"))
    nested = MixedFields.Bar(value="world")
    other = MixedFields(message_field=nested)

    merge(msg, other)
    assert msg.message_field is not None
    assert msg.message_field.value == "world"
    nested.value = "changed"
    assert msg.message_field.value == "world"


@pytest.mark.parametrize("merge", MERGE)
def test_nested_message_merge_not_present(merge: MergeFunc) -> None:
    msg = MixedFields()
    nested = MixedFields.Bar(value="world")
    other = MixedFields(message_field=nested)

    merge(msg, other)
    assert msg.message_field is not None
    assert msg.message_field.value == "world"
    nested.value = "changed"
    assert msg.message_field.value == "world"


@pytest.mark.parametrize("merge", MERGE)
def test_repeated_append(merge: MergeFunc) -> None:
    msg = MixedFields(repeated_field=["a", "b"])
    other = MixedFields(repeated_field=["c", "d"])

    merge(msg, other)
    assert msg.repeated_field == ["a", "b", "c", "d"]


@pytest.mark.parametrize("merge", MERGE)
def test_map_merge(merge: MergeFunc) -> None:
    msg = MixedFields(map_field={"a": 1, "b": 2})
    other = MixedFields(map_field={"b": 99, "c": 3})

    merge(msg, other)
    assert dict(msg.map_field) == {"a": 1, "b": 99, "c": 3}


@pytest.mark.parametrize("merge", MERGE)
def test_merge_empty_data(merge: MergeFunc) -> None:
    msg = MixedFields(explicit_field=42)

    merge(msg, MixedFields())
    assert msg.explicit_field == 42


@pytest.mark.parametrize("merge", MERGE)
def test_unknown_fields_retained(merge: MergeFunc) -> None:
    w = BinaryWriter()
    w.tag(99, WireType.VARINT)
    w.int32(777)
    unknown_data = w.finish()

    msg = MixedFields()
    merge(msg, MixedFields.from_binary(unknown_data))
    assert msg._unknown_fields is not None
    assert 99 in msg._unknown_fields
    msg._unknown_fields[99] = [unknown_data]


@pytest.mark.parametrize("merge", MERGE)
def test_unknown_fields_merged(merge: MergeFunc) -> None:
    w = BinaryWriter()
    w.tag(99, WireType.VARINT)
    w.int32(777)
    unknown_data = w.finish()

    msg = MixedFields()
    # For this test, not important to be a valid field
    msg._get_or_init_unknown_fields()[99] = [b"\x01"]
    merge(msg, MixedFields.from_binary(unknown_data))
    assert msg._unknown_fields is not None
    assert 99 in msg._unknown_fields
    assert msg._unknown_fields[99] == [b"\x01", unknown_data]


@pytest.mark.parametrize("merge", MERGE)
def test_unknown_fields_ignored(merge: MergeFunc) -> None:
    w = BinaryWriter()
    w.tag(99, WireType.VARINT)
    w.int32(777)
    unknown_data = w.finish()

    msg = MixedFields()
    merge(msg, MixedFields.from_binary(unknown_data), ignore_unknown_fields=True)
    assert msg._unknown_fields is None or 99 not in msg._unknown_fields
