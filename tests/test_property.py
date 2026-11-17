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

from typing import TYPE_CHECKING, Any

import pytest
from hypothesis import given, settings, strategies as st

from protobuf import Oneof

from .gen.delimited_encoding_pb import DelimitedEncoding
from .gen.lists_pb import Lists
from .gen.maps_pb import Maps
from .gen.messages_pb import MixedFields, Recursive
from .gen.scalars_pb import Scalars

if TYPE_CHECKING:
    from protobuf import Message

# Exceptions the parsers are allowed to raise on malformed input. Anything
# else (or a crash) is a bug.
_PARSE_ERRORS = (ValueError, EOFError, RecursionError)

_int32 = st.integers(min_value=-(2**31), max_value=2**31 - 1)
_int64 = st.integers(min_value=-(2**63), max_value=2**63 - 1)
_uint32 = st.integers(min_value=0, max_value=2**32 - 1)
_uint64 = st.integers(min_value=0, max_value=2**64 - 1)
# NaN breaks the equality assertion (NaN != NaN); float32 width keeps
# 32-bit float fields exactly representable so they round-trip losslessly.
_double = st.floats(allow_nan=False)
_float = st.floats(allow_nan=False, width=32)


def _maybe(strategy: st.SearchStrategy[Any]) -> st.SearchStrategy[Any]:
    """Value or None, so field presence is exercised too."""
    return st.none() | strategy


_scalars = st.builds(
    Scalars,
    double_field=_maybe(_double),
    float_field=_maybe(_float),
    int32_field=_maybe(_int32),
    int64_field=_maybe(_int64),
    uint32_field=_maybe(_uint32),
    uint64_field=_maybe(_uint64),
    sint32_field=_maybe(_int32),
    sint64_field=_maybe(_int64),
    fixed32_field=_maybe(_uint32),
    fixed64_field=_maybe(_uint64),
    sfixed32_field=_maybe(_int32),
    sfixed64_field=_maybe(_int64),
    bool_field=_maybe(st.booleans()),
    string_field=_maybe(st.text()),
    bytes_field=_maybe(st.binary()),
)

_lists = st.builds(
    Lists,
    double_list=st.lists(_double),
    float_list=st.lists(_float),
    int32_list=st.lists(_int32),
    sint64_list=st.lists(_int64),
    fixed32_list=st.lists(_uint32),
    bool_list=st.lists(st.booleans()),
    string_list=st.lists(st.text()),
    bytes_list=st.lists(st.binary()),
)

_maps = st.builds(
    Maps,
    int32_to_int32=st.dictionaries(_int32, _int32),
    sint64_to_sint64=st.dictionaries(_int64, _int64),
    bool_to_bool=st.dictionaries(st.booleans(), st.booleans()),
    string_to_string=st.dictionaries(st.text(), st.text()),
    string_to_bytes=st.dictionaries(st.text(), st.binary()),
    string_to_double=st.dictionaries(st.text(), _double),
)

_recursives = st.recursive(
    st.builds(Recursive),
    lambda children: st.builds(
        Recursive,
        recursive=_maybe(children),
        repeated_recursive=st.lists(children, max_size=3),
        map_recursive=st.dictionaries(st.text(), children, max_size=3),
    ),
    max_leaves=10,
)

_oneofs = st.one_of(
    st.builds(Oneof, field=st.just("oneof_field"), value=st.text()),
    st.builds(Oneof, field=st.just("oneof_baz"), value=_int32),
)

_mixed_fields = st.builds(
    MixedFields,
    explicit_field=_maybe(_int32),
    implicit_field=_int32,
    repeated_field=st.lists(st.text()),
    message_field=_maybe(st.builds(MixedFields.Bar, value=_maybe(st.text()))),
    field_with_default=_maybe(_int32),
    map_field=st.dictionaries(st.text(), _int32),
    oneof_group=_maybe(_oneofs),
    implicit_enum_field=st.sampled_from(MixedFields.E),
    explicit_enum_field=_maybe(st.sampled_from(MixedFields.E)),
)

_messages = st.one_of(_scalars, _lists, _maps, _recursives, _mixed_fields)


@settings(deadline=None)
@given(msg=_messages)
def test_binary_roundtrip(msg: Message[Any]) -> None:
    """Serializing and re-parsing any message must reproduce it exactly."""
    data = msg.to_binary()
    parsed = type(msg).from_binary(data)
    assert parsed == msg
    if isinstance(msg, (Scalars, Lists)):
        # Map entry order on the wire is unspecified, so re-serialization
        # is only byte-identical for map-free message types.
        assert parsed.to_binary() == data


@settings(deadline=None)
@given(msg=_messages)
def test_json_roundtrip(msg: Message[Any]) -> None:
    """Serializing to ProtoJSON and re-parsing must reproduce the message."""
    parsed = type(msg).from_json(msg.to_json())
    assert parsed == msg


@pytest.mark.parametrize(
    "msg_type", [Scalars, Lists, Maps, Recursive, MixedFields, DelimitedEncoding]
)
@settings(deadline=None)
@given(data=st.binary(max_size=256))
def test_from_binary_arbitrary_bytes(msg_type: type[Message[Any]], data: bytes) -> None:
    """Arbitrary bytes must parse or fail cleanly, never crash.

    When garbage happens to parse, serializing the result (unknown fields
    included) must produce bytes that parse cleanly again. Byte-identical
    round trips are not asserted here: map entry order on the wire is
    unspecified, and a fuzzed signaling NaN in a 32-bit float field may be
    quieted by the float/double conversion on parse.
    """
    try:
        msg = msg_type.from_binary(data)
    except _PARSE_ERRORS:
        return
    msg_type.from_binary(msg.to_binary())
