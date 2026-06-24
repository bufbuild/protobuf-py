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

import re

from protobuf._descriptors import DescEnum, ScalarType
from protobuf._typing import assert_never


def parse_text_format_enum_value(desc: DescEnum, value: str) -> int:
    """Parse an enum value from the Protobuf text format."""
    value_desc = next((v for v in desc.values if v.name == value), None)
    if value_desc is None:
        msg = f"cannot parse {desc} default value: {value}"
        raise ValueError(msg)
    return value_desc.number


def parse_text_format_scalar_value(  # noqa: RET503
    scalar: ScalarType, value: str
) -> int | float | bytes | str | bool:
    """Parse a scalar value from the Protobuf text format."""
    match scalar:
        case ScalarType.BOOL:
            return value == "true"
        case (
            ScalarType.INT32
            | ScalarType.UINT32
            | ScalarType.INT64
            | ScalarType.UINT64
            | ScalarType.SINT32
            | ScalarType.SINT64
            | ScalarType.FIXED32
            | ScalarType.FIXED64
            | ScalarType.SFIXED32
            | ScalarType.SFIXED64
        ):
            return int(value)
        case ScalarType.FLOAT | ScalarType.DOUBLE:
            return float(value)  # Convers inf, -inf, and nan
        case ScalarType.STRING:
            return value
        case ScalarType.BYTES:
            return _c_unescape(value)
        case _:
            assert_never(scalar)


_CUNESCAPE_HEX = re.compile(r"(\\+)x([0-9a-fA-F])(?![0-9a-fA-F])")
_CUNESCAPE_OCTAL = re.compile(r"(\\+)([0-7]{1,3})(?![0-7])")


# Copied from https://github.com/protocolbuffers/protobuf/blob/eedd2068760c946996f3095286492afc0460695a/python/google/protobuf/text_encoding.py#L77
def _c_unescape(text: str) -> bytes:
    """Unescape a text string with C-style escape sequences to UTF-8 bytes.

    Args:
      text: The data to parse in a str.

    Returns:
      A byte string.
    """

    def replace_hex(m: re.Match[str]) -> str:
        # Only replace the match if the number of leading back slashes is odd. i.e.
        # the slash itself is not escaped.
        if len(m.group(1)) & 1:
            return m.group(1) + "x0" + m.group(2)
        return m.group(0)

    def replace_octal(m: re.Match[str]) -> str:
        if len(m.group(1)) & 1:
            return f"{m.group(1)}x{int(m.group(2), 8):02x}"
        return m.group(0)

    # This is required because the 'string_escape' encoding doesn't
    # allow single-digit hex escapes (like '\xf').
    result = _CUNESCAPE_HEX.sub(replace_hex, text)
    # Pre-convert octal escapes to hex to workaround issue on PyPy with octal escapes
    result = _CUNESCAPE_OCTAL.sub(replace_octal, result)

    # Replaces Unicode escape sequences with their character equivalents.
    result = result.encode("raw_unicode_escape").decode("raw_unicode_escape")
    # Encode Unicode characters as UTF-8, then decode to Latin-1 escaping
    # unprintable characters.
    result = result.encode("utf-8").decode("unicode_escape")
    # Convert Latin-1 text back to a byte string (latin-1 codec also works here).
    return result.encode("latin-1")
