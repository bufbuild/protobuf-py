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

from dataclasses import dataclass, field as dataclassfield
from enum import IntEnum
from typing import TYPE_CHECKING, Literal, TypeAlias, cast, final

from ._typing import assert_never
from ._wire import WireType

try:
    from protobuf_ext import initialize_message_type as _initialize_message_type

    initialize_message_type = _initialize_message_type
except ImportError:
    initialize_message_type = None

if TYPE_CHECKING:
    import builtins
    from collections.abc import Sequence

    from ._enum import Enum
    from ._extension import Extension
    from ._message import Message
    from .wkt._gen.descriptor_pb import (
        DescriptorProto,
        EnumDescriptorProto,
        EnumValueDescriptorProto,
        FieldDescriptorProto,
        FileDescriptorProto,
        MethodDescriptorProto,
        MethodOptions,
        OneofDescriptorProto,
        ServiceDescriptorProto,
    )


@final
class ScalarType(IntEnum):
    # 0 is reserved for errors.
    # Order is weird for historical reasons.
    DOUBLE = 1
    FLOAT = 2
    # Not ZigZag encoded.  Negative numbers take 10 bytes.  Use TYPE_SINT64 if
    # negative values are likely.
    INT64 = 3
    UINT64 = 4
    # Not ZigZag encoded.  Negative numbers take 10 bytes.  Use TYPE_SINT32 if
    # negative values are likely.
    INT32 = 5
    FIXED64 = 6
    FIXED32 = 7
    BOOL = 8
    STRING = 9
    # Tag-delimited aggregate.
    # Group type is deprecated and not supported in proto3. However, Proto3
    # implementations should still be able to parse the group wire format and
    # treat group fields as unknown fields.
    # TYPE_GROUP = 10,  # noqa: ERA001
    # TYPE_MESSAGE = 11,  # Length-delimited aggregate.  # noqa: ERA001

    # New in version 2.
    BYTES = 12
    UINT32 = 13
    # TYPE_ENUM = 14,  # noqa: ERA001
    SFIXED32 = 15
    SFIXED64 = 16
    SINT32 = 17  # Uses ZigZag encoding.
    SINT64 = 18  # Uses ZigZag encoding.


def _scalar_wire_type(scalar_type: ScalarType) -> WireType:
    match scalar_type:
        case ScalarType.FIXED64 | ScalarType.SFIXED64 | ScalarType.DOUBLE:
            return WireType.BIT64
        case ScalarType.FIXED32 | ScalarType.SFIXED32 | ScalarType.FLOAT:
            return WireType.BIT32
        case ScalarType.STRING | ScalarType.BYTES:
            return WireType.LENGTH_DELIMITED
        case _:
            return WireType.VARINT


@final
class SupportedFieldPresence(IntEnum):
    EXPLICIT = 1  # FeatureSet.FieldPresence.EXPLICIT
    IMPLICIT = 2  # FeatureSet.FieldPresence.IMPLICIT
    LEGACY_REQUIRED = 3  # FeatureSet.FieldPresence.LEGACY_REQUIRED


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescFile:
    """Describes a protobuf source file.

    Attributes:
        edition: The edition of the protobuf file. Will be EDITION_PROTO2 for
            syntax="proto2", EDITION_PROTO3 for syntax="proto3".
        name: The name of the protobuf file, for example `foo/bar.proto`.
        dependencies: Files imported by this file.
        enums: Top-level enumerations declared in this file. Note that more
            enumerations might be declared within message declarations.
        messages: Top-level messages declared in this file. Note that more
            messages might be declared within message declarations.
        extensions: Top-level extensions declared in this file. Note that more
            extensions might be declared within message declarations.
        services: Services declared in this file.
        deprecated: Marked as deprecated in the protobuf source.
        proto: The compiler-generated descriptor.
    """

    edition: int
    name: str
    dependencies: Sequence[DescFile]
    enums: Sequence[DescEnum]
    messages: Sequence[DescMessage]
    extensions: Sequence[DescExtension]
    services: Sequence[DescService]
    deprecated: bool
    proto: FileDescriptorProto

    def __str__(self) -> str:
        return f"file {self.name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescEnum:
    """Describes an enumeration in a protobuf source file.

    Attributes:
        type_name: The fully qualified name of the enumeration. (We omit the leading dot.)
        name: The name of the enumeration, as declared in the protobuf source.
        file: The file this enumeration was declared in.
        parent: The parent message, if this enumeration was declared inside a message
            declaration.
        open: Enumerations can be open or closed.
            See <https://protobuf.dev/programming-guides/enum/>.
        values: Values declared for this enumeration.
        deprecated: Marked as deprecated in the protobuf source.
        proto: The compiler-generated descriptor.
    """

    type_name: str
    name: str
    file: DescFile
    parent: DescMessage | None
    open: bool
    values: Sequence[DescEnumValue]
    deprecated: bool
    proto: EnumDescriptorProto

    _values_by_number: dict[int, DescEnumValue] = dataclassfield(
        repr=False, compare=False, hash=False
    )
    """Enum value descriptor mapping from enum number, for lookup during binary parsing."""
    _values_by_name: dict[str, DescEnumValue] = dataclassfield(
        repr=False, compare=False, hash=False
    )
    """Enum value descriptor mapping from protobuf source name, for lookup during JSON parsing."""
    _local_name: str
    """The name of the Python class that represents the enum."""
    _local_qualname: str
    """The qualified name of the Python class that represents the enum, including parents."""

    @property
    def type(self) -> builtins.type[Enum]:
        """The Python enum class for this descriptor."""
        if self._type is not None:
            return self._type
        _type = _create_enum(self)
        object.__setattr__(self, "_type", _type)
        return _type

    _type: builtins.type[Enum] | None = dataclassfield(
        default=None, init=True, repr=False, compare=False, hash=False, kw_only=True
    )

    def __str__(self) -> str:
        return f"enum {self.type_name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescEnumValue:
    """Describes an individual value of an enumeration in a protobuf source file.

    Attributes:
        name: The name of the enumeration value, as specified in the protobuf source.
        local_name: A safe and idiomatic name for the value in Python.
        parent: The enumeration this value belongs to.
        number: The numeric enumeration value, as specified in the protobuf source.
        deprecated: Marked as deprecated in the protobuf source.
        proto: The compiler-generated descriptor.
    """

    name: str
    local_name: str
    parent: DescEnum
    number: int
    deprecated: bool
    proto: EnumValueDescriptorProto

    def __str__(self) -> str:
        return f"enum value {self.parent.type_name}.{self.name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescMessage:
    """Describes a message declaration in a protobuf source file.

    Attributes:
        type_name: The fully qualified name of the message. (We omit the leading dot.)
        name: The name of the message, as specified in the protobuf source.
        file: The file this message was declared in.
        parent: The parent message, if this message was declared inside a message
            declaration.
        fields: Fields declared for this message, including fields declared in a oneof
            group.
        oneofs: Oneof groups declared for this message. This does not include synthetic
            oneofs for proto3 optionals.
        members: Standalone fields and oneof groups for this message, ordered by their
            appearance in the protobuf source.
        nested_enums: Enumerations declared within the message, if any.
        nested_messages: Messages declared within the message, if any. This does not
            include synthetic messages like map entries.
        nested_extensions: Extensions declared within the message, if any.
        deprecated: Marked as deprecated in the protobuf source.
        proto: The compiler-generated descriptor.
    """

    type_name: str
    name: str
    file: DescFile
    parent: DescMessage | None
    fields: Sequence[DescField]
    oneofs: Sequence[DescOneof]
    members: Sequence[DescField | DescOneof]
    nested_enums: Sequence[DescEnum]
    nested_messages: Sequence[DescMessage]
    nested_extensions: Sequence[DescExtension]
    deprecated: bool
    proto: DescriptorProto

    # Private attributes eagerly resolvable
    _local_name: str = dataclassfield(repr=False, compare=False, hash=False)
    """The name of the Python class that represents the message."""
    _local_qualname: str = dataclassfield(repr=False, compare=False, hash=False)

    # Private attributes populated in finish_init.
    _fields_by_local_name: dict[str, DescField] = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Field descriptor mapping from local name, for lookup of fields as Python attributes.

    Fields within a oneof do not support access as Python attributes.
    """

    _fields_by_tag: dict[int, DescField] = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Field descriptor mapping from field tag, for lookup during binary parsing."""

    _fields_by_json_name: dict[str, DescField] = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Field descriptor mapping by JSON name (lowerCamelCase if not user-overridden), for lookup during JSON parsing."""

    _fields_by_name: dict[str, DescField] = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Field descriptor mapping from protobuf source name, for lookup in container emulation and JSON parsing."""

    _oneofs_by_local_name: dict[str, DescOneof] = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Oneof descriptor mapping from local name, for lookup of oneof groups as Python attributes."""

    _oneofs_by_name: dict[str, DescOneof] = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Oneof descriptor mapping from protobuf source name, for lookup in container emulation."""
    """The qualified name of the Python class that represents the message, including parents."""
    _defaults: list[
        tuple[str, str | bool | int | float | bytes | list | dict | None]
    ] = dataclassfield(repr=False, compare=False, hash=False, init=False)
    """Pre-computed defaults for efficient message initialization in the constructor."""
    _requires_presence: bool = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Whether this message has any fields that require separate presence tracking."""

    def _finish_init(self) -> None:
        """Finish initialization of private attributes.

        Because messages can be recursive, we cannot eagerly initialize a message descriptor,
        instead initializing mutable fields and filling them up while traversing the descriptor graph.
        Because of this, we cannot use dataclass's `__post_init__` for all initialization, and instead
        manually call this when ready. It still allows initialization logic to be encapsulated here
        instead of across multiple call sites.
        """
        from ._field_values import default_value  # noqa: PLC0415

        fields_by_local_name: dict[str, DescField] = {}
        fields_by_tag: dict[int, DescField] = {}
        fields_by_json_name: dict[str, DescField] = {}
        fields_by_name: dict[str, DescField] = {}
        for field in self.fields:
            if (
                not isinstance(field.value, DescFieldValueSingular)
                or field.value.oneof is None
            ):
                fields_by_local_name[field.local_name] = field
            fields_by_tag[field._tag] = field
            fields_by_json_name[field.name] = field
            fields_by_json_name[field.json_name] = field
            fields_by_name[field.name] = field
            fields_by_tag[field._tag] = field
            if isinstance(field.value, DescFieldValueList) and field.value._packable:
                # Allow lookup by both packed and unpacked type.
                if field.value.packed:
                    wire_type = field.value._unpacked_wire_type
                else:
                    wire_type = WireType.LENGTH_DELIMITED
                tag = field.number << 3 | wire_type
                fields_by_tag[tag] = field
        object.__setattr__(self, "_fields_by_local_name", fields_by_local_name)
        object.__setattr__(self, "_fields_by_tag", fields_by_tag)
        object.__setattr__(self, "_fields_by_json_name", fields_by_json_name)
        object.__setattr__(self, "_fields_by_name", fields_by_name)

        oneofs_by_local_name: dict[str, DescOneof] = {}
        oneofs_by_name: dict[str, DescOneof] = {}
        for oneof in self.oneofs:
            oneofs_by_local_name[oneof.local_name] = oneof
            oneofs_by_name[oneof.name] = oneof
        object.__setattr__(self, "_oneofs_by_local_name", oneofs_by_local_name)
        object.__setattr__(self, "_oneofs_by_name", oneofs_by_name)

        defaults: list[
            tuple[str, str | bool | int | float | bytes | list | dict | None]
        ] = []
        for member in self.members:
            if isinstance(member, DescOneof):
                defaults.append((member.local_name, None))
            else:
                defaults.append((member.local_name, default_value(member.value)))
        object.__setattr__(self, "_defaults", defaults)

        object.__setattr__(
            self,
            "_requires_presence",
            any(
                isinstance(member, DescField) and member._requires_presence
                for member in self.members
            ),
        )

        if initialize_message_type and self._type is not None:
            initialize_message_type(self._type)

    @property
    def type(self) -> builtins.type[Message]:
        """The Python message class for this descriptor."""
        if self._type is not None:
            return self._type
        _type = _create_message(self)
        object.__setattr__(self, "_type", _type)
        if initialize_message_type:
            initialize_message_type(_type)
        return _type

    _type: builtins.type[Message] | None = dataclassfield(
        default=None, init=True, repr=False, compare=False, hash=False, kw_only=True
    )

    def __str__(self) -> str:
        return f"message {self.type_name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescFieldValueScalar:
    """Describes the value of a scalar field declaration in a protobuf source file.

    Attributes:
        scalar: The scalar type.
        default_value: The default value for the scalar field.
        oneof: The `oneof` group this field belongs to, if any. This does not include
            synthetic oneofs for proto3 optionals.
    """

    scalar: ScalarType
    default_value: str | bool | int | float | bytes | None
    oneof: DescOneof | None


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescFieldValueMessage:
    """Describes the value of a message field declaration in a protobuf source file.

    Attributes:
        message: The message type.
        delimited_encoding: Encode the message delimited (a.k.a. proto2 group encoding),
            or length-prefixed?
        oneof: The `oneof` group this field belongs to, if any. This does not include
            synthetic oneofs for proto3 optionals.
    """

    message: DescMessage
    delimited_encoding: bool
    oneof: DescOneof | None


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescFieldValueEnum:
    """Describes the value of an enum field declaration in a protobuf source file.

    Attributes:
        enum: The enum type.
        default_value: The default value for the enum field.
        oneof: The `oneof` group this field belongs to, if any. This does not include
            synthetic oneofs for proto3 optionals.
    """

    enum: DescEnum
    default_value: int | None
    oneof: DescOneof | None


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescFieldValueMap:
    """Describes the value of a map field declaration in a protobuf source file.

    Attributes:
        key: The scalar map key type.
        value: The map value type.
    """

    key: ScalarType
    value: ScalarType | DescMessage | DescEnum

    def __post_init__(self) -> None:
        object.__setattr__(self, "_key_wire_type", _scalar_wire_type(self.key))
        object.__setattr__(
            self,
            "_value_wire_type",
            element_wire_type(self.value, delimited_encoding=False),
        )

    _key_wire_type: WireType = dataclassfield(
        init=False, repr=False, compare=False, hash=False
    )
    """The wire type for the map key, used to validate during parsing."""
    _value_wire_type: WireType = dataclassfield(
        init=False, repr=False, compare=False, hash=False
    )
    """The wire type for the map value, used to validate during parsing."""


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescFieldValueList:
    """Describes the value of a repeated field declaration in a protobuf source file.

    Attributes:
        element: The element type of the repeated field.
        packed: Pack this repeated field? Only valid for repeated enum fields, and for
            repeated scalar fields except BYTES and STRING.
        delimited_encoding: Encode the message delimited (a.k.a. proto2 group encoding),
            or length-prefixed?
    """

    element: DescMessage | DescEnum | ScalarType
    packed: bool
    delimited_encoding: bool

    def __post_init__(self) -> None:
        if (
            isinstance(self.element, ScalarType)
            and self.element not in (ScalarType.BYTES, ScalarType.STRING)
        ) or (isinstance(self.element, DescEnum)):
            object.__setattr__(self, "_packable", True)
        else:
            object.__setattr__(self, "_packable", False)
        object.__setattr__(
            self,
            "_unpacked_wire_type",
            element_wire_type(self.element, delimited_encoding=self.delimited_encoding),
        )

    _packable: bool = dataclassfield(init=False, repr=False, compare=False, hash=False)
    """Whether the field can be represented in packed encoding, used to accept packed or unpacked when parsing."""
    _unpacked_wire_type: WireType = dataclassfield(
        init=False, repr=False, compare=False, hash=False
    )
    """The wire type for the unpacked encoding, used to validate when parsing an unpacked repeated field."""


def element_wire_type(  # noqa: RET503
    element_type: DescMessage | DescEnum | ScalarType, *, delimited_encoding: bool
) -> WireType:
    match element_type:
        case ScalarType() as scalar:
            return _scalar_wire_type(scalar)
        case DescEnum():
            return WireType.VARINT
        case DescMessage():
            return WireType.SGROUP if delimited_encoding else WireType.LENGTH_DELIMITED
        case _:
            assert_never(element_type)


DescFieldValueSingular: TypeAlias = (
    DescFieldValueScalar | DescFieldValueMessage | DescFieldValueEnum
)
"""Describes the value of a non-repeated, non-map field declaration in a protobuf source file."""

DescFieldValue: TypeAlias = (
    DescFieldValueScalar
    | DescFieldValueMessage
    | DescFieldValueEnum
    | DescFieldValueMap
    | DescFieldValueList
)
"""Describes the value of a field declaration in a protobuf source file."""


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescField:
    """Describes a field declaration in a protobuf source file.

    Attributes:
        name: The field name, as specified in the protobuf source.
        value: Description of the value of the field.
        parent: The message this field is declared on.
        local_name: A safe and idiomatic name for the field as a property in Python.
        number: The field number, as specified in the protobuf source.
        json_name: The field name in JSON.
        deprecated: Marked as deprecated in the protobuf source.
        presence: Presence of the field.
            See <https://protobuf.dev/programming-guides/field_presence/>.
        proto: The compiler-generated descriptor.
    """

    name: str
    value: DescFieldValue
    parent: DescMessage
    local_name: str
    number: int
    json_name: str
    deprecated: bool
    presence: SupportedFieldPresence
    proto: FieldDescriptorProto

    def __post_init__(self) -> None:
        match self.value:
            case DescFieldValueScalar(scalar=scalar):
                wire_type = _scalar_wire_type(scalar)
            case DescFieldValueEnum():
                wire_type = WireType.VARINT
            case DescFieldValueMessage():
                if not self.value.delimited_encoding:
                    wire_type = WireType.LENGTH_DELIMITED
                else:
                    wire_type = WireType.SGROUP
            case DescFieldValueList():
                if self.value.packed:
                    wire_type = WireType.LENGTH_DELIMITED
                else:
                    wire_type = element_wire_type(
                        self.value.element,
                        delimited_encoding=self.value.delimited_encoding,
                    )
            case DescFieldValueMap():
                wire_type = WireType.LENGTH_DELIMITED
            case _:
                assert_never(self.value)
        object.__setattr__(self, "_tag", self.number << 3 | wire_type)

        # Scalar and enum fields with explicit presence need separate
        # tracking because their zero value (0, "", False, etc.) is a
        # valid user-provided value.
        if (
            isinstance(self.value, DescFieldValueSingular)
            and self.value.oneof is None
            and not isinstance(self.value, DescFieldValueMessage)
        ):
            requires_presence = self.presence != SupportedFieldPresence.IMPLICIT
        else:
            requires_presence = False
        object.__setattr__(self, "_requires_presence", requires_presence)

    _tag: int = dataclassfield(repr=False, compare=False, hash=False, init=False)
    """The field tag for serialization, which is a combination of the field number and wire type."""

    _requires_presence: bool = dataclassfield(
        repr=False, compare=False, hash=False, init=False
    )
    """Whether this field requires separate presence tracking."""

    def __str__(self) -> str:
        return f"field {self.parent.type_name}.{self.name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescExtension:
    """Describes an extension in a protobuf source file.

    Attributes:
        name: The field name, as specified in the protobuf source.
        value: Description of the value of the extension field.
        type_name: The fully qualified name of the extension.
        file: The file this extension was declared in.
        parent: The parent message, if this extension was declared inside a message
            declaration.
        extendee: The message that this extension extends.
        number: The field number, as specified in the protobuf source.
        json_name: The field name in JSON.
        deprecated: Marked as deprecated in the protobuf source.
        presence: Presence of the field.
            See <https://protobuf.dev/programming-guides/field_presence/>.
        proto: The compiler-generated descriptor.
    """

    name: str
    value: (
        DescFieldValueScalar
        | DescFieldValueMessage
        | DescFieldValueEnum
        | DescFieldValueList
    )
    type_name: str
    file: DescFile
    parent: DescMessage | None
    extendee: DescMessage
    number: int
    json_name: str
    deprecated: bool
    presence: SupportedFieldPresence
    proto: FieldDescriptorProto

    @property
    def type(self) -> Extension:
        """The Python extension for this descriptor."""
        if self._type is not None:
            return self._type
        _type = _create_extension(cast("DescExtension", self))
        object.__setattr__(self, "_type", _type)
        return _type

    _type: Extension | None = dataclassfield(
        default=None, init=True, repr=False, compare=False, hash=False, kw_only=True
    )

    def __str__(self) -> str:
        return f"extension {self.type_name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescOneof:
    """Describes a oneof group in a protobuf source file.

    Attributes:
        name: The name of the oneof group, as specified in the protobuf source.
        local_name: A safe and idiomatic name for the oneof group as a property in
            Python.
        parent: The message this oneof group was declared in.
        fields: The fields declared in this oneof group.
        proto: The compiler-generated descriptor.
    """

    name: str
    local_name: str
    parent: DescMessage
    fields: Sequence[DescField]
    proto: OneofDescriptorProto

    _fields_by_name: dict[str, DescField] = dataclassfield(
        repr=False, compare=False, hash=False
    )
    """Field descriptor mapping from protobuf source name, for lookup in validation."""

    def __str__(self) -> str:
        return f"oneof {self.parent.type_name}.{self.name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescService:
    """Describes a service declaration in a protobuf source file.

    Attributes:
        type_name: The fully qualified name of the service. (We omit the leading dot.)
        name: The name of the service, as specified in the protobuf source.
        file: The file this service was declared in.
        methods: The RPCs this service declares.
        deprecated: Marked as deprecated in the protobuf source.
        proto: The compiler-generated descriptor.
    """

    type_name: str
    name: str
    file: DescFile
    methods: Sequence[DescMethod]
    deprecated: bool
    proto: ServiceDescriptorProto

    def __str__(self) -> str:
        return f"service {self.type_name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescMethod:
    """Describes an RPC declaration in a protobuf source file.

    Attributes:
        name: The name of the RPC, as specified in the protobuf source.
        parent: The parent service.
        method_kind: One of the four available method types: "unary", "server_streaming",
            "client_streaming", "bidi_streaming".
        input: The message type for requests.
        output: The message type for responses.
        idempotency: The idempotency level declared in the protobuf source, if any.
        deprecated: Marked as deprecated in the protobuf source.
        proto: The compiler-generated descriptor.
    """

    name: str
    parent: DescService
    method_kind: Literal[
        "unary", "server_streaming", "client_streaming", "bidi_streaming"
    ]
    input: DescMessage
    output: DescMessage
    idempotency: MethodOptions.IdempotencyLevel
    deprecated: bool
    proto: MethodDescriptorProto

    def __str__(self) -> str:
        return f"method {self.parent.type_name}.{self.name}"


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescComments:
    """Comments associated with a protobuf source location.

    Attributes:
        leading_detached: Paragraphs of comments that appear before (but not
            connected to) the element.
        leading: Comment appearing before the element, if any.
        trailing: Comment appearing after the element, if any.
        source_path: The source code info path identifying the element.
    """

    leading_detached: Sequence[str]
    leading: str | None
    trailing: str | None
    source_path: Sequence[int]


def _get_wkt_mixin(desc: DescMessage) -> type | None:
    """Return the WKT mixin class for `desc`, or None if it has no mixin."""
    from ._wkt_registry import match_wkt  # noqa: PLC0415

    wkt = match_wkt(desc)
    return wkt.mixin() if wkt is not None else None


def _create_message(desc: DescMessage) -> type[Message]:
    """Create a dynamic message from a descriptor."""
    from ._message import Message  # noqa: PLC0415

    slots = [*desc._fields_by_local_name.keys(), *desc._oneofs_by_local_name.keys()]

    mixin = _get_wkt_mixin(desc)
    bases = (Message,) if mixin is None else (Message, mixin)

    dynamic_message = cast(
        "type[Message]",
        type(desc._local_name, bases, {"__slots__": tuple(slots), "_desc": desc}),
    )
    dynamic_message.__qualname__ = desc._local_qualname
    return dynamic_message


def _create_enum(desc: DescEnum) -> type[Enum]:
    """Create a dynamic enum from a descriptor."""
    from ._enum import Enum  # noqa: PLC0415

    members = {value.local_name: value.number for value in desc.values}
    dynamic_enum = cast("type[Enum]", Enum(desc._local_name, members))
    dynamic_enum._desc = desc  # type: ignore[attr-defined]
    dynamic_enum.__qualname__ = desc._local_qualname
    return dynamic_enum


def _create_extension(desc: DescExtension) -> Extension[Message, object]:
    """Create a dynamic extension from a descriptor."""
    from ._extension import Extension  # noqa: PLC0415
    from ._message import Message  # noqa: PLC0415

    ext = Extension[Message, object]()
    ext._desc = desc
    return ext


@final
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class DescUnknownField:
    """Description of an unknown field in a protobuf message.

    When a [Message][] is parsed from data with fields not present in the message definition,
    those fields are stored as unknown fields. This class can be initialized and passed to
    container methods to access structured data in unknown fields.

    Attributes:
        number: The field number of the unknown field.
        value: Description of the value of the unknown field.
    """

    number: int
    value: DescFieldValue
