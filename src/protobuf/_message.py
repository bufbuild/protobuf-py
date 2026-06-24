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

from copy import copy, deepcopy
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar, overload

from . import _native_message
from ._descriptors import (
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescFieldValueSingular,
    DescMessage,
    DescOneof,
    DescUnknownField,
)
from ._extension import Extension
from ._field_values import default_value, is_zero_value
from ._from_binary import FromBinaryOptions, read_message
from ._native_message import object_setattr
from ._oneof import Oneof
from ._to_binary import ToBinaryOptions, write_message
from ._unknown import get_unknown_field, has_unknown_field, set_unknown_field
from ._wire import BinaryReader, BinaryWriter

if TYPE_CHECKING:
    from collections.abc import Iterator

    from ._registry import Registry

Self = TypeVar("Self", bound="Message")

# TypeVar for making Message generic over its field names
FieldNamesT = TypeVar("FieldNamesT", bound=str)

M = TypeVar("M", bound="Message")
E = TypeVar("E")


class _MessageMeta(type):
    """Metaclass for Message to insert native extension when available."""

    def __new__(
        cls, name: str, bases: tuple[type, ...], classdict: dict[str, Any]
    ) -> _MessageMeta:
        is_message_base = not any(isinstance(base, _MessageMeta) for base in bases)

        # Don't eagerly import the member to allow easier overriding in benchmarks
        native_message_class = _native_message.NativeMessageClass
        if native_message_class:
            if is_message_base:
                # Python does not allow inheriting from multiple classes with fixed size, which includes
                # native classes and classes with __slots__. We go ahead and define any needed private
                # fields from Message in NativeMessage as well. A small amount of duplication, though it
                # also means we can use native alternatives where appropriate.
                classdict = {**classdict, "__slots__": ()}
            elif not any(
                isinstance(base, type) and issubclass(base, native_message_class)
                for base in bases
            ):
                bases = (native_message_class, *bases)

        return super().__new__(cls, name, bases, classdict)


MessageMeta = _MessageMeta if _native_message.NativeMessageClass else type


class Message(Generic[FieldNamesT], metaclass=MessageMeta):  # noqa: PLW1641
    """Base class for Protobuf message types.

    Most `Message` subclasses are generated from `.proto` files. A message instance
    behaves like a regular Python object: construct it with keyword arguments using
    Python field names, then read and assign fields through attributes. `Message`
    provides all the shared runtime behavior for operating on messages.

    Thread safety:
        Message instances are not thread safe for concurrent mutation with any
        other operation. Concurrent reads without mutation are safe.

    Examples:
        ```python
        user = User(first_name="Alice", active=True)
        user.last_name = "Smith"
        ```
    """

    __slots__ = ("__weakref__", "_present", "_unknown_fields")

    if TYPE_CHECKING:
        _desc: ClassVar[DescMessage]
        _present: set[int]
        _unknown_fields: dict[int, list[bytes]] | None

    def __new__(cls: type[Self], *_args: Any, **_kwargs: Any) -> Self:
        msg = object.__new__(cls)
        object_setattr(msg, "_present", set())
        object_setattr(msg, "_unknown_fields", None)
        return msg

    def __init__(self, **kwargs: Any) -> None:
        """Initialize an instance of the message.

        Args:
            **kwargs: Field names (Python local names) and their values.
        """
        for local_name, default in self._desc._defaults:
            if local_name in kwargs:
                value = kwargs.pop(local_name)
                if value is not None:
                    setattr(self, local_name, value)
                    continue
            if isinstance(default, (list, dict)):
                object_setattr(self, local_name, default.__class__())
            else:
                object_setattr(self, local_name, default)
        # Error on unexpected argument
        if len(kwargs) > 0:
            msg = f"{type(self).__qualname__}.__init__() got an unexpected keyword argument '{next(iter(kwargs))}'"
            raise TypeError(msg)

    def to_json(
        self,
        *,
        registry: Registry | None = None,
        always_emit_implicit: bool = False,
        print_enums_as_ints: bool = False,
        use_proto_field_name: bool = False,
    ) -> str:
        """Serialize this message to a ProtoJSON string.

        By default, fields with implicit presence are not serialized if
        they are set to their zero value.

        A registry is required to serialize google.protobuf.Any fields
        and extensions. Extensions not found in the registry are silently
        omitted.

        Args:
            registry: A registry for resolving google.protobuf.Any messages
                and extensions.
            always_emit_implicit: By default, fields with implicit presence
                are omitted when set to their zero value (e.g. an empty
                list, a proto3 int32 field with value 0). If `True`, include
                these fields in the output.
            print_enums_as_ints: By default, the enum value name as defined
                in Protobuf is used. If `True`, use the numeric value instead.
            use_proto_field_name: By default, field names use the
                json_name field option, which defaults to lowerCamelCase.
                If `True`, use the Protobuf field name instead.

        Raises:
            ValueError: If a google.protobuf.Any field cannot be resolved
                through the registry.
        """
        from ._validate import validate  # noqa: PLC0415

        validate(self)
        # Needs to be lazy import since JSON specially handles many WKTs.
        from ._to_json import ToJsonOptions, to_json  # noqa: PLC0415

        return to_json(
            self,
            ToJsonOptions(
                always_emit_implicit=always_emit_implicit,
                print_enums_as_ints=print_enums_as_ints,
                use_proto_field_name=use_proto_field_name,
                registry=registry,
            ),
        )

    def to_binary(self, *, write_unknown_fields: bool = True) -> bytes:
        """Serialize this message to binary protobuf format.

        Args:
            write_unknown_fields: If `True`, unknown fields encountered
                during parsing are preserved in the output.

        Returns:
            The serialized binary protobuf bytes.
        """
        from ._validate import validate  # noqa: PLC0415

        validate(self)
        writer = BinaryWriter()
        write_message(
            self, writer, ToBinaryOptions(write_unknown_fields=write_unknown_fields)
        )
        return writer.finish()

    def __copy__(self: Self) -> Self:
        """Create a shallow copy with independent presence and unknown fields tracking."""
        new: Self = self.__class__.__new__(type(self))
        for name in (
            *self._desc._fields_by_local_name,
            *self._desc._oneofs_by_local_name,
        ):
            if hasattr(self, name):
                object_setattr(new, name, getattr(self, name))
        new._present.update(self._present)
        if uf := self._unknown_fields:
            new._get_or_init_unknown_fields().update(
                {k: v.copy() for k, v in uf.items()}
            )
        return new

    def __deepcopy__(self: Self, _memo: dict[int, Any], /) -> Self:
        """Create a deep copy of the message."""
        from ._merge import merge_from  # noqa: PLC0415

        new = type(self)()
        merge_from(new, self)
        return new

    def __repr__(self) -> str:
        """Return a string representation in `__init__` syntax.

        Unknown fields and extensions are not included in the output.
        """
        parts: list[str] = []
        for member in self._desc.members:
            if isinstance(member, DescOneof):
                if (value := getattr(self, member.local_name)) is not None:
                    parts.append(f"{member.local_name}={value!r}")
                continue
            if member in self:
                value = self[member]
                parts.append(f"{member.local_name}={value!r}")
        return f"{self.__class__.__qualname__}({', '.join(parts)})"

    def __replace__(self: Self, **kwargs: Any) -> Self:
        """Create a copy by replacing fields.

        Similar to dataclasses.replace(), creates a shallow copy of the message
        with the specified fields updated to new values. This method is designed
        to work with `copy.replace()` available in Python 3.13+.

        Args:
            **kwargs: Field names and their new values.

        Returns:
            A new message instance with the specified fields replaced.

        Raises:
            AttributeError: If an unknown field name is provided.

        Examples:
            ```python
            msg1 = Message(field1=1, field2=2)
            msg2 = copy.replace(msg1, field1=10)  # Python 3.13+
            # msg2 is Message(field1=10, field2=2)
            ```
        """
        # Create a shallow copy first
        new_instance = copy(self)
        for key, value in kwargs.items():
            setattr(new_instance, key, value)
        return new_instance

    def __setattr__(self, name: str, value: Any, /) -> None:
        """Set a field or oneof attribute by local name.

        Raises:
            AttributeError: If name is not a known field, oneof, or internal attribute.
        """
        if not self._desc._requires_presence:
            return object_setattr(self, name, value)

        field = self._desc._fields_by_local_name.get(name)
        if field is not None and field._requires_presence:
            self._set_field_number_present(field.number)
        object_setattr(self, name, value)
        return None

    def has_field(self, key: FieldNamesT, /) -> bool:
        """Check if a field is set by its proto name (e.g., `msg.has_field("field_name")`).

        This can be used to check whether a field with explicit presence has been set.

        Args:
            key: The proto field name as a string.

        Returns:
            `True` if the field is set, `False` otherwise.

        Raises:
            KeyError: If the field does not exist on this message.
        """
        return self._resolve_field(key) in self

    def clear_field(self, key: FieldNamesT, /) -> None:
        """Clear a field by its proto name (e.g., `msg.clear_field("field_name")`).

        This can be used to clear a field with explicit presence or reset a
        value to its default.

        Args:
            key: The proto field name as a string.

        Raises:
            KeyError: If the field does not exist on this message.
        """
        del self[self._resolve_field(key)]

    @overload
    def __getitem__(self, key: DescField | DescUnknownField, /) -> Any: ...

    @overload
    def __getitem__(self, key: Extension[M, E], /) -> E: ...

    def __getitem__(self, key: DescField | DescUnknownField | Extension, /) -> Any:
        """Get a field value by descriptor.

        Args:
            key: A `DescField`, `DescUnknownField`, or `Extension`.

        Returns:
            The field value, or the default if unset. For message fields the
                default is `None`; for scalars the zero value (`0`, `""`,
                `False`, etc.); for repeated/map fields an empty `list`/`dict`.
                If key is a oneof, returns a [`Oneof`][] if one of its fields is
                set, `None` otherwise.

        Raises:
            KeyError: If the field does not exist on this message.
            TypeError: If the key is not a DescField, DescUnknownField, or Extension.
        """
        if isinstance(key, (Extension, DescUnknownField)):
            if isinstance(key, Extension):
                key._assert_message_type(self)
                number = key._desc.number
                field_value = key._desc.value
            else:
                number = key.number
                field_value = key.value
            if (value := get_unknown_field(self, number, field_value)) is not None:
                return value
            return default_value(field_value)

        member = self._validate_member(key)
        return self._get_member(member)

    def _get_member(self, member: DescField) -> Any:
        """Get a field without validating."""
        if (
            isinstance(member.value, DescFieldValueSingular)
            and member.value.oneof is not None
        ):
            # Return the value if the field is selected in the oneof.
            # Fall back to the zero value.
            value = getattr(self, member.value.oneof.local_name)
            if isinstance(value, Oneof) and value.field == member.name:
                return value.value
            return default_value(member.value)
        # Return the attribute as is
        return getattr(self, member.local_name)

    @overload
    def __setitem__(self, key: DescField | DescUnknownField, value: Any, /) -> None: ...

    @overload
    def __setitem__(self, key: Extension[M, E], value: E, /) -> None: ...

    def __setitem__(
        self, key: DescField | DescUnknownField | Extension, value: Any, /
    ) -> None:
        """Set a field value by descriptor or proto name.

        Fields in a oneof can be set like regular fields, which resets siblings.

        Args:
            key: A `DescField`, `DescUnknownField`, or `Extension`. If key is a oneof, a
                [`Oneof`][] is accepted.
            value: The value to assign.

        Raises:
            KeyError: If the field does not exist on this message.
            TypeError: If the key is not a DescField, DescUnknownField, or Extension.
        """
        if isinstance(key, (Extension, DescUnknownField)):
            if isinstance(key, Extension):
                key._assert_message_type(self)
                number = key._desc.number
                field_value = key._desc.value
            else:
                number = key.number
                field_value = key.value
            set_unknown_field(self, number, field_value, value)
            return None

        member = self._validate_member(key)
        return self._set_member(member, value)

    def _set_member(self, member: DescField, value: Any) -> None:
        """Set a field without validating."""
        if (
            isinstance(member.value, DescFieldValueSingular)
            and member.value.oneof is not None
        ):
            # Set a new Oneof with the selected field and value
            value = Oneof(field=member.name, value=value)
            object_setattr(self, member.value.oneof.local_name, value)
        else:
            # Set the attribute as is
            object_setattr(self, member.local_name, value)
            if member._requires_presence:
                self._set_field_number_present(member.number)

    @overload
    def __contains__(self, key: DescField | DescUnknownField, /) -> bool: ...

    @overload
    def __contains__(self, key: Extension[M, E], /) -> bool: ...

    def __contains__(self, key: DescField | DescUnknownField | Extension, /) -> bool:
        """Check if a field is set (e.g., `desc in msg`).

        For fields with explicit presence, checks if the field has been set.
        For fields without presence (implicit presence), compares against the
        default value.

        Args:
            key: A `DescField`, `DescUnknownField`, or `Extension`. If key is a oneof, a
                [`Oneof`][] is accepted.

        Returns:
            `True` if the field is set or non-zero. If key is a oneof,
                `True` if any of its fields is set.

        Raises:
            KeyError: If the field does not exist on this message.
            TypeError: If the key is not a DescField, DescUnknownField, or Extension.
        """
        if isinstance(key, (Extension, DescUnknownField)):
            if isinstance(key, Extension):
                if not key._is_correct_message_type(self):
                    return False
                number = key._desc.number
                field_value = key._desc.value
            else:
                number = key.number
                field_value = key.value
            return has_unknown_field(self, number, field_value)

        member = self._validate_member(key)
        return self._contains_member(member)

    def _contains_member(self, member: DescField) -> bool:
        """Check if a field is set without validating."""
        match field_value := member.value:
            case (
                DescFieldValueScalar(oneof=desc_oneof)
                | DescFieldValueMessage(oneof=desc_oneof)
                | DescFieldValueEnum(oneof=desc_oneof)
            ) if desc_oneof is not None:
                oneof = getattr(self, desc_oneof.local_name)
                return isinstance(oneof, Oneof) and oneof.field == member.name
            case DescFieldValueScalar(oneof=None) | DescFieldValueEnum(oneof=None):
                if member._requires_presence:
                    return self._get_field_number_present(member.number)
        return not is_zero_value(field_value, getattr(self, member.local_name))

    @overload
    def __delitem__(self, key: DescField | DescUnknownField, /) -> None: ...

    @overload
    def __delitem__(self, key: Extension[M, E], /) -> None: ...

    def __delitem__(self, key: DescField | DescUnknownField | Extension, /) -> None:
        """Clear a field by its key (e.g., `del msg[desc]`).

        Clears the field to its default value. Does not delete the attribute.
        For message fields, sets to `None`; for scalars, the zero value;
        for repeated/map fields, clears to an empty `list`/`dict`.

        Args:
            key: A `DescField`, `DescUnknownField`, or `Extension`.

        Raises:
            KeyError: If the field does not exist on this message.
            TypeError: If the key is not a DescField, DescUnknownField, or Extension.
        """
        if isinstance(key, (Extension, DescUnknownField)):
            if isinstance(key, Extension):
                key._assert_message_type(self)
                number = key._desc.number
            else:
                number = key.number
            if uf := self._unknown_fields:
                uf.pop(number, None)
            return

        member = self._validate_member(key)
        self._del_member(member)

    def _del_member(self, member: DescField) -> None:
        """Delete a field without validating."""
        attr = member.local_name
        match field_value := member.value:
            case (
                DescFieldValueScalar() | DescFieldValueMessage() | DescFieldValueEnum()
            ):
                if field_value.oneof is None:
                    # Bypass __setattr__ to avoid marking the field as present
                    object_setattr(self, attr, default_value(field_value))
                    self._clear_field_number_present(member.number)
                else:
                    oneof = getattr(self, field_value.oneof.local_name)
                    if isinstance(oneof, Oneof) and oneof.field == member.name:
                        # Clear the oneof attribute
                        object_setattr(self, field_value.oneof.local_name, None)
            case DescFieldValueList() | DescFieldValueMap():
                # Get the collection and clear it, fall back to setting a new collection
                if not hasattr(self, attr):
                    object_setattr(self, attr, default_value(field_value))
                    return
                value = getattr(self, attr)
                if not isinstance(value, list) and not isinstance(value, dict):
                    object_setattr(self, attr, default_value(field_value))
                    return
                value.clear()

    def __iter__(self) -> Iterator[DescField]:
        """Iterate over all [`DescField`][]s in this message that are set."""
        for field in self._desc.fields:
            if self._contains_member(field):
                yield field

    def __eq__(self, other: object, /) -> bool:
        """Compare two messages for equality.

        Two messages are considered equal when all of the following hold:

        - They have the same type.
        - For every field, both messages agree on whether the field is set or unset.
        - All set fields have equal values.

        NaN-valued floats are treated as equal to each other, consistent with
        Python's container equality semantics (e.g. `list`, `dict`).

        Extensions and unknown fields are not considered in the comparison.
        """
        if not isinstance(other, type(self)):
            return NotImplemented
        for field in self._desc.fields:
            self_set = field in self
            other_set = field in other
            if self_set != other_set:
                return False
            if self_set:
                self_val = self[field]
                other_val = other[field]
                if self_val is not other_val and self_val != other_val:
                    return False
        return True

    @classmethod
    def from_json(
        cls: type[Self],
        json: str | bytes | bytearray,
        *,
        ignore_unknown_fields: bool = False,
        registry: Registry | None = None,
    ) -> Self:
        """Create a new message from a ProtoJSON string.

        Args:
            json: A str, bytes, or bytearray instance containing the ProtoJSON.
            ignore_unknown_fields:
                Proto3 JSON parser should reject unknown fields by default.
                This option ignores unknown fields in parsing, as well as unrecognized
                enum string representations.
            registry:
                This option is required to read `google.protobuf.Any` and extensions
                from JSON format.

        Raises:
            json.JSONDecodeError: If json_source is not valid JSON.
            TypeError: If the JSON structure does not match expected types.
            ValueError: If a google.protobuf.Any or an extension cannot be resolved
                through the registry.
        """
        from ._from_json import merge_from_json  # noqa: PLC0415

        msg = cls()
        merge_from_json(
            msg, json, ignore_unknown_fields=ignore_unknown_fields, registry=registry
        )
        return msg

    @classmethod
    def from_binary(
        cls: type[Self], data: bytes, *, ignore_unknown_fields: bool = False
    ) -> Self:
        """Create a new message by parsing serialized binary data.

        To merge into an existing message, use [`merge_from_binary`][].

        Args:
            data: Serialized binary protobuf data.
            ignore_unknown_fields: If `True`, unknown fields in the binary data are silently discarded.
        """
        message = cls()
        message._merge_from_binary(data, ignore_unknown_fields=ignore_unknown_fields)
        return message

    @classmethod
    def desc(cls) -> DescMessage:
        """Get the associated DescMessage with this type."""
        return cls._desc

    def __getstate__(self) -> object:
        return self.to_binary()

    def __setstate__(self, state: object, /) -> None:
        if not isinstance(state, bytes):
            msg = f"invalid state for unpickling {self.__class__.__name__}: expected bytes, got {type(state).__name__}"
            raise TypeError(msg)
        self.__init__()
        self._merge_from_binary(state, ignore_unknown_fields=False)

    def _validate_member(self, key: DescField) -> DescField:
        """Validates the DescField is part of this message.

        Raises:
            KeyError: If the field does not exist on this message.
            TypeError: If the key is not a DescField.
        """
        if isinstance(key, DescField):
            if key.parent.type_name == self._desc.type_name:
                return key
            msg = f"{key!s} cannot be used with {self._desc!s}"
            raise KeyError(msg)
        msg = f"key must be a DescField, not {type(key).__name__}"
        raise TypeError(msg)

    def _resolve_field(self, key: str) -> DescField:
        if not isinstance(key, str):
            msg = f"key must be a str, not {type(key).__name__}"
            raise TypeError(msg)
        if field := self._desc._fields_by_name.get(key):
            return field
        if field := self._desc._fields_by_local_name.get(key):
            msg = (
                f"unknown key for {self._desc!s}: {key!r}, did you mean {field.name!r}?"
            )
            raise KeyError(msg)
        msg = f"unknown key for {self._desc!s}: {key!r}"
        raise KeyError(msg)

    def _merge_from_binary(self, data: bytes, ignore_unknown_fields: bool) -> None:  # noqa: FBT001
        opts = FromBinaryOptions(ignore_unknown_fields=ignore_unknown_fields)
        read_message(
            self, BinaryReader(memoryview(data)), opts, depth=0, length=len(data)
        )

    def _merge_from(self: Self, source: Self, ignore_unknown_fields: bool) -> None:  # noqa: FBT001
        for field in source:
            match field_value := field.value:
                case DescFieldValueMessage():
                    if field in self:
                        self[field]._merge_from(
                            source[field], ignore_unknown_fields=ignore_unknown_fields
                        )
                    else:
                        self[field] = deepcopy(source[field])
                case DescFieldValueList():
                    target_list: list = self[field]
                    if isinstance(field_value.element, DescMessage):
                        target_list.extend(deepcopy(m) for m in source[field])
                    else:
                        target_list.extend(source[field])
                case DescFieldValueMap():
                    target_map: dict = self[field]
                    if isinstance(field_value.value, DescMessage):
                        for key, value in source[field].items():
                            target_map[key] = deepcopy(value)
                    else:
                        target_map.update(source[field])
                case _:
                    self[field] = source[field]
        if not ignore_unknown_fields and (uf := source._unknown_fields):
            for key, value in uf.items():
                self._get_or_init_unknown_fields().setdefault(key, []).extend(value)

    # Methods for updating whether a field is present or not by number. Overridden by native code.

    def _get_field_number_present(self, number: int) -> bool:
        return number in self._present

    def _set_field_number_present(self, number: int) -> None:
        self._present.add(number)

    def _clear_field_number_present(self, number: int) -> None:
        self._present.discard(number)

    def _get_or_init_unknown_fields(self) -> dict[int, list[bytes]]:
        if (uf := self._unknown_fields) is None:
            uf = {}
            object_setattr(self, "_unknown_fields", uf)
        return uf
