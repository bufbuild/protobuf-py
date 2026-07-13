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
import struct
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from protobuf._descriptors import (
    DescEnum,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    ScalarType,
)
from protobuf._typing import assert_never
from protobuf._wire import BinaryReader, WireType
from protobuf._wire._binary_reader import DEPTH_LIMIT

if TYPE_CHECKING:
    from collections.abc import Iterator

    from protobuf._descriptors import DescExtension
    from protobuf._message import Message
    from protobuf._registry import Registry


@dataclass(slots=True, frozen=True)
class ToTextOptions:
    print_unknown_fields: bool = False
    registry: Registry | None = None


_INDENT = "  "


class _TextWriter:
    """A writer for the protobuf text format.

    The writer owns layout: indentation, line breaks, and braces. Its output
    matches the canonical writer used by `google.protobuf.text_format` (and,
    for indentation and line breaks, txtpbfmt and protobuf-go): two-space
    indentation, `name: value` with a single space after the colon for scalar
    and enum fields, submessages as `name {` (no colon — the text format spec
    leaves the colon optional before a message value, and the C++/Python
    writer omits it) with the body indented and `}` aligned under the field
    name, and a trailing newline.
    """

    __slots__ = ("_chunks", "_depth")

    def __init__(self) -> None:
        self._chunks: list[str] = []
        self._depth = 0

    def scalar(self, name: str, value: str) -> None:
        """Write a scalar field: `<indent>name: value` followed by a newline."""
        self._chunks.append(f"{_INDENT * self._depth}{name}: {value}\n")

    @contextmanager
    def open_message(self, name: str) -> Iterator[None]:
        """Enters a message field and indents the body.

        Exiting will close the message, inline if no fields were written.
        """
        self._chunks.append("")
        open_len = len(self._chunks)
        self._depth += 1
        try:
            yield
        finally:
            self._depth -= 1
        if len(self._chunks) == open_len:
            # No fields were written.
            self._chunks[open_len - 1] = f"{_INDENT * self._depth}{name} {{}}\n"
        else:
            self._chunks[open_len - 1] = f"{_INDENT * self._depth}{name} {{\n"
            self._chunks.append(f"{_INDENT * self._depth}}}\n")

    def finish(self) -> str:
        return "".join(self._chunks)


def to_text(message: Message, opts: ToTextOptions) -> str:
    """Serialize a message to the protobuf text format."""
    writer = _TextWriter()
    _write_message(writer, message, opts)
    return writer.finish()


def _write_message(writer: _TextWriter, message: Message, opts: ToTextOptions) -> None:
    """Write the body of a message.

    Regular fields in declaration order, then resolvable extensions sorted by
    full name, then unknown fields by number (only when print_unknown_fields is
    enabled). For `google.protobuf.Any`, the expanded form replaces all of this.
    """
    if _write_any(writer, message, opts):
        return
    for field in message._desc.fields:
        # Unset fields are omitted, including unset required fields; like
        # protobuf-go, we do not validate required fields when serializing.
        if message._contains_member(field):
            _write_field(
                writer,
                _field_text_name(field),
                field.value,
                message._get_member(field),
                opts,
            )
    extension_numbers = _write_extensions(writer, message, opts)
    if opts.print_unknown_fields and (uf := message._unknown_fields):
        for number, records in uf.items():
            if number in extension_numbers:
                continue
            for record in records:
                reader = BinaryReader(memoryview(record))
                while reader.offset < len(record):
                    _write_unknown_field(writer, reader, depth=0)


def _write_field(
    writer: _TextWriter,
    name: str,
    field_value: (
        DescFieldValueScalar
        | DescFieldValueEnum
        | DescFieldValueMessage
        | DescFieldValueList
        | DescFieldValueMap
    ),
    value: Any,
    opts: ToTextOptions,
) -> None:
    match field_value:
        case DescFieldValueScalar():
            writer.scalar(name, _scalar_to_text(field_value.scalar, value))
        case DescFieldValueEnum():
            writer.scalar(name, _enum_to_text(field_value.enum, value))
        case DescFieldValueMessage():
            _write_message_value(writer, name, value, opts)
        case DescFieldValueList():
            _write_list(writer, name, field_value.element, value, opts)
        case DescFieldValueMap():
            _write_map(writer, name, field_value, value, opts)
        case _:
            assert_never(field_value)


def _write_message_value(
    writer: _TextWriter, name: str, message: Message, opts: ToTextOptions
) -> None:
    """Write a message value as `name { ... }`, or `name {}` when it has no body."""
    with writer.open_message(name):
        _write_message(writer, message, opts)


def _write_list(
    writer: _TextWriter,
    name: str,
    element: DescMessage | DescEnum | ScalarType,
    value: list[Any],
    opts: ToTextOptions,
) -> None:
    match element:
        case ScalarType():
            for item in value:
                writer.scalar(name, _scalar_to_text(element, item))
        case DescEnum():
            for item in value:
                writer.scalar(name, _enum_to_text(element, item))
        case DescMessage():
            for item in value:
                _write_message_value(writer, name, item, opts)
        case _:
            assert_never(element)


def _write_map(
    writer: _TextWriter,
    name: str,
    field_value: DescFieldValueMap,
    value: dict[Any, Any],
    opts: ToTextOptions,
) -> None:
    # Map entries are emitted in iteration (insertion) order; unlike
    # protobuf-go, we deliberately do not sort them.
    for key, val in value.items():
        with writer.open_message(name):
            writer.scalar("key", _scalar_to_text(field_value.key, key))
            match value_desc := field_value.value:
                case ScalarType():
                    writer.scalar("value", _scalar_to_text(value_desc, val))
                case DescEnum():
                    writer.scalar("value", _enum_to_text(value_desc, val))
                case DescMessage():
                    _write_message_value(writer, "value", val, opts)
                case _:
                    assert_never(value_desc)


def _write_any(writer: _TextWriter, message: Message, opts: ToTextOptions) -> bool:
    """Write `google.protobuf.Any` in its expanded form `[type.url] { ... }`.

    Returns False (so the generic path writes `type_url`/`value` instead) when
    the message is not an Any, has no type URL, or the type cannot be resolved.
    """
    desc = message._desc
    if desc.type_name != "google.protobuf.Any" or opts.registry is None:
        return False
    type_url_field = desc._fields_by_name.get("type_url")
    value_field = desc._fields_by_name.get("value")
    if type_url_field is None or value_field is None:
        return False
    type_url = message._get_member(type_url_field)
    if type_url == "":
        return False
    unpacked_desc = opts.registry.message(type_url.rpartition("/")[2])
    if unpacked_desc is None:
        return False
    unpacked = unpacked_desc.type.from_binary(message._get_member(value_field))
    # The bracketed name preserves the exact type URL, including a custom domain.
    _write_message_value(writer, f"[{type_url}]", unpacked, opts)
    return True


def _write_extensions(
    writer: _TextWriter, message: Message, opts: ToTextOptions
) -> set[int]:
    """Write resolvable extensions, sorted by full name.

    Returns their field numbers so _write_message does not also emit them as
    raw unknown fields.
    """
    numbers: set[int] = set()
    if opts.registry is None or not (uf := message._unknown_fields):
        return numbers
    extensions: list[DescExtension] = []
    for number in uf:
        extension = opts.registry.extension_for(message._desc, number)
        if extension is not None:
            numbers.add(number)
            extensions.append(extension)
    extensions.sort(key=lambda extension: extension.type_name)
    for extension in extensions:
        # A group-declared extension is still addressed by its extension name,
        # never by its group message type name.
        _write_field(
            writer,
            f"[{extension.type_name}]",
            extension.value,
            message[extension.type],
            opts,
        )
    return numbers


def _write_unknown_field(writer: _TextWriter, reader: BinaryReader, depth: int) -> None:
    """Write an unknown field by its field number, mirroring protobuf-go.

    Varints print as decimal, fixed-width values as hexadecimal,
    length-delimited data as a nested message when it parses cleanly as one and
    a quoted byte string otherwise, and groups recursively.
    """
    tag = reader.tag()
    name = str(tag.number)
    match tag.wire_type:
        case WireType.VARINT:
            writer.scalar(name, str(reader.uint64()))
        case WireType.BIT32:
            writer.scalar(name, f"0x{reader.fixed32():08x}")
        case WireType.BIT64:
            writer.scalar(name, f"0x{reader.fixed64():016x}")
        case WireType.LENGTH_DELIMITED:
            data = reader.bytes_()
            if depth < DEPTH_LIMIT and _parses_as_message(data):
                with writer.open_message(name):
                    nested = BinaryReader(memoryview(data))
                    while nested.offset < len(data):
                        _write_unknown_field(writer, nested, depth + 1)
            else:
                writer.scalar(name, _quote_bytes(data))
        case WireType.SGROUP:
            with writer.open_message(name):
                while True:
                    offset = reader.offset
                    if reader.tag().wire_type == WireType.EGROUP:
                        break
                    reader.seek(offset)
                    _write_unknown_field(writer, reader, depth + 1)
        case WireType.EGROUP:
            msg = "unexpected end group tag in unknown fields"
            raise ValueError(msg)
        case _:
            assert_never(tag.wire_type)


def _parses_as_message(data: bytes) -> bool:
    """Whether length-delimited bytes can be interpreted as a nested message.

    True if the bytes parse cleanly and completely as fields; otherwise the
    data is rendered as a quoted byte string.
    """
    if len(data) == 0:
        return False
    reader = BinaryReader(memoryview(data))
    try:
        while reader.offset < len(data):
            tag = reader.tag()
            if tag.wire_type == WireType.EGROUP:
                return False
            reader.skip(tag.wire_type, 0, field_number=tag.number)
    except (ValueError, EOFError, RecursionError):
        return False
    return reader.offset == len(data)


def _field_text_name(field: DescField) -> str:
    """The name a field is addressed by in the text format.

    A group-like (delimited) field uses its message type name, every other
    field its proto name.
    """
    group = group_like_message(field)
    return field.name if group is None else group.name


def group_like_message(field: DescField) -> DescMessage | None:
    """The message type of a field that is structured like a proto2 group, if any.

    A field is group-like when it is a delimited message field whose name is
    the lowercase of its message type name, declared in the same scope as that
    message. The text format addresses such fields by their message type name
    (e.g. `MyGroup`) rather than their field name. This is a faithful port of
    protobuf-go's isGroupLike (internal/filedesc/desc.go), so editions
    delimited fields are treated exactly like proto2 groups.
    """
    # Groups are always delimited-encoded message fields. Maps are excluded
    # automatically, because their encoding is never delimited.
    match field.value:
        case DescFieldValueMessage(message=message, delimited_encoding=True):
            pass
        case DescFieldValueList(
            element=DescMessage() as message, delimited_encoding=True
        ):
            pass
        case _:
            return None
    # Group fields are always named after the lowercase message type name.
    if message.name.lower() != field.name:
        return None
    # Groups can only be defined in the file they are used in.
    if message.file is not field.parent.file:
        return None
    # Group messages are always defined in the same scope as the field.
    return message if message.parent is field.parent else None


def _scalar_to_text(scalar_type: ScalarType, value: Any) -> str:
    match scalar_type:
        case ScalarType.STRING:
            return _quote_string(value)
        case ScalarType.BYTES:
            return _quote_bytes(value)
        case ScalarType.BOOL:
            return "true" if value else "false"
        case ScalarType.FLOAT:
            return _float32_to_text(value)
        case ScalarType.DOUBLE:
            return _float64_to_text(value)
        case _:
            # All integer types print as decimal with no prefix.
            return str(int(value))


def _enum_to_text(desc_enum: DescEnum, value: Any) -> str:
    # Emit the first-declared name for a value, so allow_alias enums match
    # protobuf-go (the by-number record can resolve to a non-first alias). An
    # unknown value prints as a decimal.
    number = int(value)
    for enum_value in desc_enum.values:
        if enum_value.number == number:
            return enum_value.name
    return str(number)


def _float64_to_text(value: float) -> str:
    if math.isnan(value):
        return "nan"
    if value == math.inf:
        return "inf"
    if value == -math.inf:
        return "-inf"
    if value == 0 and math.copysign(1, value) < 0:
        return "-0"
    # repr already yields the shortest decimal that round-trips to the same
    # 64-bit value; an integral value drops the redundant ".0".
    text = repr(value)
    return text.removesuffix(".0")


def _float32_to_text(value: float) -> str:
    # Round to 32-bit precision first so an overflow becomes inf and the value
    # is the true 32-bit value before we test it.
    n = fround(value)
    if math.isnan(n) or math.isinf(n) or n == 0:
        return _float64_to_text(n)
    # Find the shortest decimal that round-trips to the same float32, mirroring
    # strconv.AppendFloat(n, 'g', -1, 32) in protobuf-go.
    for precision in range(1, 10):
        candidate = float(format(n, f".{precision}g"))
        if fround(candidate) == n:
            return _float64_to_text(candidate)
    return _float64_to_text(n)


def fround(value: float) -> float:
    """Round a float to 32-bit precision, with out-of-range values becoming ±inf."""
    try:
        return struct.unpack("<f", struct.pack("<f", value))[0]
    except OverflowError:
        return math.inf if value > 0 else -math.inf


def _quote_string(value: str) -> str:
    """Quote and escape a string field value as a double-quoted text format literal.

    Uses the single escaping decision in _escape_code_point, so string fields,
    bytes fields, and unknown length-delimited rendering can never drift apart.
    Valid non-ASCII passes through as raw UTF-8; a lone surrogate (which cannot
    be encoded as UTF-8) is substituted with U+FFFD.
    """
    out = ['"']
    for ch in value:
        code = ord(ch)
        if 0xD800 <= code <= 0xDFFF:
            out.append("�")
        else:
            out.append(_escape_code_point(code) or ch)
    out.append('"')
    return "".join(out)


def _quote_bytes(value: bytes) -> str:
    r"""Quote and escape a bytes field value as a double-quoted text format literal.

    Valid UTF-8 runs are emitted with _escape_code_point (so they read
    identically to a string field); any byte that is not part of a valid UTF-8
    sequence is emitted as `\\xHH`, keeping the output round-tripping exactly.
    """
    out = ['"']
    pos = 0
    while pos < len(value):
        # Valid data takes a single pass; the loop repeats once per invalid byte.
        try:
            text = value[pos:].decode()
        except UnicodeDecodeError as e:  # noqa: PERF203
            # Emit the valid prefix, escape the first invalid byte individually,
            # and resume decoding right after it.
            if e.start > 0:
                _append_escaped(out, value[pos : pos + e.start].decode())
            out.append(f"\\x{value[pos + e.start]:02x}")
            pos += e.start + 1
        else:
            _append_escaped(out, text)
            break
    out.append('"')
    return "".join(out)


def _append_escaped(out: list[str], text: str) -> None:
    out.extend(_escape_code_point(ord(ch)) or ch for ch in text)


def _escape_code_point(code: int) -> str | None:
    r"""The single source of truth for escaping a code point in a text format string literal.

    Returns the escape sequence, or None when the code point may be emitted
    raw. Escapes the conventional sequences, all C0 controls and DEL as
    `\\xHH`, and the C1 controls (U+0080-U+009F) as `\\u00HH`.
    """
    match code:
        case 0x5C:
            return "\\\\"
        case 0x22:
            return '\\"'
        case 0x0A:
            return "\\n"
        case 0x0D:
            return "\\r"
        case 0x09:
            return "\\t"
    if code < 0x20 or code == 0x7F:
        return f"\\x{code:02x}"
    if 0x80 <= code <= 0x9F:
        return f"\\u{code:04x}"
    return None
