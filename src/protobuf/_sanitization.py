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

import hashlib
import re
from typing import Final

_INVALID_MODULE_COMPONENT_RE: Final[re.Pattern] = re.compile(r"[^a-zA-Z0-9_]")


def escape_proto_module_component(ident: str, *, escape_with_hash: bool = False) -> str:
    """Escape a single component of a dotted module path.

    Non-alphanumeric characters are replaced with underscores. Dots are replaced with
    two underscores to differentiate from the dot introduced by a module path.

    If replacing happens and conflicts aren't allowed, we append a hash suffix from the
    original name to prevent collision with files that have the same sanitized name.
    We assume collisions with the hash are too rare and do not try to escape the hash.

    The first character must not be a number and is prefixed with pb__ if it is.

    Python keywords and the reserved `_pb` suffix are escaped by appending an
    underscore.  Stripping trailing underscores before each check keeps the
    mapping injective. Leading underscore is prefixed by pb_.
    """
    component = _INVALID_MODULE_COMPONENT_RE.sub("_", ident)
    if component != ident and escape_with_hash:
        hash_suffix = hashlib.sha256(ident.encode()).hexdigest()[:8]
        component = f"{component}_{hash_suffix}"

    if component[0].isdigit():
        component = f"_{component}"
    component = escape_public_identifier(component, PYTHON_KEYWORDS)

    # The _pb suffix is reserved for generated proto modules (e.g. foo.proto -> foo_pb).
    # We must ensure the mapping is injective, so any component whose base already ends
    # with _pb gets an extra underscore, same as the keyword rule above.
    if component.rstrip("_").endswith("_pb"):
        return component + "_"

    return component


PYTHON_KEYWORDS: Final[frozenset[str]] = frozenset(
    {
        "False",
        "None",
        "True",
        "and",
        "as",
        "assert",
        "async",
        "await",
        "break",
        "class",
        "continue",
        "def",
        "del",
        "elif",
        "else",
        "except",
        "finally",
        "for",
        "from",
        "global",
        "if",
        "import",
        "in",
        "is",
        "lambda",
        "nonlocal",
        "not",
        "or",
        "pass",
        "raise",
        "return",
        "try",
        "while",
        "with",
        "yield",
    }
)

# These names are not allowed for class names and escaped. Because they can be message
# field names as well, the escaped form is reserved for message attributes but not the
# unescaped form to prevent overescaping.
_DISALLOWED_CLASS_NAMES: Final[frozenset[str]] = frozenset(
    {"int", "str", "bytes", "float", "bool", "list", "dict"}
)

_RESERVED_MESSAGE_ATTRS: Final[frozenset[str]] = frozenset(
    {
        "has_field",
        "clear_field",
        "to_binary",
        "to_json",
        "from_binary",
        "from_json",
        "desc",
        "self",
    }
    | PYTHON_KEYWORDS
)
_RESERVED_ENUM_ATTRS: Final[frozenset[str]] = frozenset(
    {"name", "value", "mro", "desc"} | PYTHON_KEYWORDS
)

_RESERVED_CLASS_NAMES: Final[frozenset[str]] = frozenset(
    _DISALLOWED_CLASS_NAMES | PYTHON_KEYWORDS | _RESERVED_MESSAGE_ATTRS
)


def escape_public_identifier(ident: str, reserved: frozenset[str]) -> str:
    """Escapes an identifier such as a class or attribute name.

    We escape for two points:

      - Reserved words which can cause conflicts with other code. We suffix with `_`.
        Identifiers that are already a reserved word with `_` suffixes also get an extra
        `_` to ensure the mapping is injective.
      - Starting with `_` which can cause visibility issues, especially if it results in
        name mangling from double underscores. We prefix with `pb_`. Identifiers that already
        start with `pb_` are also prefixed with `pb_` to ensure the mapping is injective.
    """
    if ident.rstrip("_") in reserved:
        ident = ident + "_"
    if ident.startswith(("_", "pb_")):
        ident = f"pb_{ident}"
    return ident


def escape_message_attr(attr: str) -> str:
    """Escape a message attribute name.

    Examples:
        >>> escape_message_attr("to_json")
        'to_json_'
        >>> escape_message_attr("_private")
        'pb__private'
        >>> escape_message_attr("field")
        'field'
    """
    name = escape_public_identifier(attr, _RESERVED_MESSAGE_ATTRS)

    # Only escape a suffixed value that collides with a reserved class name.
    if name.endswith("_") and name.rstrip("_") in _DISALLOWED_CLASS_NAMES:
        return name + "_"

    # Prevent collisions with extensions
    if name.startswith("ext_"):
        return f"pb_{name}"

    return name


def escape_enum_attr(attr: str) -> str:
    """Escape an enum attribute name.

    Examples:
        >>> escape_enum_attr("name")
        'name_'
        >>> escape_enum_attr("_private")
        'pb__private'
        >>> escape_enum_attr("VALUE")
        'VALUE'
    """
    return escape_public_identifier(attr, _RESERVED_ENUM_ATTRS)


def escape_class_name(name: str) -> str:
    """Escape a message or enum class name.

    These can be either at the top level or nested in messages. So we escape against
    top-level identifiers we use for other generated code as well as message attributes.

    Examples:
        >>> escape_class_name("MyMessage")
        'MyMessage'
        >>> escape_class_name("int")
        'int_'
        >>> escape_class_name("ext_Foo")
        'pb_ext_Foo'
    """
    name = escape_public_identifier(name, _RESERVED_CLASS_NAMES)

    # Prevent collisions with extensions
    if name.startswith("ext_"):
        return f"pb_{name}"

    return name


def escape_extension_name(name: str) -> str:
    # Prefixing with ext_ automatically passes all of our sanitization requirements.
    return f"ext_{name}"


def escape_identifier(ident: str) -> str:
    """Escape an arbitrary identifier.

    For use when creating valid Python code without other restrictions such as shadowing.

    Examples:
        >>> escape_identifier("yield")
        'yield_'
        >>> escape_identifier("_hidden")
        '_hidden'
        >>> escape_identifier("normal")
        'normal'
    """
    if ident.rstrip("_") in PYTHON_KEYWORDS:
        return ident + "_"
    return ident
