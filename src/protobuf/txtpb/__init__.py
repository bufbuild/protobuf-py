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
"""Protobuf text format (`.txtpb`) serialization.

The [text format](https://protobuf.dev/reference/protobuf/textformat-spec/)
is a plain-text syntax mainly used for debugging, tests, and config files.

This functionality is kept in its own module, separate from `protobuf`, so
that using it never adds new reserved attribute names to `Message` subclasses.

Examples:
    ```python
    from protobuf.txtpb import from_text, to_text

    text = to_text(user)
    user = from_text(User, text)
    ```
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from ._from_text import merge_from_text
from ._to_text import ToTextOptions, to_text as _to_text_impl

if TYPE_CHECKING:
    from protobuf._message import Message
    from protobuf._registry import Registry

T = TypeVar("T", bound="Message")

__all__ = ["from_text", "merge_from_text", "to_text"]


def to_text(
    message: Message,
    /,
    *,
    registry: Registry | None = None,
    print_unknown_fields: bool = False,
) -> str:
    """Serialize a message to the protobuf text format.

    The output matches the canonical `google.protobuf.text_format` writer:
    two-space indentation, one field per line, no colon before a message
    value's `{`, and a trailing newline.

    Unset fields are omitted, including unset required fields; unlike
    [`Message.to_binary`][] and [`Message.to_json`][], legacy required fields
    are not validated when serializing to text.

    Args:
        message: The message to serialize.
        registry: A registry for resolving google.protobuf.Any messages
            and extensions. Without it, an Any is written as its raw
            `type_url`/`value` fields and extensions are omitted.
        print_unknown_fields: If `True`, unknown fields are printed by
            field number. This is a debugging aid only: `from_text`
            rejects fields named by number, so output that includes them
            cannot be parsed back.

    Returns:
        The message in protobuf text format.
    """
    return _to_text_impl(
        message,
        ToTextOptions(print_unknown_fields=print_unknown_fields, registry=registry),
    )


def from_text(
    message_type: type[T],
    text: str | bytes | bytearray,
    *,
    registry: Registry | None = None,
) -> T:
    """Create a new message by parsing the protobuf text format.

    To merge into an existing message, use [`merge_from_text`][].

    Args:
        message_type: The type of message to create.
        text: A str, bytes, or bytearray instance containing the text
            format.
        registry: Required to read `google.protobuf.Any` in its expanded
            `[type.url] {...}` form, and extension fields, from text
            format.

    Raises:
        ValueError: If the text cannot be parsed into the message.
    """
    message = message_type()
    merge_from_text(message, text, registry=registry)
    return message
