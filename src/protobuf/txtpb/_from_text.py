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

import math
from dataclasses import dataclass
from enum import Enum as _StdEnum
from typing import TYPE_CHECKING, Any

from protobuf._descriptors import (
    DescEnum,
    DescExtension,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    ScalarType,
)
from protobuf._field_values import scalar_zero_value
from protobuf._from_json import _read_int
from protobuf._typing import assert_never
from protobuf._wire._binary_reader import DEPTH_LIMIT

from ._to_text import fround, group_like_message

if TYPE_CHECKING:
    from collections.abc import Callable

    from protobuf._descriptors import DescOneof
    from protobuf._enum import Enum as ProtoEnum
    from protobuf._message import Message
    from protobuf._registry import Registry


def merge_from_text(
    message: Message,
    text: str | bytes | bytearray,
    *,
    registry: Registry | None = None,
    ignore_unknown_fields: bool = False,
) -> None:
    """Parse a protobuf text format string, merging fields into an existing message.

    Merge rules by field kind:

    - Scalar and enum: the existing value is overwritten.
    - Message: recursively merged if already present, otherwise set.
    - Repeated: elements are appended.
    - Map: entries are added; existing keys are overwritten.

    Args:
        message: The message instance to merge into.
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
        RecursionError: If messages are nested deeper than the supported limit.
    """
    if isinstance(text, (bytes, bytearray)):
        text = text.decode()
    ctx = _ParseContext(
        reader=_TextReader(text),
        registry=registry,
        ignore_unknown_fields=ignore_unknown_fields,
    )
    _read_message_body(message, ctx, _TokenKind.EOF)


class _ParseContext:
    __slots__ = ("depth", "ignore_unknown_fields", "reader", "registry")

    def __init__(
        self,
        reader: _TextReader,
        registry: Registry | None,
        *,
        ignore_unknown_fields: bool,
    ) -> None:
        self.reader = reader
        self.registry = registry
        self.ignore_unknown_fields = ignore_unknown_fields
        self.depth = 0


def _read_message_body(msg: Message, ctx: _ParseContext, close: _TokenKind) -> None:
    """Read a message body (its fields until `close`), guarding nesting depth."""
    ctx.depth += 1
    if ctx.depth > DEPTH_LIMIT:
        msg_ = f"exceeded maximum recursion depth {DEPTH_LIMIT} while parsing message"
        raise RecursionError(msg_)
    _read_fields(msg, ctx, close)
    ctx.depth -= 1


def _read_fields(msg: Message, ctx: _ParseContext, close: _TokenKind) -> None:
    """Read the fields of a message until `close` (or EOF for the top level)."""
    # Tracks the fields and oneofs seen in this message body, so a non-repeated
    # field set twice, or two members of the same oneof, are rejected.
    seen_fields: set[int] = set()
    seen_oneofs: set[DescOneof] = set()
    while True:
        tok = ctx.reader.peek()
        if tok.kind == _TokenKind.EOF:
            if close != _TokenKind.EOF:
                msg_ = f'unexpected end of input, expected "{close.value}"'
                raise ValueError(msg_)
            return
        if close != _TokenKind.EOF and tok.kind == close:
            ctx.reader.next()
            return
        _read_field(msg, ctx, seen_fields, seen_oneofs)
        # A single optional "," or ";" may follow a field. Because the next
        # iteration treats a separator as a field name and rejects it, a
        # doubled separator is an error, while a single trailing one is
        # allowed.
        _consume_separator(ctx)


def _read_field(
    msg: Message, ctx: _ParseContext, seen_fields: set[int], seen_oneofs: set[DescOneof]
) -> None:
    name_tok = ctx.reader.next()
    desc = msg._desc
    match name_tok.kind:
        case _TokenKind.IDENTIFIER:
            if (field := _field_by_text_name(desc, name_tok.text)) is not None:
                _check_seen(field, seen_fields, seen_oneofs)
                _read_field_value(msg, field, ctx)
                return
            # Reserved field names are silently skipped; any other unknown name is
            # an error, unless ignore_unknown_fields is set.
            if name_tok.text in desc.proto.reserved_name or ctx.ignore_unknown_fields:
                _skip_field_value(ctx)
                return
            msg_ = f'unknown field "{name_tok.text}" for {desc}'
            raise ValueError(msg_)
        case _TokenKind.LBRACKET:
            name = ctx.reader.read_type_name()
            # Inside google.protobuf.Any, a bracketed name is always a type URL; in
            # any other message it is an extension name.
            if desc.type_name == "google.protobuf.Any":
                _read_expanded_any(msg, ctx, name, seen_fields)
                return
            if (
                ctx.registry
                and (extension := ctx.registry.extension(name))
                and extension.extendee.type_name == desc.type_name
            ):
                _check_seen(extension, seen_fields, seen_oneofs)
                _read_extension_field(msg, extension, ctx)
                return
            if ctx.ignore_unknown_fields:
                _skip_field_value(ctx)
                return
            msg_ = f'unknown extension "[{name}]" for {desc}'
            raise ValueError(msg_)
        case _TokenKind.INT:
            # Like protobuf-go, a field cannot be addressed by number, so the
            # numbered output of print_unknown_fields cannot be read back.
            msg_ = f"cannot specify field by number: {name_tok.text}"
            raise ValueError(msg_)
        case _:
            msg_ = f"expected a field name, got {_describe(name_tok)}"
            raise ValueError(msg_)


def _check_seen(
    field: DescField | DescExtension, seen_fields: set[int], seen_oneofs: set[DescOneof]
) -> None:
    """Reject a repeated occurrence of a singular field, or a second member of the same oneof."""
    match field_value := field.value:
        case DescFieldValueList() | DescFieldValueMap():
            return
        case _:
            oneof = field_value.oneof
    if oneof:
        if oneof in seen_oneofs:
            msg = f'oneof "{oneof.name}" is already set'
            raise ValueError(msg)
        seen_oneofs.add(oneof)
    if field.number in seen_fields:
        name = (
            f'extension "[{field.type_name}]"'
            if isinstance(field, DescExtension)
            else f'field "{field.name}"'
        )
        msg = f"non-repeated {name} is repeated"
        raise ValueError(msg)
    seen_fields.add(field.number)


def _read_field_value(msg: Message, field: DescField, ctx: _ParseContext) -> None:
    # The ":" separator is optional before a message, group, or map value, but
    # required for scalars, enums, and lists of them.
    has_colon = _consume_colon(ctx)
    if not has_colon and not _colon_optional(field.value):
        msg_ = f'expected ":" before value of field "{field.name}"'
        raise ValueError(msg_)
    match field_value := field.value:
        case DescFieldValueScalar():
            msg._set_member(field, _read_scalar_value(field, field_value.scalar, ctx))
        case DescFieldValueEnum():
            msg._set_member(field, _read_enum_value(field_value.enum, ctx))
        case DescFieldValueMessage():
            if msg._contains_member(field):
                sub = msg._get_member(field)
            else:
                sub = field_value.message.type()
                msg._set_member(field, sub)
            _read_message_value(sub, ctx)
        case DescFieldValueList():
            _read_list_field(msg._get_member(field), field, field_value, ctx)
        case DescFieldValueMap():
            _read_map_field(msg._get_member(field), field, field_value, ctx)
        case _:
            assert_never(field_value)


def _read_extension_field(msg: Message, ext: DescExtension, ctx: _ParseContext) -> None:
    # Extensions live in the unknown-field set: read the new value into a
    # regular Python value seeded with any existing one, so a repeated
    # extension appends and a message extension merges, then store it back.
    has_colon = _consume_colon(ctx)
    if not has_colon and not _colon_optional(ext.value):
        msg_ = f'expected ":" before value of extension "[{ext.type_name}]"'
        raise ValueError(msg_)
    extension = ext.type
    match field_value := ext.value:
        case DescFieldValueScalar():
            msg[extension] = _read_scalar_value(ext, field_value.scalar, ctx)
        case DescFieldValueEnum():
            msg[extension] = _read_enum_value(field_value.enum, ctx)
        case DescFieldValueMessage():
            sub = msg[extension] if extension in msg else field_value.message.type()
            _read_message_value(sub, ctx)
            msg[extension] = sub
        case DescFieldValueList():
            existing = msg[extension] if extension in msg else []  # noqa: SIM401 # false positive, not a dict
            _read_list_field(existing, ext, field_value, ctx)
            msg[extension] = existing
        case _:
            assert_never(field_value)


def _colon_optional(
    field_value: (
        DescFieldValueScalar
        | DescFieldValueEnum
        | DescFieldValueMessage
        | DescFieldValueList
        | DescFieldValueMap
    ),
) -> bool:
    match field_value:
        case DescFieldValueMessage() | DescFieldValueMap():
            return True
        case DescFieldValueList(element=DescMessage()):
            return True
        case _:
            return False


def _read_message_value(msg: Message, ctx: _ParseContext) -> None:
    """Read a "{ ... }" or "< ... >" block into the given message."""
    _read_message_body(msg, ctx, _read_message_open(ctx))


def _read_message_open(ctx: _ParseContext) -> _TokenKind:
    open_tok = ctx.reader.next()
    match open_tok.kind:
        case _TokenKind.LBRACE:
            return _TokenKind.RBRACE
        case _TokenKind.LANGLE:
            return _TokenKind.RANGLE
        case _:
            msg = f'expected "{{" or "<", got {_describe(open_tok)}'
            raise ValueError(msg)


def _read_bracketed_list(ctx: _ParseContext, read_element: Callable[[], None]) -> None:
    """Read a repeated value: either a single element, or a bracketed list "[e, e, ...]"."""
    if ctx.reader.peek().kind != _TokenKind.LBRACKET:
        read_element()
        return
    ctx.reader.next()  # "["
    if ctx.reader.peek().kind == _TokenKind.RBRACKET:
        ctx.reader.next()
        return
    while True:
        read_element()
        sep = ctx.reader.next()
        if sep.kind == _TokenKind.RBRACKET:
            return
        if sep.kind != _TokenKind.COMMA:
            msg = f'expected "," or "]" in list, got {_describe(sep)}'
            raise ValueError(msg)


def _read_list_field(
    target: list[Any],
    field: DescField | DescExtension,
    field_value: DescFieldValueList,
    ctx: _ParseContext,
) -> None:
    _read_bracketed_list(
        ctx, lambda: target.append(_read_list_item(field, field_value, ctx))
    )


def _read_list_item(
    field: DescField | DescExtension,
    field_value: DescFieldValueList,
    ctx: _ParseContext,
) -> Any:
    match element := field_value.element:
        case ScalarType():
            return _read_scalar_value(field, element, ctx)
        case DescEnum():
            return _read_enum_value(element, ctx)
        case DescMessage():
            sub = element.type()
            _read_message_value(sub, ctx)
            return sub
        case _:
            assert_never(element)
    return None


def _read_map_field(
    target: dict[Any, Any],
    field: DescField,
    field_value: DescFieldValueMap,
    ctx: _ParseContext,
) -> None:
    _read_bracketed_list(ctx, lambda: _read_map_entry(target, field, field_value, ctx))


def _read_map_entry(
    target: dict[Any, Any],
    field: DescField,
    field_value: DescFieldValueMap,
    ctx: _ParseContext,
) -> None:
    """Read a map entry: a "{ key: ... value: ... }" block.

    A missing key or value defaults to the zero value, like protobuf-go. A
    duplicate "key" or "value" within one entry is an error; duplicate keys
    across separate entries are legal, with the last entry winning.
    """
    ctx.depth += 1
    if ctx.depth > DEPTH_LIMIT:
        msg = (
            f"exceeded maximum recursion depth {DEPTH_LIMIT} while parsing a map entry"
        )
        raise RecursionError(msg)
    close = _read_message_open(ctx)
    key = scalar_zero_value(field_value.key)
    value = _map_value_zero(field_value)
    key_seen = False
    value_seen = False
    while True:
        tok = ctx.reader.peek()
        if tok.kind == close:
            ctx.reader.next()
            break
        if tok.kind == _TokenKind.EOF:
            msg = f'unexpected end of input, expected "{close.value}"'
            raise ValueError(msg)
        name_tok = ctx.reader.next()
        if name_tok.kind != _TokenKind.IDENTIFIER:
            msg = f'expected "key" or "value", got {_describe(name_tok)}'
            raise ValueError(msg)
        if name_tok.text == "key":
            if key_seen:
                msg = 'map entry "key" is already set'
                raise ValueError(msg)
            key_seen = True
            _require_colon(ctx)
            key = _read_scalar_value(field, field_value.key, ctx)
        elif name_tok.text == "value":
            if value_seen:
                msg = 'map entry "value" is already set'
                raise ValueError(msg)
            value_seen = True
            value = _read_map_value(field, field_value, ctx)
        else:
            msg = f'unknown field "{name_tok.text}" in map entry'
            raise ValueError(msg)
        _consume_separator(ctx)
    ctx.depth -= 1
    target[key] = value


def _read_map_value(
    field: DescField, field_value: DescFieldValueMap, ctx: _ParseContext
) -> Any:
    match value_desc := field_value.value:
        case ScalarType():
            _require_colon(ctx)
            return _read_scalar_value(field, value_desc, ctx)
        case DescEnum():
            _require_colon(ctx)
            return _read_enum_value(value_desc, ctx)
        case DescMessage():
            _consume_colon(ctx)
            sub = value_desc.type()
            _read_message_value(sub, ctx)
            return sub
        case _:
            assert_never(value_desc)
    return None


def _map_value_zero(field_value: DescFieldValueMap) -> Any:
    match value_desc := field_value.value:
        case ScalarType():
            return scalar_zero_value(value_desc)
        case DescEnum():
            return value_desc.type(value_desc.values[0].number)
        case DescMessage():
            return value_desc.type()
        case _:
            assert_never(value_desc)
    return None


def _read_expanded_any(
    msg: Message, ctx: _ParseContext, type_url: str, seen_fields: set[int]
) -> None:
    """Read `google.protobuf.Any` in its expanded form `[type.url] { ... }`.

    The colon before `{` is optional here, as for any message value.

    The expanded form is mutually exclusive with the raw `type_url` (field 1)
    and `value` (field 2) fields, and may appear only once. We enforce that
    through the same seen-set the duplicate-field check uses: the expansion is
    rejected if either field is already set, and it marks both as set so a
    following `type_url` or `value` is rejected too.
    """
    if 1 in seen_fields or 2 in seen_fields:
        msg_ = "google.protobuf.Any cannot mix the expanded form with type_url/value"
        raise ValueError(msg_)
    if (
        not ctx.registry
        or (desc := ctx.registry.message(type_url.rpartition("/")[2])) is None
    ):
        msg_ = f'unable to resolve "{type_url}" for google.protobuf.Any'
        raise ValueError(msg_)
    _consume_colon(ctx)
    unpacked = desc.type()
    _read_message_value(unpacked, ctx)
    any_desc = msg._desc
    # Preserve the exact type URL, including any custom domain prefix.
    msg._set_member(any_desc._fields_by_name["type_url"], type_url)
    msg._set_member(any_desc._fields_by_name["value"], unpacked.to_binary())
    seen_fields.add(1)
    seen_fields.add(2)


def _consume_sign(ctx: _ParseContext) -> bool:
    """Consume an optional leading "-" sign and report whether one was present.

    This sees a sign token only before a number (the scanner glues a sign onto
    an identifier as in "-inf"), and whitespace and comments between the sign
    and the number are insignificant, so "- 42" means -42, matching
    protobuf-go.
    """
    if ctx.reader.peek().kind == _TokenKind.MINUS:
        ctx.reader.next()
        return True
    return False


def _read_scalar_value(
    field: DescField | DescExtension, scalar_type: ScalarType, ctx: _ParseContext
) -> Any:
    match scalar_type:
        case ScalarType.STRING | ScalarType.BYTES:
            tok = ctx.reader.next()
            if tok.kind != _TokenKind.STRING:
                msg = f"expected a string, got {_describe(tok)}"
                raise ValueError(msg)
            data = _concat_strings(tok, ctx)
            if scalar_type == ScalarType.BYTES:
                return data
            try:
                return data.decode()
            except UnicodeDecodeError:
                msg = f"invalid UTF-8 in string for {field}"
                raise ValueError(msg) from None
        case ScalarType.BOOL:
            return _read_bool_value(ctx.reader.next())
        case ScalarType.FLOAT:
            negative = _consume_sign(ctx)
            # Round to 32-bit precision: an out-of-range value becomes ±inf,
            # which is what the text format requires for float overflow.
            return fround(_read_float_value(ctx.reader.next(), negative))
        case ScalarType.DOUBLE:
            negative = _consume_sign(ctx)
            return _read_float_value(ctx.reader.next(), negative)
        case (
            ScalarType.UINT32
            | ScalarType.FIXED32
            | ScalarType.UINT64
            | ScalarType.FIXED64
        ):
            negative = _consume_sign(ctx)
            tok = ctx.reader.next()
            # Reject any sign for an unsigned field, including "-0".
            if negative:
                msg = "an unsigned field does not accept a negative value"
                raise ValueError(msg)
            return _read_int(field, scalar_type, _int_token_value(tok))
        case _:
            negative = _consume_sign(ctx)
            value = _int_token_value(ctx.reader.next())
            return _read_int(field, scalar_type, -value if negative else value)


def _read_enum_value(desc_enum: DescEnum, ctx: _ParseContext) -> ProtoEnum | int:
    negative = _consume_sign(ctx)
    tok = ctx.reader.next()
    if tok.kind == _TokenKind.IDENTIFIER:
        if negative:
            msg = f'invalid enum value "-{tok.text}" for {desc_enum}'
            raise ValueError(msg)
        for enum_value in desc_enum.values:
            if enum_value.name == tok.text:
                return desc_enum.type(enum_value.number)
        msg = f'unknown enum value "{tok.text}" for {desc_enum}'
        raise ValueError(msg)
    if tok.kind == _TokenKind.INT:
        value = _int_token_value(tok)
        if negative:
            value = -value
        if not -(2**31) <= value < 2**31:
            msg = f"enum value {value} out of range for {desc_enum}"
            raise ValueError(msg)
        # Succeeds for any int32 with an open enum, raises an error for an
        # unknown value with a closed (proto2) enum.
        return desc_enum.type(value)
    msg = f"expected an enum value for {desc_enum}, got {_describe(tok)}"
    raise ValueError(msg)


def _read_bool_value(tok: _Token) -> bool:
    if tok.kind == _TokenKind.IDENTIFIER:
        if tok.text in ("true", "True", "t"):
            return True
        if tok.text in ("false", "False", "f"):
            return False
    if tok.kind == _TokenKind.INT:
        value = _int_token_value(tok)
        if value == 0:
            return False
        if value == 1:
            return True
    msg = f"expected a bool, got {_describe(tok)}"
    raise ValueError(msg)


def _read_float_value(tok: _Token, negative: bool) -> float:  # noqa: FBT001
    if tok.kind == _TokenKind.IDENTIFIER:
        # A separate "-" token (negative) before a non-numeric float literal is
        # invalid; the only signed literals are "-inf"/"-infinity", which the
        # scanner glues into one identifier token. "-nan" is not a literal, so
        # it falls through to the error below. This matches protobuf-go's
        # identifier-path sign handling.
        if negative:
            msg = f'invalid float value "-{tok.text}"'
            raise ValueError(msg)
        match tok.text.lower():
            case "inf" | "infinity":
                return math.inf
            case "-inf" | "-infinity":
                return -math.inf
            case "nan":
                return math.nan
        msg = f'invalid float value "{tok.text}"'
        raise ValueError(msg)
    if tok.kind == _TokenKind.FLOAT:
        value = float(tok.text)
        return -value if negative else value
    if tok.kind == _TokenKind.INT:
        # Octal and hexadecimal literals are not valid for float and double
        # fields.
        if tok.base != 10:
            msg = "octal and hexadecimal are not valid for a float field"
            raise ValueError(msg)
        value = float(tok.text)
        return -value if negative else value
    msg = f"expected a float, got {_describe(tok)}"
    raise ValueError(msg)


def _int_token_value(tok: _Token) -> int:
    if tok.kind != _TokenKind.INT:
        msg = f"expected an integer, got {_describe(tok)}"
        raise ValueError(msg)
    return int(tok.text, tok.base)


def _concat_strings(first: _Token, ctx: _ParseContext) -> bytes:
    """Concatenate adjacent string literals into a single byte string."""
    data = first.bytes_value
    while ctx.reader.peek().kind == _TokenKind.STRING:
        data += ctx.reader.next().bytes_value
    return data


def _skip_field_value(ctx: _ParseContext) -> None:
    """Skip the value of a reserved field."""
    _consume_colon(ctx)
    _read_bracketed_list(ctx, lambda: _skip_single_value(ctx))


def _skip_single_value(ctx: _ParseContext) -> None:
    tok = ctx.reader.peek()
    if tok.kind in (_TokenKind.LBRACE, _TokenKind.LANGLE):
        _skip_message_block(ctx)
        return
    # A leading sign is consumed leniently here: skipping a reserved value
    # should tolerate "- 5".
    _consume_sign(ctx)
    value = ctx.reader.next()
    if value.kind == _TokenKind.STRING:
        while ctx.reader.peek().kind == _TokenKind.STRING:
            ctx.reader.next()
        return
    if value.kind not in (_TokenKind.IDENTIFIER, _TokenKind.INT, _TokenKind.FLOAT):
        msg = f"expected a value, got {_describe(value)}"
        raise ValueError(msg)


def _skip_message_block(ctx: _ParseContext) -> None:
    ctx.depth += 1
    if ctx.depth > DEPTH_LIMIT:
        msg = f"exceeded maximum recursion depth {DEPTH_LIMIT} while skipping a reserved field"
        raise RecursionError(msg)
    close = _read_message_open(ctx)
    while True:
        tok = ctx.reader.peek()
        if tok.kind == close:
            ctx.reader.next()
            ctx.depth -= 1
            return
        if tok.kind == _TokenKind.EOF:
            msg = f'unexpected end of input, expected "{close.value}"'
            raise ValueError(msg)
        name_tok = ctx.reader.next()
        if name_tok.kind == _TokenKind.LBRACKET:
            ctx.reader.read_type_name()
        elif name_tok.kind not in (_TokenKind.IDENTIFIER, _TokenKind.INT):
            msg = f"expected a field name, got {_describe(name_tok)}"
            raise ValueError(msg)
        _skip_field_value(ctx)
        _consume_separator(ctx)


def _consume_separator(ctx: _ParseContext) -> None:
    """Consume an optional "," or ";" that separates fields or list/map elements."""
    if ctx.reader.peek().kind in (_TokenKind.COMMA, _TokenKind.SEMICOLON):
        ctx.reader.next()


def _consume_colon(ctx: _ParseContext) -> bool:
    if ctx.reader.peek().kind == _TokenKind.COLON:
        ctx.reader.next()
        return True
    return False


def _require_colon(ctx: _ParseContext) -> None:
    if not _consume_colon(ctx):
        msg = f'expected ":", got {_describe(ctx.reader.peek())}'
        raise ValueError(msg)


def _field_by_text_name(desc: DescMessage, name: str) -> DescField | None:
    """Resolve a field by its text format name, mirroring protobuf-go's ByTextName.

    Group-like fields are addressed by their field name (which is the
    lowercase of the message type name) or by the message type name itself;
    JSON names are not valid.
    """
    if field := desc._fields_by_name.get(name):
        return field
    # A group-like field is also addressable by its message type name.
    if (
        (candidate := desc._fields_by_name.get(name.lower()))
        and (group := group_like_message(candidate))
        and group.name == name
    ):
        return candidate
    return None


def _describe(tok: _Token) -> str:
    match tok.kind:
        case _TokenKind.IDENTIFIER | _TokenKind.INT | _TokenKind.FLOAT:
            return f'"{tok.text}"'
        case _TokenKind.STRING:
            return "a string"
        case _TokenKind.EOF:
            return "end of input"
        case _:
            return f'"{tok.kind.value}"'


class _TokenKind(_StdEnum):
    """The kind of a lexical token of the protobuf text format."""

    EOF = "eof"
    IDENTIFIER = "identifier"
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    LBRACE = "{"
    RBRACE = "}"
    LANGLE = "<"
    RANGLE = ">"
    LBRACKET = "["
    RBRACKET = "]"
    COLON = ":"
    COMMA = ","
    SEMICOLON = ";"
    MINUS = "-"


@dataclass(slots=True, frozen=True)
class _Token:
    """A lexical token of the protobuf text format.

    Identifiers and numbers carry their text (numbers also their base, so the
    parser can accept or reject octal and hexadecimal per field type); string
    tokens carry their decoded bytes (the same bytes back both string and
    bytes fields, and bytes fields may hold sequences that are not valid
    UTF-8). Punctuation tokens and eof carry no payload.

    The minus sign before a number is its own token rather than part of the
    number, which keeps numeric sign handling in one place in the parser and,
    because whitespace and comments between tokens are insignificant, makes
    `- 42` mean `-42`, matching protobuf-go. A minus glued to a letter is
    instead folded into a negative identifier (`-inf`/`-infinity`), because
    protobuf-go requires the sign glued for those literals — `- inf` is an
    error there, not negative infinity.
    """

    kind: _TokenKind
    text: str = ""
    bytes_value: bytes = b""
    base: int = 10


_TOKEN_EOF = _Token(kind=_TokenKind.EOF)
_STRUCTURAL = {
    "{": _TokenKind.LBRACE,
    "}": _TokenKind.RBRACE,
    "<": _TokenKind.LANGLE,
    ">": _TokenKind.RANGLE,
    "[": _TokenKind.LBRACKET,
    "]": _TokenKind.RBRACKET,
    ":": _TokenKind.COLON,
    ",": _TokenKind.COMMA,
    ";": _TokenKind.SEMICOLON,
}


class _TextReader:
    """A tokenizer for the protobuf text format.

    The parser drives it with `peek()` and `next()` (one-token lookahead) and,
    once it knows it is in a field-name position, asks for the contents of a
    bracketed name with `read_type_name()` — the `[...]` syntax for extensions
    and Any type URLs is ambiguous with the list syntax at the lexical level.
    """

    __slots__ = ("_input", "_length", "_lookahead", "_pos")

    def __init__(self, text: str) -> None:
        # Skip any unicode BOM
        self._input = text.removeprefix("\ufeff")
        self._length = len(self._input)
        self._pos = 0
        self._lookahead: _Token | None = None

    def peek(self) -> _Token:
        """Return the next token without consuming it."""
        if self._lookahead is None:
            self._lookahead = self._scan()
        return self._lookahead

    def next(self) -> _Token:
        """Consume and return the next token."""
        tok = self.peek()
        self._lookahead = None
        return tok

    def read_type_name(self) -> str:
        """Read the contents of a bracketed name.

        Used for extension fields and the expanded form of
        google.protobuf.Any. The opening `[` must already have been consumed
        with `next()`. Whitespace and comments inside the brackets are
        insignificant. Returns the inner name with the brackets removed, e.g.
        "pkg.Message.field" or "type.googleapis.com/pkg.Message".

        The text format grammar for this is incomplete, so we follow
        protobuf-go's parseTypeName: the prefix may contain URL characters,
        `/` separators, and well-formed percent-escapes, and the type name
        after the last `/` must be a dotted identifier.
        """
        parts: list[str] = []
        while True:
            self._skip_space()
            c = self._char_at(self._pos)
            if c is None:
                msg = "unterminated [...] name"
                raise ValueError(msg)
            if c == "]":
                self._pos += 1
                break
            if c == "/":
                parts.append("/")
                self._pos += 1
            elif c == "%":
                if not _is_hex_digit(self._char_at(self._pos + 1)) or not _is_hex_digit(
                    self._char_at(self._pos + 2)
                ):
                    msg = "invalid percent-escape in [...] name"
                    raise ValueError(msg)
                parts.append(self._input[self._pos : self._pos + 3])
                self._pos += 3
            elif _is_url_char(c):
                parts.append(c)
                self._pos += 1
            else:
                msg = f"unexpected {_quote_char(c)} in [...] name"
                raise ValueError(msg)
        name = "".join(parts)
        _validate_type_name(name)
        return name

    def _scan(self) -> _Token:
        self._skip_space()
        c = self._char_at(self._pos)
        if c is None:
            return _TOKEN_EOF
        if c in _STRUCTURAL:
            self._pos += 1
            return _Token(kind=_STRUCTURAL[c])
        if c == "-":
            # A "-" glued to a letter begins a negative identifier (-inf or
            # -infinity); otherwise it is a sign token. A number may have
            # whitespace between the sign and the digits, so the sign is a
            # separate token the parser reassembles; a float literal may not,
            # matching protobuf-go, where inf/infinity parse through the
            # identifier path with the sign glued (so "- inf" is an error but
            # "- 42" is -42).
            if _is_letter(self._char_at(self._pos + 1)):
                return self._scan_identifier()
            self._pos += 1
            return _Token(kind=_TokenKind.MINUS)
        if c in ('"', "'"):
            return self._scan_string(c)
        if _is_digit(c) or (c == "." and _is_digit(self._char_at(self._pos + 1))):
            return self._scan_number()
        if _is_letter(c):
            return self._scan_identifier()
        msg = f"unexpected {_quote_char(c)}"
        raise ValueError(msg)

    def _skip_space(self) -> None:
        while self._pos < self._length:
            c = self._input[self._pos]
            if c in " \t\n\r\v\f":
                self._pos += 1
            elif c == "#":
                # A comment runs to the end of the line.
                self._pos += 1
                while self._pos < self._length and self._input[self._pos] != "\n":
                    self._pos += 1
            else:
                return

    def _scan_identifier(self) -> _Token:
        start = self._pos
        if self._char_at(self._pos) == "-":
            self._pos += 1  # a glued negative identifier such as -inf
        self._pos += 1  # the first letter (the caller guarantees one is present)
        while _is_letter_or_digit(self._char_at(self._pos)):
            self._pos += 1
        return _Token(kind=_TokenKind.IDENTIFIER, text=self._input[start : self._pos])

    def _scan_number(self) -> _Token:
        """Scan a numeric literal.

        The sign is a separate token, so a number never starts with `-`. The
        literal must end at a delimiter, so `10f` is a float but `10bar`,
        `1.2.3`, `09`, and `0xZ` are errors.
        """
        start = self._pos
        if self._input[self._pos] == "0" and self._char_at(self._pos + 1) in ("x", "X"):
            # Hexadecimal: `0x` followed by one or more hex digits.
            self._pos += 2
            digits = self._pos
            while _is_hex_digit(self._char_at(self._pos)):
                self._pos += 1
            if self._pos == digits:
                msg = "invalid hexadecimal literal"
                raise ValueError(msg)
            self._expect_delimiter()
            return _Token(
                kind=_TokenKind.INT, text=self._input[start : self._pos], base=16
            )
        if self._input[self._pos] == "0" and _is_octal_digit(
            self._char_at(self._pos + 1)
        ):
            # Octal: a leading `0` followed by octal digits. A subsequent
            # non-octal digit (as in `078`) ends the run, and the delimiter
            # check rejects it.
            self._pos += 1
            while _is_octal_digit(self._char_at(self._pos)):
                self._pos += 1
            self._expect_delimiter()
            return _Token(
                kind=_TokenKind.INT, text=self._input[start : self._pos], base=8
            )
        # A decimal integer or a floating point literal. A leading "0" stands
        # alone (octal and hex were handled above), so the delimiter check
        # below rejects a following digit — `08` and `09` are malformed, not
        # decimal.
        is_float = False
        if self._char_at(self._pos) == "0":
            self._pos += 1
        else:
            while _is_digit(self._char_at(self._pos)):
                self._pos += 1
        if self._char_at(self._pos) == ".":
            is_float = True
            self._pos += 1
            while _is_digit(self._char_at(self._pos)):
                self._pos += 1
        if self._char_at(self._pos) in ("e", "E"):
            is_float = True
            self._pos += 1
            if self._char_at(self._pos) in ("+", "-"):
                self._pos += 1
            digits = self._pos
            while _is_digit(self._char_at(self._pos)):
                self._pos += 1
            if self._pos == digits:
                msg = "invalid exponent"
                raise ValueError(msg)
        # A trailing `f`/`F` marks a float and is not part of the value passed
        # to float(); capture the end before consuming it so it stays out of
        # the text.
        end = self._pos
        if self._char_at(self._pos) in ("f", "F"):
            is_float = True
            self._pos += 1
        self._expect_delimiter()
        text = self._input[start:end]
        if is_float:
            return _Token(kind=_TokenKind.FLOAT, text=text)
        return _Token(kind=_TokenKind.INT, text=text, base=10)

    def _expect_delimiter(self) -> None:
        # A number must be terminated by a delimiter — any character that
        # cannot continue a name or number. This rejects `09`, `0xZ`, `1.2.3`,
        # and `5bar`.
        c = self._char_at(self._pos)
        if c is not None and (_is_letter_or_digit(c) or c in ("-", "+", ".")):
            msg = "invalid number"
            raise ValueError(msg)

    def _scan_string(self, quote: str) -> _Token:
        self._pos += 1  # opening quote
        data = bytearray()
        # Literal characters are accumulated as a run and encoded as UTF-8 in
        # one batch when the run ends (at an escape or the closing quote).
        # Escapes contribute their bytes directly.
        run_start = self._pos
        while True:
            c = self._char_at(self._pos)
            if c is None:
                msg = "unterminated string"
                raise ValueError(msg)
            if c == quote:
                _push_utf8(data, self._input[run_start : self._pos])
                self._pos += 1  # closing quote
                return _Token(kind=_TokenKind.STRING, bytes_value=bytes(data))
            if c == "\\":
                _push_utf8(data, self._input[run_start : self._pos])
                self._pos += 1  # backslash
                self._scan_escape(data)
                run_start = self._pos
                continue
            # A raw newline or NUL is not allowed in a string, matching
            # protobuf-go.
            if c in ("\n", "\0"):
                msg = f"invalid {_quote_char(c)} in string"
                raise ValueError(msg)
            self._pos += 1

    def _scan_escape(self, data: bytearray) -> None:
        c = self._char_at(self._pos)
        if c is None:
            msg = "unterminated escape sequence"
            raise ValueError(msg)
        if c in ('"', "'", "\\", "?"):
            data.append(ord(c))
            self._pos += 1
            return
        if simple := _SIMPLE_ESCAPES.get(c):
            data.append(simple)
            self._pos += 1
            return
        if c == "x":
            self._pos += 1
            hex_digits = self._take_while(_is_hex_digit, 2)
            if not hex_digits:
                msg = "invalid hex escape \\x"
                raise ValueError(msg)
            data.append(int(hex_digits, 16))
            return
        if c in ("u", "U"):
            self._pos += 1
            width = 4 if c == "u" else 8
            hex_digits = self._take_while(_is_hex_digit, width)
            if len(hex_digits) != width:
                msg = f"invalid unicode escape \\{c}"
                raise ValueError(msg)
            code = int(hex_digits, 16)
            # Reject surrogate code points and values beyond U+10FFFF. We
            # deliberately do NOT combine an adjacent `\u` low surrogate into
            # a pair the way protobuf-go does: the conformance suite (the
            # StringLiteral*Surrogate* cases) requires every surrogate escape,
            # lone or paired, to be a parse error. Do not "fix" this toward
            # Go.
            if code > 0x10FFFF or 0xD800 <= code <= 0xDFFF:
                msg = f"invalid unicode escape \\{c}{hex_digits}"
                raise ValueError(msg)
            _push_utf8(data, chr(code))
            return
        if _is_octal_digit(c):
            octal_digits = self._take_while(_is_octal_digit, 3)
            value = int(octal_digits, 8)
            if value > 0xFF:
                msg = f"octal escape \\{octal_digits} out of range"
                raise ValueError(msg)
            data.append(value)
            return
        msg = f"invalid escape \\{c}"
        raise ValueError(msg)

    def _take_while(self, pred: Callable[[str | None], bool], limit: int) -> str:
        """Consume up to `limit` consecutive characters matching `pred` and return them."""
        start = self._pos
        while self._pos < start + limit and pred(self._char_at(self._pos)):
            self._pos += 1
        return self._input[start : self._pos]

    def _char_at(self, index: int) -> str | None:
        return self._input[index] if index < self._length else None


_SIMPLE_ESCAPES = {
    "a": 0x07,
    "b": 0x08,
    "f": 0x0C,
    "n": 0x0A,
    "r": 0x0D,
    "t": 0x09,
    "v": 0x0B,
}


def _validate_type_name(name: str) -> None:
    """Validate a type name (and URL prefix) from a bracketed name.

    Mirrors protobuf-go's parseTypeName: the type name is everything after the
    last `/`; the prefix before it is a URL that may carry extra characters
    and percent-escapes, but must not begin with `/`.
    """
    last_slash = name.rfind("/")
    if last_slash >= 0 and name.startswith("/"):
        msg = "invalid type name: empty URL host"
        raise ValueError(msg)
    type_name = name[last_slash + 1 :]
    if not type_name:
        msg = "invalid type name: empty"
        raise ValueError(msg)
    for part in type_name.split("."):
        if not part:
            msg = "invalid type name: empty component"
            raise ValueError(msg)
    for c in type_name:
        if not (_is_letter_or_digit(c) or c in (".", "-")):
            msg = f"unexpected {_quote_char(c)} in type name"
            raise ValueError(msg)


# These functions require the caller to ensure `c` is a single character string


def _is_digit(c: str | None) -> bool:
    return c is not None and "0" <= c <= "9"


def _is_octal_digit(c: str | None) -> bool:
    return c is not None and "0" <= c <= "7"


def _is_hex_digit(c: str | None) -> bool:
    return c is not None and ("0" <= c <= "9" or "a" <= c <= "f" or "A" <= c <= "F")


def _is_letter(c: str | None) -> bool:
    return c is not None and ("a" <= c <= "z" or "A" <= c <= "Z" or c == "_")


def _is_letter_or_digit(c: str | None) -> bool:
    return _is_letter(c) or _is_digit(c)


def _is_url_char(c: str) -> bool:
    """A character permitted in the URL prefix of an Any type name.

    Matches protobuf-go's isUrlChar plus the type-name characters.
    """
    return _is_letter_or_digit(c) or c in "-.~!$&()*+,;="


def _quote_char(c: str) -> str:
    code = ord(c)
    if 0x20 <= code <= 0x7E:
        return f'"{c}"'
    return f"U+{code:04X}"


def _push_utf8(data: bytearray, text: str) -> None:
    """Append the UTF-8 encoding of `text` to `data`.

    A lone surrogate (which cannot be encoded as UTF-8) becomes U+FFFD,
    matching the standard TextEncoder behavior of other implementations.
    """
    if not text:
        return
    try:
        data += text.encode()
    except UnicodeEncodeError:
        data += "".join(
            "�" if 0xD800 <= ord(ch) <= 0xDFFF else ch for ch in text
        ).encode()
