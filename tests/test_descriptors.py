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

from typing import cast

from protobuf import (
    DescFieldValue,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
)
from protobuf.wkt import descriptor_pb


def test_descriptor_type_narrow() -> None:
    """This is more an example than a test."""
    desc = cast("DescFieldValue", None)
    match desc:
        case DescFieldValueList(element=_):
            pass
        case DescFieldValueMap(key=_, value=_):
            pass
        case DescFieldValueMessage(message=_):
            pass
        case DescFieldValueEnum(enum=_):
            pass
        case DescFieldValueScalar(scalar=_):
            pass


# Bootstrap protos are initialized differently from others, this test ensures they still
# work as a normal message, including marshaling. Notably, special care needs to be taken for
# presence.
def test_bootstrap_descriptor_proto_roundtrip() -> None:
    proto = descriptor_pb.desc().proto
    round_trip = descriptor_pb.FileDescriptorProto.from_binary(proto.to_binary())
    assert round_trip.name == "google/protobuf/descriptor.proto"
    assert round_trip.package == "google.protobuf"
    assert [m.name for m in round_trip.message_type] == [
        m.name for m in proto.message_type
    ]
    fdp_message = next(
        m for m in round_trip.message_type if m.name == "FieldDescriptorProto"
    )
    assert {f.name for f in fdp_message.field} >= {"name", "number", "type", "label"}
    assert all(f.number > 0 for f in fdp_message.field)
    # The re-exported file is a valid closure: it can build a fresh registry.
    registry = descriptor_pb.FileDescriptorSet(file=[round_trip]).to_registry()
    assert registry.message("google.protobuf.FileDescriptorProto") is not None
