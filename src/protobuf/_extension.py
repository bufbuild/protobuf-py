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

from typing import TYPE_CHECKING, Generic, TypeVar, final

if TYPE_CHECKING:
    from ._descriptors import DescExtension
    from ._message import Message

M = TypeVar("M", bound="Message")
E = TypeVar("E")


@final
class Extension(Generic[M, E]):
    """A protobuf extension field.

    Extensions allow adding fields to a message without modifying the original
    message definition. This class provides type-safe access to extension fields
    on messages.

    This is meant for the generated code. For dynamic extensions use
    [`DescExtension.type`][protobuf.DescExtension.type].

    Attributes:
        desc: The extension descriptor.

    Examples:
        ```python
        # Given a protobuf extension definition:
        # extend Foo {
        #     optional string extra = 1000;
        # }

        from .gen.ext_pb import ext_extra  # The generated extension instance.
        from .gen.foo_pb import Foo

        foo = Foo()

        # Set a new extension value
        foo[ext_extra] = "new value"
        # Access the extension value
        value = foo[ext_extra]

        # Check if extension is set and clear it
        if ext_extra in foo:
            del foo[ext_extra]
        ```
    """

    __slots__ = ("__weakref__", "_desc")

    if TYPE_CHECKING:
        _desc: DescExtension

    def desc(self) -> DescExtension:
        """The extension descriptor."""
        return self._desc

    def _is_correct_message_type(self, message: Message) -> bool:
        return self._desc.extendee.type_name == message.desc().type_name

    def _assert_message_type(self, message: M) -> None:
        if not self._is_correct_message_type(message):
            msg = (
                f"extension {self._desc.name} extends {self._desc.extendee.type_name}, "
                f"but got message of type {message.desc().type_name}"
            )
            raise TypeError(msg)
