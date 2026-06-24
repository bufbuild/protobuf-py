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
"""Tests for dynamic message and enum creation from descriptors."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, cast

import pytest

import protobuf
from protobuf.wkt._mixin import (
    AnyMixin,
    DurationMixin,
    FileDescriptorSetMixin,
    TimestampMixin,
)

if TYPE_CHECKING:
    from tests.conftest import Protoc

MESSAGE_PROTO = """\
edition = "2023";

message Foo {
  int32 explicit_field = 1;
  int32 implicit_field = 2 [features.field_presence = IMPLICIT];

  message Bar {
    string value = 1;
  }

  enum Baz {
    BAZ_UNSPECIFIED = 0;
    BAZ_VALUE = 1;
  }
}
"""

COLOR_PROTO = """\
edition = "2023";

enum Color {
  COLOR_UNSPECIFIED = 0;
  COLOR_RED = 1;
  COLOR_GREEN = 2;
  COLOR_BLUE = 3;
}
"""


def test_dynamic_create_message(protoc: Protoc) -> None:
    desc_message = protoc.compile_message(MESSAGE_PROTO)
    assert isinstance(desc_message, protobuf.DescMessage)
    msg_class = desc_message.type
    assert msg_class.desc() is desc_message
    msg = msg_class()
    assert isinstance(msg, protobuf.Message)
    assert msg.desc() is desc_message


def test_dynamic_message_init(protoc: Protoc) -> None:
    msg_class = protoc.compile_message(MESSAGE_PROTO).type

    # Fields are initialized
    msg = msg_class()
    msg_as_any = cast("Any", msg)
    assert msg_as_any.explicit_field == 0
    assert not msg.has_field("explicit_field")

    # Init argument for known fields are set
    msg = msg_class(explicit_field=123)
    msg_as_any = cast("Any", msg)
    assert msg_as_any.explicit_field == 123
    assert msg.has_field("explicit_field")

    # Non-existent field in __init__ raises error
    with pytest.raises(
        TypeError,
        match=re.escape(
            r"Foo.__init__() got an unexpected keyword argument 'nonexistent_field'"
        ),
    ):
        _ = msg_class(nonexistent_field="should error")


def test_dynamic_unknown_attr_access(protoc: Protoc) -> None:
    msg_class = protoc.compile_message(MESSAGE_PROTO).type
    msg = cast("Any", msg_class())

    with pytest.raises(AttributeError):
        _ = msg.nonexistent_field

    with pytest.raises(AttributeError):
        msg.nonexistent_field = "foo"


def test_dynamic_create_enum(protoc: Protoc) -> None:
    desc_enum = protoc.compile_enum(COLOR_PROTO)
    enum_class = desc_enum.type
    assert enum_class.desc() is desc_enum
    assert issubclass(enum_class, protobuf.Enum)


def test_dynamic_enum_values(protoc: Protoc) -> None:
    desc_enum = protoc.compile_enum(COLOR_PROTO)
    Color = cast("Any", desc_enum.type)  # noqa: N806

    # Test accessing enum values by name
    assert Color.UNSPECIFIED == 0
    assert Color.RED == 1
    assert Color.GREEN == 2
    assert Color.BLUE == 3

    # Test that values are instances of the enum class
    assert isinstance(Color.RED, Color)
    assert isinstance(Color.GREEN, Color)

    # Test string representation
    assert str(Color.RED) == "RED"
    assert repr(Color.RED) == "Color.RED"

    # Test integer comparison
    assert Color.RED == 1
    assert Color.GREEN == 2

    # Test enum comparison
    assert Color.RED != Color.GREEN
    assert Color(1) == Color.RED


def test_dynamic_enum_unknown_value(protoc: Protoc) -> None:
    desc_enum = protoc.compile_enum(COLOR_PROTO)
    Color = desc_enum.type  # noqa: N806

    # Test handling of unknown enum values (open enum support)
    unknown = Color(99)
    assert unknown == 99
    assert str(unknown) == "99"
    assert repr(unknown) == "Color(99)"


def test_file_descriptor_set(protoc: Protoc) -> None:
    file_set = protoc.compile_set(
        {"test.proto": MESSAGE_PROTO, "color.proto": COLOR_PROTO}
    )
    reg = file_set.to_registry()
    foo_desc = reg.message("Foo")
    color_desc = reg.enum("Color")
    assert foo_desc is not None
    assert color_desc is not None
    color = color_desc.type(0)
    assert color.__class__.__name__ == "Color"
    assert color.__class__.__qualname__ == "Color"
    foo = foo_desc.type()
    assert foo.__class__.__name__ == "Foo"
    assert foo.__class__.__qualname__ == "Foo"
    assert cast("Any", foo).explicit_field == 0
    with pytest.raises(AttributeError, match="has no attribute 'nonexistent_field'"):
        _ = cast("Any", foo).nonexistent_field

    bar_desc = reg.message("Foo.Bar")
    assert bar_desc is not None
    bar = bar_desc.type()
    assert bar.__class__.__name__ == "Bar"
    assert bar.__class__.__qualname__ == "Foo.Bar"

    baz_desc = reg.enum("Foo.Baz")
    assert baz_desc is not None
    baz = baz_desc.type
    assert baz.__name__ == "Baz"
    assert baz.__qualname__ == "Foo.Baz"


WKT_IMPORTS_PROTO = """\
edition = "2023";
import "google/protobuf/timestamp.proto";
import "google/protobuf/duration.proto";
import "google/protobuf/any.proto";
import "google/protobuf/descriptor.proto";
"""


def test_dynamic_wkt_timestamp_mixin(protoc: Protoc) -> None:
    file_set = protoc.compile_set({"test.proto": WKT_IMPORTS_PROTO}, "include_imports")
    reg = file_set.to_registry()
    desc = reg.message("google.protobuf.Timestamp")
    assert desc is not None
    ts_class = desc.type
    assert issubclass(ts_class, TimestampMixin)
    ts = ts_class(seconds=10, nanos=0)
    assert ts.to_seconds() == 10.0
    assert ts.to_nanos() == 10_000_000_000


def test_dynamic_wkt_duration_mixin(protoc: Protoc) -> None:
    file_set = protoc.compile_set({"test.proto": WKT_IMPORTS_PROTO}, "include_imports")
    reg = file_set.to_registry()
    desc = reg.message("google.protobuf.Duration")
    assert desc is not None
    dur_class = desc.type
    assert issubclass(dur_class, DurationMixin)
    dur = dur_class(seconds=5, nanos=0)
    assert dur.to_nanos() == 5_000_000_000


def test_dynamic_wkt_any_mixin(protoc: Protoc) -> None:
    file_set = protoc.compile_set({"test.proto": WKT_IMPORTS_PROTO}, "include_imports")
    reg = file_set.to_registry()
    desc = reg.message("google.protobuf.Any")
    assert desc is not None
    any_class = desc.type
    assert issubclass(any_class, AnyMixin)
    assert hasattr(any_class, "pack")
    assert hasattr(any_class, "unpack")


def test_dynamic_wkt_file_descriptor_set_mixin(protoc: Protoc) -> None:
    file_set = protoc.compile_set({"test.proto": WKT_IMPORTS_PROTO}, "include_imports")
    reg = file_set.to_registry()
    desc = reg.message("google.protobuf.FileDescriptorSet")
    assert desc is not None
    fds_class = desc.type
    assert issubclass(fds_class, FileDescriptorSetMixin)
    assert hasattr(fds_class, "to_registry")
