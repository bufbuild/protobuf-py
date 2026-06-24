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

from typing import TYPE_CHECKING, Any, TypeVar, cast

from protobuf._descriptors import (
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescMessage,
)
from protobuf._file_registry import create_file_registry
from protobuf._message import Message as BaseMessage
from protobuf._native_message import object_setattr

try:
    from protobuf_ext import generic_setattr

    # Workaround Python <3.13 prevents calling object.__setattr__ on objects with
    # a native base class that implements __setattr__.
    object_setattr = generic_setattr
except ImportError:
    object_setattr = object.__setattr__


if TYPE_CHECKING:
    from collections.abc import Mapping

    from protobuf._descriptors import DescFile
    from protobuf._enum import Enum
    from protobuf._extension import Extension
    from protobuf.wkt._gen.descriptor_pb import FileDescriptorProto


FieldNamesT = TypeVar("FieldNamesT", bound=str)


def boot(
    proto: FileDescriptorProto,
    stubs: Mapping[str, type[BaseMessage | Enum] | Extension],
) -> DescFile:
    """Bootstrap google/protobuf/descriptor.proto.

    The file descriptor for google/protobuf/descriptor.proto cannot be
    embedded in serialized form, because it is required to parse itself.

    Instead, the code generator emits descriptor.proto messages as Python
    constructor calls (keyword arguments with literal values). This module
    provides the primitives that make those calls work before descriptors
    exist:

    - boot() creates a DescFile from an already-instantiated
    FileDescriptorProto, bypassing binary deserialization.
    - BootMessage is a base class for descriptor.proto messages that
    stores fields as plain attributes during bootstrap, then delegates
    to the normal Message once descriptors are attached.
    - Unset is a sentinel that distinguishes "field absent with a default
    value" from "field explicitly set" in bootstrapped messages.

    This module is used exclusively for google/protobuf/descriptor.proto.
    All other generated files use file_desc(), which deserializes from
    bytes.
    """
    reg = create_file_registry(proto, _err_resolve, stubs=stubs)
    res = reg.file(proto.name)
    assert res is not None  # noqa: S101 # We just added it.
    _fill_presence(proto)
    return res


def _fill_presence(msg: Message) -> None:
    """Fills presence tracking for bootstrapped descriptor messages.

    Bootstrap construction writes field values straight into storage,
    bypassing ``Message.__setattr__``, so presence for explicit-presence
    fields is never recorded, which causes marshaling to fail. We go through
    the message after descriptor initialization to fill presence.

    We can fill presence by simply traversing FileDescriptorProto for
    descriptor.proto since all bootstrapped protos are children of it.
    """
    if (boot_unset := msg._boot_unset) is None:
        return
    for field in type(msg)._desc.fields:
        key = field.local_name
        if key in boot_unset:
            continue
        value = getattr(msg, key)
        match field.value:
            case DescFieldValueMessage():
                if value is not None:
                    _fill_presence(value)
            case DescFieldValueList(element=DescMessage()):
                for item in value:
                    _fill_presence(item)
            case DescFieldValueMap(value=DescMessage()):
                for item in value.values():
                    _fill_presence(item)
        if field._requires_presence:
            msg._set_field_number_present(field.number)
    object_setattr(msg, "_boot_unset", None)


class Message(BaseMessage[FieldNamesT]):
    """A thin wrapper on message to handle bootstrapping."""

    __slots__ = ("_boot_unset",)

    if TYPE_CHECKING:
        _boot_unset: set[str] | None

    def __init__(self, **kwargs: Any) -> None:
        # If the descriptor is set at init time, we treat it like
        # a regular message.
        if hasattr(self.__class__, "_desc"):
            object_setattr(self, "_boot_unset", None)
            super().__init__(**kwargs)
            return
        # Bootstrap
        boot_unset = set()
        object_setattr(self, "_boot_unset", boot_unset)
        for key, value in kwargs.items():
            if value is None or isinstance(value, _Unset):
                boot_unset.add(key)
            object_setattr(
                self, key, value.default if isinstance(value, _Unset) else value
            )  # Bypasses Message's __setattr__ which requires a descriptor

    def has_field(self, key: FieldNamesT) -> bool:
        if (boot_unset := getattr(self, "_boot_unset", None)) is None:
            return super().has_field(key)
        # Bootstrap
        # descriptor.proto doesn't use oneofs, so we can safely ignore them here.
        return key not in boot_unset


def unset(default: object) -> Any:
    """Used to track unset fields with default values for bootstrapped messages."""
    return cast("Any", _Unset(default))


class _Unset:
    def __init__(self, default: object) -> None:
        self.default = default


def _err_resolve(name: str) -> DescFile:
    msg = f"unexpected dependency for google/protobuf/descriptor.proto: {name}"
    raise NotImplementedError(msg)
