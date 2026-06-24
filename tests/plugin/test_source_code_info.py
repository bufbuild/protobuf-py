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

from typing import TYPE_CHECKING

from protobuf.plugin import get_comments, get_package_comments, get_syntax_comments

if TYPE_CHECKING:
    from tests.conftest import Protoc


def test_get_syntax_comments(protoc: Protoc) -> None:
    file = protoc.compile_file(
        """\
// Copyright ACME, Inc.
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// WITHOUT WARRANTIES

// Comment before syntax.
syntax = "proto3"; // Comment next to syntax.
// Comment after syntax.

// Comment before package.
package testcomments;
"""
    )
    comments = get_syntax_comments(file)
    assert comments.leading_detached == [
        " Copyright ACME, Inc.\n\n      http://www.apache.org/licenses/LICENSE-2.0\n\n WITHOUT WARRANTIES\n"
    ]
    assert comments.leading == " Comment before syntax.\n"
    assert comments.trailing == " Comment next to syntax.\n"


def test_get_package_comments(protoc: Protoc) -> None:
    file = protoc.compile_file(
        """\
// Comment before syntax.
syntax = "proto3"; // Comment next to syntax.
// Comment after syntax.

// Comment before package.
package testcomments; // Comment next to package.
// Comment after package.

// Comment between package and message.

// Comment before message.
message MessageWithComments {}
"""
    )
    comments = get_package_comments(file)
    assert comments.leading_detached == [" Comment after syntax.\n"]
    assert comments.leading == " Comment before package.\n"
    assert comments.trailing == " Comment next to package.\n"


def test_get_comments_for_messages(protoc: Protoc) -> None:
    file = protoc.compile_file(
        """\
syntax="proto3";
package testcomments; // Comment next to package.
// Comment after package.

// Comment between package and message.

// Comment before message.
message MessageWithComments {}
"""
    )
    comments = get_comments(file.messages[0])
    assert comments.leading_detached == [
        " Comment after package.\n",
        " Comment between package and message.\n",
    ]
    assert comments.leading == " Comment before message.\n"
    assert comments.trailing is None


def test_get_comments_for_fields(protoc: Protoc) -> None:
    file = protoc.compile_file(
        """\
syntax="proto3";
message MessageWithComments {

    //
    // Comment after start of message,
        // with funny indentation,
    // and empty lines on start and end.
    //

    // Comment before field with 5 lines:
    // line 2, next is empty
    //
    // line 4, next is empty
    //
    string foo = 1; // Comment next to field.
    // Comment after field.
}
"""
    )
    comments = get_comments(file.messages[0].fields[0])
    assert comments.leading_detached == [
        "\n Comment after start of message,\n with funny indentation,\n and empty lines on start and end.\n\n"
    ]
    assert comments.leading == (
        " Comment before field with 5 lines:\n line 2, next is empty\n\n line 4, next is empty\n\n"
    )
    assert comments.trailing == " Comment next to field.\n"
