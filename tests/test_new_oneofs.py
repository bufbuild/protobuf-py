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

from typing import Literal, TypeAlias

from typing_extensions import assert_never

from protobuf import Message, Oneof
from protobuf.wkt import Struct, Value
from tests.gen.messages_pb import MixedFields

# Type alias for pattern matching test
StringOrInt: TypeAlias = Oneof[Literal["text"], str] | Oneof[Literal["number"], int]


def test_oneof_creation() -> None:
    """Test creating Oneof instances."""
    # Create a string oneof
    str_oneof = Oneof(field="name", value="Alice")
    assert str_oneof.field == "name"
    assert str_oneof.value == "Alice"

    # Create an int oneof
    int_oneof = Oneof(field="age", value=30)
    assert int_oneof.field == "age"
    assert int_oneof.value == 30

    # Create a message oneof (using a dict as a placeholder)
    msg_oneof = Oneof(field="profile", value={"name": "Bob"})
    assert msg_oneof.field == "profile"
    assert msg_oneof.value == {"name": "Bob"}


def test_oneof_pattern_matching() -> None:
    """Test pattern matching with Oneof for type narrowing."""

    def process_value(val: StringOrInt) -> str:
        match val:
            case Oneof(field="text", value=v):
                # v should be narrowed to str
                return f"String: {v.upper()}"
            case Oneof("number", v):
                # v should be narrowed to int
                return f"Number: {v * 2}"
            case _:
                assert_never(val)

    # Test with string case
    str_val: StringOrInt = Oneof[Literal["text"], str](field="text", value="hello")
    assert process_value(str_val) == "String: HELLO"

    # Test with int case
    int_val: StringOrInt = Oneof[Literal["number"], int](field="number", value=21)
    assert process_value(int_val) == "Number: 42"


def test_oneof_covariance() -> None:
    """Test that generated oneofs are assignable to wider Oneof types."""

    def describe(o: Oneof[str, object]) -> str:
        return f"{o.field}={o.value!r}"

    def active_message(o: Oneof[str, Message]) -> Message:
        return o.value

    v = Value.from_python("hi")
    assert v.kind is not None
    # Literal field name widens to str, value type widens to object
    assert describe(v.kind) == "string_value='hi'"

    s = Value.from_python({"a": 1})
    assert s.kind is not None
    assert s.kind.field == "struct_value"
    # Struct widens to Message
    assert isinstance(active_message(s.kind), Struct)


def test_oneof_descriptor_access() -> None:
    """Test accessing oneof descriptors from the oneofs list."""
    # Get the message descriptor
    desc = MixedFields._desc

    # Access oneofs from the list
    assert len(desc.oneofs) == 1
    oneof_desc = desc.oneofs[0]

    assert oneof_desc.name == "oneof_group"
    assert oneof_desc.local_name == "oneof_group"
    assert oneof_desc.parent == desc
