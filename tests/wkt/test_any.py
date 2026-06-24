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

from protobuf.wkt import Any, FieldMask, ListValue, Value


class TestAnyIs:
    def test_matches_desc(self) -> None:
        any_pb = Any(type_url="type.googleapis.com/google.protobuf.Value")
        assert any_pb.is_type(Value.desc())

    def test_matches_message_class(self) -> None:
        any_pb = Any(type_url="type.googleapis.com/google.protobuf.Value")
        assert any_pb.is_type(Value)

    def test_matches_type_name(self) -> None:
        any_pb = Any(type_url="type.googleapis.com/google.protobuf.Value")
        assert any_pb.is_type("google.protobuf.Value")

    def test_doesnt_match_a_different_type(self) -> None:
        any_pb = Any(type_url="type.googleapis.com/google.protobuf.Value")
        assert any_pb.is_type(ListValue) is False

    def test_returns_false_for_empty_url(self) -> None:
        assert Any().is_type(Value) is False

    def test_returns_false_for_empty_name(self) -> None:
        any_pb = Any(type_url="type.googleapis.com/google.protobuf.Value")
        assert Any().is_type("") is False
        assert any_pb.is_type("") is False

    def test_matches_custom_type_url(self) -> None:
        assert Any(type_url="example.com/google.protobuf.Value").is_type(Value)


class TestAnyPackUnpack:
    def test_unpack_returns_none_if_empty(self) -> None:
        assert Any().unpack(Value) is None

    def test_unpack_returns_none_if_different_type(self) -> None:
        assert (
            Any(type_url="type.googleapis.com/google.protobuf.ListValue").unpack(Value)
            is None
        )

    def test_packs_and_unpacks(self) -> None:
        any_pb = Any.pack(FieldMask(paths=["foo"]))
        unpacked = any_pb.unpack(FieldMask)
        assert unpacked is not None
        assert unpacked.paths == ["foo"]

    def test_packs_and_unpacks_with_a_descriptor(self) -> None:
        any_pb = Any.pack(FieldMask(paths=["foo"]))
        unpacked = any_pb.unpack(FieldMask.desc())
        assert isinstance(unpacked, FieldMask)
        assert unpacked.paths == ["foo"]
