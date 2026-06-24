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
"""protoc-gen-py: a protoc plugin that generates Python code from .proto files."""

from __future__ import annotations

import importlib.metadata
from copy import copy
from dataclasses import dataclass
from itertools import chain
from typing import TYPE_CHECKING, Any

from protobuf import (
    DescEnum,
    DescEnumValue,
    DescExtension,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescFieldValueSingular,
    DescFile,
    DescMessage,
    DescOneof,
    Enum,
    Message,
    ScalarType,
)
from protobuf._descriptors import SupportedFieldPresence
from protobuf._names import proto_camel_case
from protobuf._sanitization import escape_extension_name
from protobuf._typing import assert_never
from protobuf.plugin import File, Ident, Module, Schema, get_comments, run

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence

_PROTOBUF = Module("protobuf")
_DESC_FILE = _PROTOBUF.ident("DescFile", type_only=True)
_MESSAGE = _PROTOBUF.ident("Message")
_ENUM = _PROTOBUF.ident("Enum")
_ONE_OF = _PROTOBUF.ident("Oneof")
_EXTENSION = _PROTOBUF.ident("Extension")
_CODEGEN = _PROTOBUF.module("_codegen")
_FILE_DESC = _CODEGEN.ident("file_desc")
_BOOT_MESSAGE = _CODEGEN.ident("Message")
_BOOT = _CODEGEN.ident("boot")
_UNSET = _CODEGEN.ident("unset")
_TYPING = Module("typing")
_FINAL = _TYPING.ident("Final")
_LITERAL = _TYPING.ident("Literal")
_NO_RETURN = _TYPING.ident("NoReturn")
_TYPE_ALIAS = _TYPING.ident("TypeAlias")
_WKT_MIXIN = Module("protobuf.wkt._mixin")
_ANY_MIXIN = _WKT_MIXIN.ident("AnyMixin")
_DURATION_MIXIN = _WKT_MIXIN.ident("DurationMixin")
_FILE_DESCRIPTOR_SET_MIXIN = _WKT_MIXIN.ident("FileDescriptorSetMixin")
_LIST_VALUE_MIXIN = _WKT_MIXIN.ident("ListValueMixin")
_STRUCT_MIXIN = _WKT_MIXIN.ident("StructMixin")
_TIMESTAMP_MIXIN = _WKT_MIXIN.ident("TimestampMixin")
_VALUE_MIXIN = _WKT_MIXIN.ident("ValueMixin")
_BOOT_FILE_PATH = "google/protobuf/descriptor.proto"


def main() -> None:
    """Entry point for the protoc-gen-py plugin."""
    run(
        "protoc-gen-py",
        importlib.metadata.version("protoc-gen-py"),
        _Options,
        _generate,
    )


def _generate(schema: Schema[_Options]) -> None:
    generated_paths: set[str] = set()
    for desc in schema.files_to_generate:
        f = schema.generate_file(desc, "_pb.py")
        _generate_file(f, desc)
        generated_paths.add(f.path)
    if schema.options.init_files:
        _generate_init_files(schema, generated_paths)


def _generate_file(f: File, desc: DescFile) -> None:
    f.preamble(desc)
    for msg in desc.messages:
        _generate_message(f, msg)
    for enum in desc.enums:
        _generate_enum(f, enum)
    for ext in desc.extensions:
        _generate_extension(f, ext)

    _generate_desc(f, desc)


def _get_mixin(msg: DescMessage) -> Ident | None:
    if msg.file.name == "google/protobuf/duration.proto" and msg.name == "Duration":
        return _DURATION_MIXIN
    if msg.file.name == "google/protobuf/timestamp.proto" and msg.name == "Timestamp":
        return _TIMESTAMP_MIXIN
    if msg.file.name == "google/protobuf/any.proto" and msg.name == "Any":
        return _ANY_MIXIN
    if (
        msg.file.name == "google/protobuf/descriptor.proto"
        and msg.name == "FileDescriptorSet"
    ):
        return _FILE_DESCRIPTOR_SET_MIXIN
    if msg.file.name == "google/protobuf/struct.proto":
        match msg.name:
            case "Struct":
                return _STRUCT_MIXIN
            case "Value":
                return _VALUE_MIXIN
            case "ListValue":
                return _LIST_VALUE_MIXIN
    return None


def _generate_message(f: File, msg: DescMessage) -> None:
    slots = []
    if not msg.fields and not msg.oneofs:
        field_names_param = [_NO_RETURN]
    else:
        field_names_param = [_LITERAL, "["]
        for field in msg.fields:
            field_names_param.append(f'"{field.name}"')
            field_names_param.append(", ")
            if (
                not isinstance(field.value, DescFieldValueSingular)
                or not field.value.oneof
            ):
                slots.append(f'"{field.local_name}"')
        slots.extend(f'"{oneof.local_name}"' for oneof in msg.oneofs)
        field_names_param = field_names_param[:-1]  # Remove the trailing comma.
        field_names_param.append("]")

    field_names_var = f.ident(f"_{msg._local_name}Fields")
    f.print(field_names_var, ": ", _TYPE_ALIAS, " = ", field_names_param)
    f.print()

    # Consistently output tuple by forcing trailing comma for single slot case.
    slots_str = f"{slots[0]}," if len(slots) == 1 else ", ".join(slots)

    message = _BOOT_MESSAGE if msg.file.name == _BOOT_FILE_PATH else _MESSAGE
    mixin = _get_mixin(msg)
    base = (
        [message, "[", field_names_var, "]"]
        if mixin is None
        else [message, "[", field_names_var, "], ", mixin]
    )

    with f.scope("class ", f.ident(msg._local_name), "(", *base, "):"):
        _generate_message_docstring(f, msg)
        f.print("__slots__ = (", slots_str, ")")
        f.print()
        with f.type_checking():
            f.print()
            _generate_message_init(f, msg.members)
            _generate_message_members(f, msg.members)
        for nested_msg in msg.nested_messages:
            _generate_message(f, nested_msg)
        for nested_enum in msg.nested_enums:
            _generate_enum(f, nested_enum)
        for nested_ext in msg.nested_extensions:
            _generate_extension(f, nested_ext)


def _generate_message_init(f: File, members: Sequence[DescField | DescOneof]) -> None:
    with f.scope("def __init__("):
        f.print("self,")
        if len(members) > 0:
            f.print("*,")  # Avoids positional arguments.
        for member in members:
            f.print(
                member.local_name,
                ": ",
                _oneof_type(member)
                if isinstance(member, DescOneof)
                else _field_type(member),
                _member_init_default(member),
                ",",
            )
    with f.scope(") -> None:"):
        f.print("pass")
    f.print()


def _generate_message_members(
    f: File, members: Sequence[DescField | DescOneof]
) -> None:
    for member in members:
        match member:
            case DescField(value=DescFieldValueMessage()) | DescOneof():
                allow_none = True
            case _:
                allow_none = False
        f.print(
            member.local_name,
            ": ",
            _oneof_type(member)
            if isinstance(member, DescOneof)
            else _field_type(member),
            " | None" if allow_none else "",
        )
    if len(members) > 0:
        f.print()


def _generate_message_docstring(f: File, msg: DescMessage) -> None:
    with f.doc():
        _generate_docstring(f, msg)
        if len(msg.members) > 0:
            f.print()
            with f.scope("Attributes:"):
                for member in msg.members:
                    with f.scope(member.local_name, ":"):
                        _generate_docstring(f, member)
    f.print()


def _generate_enum(f: File, enum: DescEnum) -> None:
    with f.scope("class ", f.ident(enum._local_name), "(", _ENUM, "):"):
        _generate_enum_docstring(f, enum)
        for value in enum.values:
            f.print(value.local_name, " = ", value.number)
    f.print()


def _generate_enum_docstring(f: File, enum: DescEnum) -> None:
    with f.doc():
        _generate_docstring(f, enum)
        if len(enum.values) > 0:
            f.print()
            with f.scope("Attributes:"):
                for value in enum.values:
                    with f.scope(value.local_name, ":"):
                        _generate_docstring(f, value)
    f.print()


def _generate_extension(f: File, ext: DescExtension) -> None:
    f.print(
        f.ident(escape_extension_name(ext.name)),
        ": ",
        [_FINAL, "[", _EXTENSION, "[", ext.extendee, ", ", _extension_type(ext), "]]"],
        " = ",
        _EXTENSION,
        "()",
    )
    with f.doc():
        _generate_docstring(f, ext)
    f.print()


def _extension_type(ext: DescExtension) -> Any:
    match ext.value:
        case DescFieldValueMessage(message=message):
            return message
        case DescFieldValueScalar(scalar=scalar):
            return scalar
        case DescFieldValueEnum(enum=enum):
            return enum
        case DescFieldValueList(element=element):
            return ["list[", element, "]"]


def _generate_desc(f: File, desc: DescFile) -> None:
    f.print()
    if desc.name == _BOOT_FILE_PATH:
        _generate_boot(f, desc)
    else:
        with f.scope("_DESC = ", _FILE_DESC, "("):
            # Descriptor bytes
            f.print(_desc_bytes(desc), ",")
            # Dependency Array
            if desc.dependencies:
                with f.scope("["):
                    for dep in desc.dependencies:
                        f.print(dep, ".desc(),")
                f.print("],")
            else:
                f.print("[],")
            # Stubs
            _generate_stub_map(f, desc)
        f.print(")")
    f.print("")
    f.print("")
    with f.scope("def desc() -> ", _DESC_FILE, ":"):
        with f.doc(f"Returns the descriptor for the file `{desc.name}`."):
            pass
        f.print("return _DESC")


def _generate_boot(f: File, desc: DescFile) -> None:
    """Emit the code-generation counterpart of protobuf._codegen.boot()."""
    with f.scope("_DESC = ", _BOOT, "("):
        # Descriptor repr
        # Before we print the descriptor just like the bytes
        # we strip the source code info to reduce the size.
        proto = copy(desc.proto)
        proto.source_code_info = None
        f.print(_repr(proto), ",")
        # Stubs
        _generate_stub_map(f, desc)
    f.print(")")


def _generate_stub_map(f: File, desc: DescFile) -> None:
    # Stubs
    with f.scope("{"):
        for symbol in _all_symbols_in_file(desc):
            f.print('"', _stub_key(symbol), '": ', symbol, ",")
    f.print("},")


def _stub_key(desc: DescMessage | DescEnum | DescExtension) -> str:
    return (
        desc.type_name
        if desc.file.proto.package == ""
        else desc.type_name.removeprefix(f"{desc.file.proto.package}.")
    )


def _repr(value: object) -> str | list[object]:
    match value:
        case list():
            return ["[", [[_repr(value=item), ","] for item in value], "]"]
        case dict():
            return [
                "{",
                [[_repr(k), ": ", _repr(v), ","] for k, v in value.items()],
                "}",
            ]
        case Enum():
            return [value.__class__.__qualname__, ".", value.name]
        case Message():
            parts: list[object] = []
            for member in value.desc().members:
                # There are no oneofs in descriptor.proto. We
                # can add support when they are used.
                if isinstance(member, DescOneof):
                    msg = "unexpected oneof field in descriptor.proto"
                    raise NotImplementedError(msg)
                member_value = value[member]
                if (
                    isinstance(member.value, DescFieldValueSingular)
                    and not isinstance(member.value, DescFieldValueMessage)
                    and member.presence != SupportedFieldPresence.IMPLICIT
                    and member not in value
                ):
                    parts.extend(
                        [
                            member.local_name,
                            "=",
                            _UNSET,
                            "(",
                            _repr(member_value),
                            ")",
                            ",",
                        ]
                    )
                else:
                    parts.extend([member.local_name, "=", _repr(member_value), ","])

            return [value.__class__.__qualname__, "(", parts, ")"]
        case _:
            return repr(value)


def _desc_bytes(desc: DescFile) -> bytes:
    """Returns protobuf bytes of the FileDescriptorProto excluding the source code info."""
    proto = copy(desc.proto)
    proto.source_code_info = None
    return proto.to_binary()


def _all_symbols_in_file(
    file: DescFile,
) -> Generator[DescEnum | DescMessage | DescExtension, None, None]:
    for msg in file.messages:
        yield from _all_symbols_in_message(msg)
    yield from file.enums
    yield from file.extensions


def _all_symbols_in_message(
    msg: DescMessage,
) -> Generator[DescEnum | DescMessage | DescExtension, None, None]:
    yield msg
    for nested_msg in msg.nested_messages:
        yield from _all_symbols_in_message(nested_msg)
    yield from msg.nested_enums
    yield from msg.nested_extensions


def _oneof_type(oneof: DescOneof) -> list[Any]:
    return list(
        chain.from_iterable(
            [
                " | ",
                _ONE_OF,
                "[",
                _LITERAL,
                '["',
                field.name,
                '"], ',
                _field_type(field),
                "]",
            ]
            for field in oneof.fields
        )
    )[1:]


def _field_type(field: DescField) -> Any:
    match field.value:
        case DescFieldValueMessage(message=message):
            return message
        case DescFieldValueScalar(scalar=scalar):
            return scalar
        case DescFieldValueEnum(enum=enum):
            return enum
        case DescFieldValueList(element=element):
            return ["list[", element, "]"]
        case DescFieldValueMap(key=key, value=value):
            return ["dict[", key, ", ", value, "]"]


def _member_init_default(member: DescField | DescOneof) -> str | list[object]:
    if (
        isinstance(member, DescField)
        and isinstance(member.value, DescFieldValueScalar)
        and member.presence == SupportedFieldPresence.IMPLICIT
    ):
        return [" = ", _scalar_zero_value(member.value.scalar)]
    return " | None = None"


def _scalar_zero_value(scalar: ScalarType) -> bool | str | int:
    match scalar:
        case ScalarType.BOOL:
            return False
        case ScalarType.STRING:
            return '""'
        case ScalarType.BYTES:
            return 'b""'
        case _:
            return 0


def _generate_docstring(
    f: File,
    desc: DescMessage
    | DescField
    | DescEnum
    | DescExtension
    | DescOneof
    | DescEnumValue,
) -> None:
    comments = get_comments(desc)
    text = ""
    if comments.leading:
        text += comments.leading.removesuffix("\n")
    if comments.trailing:
        if len(text) > 0:
            text += "\n\n"
        text += comments.trailing.removesuffix("\n")
    if len(text) > 0:
        text += "\n\n"

    for line in text.splitlines():
        # Comments in protobuf often start with a space, this
        # leads to weird indentation in the generated docstring, so we remove it.
        f.print(line.removeprefix(" "))
    provenance = _provenance_text(desc)
    f.print("```proto")
    f.print(provenance)
    f.print("```")


def _provenance_text(  # noqa: RET503
    desc: DescMessage
    | DescField
    | DescEnum
    | DescExtension
    | DescOneof
    | DescEnumValue,
) -> str:
    """Returns a proto-syntax provenance string for embedding in docstrings."""
    match desc:
        case DescMessage():
            suffix = " [deprecated = true]" if desc.deprecated else ""
            return f"message {desc.type_name}{suffix}"
        case DescEnum():
            suffix = " [deprecated = true]" if desc.deprecated else ""
            return f"enum {desc.type_name}{suffix}"
        case DescEnumValue():
            suffix = " [deprecated = true]" if desc.deprecated else ""
            return f"{desc.name} = {desc.number}{suffix}"
        case DescOneof():
            return f"oneof {desc.name}"
        case DescField():
            return _field_provenance(desc)  # type: ignore[arg-type]
        case DescExtension():
            return _extension_provenance(desc)  # type: ignore[arg-type]
        case _:
            assert_never(desc)


def _field_provenance(desc: DescField) -> str:
    """Returns a proto-syntax provenance line for a field."""
    pre_opts: list[str] = []
    post_opts: list[str] = []

    match field_value := desc.value:
        case DescFieldValueMap(key=key, value=value):
            type_str = f"map<{key.name.lower()}, {_element_type_name(value)}>"
        case DescFieldValueList(element=element):
            type_str = f"repeated {_element_type_name(element)}"
            if field_value._packable:
                pre_opts.append(f"packed = {'true' if field_value.packed else 'false'}")
        case DescFieldValueScalar(scalar=scalar):
            type_str = _singular_label(desc, field_value) + scalar.name.lower()
            default = _scalar_default_str(field_value.scalar, field_value.default_value)
            if default is not None:
                post_opts.append(f"default = {default}")
        case DescFieldValueMessage(message=message):
            type_str = _singular_label(desc, field_value) + message.type_name
        case DescFieldValueEnum(enum=enum):
            type_str = _singular_label(desc, field_value) + enum.type_name
            if field_value.default_value is not None:
                default_val = enum._values_by_number.get(field_value.default_value)
                if default_val is not None:
                    post_opts.append(f"default = {default_val.name}")
        case _:
            assert_never(desc)

    opts = [*pre_opts]
    if desc.json_name != proto_camel_case(desc.name):
        opts.append(f'json_name = "{desc.json_name}"')
    opts.extend(post_opts)
    if desc.deprecated:
        opts.append("deprecated = true")
    opts_str = f" [{', '.join(opts)}]" if opts else ""
    return f"{type_str} {desc.name} = {desc.number}{opts_str};"


def _extension_provenance(desc: DescExtension) -> str:
    """Returns a proto-syntax provenance line for an extension field."""
    pre_opts: list[str] = []
    post_opts: list[str] = []

    match field_value := desc.value:
        case DescFieldValueList(element=element):
            type_str = f"repeated {_element_type_name(element)}"
            if field_value._packable:
                pre_opts.append(f"packed = {'true' if field_value.packed else 'false'}")
        case DescFieldValueScalar(scalar=scalar):
            type_str = _extension_singular_label(desc) + scalar.name.lower()
            default = _scalar_default_str(field_value.scalar, field_value.default_value)
            if default is not None:
                post_opts.append(f"default = {default}")
        case DescFieldValueMessage(message=message):
            type_str = _extension_singular_label(desc) + message.type_name
        case DescFieldValueEnum(enum=enum):
            type_str = _extension_singular_label(desc) + enum.type_name
            if field_value.default_value is not None:
                default_val = enum._values_by_number.get(field_value.default_value)
                if default_val is not None:
                    post_opts.append(f"default = {default_val.name}")
        case _:
            assert_never(desc)

    opts = [*pre_opts]
    if desc.json_name != proto_camel_case(desc.name):
        opts.append(f'json_name = "{desc.json_name}"')
    opts.extend(post_opts)
    if desc.deprecated:
        opts.append("deprecated = true")
    opts_str = f" [{', '.join(opts)}]" if opts else ""
    return f"extend {desc.extendee.type_name} {{ {type_str} {desc.name} = {desc.number}{opts_str} }}"


def _singular_label(field: DescField, field_value: DescFieldValueSingular) -> str:
    """Returns the label prefix for a singular field ('optional ', 'required ', or '')."""
    match field.presence:
        case SupportedFieldPresence.LEGACY_REQUIRED:
            return "required "
        case SupportedFieldPresence.EXPLICIT if field_value.oneof is None:
            return "optional "
        case _:
            return ""


def _extension_singular_label(ext: DescExtension) -> str:
    """Returns the label prefix for a singular extension ('optional ', 'required ', or '')."""
    match ext.presence:
        case SupportedFieldPresence.LEGACY_REQUIRED:
            return "required "
        case SupportedFieldPresence.EXPLICIT:
            return "optional "
        case _:
            return ""


def _element_type_name(element: ScalarType | DescMessage | DescEnum) -> str:
    """Returns the proto type name for a repeated element or map value type."""
    if isinstance(element, ScalarType):
        return element.name.lower()
    return element.type_name


def _scalar_default_str(scalar: ScalarType, default: object) -> str | None:
    """Returns a proto-style string for a scalar default value, or None if absent."""
    if default is None:
        return None
    match scalar:
        case ScalarType.BOOL:
            return "true" if default else "false"
        case ScalarType.STRING:
            if isinstance(default, str):
                escaped = (
                    default.replace("\\", "\\\\")
                    .replace('"', '\\"')
                    .replace("\n", "\\n")
                    .replace("\r", "\\r")
                    .replace("\t", "\\t")
                )
                return f'"{escaped}"'
            return repr(default)
        case _:
            return repr(default)


def _generate_init_files(schema: Schema, generated_paths: set[str]) -> None:
    """Generate __init__.py files for every package directory implied by generated files.

    Directories that already have a generated file are excluded.
    """
    init_dirs: set[str] = set()

    for path in generated_paths:
        parts = path.split("/")
        # Collect all parent directories
        for i in range(1, len(parts)):
            dir_path = "/".join(parts[:i])
            if dir_path:
                init_dirs.add(dir_path)

    generated_init = False
    for dir_path in init_dirs:
        init_path = f"{dir_path}/__init__.py"
        if init_path not in generated_paths:
            schema.generate_file(init_path)
            generated_init = True
    # Always include a root __init__.py for the output directory.
    if "__init__.py" not in generated_paths and generated_init:
        schema.generate_file("__init__.py")


@dataclass
class _Options:
    init_files: bool = True
