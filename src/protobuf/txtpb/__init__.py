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
is a plain-text syntax used for debugging, tests, and config files.

Examples:
    ```python
    from protobuf.txtpb import message_from_text, message_to_text

    text = message_to_text(user)
    user = message_from_text(User, text)
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

__all__ = ["merge_from_text", "message_from_text", "message_to_text"]


def message_to_text(
    message: Message,
    /,
    *,
    registry: Registry | None = None,
    print_unknown_fields: bool = False,
) -> str:
    """Serialize a message to the protobuf text format.

    Unlike standard serialization, unset required fields will not raise an error.

    Args:
        message: The message to serialize.
        registry: A registry for resolving google.protobuf.Any messages
            and extensions. Without it, an Any is written as its raw
            `type_url`/`value` fields and extensions are omitted.
        print_unknown_fields: If `True`, unknown fields are printed by
            field number.

    Returns:
        The message in protobuf text format.
    """
    return _to_text_impl(
        message,
        ToTextOptions(print_unknown_fields=print_unknown_fields, registry=registry),
    )


def message_from_text(
    message_type: type[T],
    text: str | bytes | bytearray,
    *,
    registry: Registry | None = None,
    ignore_unknown_fields: bool = False,
) -> T:
    """Create a new message by parsing the protobuf text format.

    To merge into an existing message, use [`merge_from_text`][].

    Args:
        message_type: The type of message to create.
        text: The text data to parse.
        registry: Required to read `google.protobuf.Any` in its expanded
            `[type.url] {...}` form, and extension fields, from text
            format.
        ignore_unknown_fields: If `True`, unknown fields are silently
            skipped instead of raising an error.

    Raises:
        ValueError: If the text cannot be parsed into the message. This
            includes encountering an unknown field, unless
            ignore_unknown_fields is set.
        RecursionError: If messages are nested deeper than the supported
            limit.
    """
    message = message_type()
    merge_from_text(
        message, text, registry=registry, ignore_unknown_fields=ignore_unknown_fields
    )
    return message
