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

import json
from typing import TYPE_CHECKING, Any

import pytest

from protobuf import Registry

from .gen.example_pb import User
from .gen.extensions_proto2_pb import (
    Proto2Extendee,
    Proto2ExtEnum,
    Proto2ExtMessage,
    ext_enum_ext,
    ext_message_ext,
    ext_message_ext_proto3,
    ext_repeated_string_ext,
    ext_string_ext,
    ext_uint32_ext,
    ext_uint64_ext,
)

if TYPE_CHECKING:
    from protobuf import Extension, Message


@pytest.mark.parametrize(
    ("msg", "exts", "expected"),
    [
        pytest.param(
            Proto2Extendee(),
            [(ext_enum_ext, Proto2ExtEnum.YES)],
            {"[proto2ext.enum_ext]": "PROTO2_EXT_ENUM_YES"},
            id="enum",
        ),
        pytest.param(
            Proto2Extendee(),
            [(ext_uint32_ext, 123)],
            {"[proto2ext.uint32_ext]": 123},
            id="uint32",
        ),
        pytest.param(
            Proto2Extendee(),
            [(ext_uint64_ext, 9876543210)],
            {"[proto2ext.uint64_ext]": "9876543210"},
            id="uint64",
        ),
        pytest.param(
            Proto2Extendee(),
            [(ext_string_ext, "hello")],
            {"[proto2ext.string_ext]": "hello"},
            id="string",
        ),
        pytest.param(
            Proto2Extendee(),
            [(ext_message_ext, Proto2ExtMessage(string_field="hi"))],
            {"[proto2ext.message_ext]": {"stringField": "hi"}},
            id="message",
        ),
        pytest.param(
            Proto2Extendee(),
            [(ext_repeated_string_ext, ["a", "b"])],
            {"[proto2ext.repeated_string_ext]": ["a", "b"]},
            id="repeated_string",
        ),
        pytest.param(
            Proto2Extendee(),
            [(ext_message_ext_proto3, User(first_name="Jane", last_name="Doe"))],
            {
                "[proto2ext.message_ext_proto3]": {
                    "firstName": "Jane",
                    "lastName": "Doe",
                }
            },
            id="message_proto3",
        ),
        pytest.param(
            Proto2Extendee(own_field=42),
            [
                (ext_uint32_ext, 123),
                (ext_uint64_ext, 9876543210),
                (ext_string_ext, "hello"),
                (ext_enum_ext, Proto2ExtEnum.YES),
                (ext_message_ext, Proto2ExtMessage(string_field="hi")),
                (ext_repeated_string_ext, ["a", "b"]),
            ],
            {
                "ownField": 42,
                "[proto2ext.uint32_ext]": 123,
                "[proto2ext.uint64_ext]": "9876543210",
                "[proto2ext.string_ext]": "hello",
                "[proto2ext.enum_ext]": "PROTO2_EXT_ENUM_YES",
                "[proto2ext.message_ext]": {"stringField": "hi"},
                "[proto2ext.repeated_string_ext]": ["a", "b"],
            },
            id="multiple_with_own_field",
        ),
    ],
)
def test_extensions(
    msg: Message, exts: list[tuple[Extension, Any]], expected: Any
) -> None:
    message = _with_exts(msg, *exts)
    registry = Registry(*(ext for ext, _ in exts))
    _test_roundtrip(message, expected, registry=registry)


def test_print_enums_as_ints() -> None:
    message = _with_exts(Proto2Extendee(), (ext_enum_ext, Proto2ExtEnum.YES))
    registry = Registry(ext_enum_ext)
    _test_roundtrip(
        message,
        {"[proto2ext.enum_ext]": 1},
        registry=registry,
        print_enums_as_ints=True,
    )


def test_without_registry() -> None:
    msg = _with_exts(Proto2Extendee(), (ext_uint32_ext, 123))
    json_str = msg.to_json()
    assert json.loads(json_str) == {}


def test_not_in_registry() -> None:
    msg = _with_exts(Proto2Extendee(), (ext_uint32_ext, 123))
    json_str = msg.to_json(registry=Registry())
    assert json.loads(json_str) == {}


def _test_roundtrip(
    message: Message,
    expected: Any,
    /,
    *,
    registry: Registry | None = None,
    print_enums_as_ints: bool = False,
) -> None:
    json_str = message.to_json(
        registry=registry, print_enums_as_ints=print_enums_as_ints
    )
    assert json.loads(json_str) == expected

    roundtripped = type(message).from_json(json_str, registry=registry)
    assert roundtripped == message


def _with_exts(msg: Message, *exts: tuple[Extension, Any]) -> Message:
    for ext, value in exts:
        msg[ext] = value
    return msg
