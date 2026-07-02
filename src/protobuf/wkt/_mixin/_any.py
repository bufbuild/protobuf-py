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

from typing import TYPE_CHECKING, TypeVar, cast, overload

from protobuf import DescMessage, Message

T = TypeVar("T", bound=Message)
Self = TypeVar("Self", bound="AnyMixin")


class AnyMixin:
    __slots__ = ()

    if TYPE_CHECKING:

        def __init__(self, *, type_url: str = "", value: bytes = b"") -> None:
            pass

        type_url: str
        value: bytes

    @classmethod
    def pack(cls: type[Self], message: Message) -> Self:
        """Creates an `Any` from a message."""
        type_url = f"type.googleapis.com/{message._desc.type_name}"

        return cls(type_url=type_url, value=message.to_binary())

    def is_type(self, type_info: type[Message] | DescMessage | str) -> bool:
        """Returns true if the Any contains the type given by schema or type name."""
        if self.type_url == "":
            return False
        type_name: str
        match type_info:
            case str():
                type_name = type_info
            case DescMessage():
                type_name = type_info.type_name
            case _:
                type_name = type_info._desc.type_name
        return type_name == type_url_to_name(self.type_url)

    @overload
    def unpack(self, type_info: DescMessage, /) -> Message | None: ...

    @overload
    def unpack(self, type_info: type[T], /) -> T | None: ...

    def unpack(self, type_info: DescMessage | type[T], /) -> T | None:
        """Unpacks the message the Any represents.

        Returns:
            The unpacked message, or None if the Any is empty or does
                not contain the type given by schema.
        """
        if not self.is_type(type_info):
            return None
        stub: type[T]
        match type_info:
            case DescMessage() as desc:
                stub = cast("type[T]", desc.type)
            case _:
                stub = type_info
        return stub.from_binary(self.value)


def type_url_to_name(url: str) -> str:
    # rindex raises an error if sub str is not found
    name = url[(url.rindex("/") if "/" in url else -1) + 1 :]
    if len(name) == 0:
        msg = f"invalid type url: {url}"
        raise ValueError(msg)

    return name
