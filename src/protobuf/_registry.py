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

from collections import defaultdict
from typing import TYPE_CHECKING, TypeVar, final

from ._descriptors import DescEnum, DescExtension, DescFile, DescMessage, DescService
from ._extension import Extension
from ._message import Message
from ._typing import assert_never

if TYPE_CHECKING:
    from collections.abc import Iterator

    from ._enum import Enum

_Types = DescMessage | DescEnum | DescExtension | DescService
_T = TypeVar("_T", bound=_Types)


@final
class Registry:
    """A set of descriptors for files, messages, enums, extensions, and services."""

    def __init__(
        self,
        *args: Registry
        | DescFile
        | DescMessage
        | DescEnum
        | DescExtension
        | DescService
        | Extension
        | type[Message | Enum],
    ) -> None:
        """Initializes a new registry with the given types, descriptors, or registries.

        See [add][] for more details.
        """
        self._files = dict[str, DescFile]()
        self._types = dict[str, _Types]()
        self._extendees: dict[str, dict[int, DescExtension]] = defaultdict(dict)
        self.add(*args)

    def add(
        self,
        *args: Registry
        | DescFile
        | DescMessage
        | DescEnum
        | DescExtension
        | DescService
        | Extension
        | type[Message | Enum],
    ) -> None:
        """Add types, descriptors, or other registries.

        Args:
            *args:
                Types, descriptors, or registries to add.
                All entries from registries are copied.

                In case of duplicates, the last entry wins.

                For DescFile, the types and descriptors from the defined files are all
                collected into this registry.

                For DescMessage, the message itself and all nested types are collected
                into this registry.
        """
        for arg in args:
            match arg:
                case type() | Extension():
                    desc_or_reg = arg.desc()
                case _:
                    desc_or_reg = arg

            match desc_or_reg:
                case DescEnum() | DescService():
                    self._types[desc_or_reg.type_name] = desc_or_reg

                case DescMessage():
                    self._types[desc_or_reg.type_name] = desc_or_reg
                    for desc in (
                        *desc_or_reg.nested_enums,
                        *desc_or_reg.nested_messages,
                        *desc_or_reg.nested_extensions,
                    ):
                        self.add(desc)
                case DescExtension():
                    self._types[desc_or_reg.type_name] = desc_or_reg
                    self._extendees[desc_or_reg.extendee.type_name][
                        desc_or_reg.number
                    ] = desc_or_reg
                case DescFile():
                    self._files[desc_or_reg.name] = desc_or_reg
                    for desc in (
                        *desc_or_reg.enums,
                        *desc_or_reg.messages,
                        *desc_or_reg.extensions,
                        *desc_or_reg.services,
                    ):
                        self.add(desc)
                case Registry():
                    self._extend(desc_or_reg)
                case _:
                    assert_never(desc_or_reg)

    def file(self, path: str) -> DescFile | None:
        """Look up a file descriptor by its path.

        Args:
            path: The protobuf file path as it appears in the file
                descriptor (e.g. `"example/foo.proto"`).

        Returns:
            The descriptor for the file, or `None` if not found.
        """
        return self._files.get(path)

    def message(self, type_name: str) -> DescMessage | None:
        """Look up a message descriptor by its fully qualified name.

        Args:
            type_name: The fully qualified name of the message.

        Returns:
            The descriptor for the message, or `None` if not found.
        """
        return self._get_type(type_name, DescMessage)

    def service(self, type_name: str) -> DescService | None:
        """Look up a service descriptor by its fully qualified name.

        Args:
            type_name: The fully qualified name of the service.

        Returns:
            The descriptor for the service, or `None` if not found.
        """
        return self._get_type(type_name, DescService)

    def enum(self, type_name: str) -> DescEnum | None:
        """Look up an enumeration descriptor by its fully qualified name.

        Args:
            type_name: The fully qualified name of the enum.

        Returns:
            The descriptor for the enum, or `None` if not found.
        """
        return self._get_type(type_name, DescEnum)

    def extension(self, type_name: str) -> DescExtension | None:
        """Look up an extension descriptor by its fully qualified name.

        Args:
            type_name: The fully qualified name of the extension.

        Returns:
            The descriptor for the extension, or `None` if not found.
        """
        # Avoid _get_type since we cant pass a type alias to it.
        msg = self._types.get(type_name)
        return msg if isinstance(msg, DescExtension) else None

    def extension_for(
        self, type_info: DescMessage | str | Message, number: int
    ) -> DescExtension | None:
        """Look up an extension by the message it extends and field number.

        Args:
            type_info: The extended message, either as a
                DescMessage or its fully qualified name.
            number: The extension field number.

        Returns:
            The descriptor for the extension, or `None` if not found.
        """
        match type_info:
            case DescMessage():
                msg_type_name = type_info.type_name
            case Message():
                msg_type_name = type_info.desc().type_name
            case str():
                msg_type_name = type_info

        return self._extendees[msg_type_name].get(number)

    def _get_type(self, type_name: str, typ: type[_T]) -> None | _T:
        msg = self._types.get(type_name)
        return msg if isinstance(msg, typ) else None

    def _extend(self, other: Registry) -> None:
        self._files |= other._files
        self._types |= other._types
        for key in other._extendees:
            self._extendees[key] |= other._extendees[key]

    def __iter__(
        self,
    ) -> Iterator[DescFile | DescMessage | DescEnum | DescExtension | DescService]:
        """Iterate over all descriptors in the registry.

        Yields files, messages, enums, extensions, and services.
        """
        yield from self._files.values()
        yield from self._types.values()

    __slots__ = "_extendees", "_files", "_types"
