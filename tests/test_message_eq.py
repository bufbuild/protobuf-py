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

import math
import platform

import pytest

from protobuf import Message, Oneof
from tests.gen.lists_pb import Lists
from tests.gen.messages_pb import MixedFields
from tests.gen.scalars_pb import Scalars


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (MixedFields(), MixedFields()),
        (MixedFields(), MixedFields(implicit_field=0)),
        (MixedFields(), MixedFields(repeated_field=[])),
        (MixedFields(), MixedFields(map_field={})),
        (
            MixedFields(repeated_field=["a", "b"]),
            MixedFields(repeated_field=["a", "b"]),
        ),
        (MixedFields(map_field={"a": 1}), MixedFields(map_field={"a": 1})),
        (
            MixedFields(message_field=MixedFields.Bar(value="hi")),
            MixedFields(message_field=MixedFields.Bar(value="hi")),
        ),
        (
            MixedFields(explicit_enum_field=MixedFields.E.ONE),
            MixedFields(explicit_enum_field=MixedFields.E.ONE),
        ),
        (
            MixedFields(oneof_group=Oneof(field="oneof_field", value="hello")),
            MixedFields(oneof_group=Oneof(field="oneof_field", value="hello")),
        ),
    ],
)
def test_equal(a: Message, b: Message) -> None:
    assert a == b
    assert b == a


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (MixedFields(), 42),
        (MixedFields(), "hello"),
        (MixedFields(), None),
        (MixedFields.Bar(), None),
        (MixedFields(), MixedFields(explicit_field=0)),
        (MixedFields(implicit_field=1), MixedFields(implicit_field=2)),
        (
            MixedFields(repeated_field=["a", "b"]),
            MixedFields(repeated_field=["b", "a"]),
        ),
        (MixedFields(map_field={"a": 1}), MixedFields(map_field={"a": 2})),
        (
            MixedFields(message_field=MixedFields.Bar(value="hi")),
            MixedFields(message_field=MixedFields.Bar(value="bye")),
        ),
        (MixedFields(), MixedFields(message_field=MixedFields.Bar())),
        (MixedFields(field_with_default=42), MixedFields()),
        (
            MixedFields(explicit_enum_field=MixedFields.E.ONE),
            MixedFields(explicit_enum_field=MixedFields.E.TWO),
        ),
        (
            MixedFields(oneof_group=Oneof(field="oneof_field", value="hello")),
            MixedFields(oneof_group=Oneof(field="oneof_field", value="world")),
        ),
        (
            MixedFields(oneof_group=Oneof(field="oneof_field", value="hello")),
            MixedFields(oneof_group=Oneof(field="oneof_baz", value=1)),
        ),
        (
            MixedFields(oneof_group=Oneof(field="oneof_field", value="hello")),
            MixedFields(),
        ),
    ],
)
def test_not_equal(
    a: Message | int | str | None, b: Message | int | str | None
) -> None:
    assert a != b
    assert b != a


def test_eq_unknown_fields_ignored() -> None:
    a = MixedFields(explicit_field=1)
    b = MixedFields(explicit_field=1)
    a._get_or_init_unknown_fields()[999] = [b"\x01\x02"]
    assert a == b


def test_eq_not_hashable() -> None:
    with pytest.raises(TypeError):
        hash(MixedFields())


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (Scalars(float_field=math.nan), Scalars(float_field=math.nan)),
        (Lists(float_list=[math.nan]), Lists(float_list=[math.nan])),
    ],
)
def test_eq_nan(a: Message, b: Message) -> None:
    """Same as with built-in containers, the same nan is equal."""
    assert a == b


@pytest.mark.skipif(
    platform.python_implementation() == "PyPy",
    reason="PyPy's NaN are always equal. We go ahead and align with CPython",
)
@pytest.mark.parametrize(
    ("a", "b"),
    [
        (Scalars(float_field=float("nan")), Scalars(float_field=float("nan"))),
        (Lists(float_list=[float("nan")]), Lists(float_list=[float("nan")])),
    ],
)
def test_not_equal_nan(a: Message, b: Message) -> None:
    """Same as with built-in containers, different nan are not equal."""
    assert a != b
