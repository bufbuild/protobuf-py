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

from protobuf import (
    DescComments,
    DescEnum,
    DescEnumValue,
    DescExtension,
    DescField,
    DescFile,
    DescMessage,
    DescMethod,
    DescOneof,
    DescService,
    Message,
)
from protobuf.wkt import (
    DescriptorProto,
    EnumDescriptorProto,
    FileDescriptorProto,
    ServiceDescriptorProto,
    SourceCodeInfo,
)

if TYPE_CHECKING:
    from collections.abc import Sequence


def get_package_comments(desc: DescFile) -> DescComments:
    """Get comments on the package element in the protobuf source."""
    return _find_comments(
        desc.proto.source_code_info, [_field_number(FileDescriptorProto, "package")]
    )


def get_syntax_comments(desc: DescFile) -> DescComments:
    """Get comments on the syntax element in the protobuf source."""
    return _find_comments(
        desc.proto.source_code_info, [_field_number(FileDescriptorProto, "syntax")]
    )


def get_comments(
    desc: DescEnum
    | DescEnumValue
    | DescExtension
    | DescField
    | DescMessage
    | DescMethod
    | DescOneof
    | DescService,
) -> DescComments:
    """Get comments on the element in the protobuf source."""
    match desc:
        case DescEnum(parent=parent, file=file, proto=proto):
            path = (
                [
                    *get_comments(parent).source_path,
                    _field_number(DescriptorProto, "enum_type"),
                    parent.proto.enum_type.index(proto),
                ]
                if parent is not None
                else [
                    _field_number(FileDescriptorProto, "enum_type"),
                    file.proto.enum_type.index(proto),
                ]
            )
        case DescOneof(parent=DescMessage(file=file) as parent, proto=proto):
            path = [
                *get_comments(parent).source_path,
                _field_number(DescriptorProto, "oneof_decl"),
                parent.proto.oneof_decl.index(proto),
            ]
        case DescMessage(parent=parent, file=file, proto=proto):
            path = (
                [
                    *get_comments(parent).source_path,
                    _field_number(DescriptorProto, "nested_type"),
                    parent.proto.nested_type.index(proto),
                ]
                if parent is not None
                else [
                    _field_number(FileDescriptorProto, "message_type"),
                    file.proto.message_type.index(proto),
                ]
            )
        case DescEnumValue(parent=DescEnum(file=file) as parent, proto=proto):
            path = [
                *get_comments(parent).source_path,
                _field_number(EnumDescriptorProto, "value"),
                parent.proto.value.index(proto),
            ]
        case DescField(parent=DescMessage(file=file) as parent, proto=proto):
            path = [
                *get_comments(parent).source_path,
                _field_number(DescriptorProto, "field"),
                parent.proto.field.index(proto),
            ]
        case DescExtension(parent=parent, file=file, proto=proto):
            path = (
                [
                    *get_comments(parent).source_path,
                    _field_number(DescriptorProto, "extension"),
                    parent.proto.extension.index(proto),
                ]
                if parent is not None
                else [
                    _field_number(FileDescriptorProto, "extension"),
                    file.proto.extension.index(proto),
                ]
            )
        case DescService(file=file, proto=proto):
            path = [
                _field_number(FileDescriptorProto, "service"),
                file.proto.service.index(proto),
            ]
        case DescMethod(parent=DescService(file=file) as parent, proto=proto):
            path = [
                *get_comments(parent).source_path,
                _field_number(ServiceDescriptorProto, "method"),
                parent.proto.method.index(proto),
            ]
        case _:
            msg = f"unexpected descriptor type: {type(desc)}"
            raise TypeError(msg)
    return _find_comments(file.proto.source_code_info, path)


def _find_comments(
    source_code_info: SourceCodeInfo | None, source_path: Sequence[int]
) -> DescComments:
    """Find comments for a given source path in the source code info."""
    location = next(
        (
            location
            for location in (
                source_code_info.location if source_code_info is not None else []
            )
            if location.path == source_path
        ),
        SourceCodeInfo.Location(),
    )
    return DescComments(
        leading_detached=location.leading_detached_comments,
        leading=location.leading_comments
        if location.has_field("leading_comments")
        else None,
        trailing=location.trailing_comments
        if location.has_field("trailing_comments")
        else None,
        source_path=source_path,
    )


def _field_number(msg: type[Message], name: str) -> int:
    return msg._desc._fields_by_local_name[name].number
