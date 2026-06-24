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

import itertools
import re
from bisect import bisect_right
from typing import TYPE_CHECKING, TypeVar, cast

from ._bootstrap import (
    _EDITION_PROTO2,
    _EDITION_PROTO3,
    _EDITION_UNSTABLE,
    _ENUM_TYPE_OPEN,
    _IDEMPOTENCY_UNKNOWN,
    _LABEL_REPEATED,
    _LABEL_REQUIRED,
    _MAXIMUM_EDITION,
    _MESSAGE_ENCODING_DELIMITED,
    _REPEATED_FIELD_ENCODING_PACKED,
    _TYPE_BYTES,
    _TYPE_ENUM,
    _TYPE_GROUP,
    _TYPE_MESSAGE,
    _TYPE_STRING,
    _feature_defaults,
    _FeatureKey,
)
from ._descriptors import (
    DescEnum,
    DescEnumValue,
    DescExtension,
    DescField,
    DescFieldValue,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescFile,
    DescMessage,
    DescMethod,
    DescOneof,
    DescService,
    ScalarType,
    SupportedFieldPresence,
)
from ._registry import Registry
from ._sanitization import escape_class_name, escape_enum_attr, escape_message_attr
from ._wire._text_format import (
    parse_text_format_enum_value,
    parse_text_format_scalar_value,
)

_SORTED_EDITION_KEYS: tuple[int, ...] = tuple(sorted(_feature_defaults))

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ._enum import Enum
    from ._extension import Extension
    from ._message import Message
    from .wkt._gen.descriptor_pb import (
        DescriptorProto,
        EnumDescriptorProto,
        FieldDescriptorProto,
        FileDescriptorProto,
        MethodDescriptorProto,
        MethodOptions,
        OneofDescriptorProto,
        ServiceDescriptorProto,
    )

    _StubMap = Mapping[str, type[Message | Enum] | Extension] | None


def create_file_registry(
    proto: FileDescriptorProto,
    resolve: Callable[[str], DescFile | FileDescriptorProto | None],
    stubs: _StubMap = None,
) -> Registry:
    """Create a registry from a single FileDescriptorProto.

    Recursively resolves imports using *resolve*, which must return a
    `DescFile` or `FileDescriptorProto` for every transitive
    dependency.

    Args:
        proto: The file descriptor proto to build a registry for.
        resolve: Callback that resolves an import path to its
            descriptor.
        stubs: Optional stub map of generated symbols.

    Returns:
        A registry containing the file and all of its transitive
        dependencies.
    """
    seen = set[str]()
    reg = Registry()

    def recurse_deps(file: FileDescriptorProto) -> list[FileDescriptorProto]:
        deps: list[FileDescriptorProto] = []
        for path in file.dependency:
            if reg.file(path) is not None:
                continue
            if path in seen:
                continue
            dep = resolve(path)
            match dep:
                case None:
                    msg = f"unable to resolve {path}, imported by {file.name}"
                    raise ValueError(msg)
                case DescFile():
                    reg.add(dep)
                case _:
                    seen.add(dep.name)
                    deps.append(dep)

        return [
            *deps,
            *itertools.chain.from_iterable(
                recurse_deps(nested_dep) for nested_dep in deps
            ),
        ]

    for file in reversed([proto, *recurse_deps(proto)]):
        add_file(reg, file, stubs)
    return reg


def add_file(reg: Registry, proto: FileDescriptorProto, stubs: _StubMap) -> None:
    enums: list[DescEnum] = []
    messages: list[DescMessage] = []
    extensions: list[DescExtension] = []
    services: list[DescService] = []

    desc_file = DescFile(
        edition=_get_file_edition(proto),
        name=proto.name,
        dependencies=_find_file_dependencies(reg, proto),
        enums=enums,
        messages=messages,
        extensions=extensions,
        services=services,
        deprecated=proto.options.deprecated if proto.options else False,
        proto=proto,
    )

    enums.extend(
        _add_enum(reg, enum, desc_file, None, stubs) for enum in proto.enum_type
    )
    map_entries = _FileMapEntries()
    for msg_proto in proto.message_type:
        msg = _add_message(reg, msg_proto, desc_file, None, map_entries, stubs)
        if (options := msg_proto.options) is not None and options.map_entry:
            map_entries.add(msg)
        else:
            messages.append(msg)

    services.extend(
        _add_service(reg, svc_proto, file=desc_file) for svc_proto in proto.service
    )

    extensions.extend(
        _add_extension(reg, proto, desc_file, None, stubs) for proto in proto.extension
    )

    for msg in map_entries._map.values():
        _build_fields(reg, msg, map_entries)

    for msg in desc_file.messages:
        _build_fields(reg, msg, map_entries)
        _add_message_extensions(reg, msg, stubs)
    reg.add(desc_file)


def _add_enum(
    reg: Registry,
    proto: EnumDescriptorProto,
    file: DescFile,
    parent: DescMessage | None,
    stubs: _StubMap,
) -> DescEnum:
    type_name = _build_type_name(proto, parent, file)

    values: list[DescEnumValue] = []
    values_by_number: dict[int, DescEnumValue] = {}
    values_by_name: dict[str, DescEnumValue] = {}

    stub = cast("type[Enum]", _find_stub(type_name, file, stubs))
    local_name = escape_class_name(proto.name)
    local_qualname = f"{parent._local_qualname}.{local_name}" if parent else local_name
    desc_enum = DescEnum(
        type_name=type_name,
        name=proto.name,
        _local_name=local_name,
        _local_qualname=local_qualname,
        file=file,
        parent=parent,
        open=_is_enum_open(proto, parent if parent is not None else file),
        values=values,
        _values_by_number=values_by_number,
        _values_by_name=values_by_name,
        deprecated=proto.options.deprecated if proto.options else False,
        proto=proto,
        _type=stub,
    )
    if stub:
        stub._desc = desc_enum

    stripped_prefix = f"{_pascal_to_upper_snake_case(proto.name)}_"
    unstripped_names = {value_proto.name for value_proto in proto.value}

    for value_proto in proto.value:
        local_name = value_proto.name
        if local_name.startswith(stripped_prefix) and len(local_name) > len(
            stripped_prefix
        ):
            stripped_local_name = local_name[len(stripped_prefix) :]
            # Only strip if it does not match any unstripped name and does not start with digit.
            if (
                stripped_local_name not in unstripped_names
                and not stripped_local_name[0].isdigit()
            ):
                local_name = stripped_local_name

        desc_value = DescEnumValue(
            name=value_proto.name,
            local_name=escape_enum_attr(local_name),
            parent=desc_enum,
            number=value_proto.number,
            deprecated=value_proto.options.deprecated if value_proto.options else False,
            proto=value_proto,
        )
        values.append(desc_value)
        values_by_number[value_proto.number] = desc_value
        values_by_name[value_proto.name] = desc_value
    reg.add(desc_enum)
    return desc_enum


def _add_message(
    reg: Registry,
    msg_proto: DescriptorProto,
    file: DescFile,
    parent: DescMessage | None,
    map_entries: _FileMapEntries,
    stubs: _StubMap,
) -> DescMessage:
    type_name = _build_type_name(msg_proto, parent, file)

    nested_enums: list[DescEnum] = []
    nested_messages: list[DescMessage] = []
    nested_extensions: list[DescExtension] = []
    fields: list[DescField] = []
    oneofs: list[DescOneof] = []
    members: list[DescField | DescOneof] = []

    stub = (
        cast("type[Message]", _find_stub(type_name, file, stubs))
        if msg_proto.options is None or msg_proto.options.map_entry is False
        else None
    )
    local_name = escape_class_name(msg_proto.name)
    local_qualname = f"{parent._local_qualname}.{local_name}" if parent else local_name
    desc_message = DescMessage(
        type_name=type_name,
        name=msg_proto.name,
        file=file,
        parent=parent,
        fields=fields,
        oneofs=oneofs,
        members=members,
        nested_enums=nested_enums,
        nested_messages=nested_messages,
        nested_extensions=nested_extensions,
        deprecated=msg_proto.options.deprecated if msg_proto.options else False,
        proto=msg_proto,
        _local_name=local_name,
        _local_qualname=local_qualname,
        _type=stub,
    )
    if stub:
        stub._desc = desc_message

    nested_enums.extend(
        _add_enum(reg, proto, file, desc_message, stubs)
        for proto in msg_proto.enum_type
    )

    for nested_proto in msg_proto.nested_type:
        nested_msg = _add_message(
            reg, nested_proto, file, desc_message, map_entries, stubs
        )
        if nested_proto.options is not None and nested_proto.options.map_entry:
            map_entries.add(nested_msg)
        else:
            nested_messages.append(nested_msg)

    reg.add(desc_message)
    return desc_message


def _build_fields(
    reg: Registry, msg: DescMessage, map_entries: _FileMapEntries
) -> None:
    fields = cast("list[DescField]", msg.fields)
    oneofs = cast("list[DescOneof]", msg.oneofs)
    oneof_fields: list[list[DescField]] = [[] for _ in range(len(msg.proto.oneof_decl))]
    oneof_fields_by_name: list[dict[str, DescField]] = [
        {} for _ in range(len(msg.proto.oneof_decl))
    ]
    members = cast("list[DescField | DescOneof]", msg.members)

    oneofs.extend(
        _build_oneof(oneof_proto, msg, oneof_fields[idx], oneof_fields_by_name[idx])
        for idx, oneof_proto in enumerate(msg.proto.oneof_decl)
    )

    for field_proto in msg.proto.field:
        in_oneof = not field_proto.proto3_optional and field_proto.has_field(
            "oneof_index"
        )
        desc_field = _build_field(
            reg,
            field_proto,
            msg,
            oneofs[field_proto.oneof_index] if in_oneof else None,
            map_entries,
        )
        fields.append(desc_field)

        if in_oneof:
            assert isinstance(  # noqa: S101
                desc_field.value,
                (DescFieldValueScalar, DescFieldValueMessage, DescFieldValueEnum),
            )
            oneof_fields[field_proto.oneof_index].append(desc_field)
            oneof_fields_by_name[field_proto.oneof_index][desc_field.name] = desc_field
            if len(oneof_fields[field_proto.oneof_index]) == 1:  # Only add once
                members.append(oneofs[field_proto.oneof_index])
        else:
            members.append(desc_field)

    oneofs[:] = [oneof for oneof in oneofs if len(oneof.fields) > 0]

    for nested_msg in msg.nested_messages:
        _build_fields(reg, nested_msg, map_entries)

    msg._finish_init()


def _build_field_value(
    reg: Registry,
    proto: FieldDescriptorProto,
    parent: DescFile | DescMessage,
    oneof: DescOneof | None,
    map_entries: _FileMapEntries,
) -> DescFieldValue:
    if proto.label == _LABEL_REPEATED:
        map_entry = (
            map_entries.get(proto.type_name.removeprefix("."))
            if proto.type == _TYPE_MESSAGE
            else None
        )
        if map_entry:
            (key, value) = _find_map_entry_fields(map_entry)
            return DescFieldValueMap(key=key, value=value)
        if proto.type in (_TYPE_MESSAGE, _TYPE_GROUP):
            return DescFieldValueList(
                element=_assert(
                    reg.message(proto.type_name.removeprefix(".")),
                    f"could not find message: {proto.type_name}",
                ),
                packed=_is_packed_field(proto, parent),
                delimited_encoding=_is_delimited_encoding(proto, parent),
            )
        if proto.type == _TYPE_ENUM:
            field_enum = _assert(
                reg.enum(proto.type_name.removeprefix(".")),
                f"could not find enum: {proto.type_name}",
            )
            return DescFieldValueList(
                element=field_enum,
                delimited_encoding=False,
                packed=_is_packed_field(proto, parent),
            )
        return DescFieldValueList(
            delimited_encoding=False,
            element=ScalarType(proto.type),
            packed=_is_packed_field(proto, parent),
        )
    # Singular
    if proto.type in (_TYPE_MESSAGE, _TYPE_GROUP):
        return DescFieldValueMessage(
            message=_assert(
                reg.message(proto.type_name.removeprefix(".")),
                f"could not find message: {proto.type_name}",
            ),
            delimited_encoding=_is_delimited_encoding(proto, parent),
            oneof=oneof,
        )
    if proto.type == _TYPE_ENUM:
        field_enum = _assert(
            reg.enum(proto.type_name.removeprefix(".")),
            f"could not find enum: {proto.type_name}",
        )
        return DescFieldValueEnum(
            enum=field_enum,
            oneof=oneof,
            default_value=parse_text_format_enum_value(field_enum, proto.default_value)
            if proto.has_field("default_value")
            else None,
        )
    scalar = ScalarType(proto.type)
    return DescFieldValueScalar(
        oneof=oneof,
        default_value=parse_text_format_scalar_value(scalar, proto.default_value)
        if proto.has_field("default_value")
        else None,
        scalar=scalar,
    )


def _build_field(
    reg: Registry,
    proto: FieldDescriptorProto,
    msg: DescMessage,
    oneof: DescOneof | None,
    map_entries: _FileMapEntries,
) -> DescField:
    field_value = _build_field_value(reg, proto, msg, oneof, map_entries)
    in_oneof = proto.has_field("oneof_index")
    return DescField(
        name=proto.name,
        value=field_value,
        parent=msg,
        local_name=escape_message_attr(proto.name)
        if not in_oneof or proto.proto3_optional
        else proto.name,
        number=proto.number,
        json_name=proto.json_name,
        deprecated=proto.options.deprecated if proto.options else False,
        presence=_get_field_presence(proto, msg, in_oneof=in_oneof),
        proto=proto,
    )


def _add_extension(
    reg: Registry,
    proto: FieldDescriptorProto,
    file: DescFile,
    parent: DescMessage | None,
    stubs: _StubMap,
) -> DescExtension:
    """Build a DescExtension and append to parent list."""
    type_name = _build_type_name(proto, parent, file)

    extendee = _assert(
        reg.message(proto.extendee.removeprefix(".")),
        f"could not find extendee message: {proto.extendee}",
    )
    stub = cast("Extension", _find_stub(type_name, file, stubs))

    field_value = _build_field_value(reg, proto, file, None, _FileMapEntries())
    assert not isinstance(field_value, DescFieldValueMap), (  # noqa: S101
        "extensions cannot be map fields"
    )
    desc_ext = DescExtension(
        name=proto.name,
        value=field_value,
        type_name=type_name,
        file=file,
        parent=parent,
        extendee=extendee,
        number=proto.number,
        json_name=f"[{type_name}]",
        deprecated=proto.options.deprecated if proto.options else False,
        presence=_get_field_presence(proto, file, is_ext=True),
        proto=proto,
        _type=stub,
    )

    if stub:
        stub._desc = desc_ext
    reg.add(desc_ext)
    return desc_ext


def _build_oneof(
    proto: OneofDescriptorProto,
    parent: DescMessage,
    fields: list[DescField],
    fields_by_name: dict[str, DescField],
) -> DescOneof:
    return DescOneof(
        name=proto.name,
        local_name=escape_message_attr(proto.name),
        parent=parent,
        fields=fields,
        proto=proto,
        _fields_by_name=fields_by_name,
    )


def _add_service(
    reg: Registry, svc_proto: ServiceDescriptorProto, file: DescFile
) -> DescService:
    type_name = _build_type_name(svc_proto, None, file)

    methods: list[DescMethod] = []

    desc_service = DescService(
        type_name=type_name,
        name=svc_proto.name,
        file=file,
        methods=methods,
        deprecated=svc_proto.options.deprecated if svc_proto.options else False,
        proto=svc_proto,
    )

    for proto in svc_proto.method:
        method = _build_method(reg, proto, parent=desc_service)
        methods.append(method)

    reg.add(desc_service)
    return desc_service


def _add_message_extensions(reg: Registry, msg: DescMessage, stubs: _StubMap) -> None:
    nested_extensions = cast("list[DescExtension]", msg.nested_extensions)
    nested_extensions.extend(
        _add_extension(reg, proto, msg.file, msg, stubs)
        for proto in msg.proto.extension
    )
    for nested_msg in msg.nested_messages:
        _add_message_extensions(reg, nested_msg, stubs)


def _build_method(
    reg: Registry, method_proto: MethodDescriptorProto, parent: DescService
) -> DescMethod:
    # Determine method kind
    if method_proto.client_streaming and method_proto.server_streaming:
        method_kind = "bidi_streaming"
    elif method_proto.client_streaming:
        method_kind = "client_streaming"
    elif method_proto.server_streaming:
        method_kind = "server_streaming"
    else:
        method_kind = "unary"

    input_msg = reg.message(method_proto.input_type.removeprefix("."))
    output_msg = reg.message(method_proto.output_type.removeprefix("."))

    if not input_msg or not output_msg:
        msg = f"could not find input/output types for method {method_proto.name}"
        raise ValueError(msg)

    idempotency = _IDEMPOTENCY_UNKNOWN
    if method_proto.options:
        idempotency = method_proto.options.idempotency_level

    return DescMethod(
        name=method_proto.name,
        parent=parent,
        method_kind=method_kind,
        input=input_msg,
        output=output_msg,
        idempotency=cast("MethodOptions.IdempotencyLevel", idempotency),
        deprecated=method_proto.options.deprecated if method_proto.options else False,
        proto=method_proto,
    )


def _build_type_name(
    proto: EnumDescriptorProto
    | DescriptorProto
    | ServiceDescriptorProto
    | FieldDescriptorProto,
    parent: DescMessage | DescService | None,
    file: DescFile,
) -> str:
    """Create a fully qualified name for a protobuf type or extension field.

    The fully qualified name for messages, enumerations, and services is
    constructed by concatenating the package name (if present), parent
    message names (for nested types), and the type name. We omit the leading
    dot added by protobuf compilers. Examples:
    - mypackage.MyMessage
    - mypackage.MyMessage.NestedMessage

    The fully qualified name for extension fields is constructed by
    concatenating the package name (if present), parent message names (for
    extensions declared within a message), and the field name. Examples:
    - mypackage.extfield
    - mypackage.MyMessage.extfield
    """
    if parent is not None:
        return f"{parent.type_name}.{proto.name}"
    if len(file.proto.package) > 0:
        return f"{file.proto.package}.{proto.name}"
    return proto.name


def _find_file_dependencies(
    reg: Registry, proto: FileDescriptorProto
) -> list[DescFile]:
    deps: list[DescFile] = []
    for path in proto.dependency:
        dep = reg.file(path)
        if dep is None:
            msg = f"cannot find {path}, imported by {proto.name}"
            raise ValueError(msg)
        deps.append(dep)
    return deps


def _find_stub(
    type_name: str, file: DescFile, stubs: Mapping[str, type | Extension] | None
) -> type | Extension | None:
    if stubs is None:
        return None
    return stubs.get(
        type_name
        if file.proto.package == ""
        else type_name.removeprefix(f"{file.proto.package}.")
    )


_RE_UPPER_TO_LOWER = re.compile("([^_])([A-Z][a-z]+)")
_RE_LOWER_TO_UPPER = re.compile("([a-z])([A-Z])")


def _pascal_to_upper_snake_case(text: str) -> str:
    """Convert a PascalCase enum name to UPPER_SNAKE_CASE."""
    s1 = _RE_UPPER_TO_LOWER.sub(r"\1_\2", text)
    return _RE_LOWER_TO_UPPER.sub(r"\1_\2", s1).upper()


def _find_map_entry_fields(
    map_entry: DescMessage,
) -> tuple[ScalarType, ScalarType | DescMessage | DescEnum]:
    key_f = next(f for f in map_entry.fields if f.number == 1)
    value_f = next(f for f in map_entry.fields if f.number == 2)
    if not isinstance(key_f.value, DescFieldValueScalar) or key_f.value.scalar in (
        ScalarType.BYTES,
        ScalarType.FLOAT,
        ScalarType.DOUBLE,
    ):
        msg = "invalid map key type"
        raise ValueError(msg)
    key = key_f.value.scalar
    match value_f.value:
        case DescFieldValueScalar(scalar=scalar):
            return (key, scalar)
        case DescFieldValueMessage(message=message):
            return (key, message)
        case DescFieldValueEnum(enum=enum):
            return (key, enum)
        case _:
            msg = "unexpected map value type"
            raise TypeError(msg)


def _get_file_edition(proto: FileDescriptorProto) -> int:
    match proto.syntax:
        case "" | "proto2":
            return _EDITION_PROTO2
        case "proto3":
            return _EDITION_PROTO3
        case "editions":
            if proto.edition == _EDITION_UNSTABLE:
                # EDITION_UNSTABLE is a sandbox for in-development features. Collapse it
                # to maximum edition so test-only editions aren't leaked to users.
                return _MAXIMUM_EDITION
            if proto.edition > _MAXIMUM_EDITION:
                msg = f"{proto.name}: unsupported edition: {proto.edition}"
                raise ValueError(msg)
            return proto.edition
        case _:
            msg = f"{proto.name}: unsupported syntax"
            raise ValueError(msg)


def _is_enum_open(proto: EnumDescriptorProto, parent: DescFile | DescMessage) -> bool:
    return _resolve_feature("enum_type", (proto, parent)) == _ENUM_TYPE_OPEN


def _get_field_presence(
    proto: FieldDescriptorProto,
    parent: DescFile | DescMessage,
    *,
    in_oneof: bool = False,
    is_ext: bool = False,
) -> SupportedFieldPresence:
    if proto.label == _LABEL_REQUIRED:
        return SupportedFieldPresence.LEGACY_REQUIRED
    if proto.label == _LABEL_REPEATED:
        return SupportedFieldPresence.IMPLICIT
    if in_oneof or proto.proto3_optional or is_ext:
        return SupportedFieldPresence.EXPLICIT
    resolved = _resolve_feature("field_presence", (proto, parent))
    if resolved == SupportedFieldPresence.IMPLICIT and proto.type in (
        _TYPE_GROUP,
        _TYPE_MESSAGE,
    ):
        return SupportedFieldPresence.EXPLICIT
    return SupportedFieldPresence(resolved)


def _is_packable_field(proto: FieldDescriptorProto) -> bool:
    return proto.type not in (_TYPE_STRING, _TYPE_BYTES, _TYPE_GROUP, _TYPE_MESSAGE)


def _is_packed_field(
    proto: FieldDescriptorProto, parent: DescMessage | DescFile
) -> bool:
    if proto.label != _LABEL_REPEATED:
        return False
    if not _is_packable_field(proto):
        # length-delimited types cannot be packed
        return False
    if (options := proto.options) is not None and options.has_field("packed"):
        # prefer the field option over edition features
        return options.packed
    return (
        _resolve_feature("repeated_field_encoding", (proto, parent))
        == _REPEATED_FIELD_ENCODING_PACKED
    )


def _is_delimited_encoding(
    proto: FieldDescriptorProto, parent: DescMessage | DescFile
) -> bool:
    if proto.type == _TYPE_GROUP:
        return True
    return (
        _resolve_feature("message_encoding", (proto, parent))
        == _MESSAGE_ENCODING_DELIMITED
    )


def _resolve_feature(
    name: _FeatureKey,
    ref: DescFile
    | DescMessage
    | tuple[
        DescriptorProto | EnumDescriptorProto | FieldDescriptorProto,
        DescFile | DescMessage,
    ],
) -> int:
    proto = ref.proto if isinstance(ref, (DescFile, DescMessage)) else ref[0]
    if (options := proto.options) and (features := options.features):
        val = getattr(features, name)
        if val != 0:
            return val
    if isinstance(ref, DescMessage):
        return _resolve_feature(
            name, ref.parent if ref.parent is not None else ref.file
        )
    if isinstance(ref, DescFile):
        # Use the closest entry at or before ref.edition, per the FeatureSetDefaults spec.
        idx = bisect_right(_SORTED_EDITION_KEYS, ref.edition) - 1
        if idx < 0:
            msg = f"no feature defaults for edition {ref.edition}"
            raise ValueError(msg)
        return _feature_defaults[_SORTED_EDITION_KEYS[idx]][name]
    return _resolve_feature(name, ref[1])


class _FileMapEntries:
    def __init__(self) -> None:
        self._map: dict[str, DescMessage] = {}

    def get(self, type_name: str) -> DescMessage | None:
        if type_name in self._map:
            return self._map[type_name]
        return None

    def add(self, desc: DescMessage) -> None:
        options = _assert(desc.proto.options, "map entry message must have options")
        if options.map_entry is False:
            msg = "invalid map entry"
            raise ValueError(msg)
        self._map[desc.type_name] = desc


_AT = TypeVar("_AT")


def _assert(value: _AT | None, msg: str) -> _AT:
    if value is None:
        raise ValueError(msg)
    return value
