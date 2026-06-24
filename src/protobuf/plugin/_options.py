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

"""Dataclass option parser for protoc plugin parameters."""

from __future__ import annotations

import dataclasses
import enum
import types
import typing
from typing import TYPE_CHECKING, Any, TypeVar, get_type_hints

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

_Options = TypeVar("_Options", bound="DataclassInstance")


def parse_options(cls: type[_Options], parameter: str) -> tuple[_Options, str]:
    """Parse a comma-separated `key=value` parameter string into a dataclass.

    Args:
        cls: A dataclass type whose fields define the schema.
        parameter: The `CodeGeneratorRequest.parameter` string.

    Returns:
        A tuple of (instance of `cls`, unparsed parameter string). The
        unparsed string contains comma-separated tokens for keys that do
        not correspond to any field in `cls`.

    Raises:
        ValueError: On missing required fields, type coercion failures,
            or bare keys for non-bool fields.
    """
    # Resolve string annotations (from `from __future__ import annotations`)
    # into actual types. field.type is unreliable for this.
    hints = get_type_hints(cls)
    field_by_key = {f.metadata.get("name", f.name): f for f in dataclasses.fields(cls)}

    # Parse the raw parameter string into (key, value | None) pairs.
    # An empty string produces no pairs.
    raw_pairs: list[tuple[str, str | None]] = []
    if parameter:
        for token in parameter.split(","):
            if "=" in token:
                key, _, value = token.partition("=")
                raw_pairs.append((key.strip(), value))
            else:
                raw_pairs.append((token.strip(), None))

    # Separate known and unknown keys, preserving original tokens for
    # unknown keys.
    unknown_tokens: list[str] = []
    grouped: dict[str, list[str | None]] = {}
    for key, value in raw_pairs:
        if key not in field_by_key:
            unknown_tokens.append(key if value is None else f"{key}={value}")
        else:
            grouped.setdefault(key, []).append(value)

    # Build keyword arguments for the dataclass constructor.
    kwargs: dict[str, Any] = {}
    for key, field in field_by_key.items():
        hint = hints[field.name]
        entries = grouped.get(key, [])
        kwargs[field.name] = _parse_field(key, hint, entries, field)

    return cls(**kwargs), ",".join(unknown_tokens)


def _parse_field(
    name: str, hint: Any, entries: list[str | None], field: dataclasses.Field[Any]
) -> Any:
    origin = typing.get_origin(hint)

    if origin is list:
        return _parse_list(name, hint, entries)

    if origin is dict:
        return _parse_dict(name, hint, entries)

    # Scalar field — at most one entry expected.
    if not entries:
        if field.default is not dataclasses.MISSING:
            return field.default
        if field.default_factory is not dataclasses.MISSING:
            return field.default_factory()
        msg = f"missing required option '{name}'"
        raise ValueError(msg)

    if len(entries) > 1:
        msg = (
            f"option '{name}' specified {len(entries)} times but expects a single value"
        )
        raise ValueError(msg)

    return _parse_scalar(name, hint, entries[0])


def _parse_list(name: str, hint: Any, entries: list[str | None]) -> list[Any]:
    args = typing.get_args(hint)
    if not args:
        msg = f"list field '{name}' has no element type annotation"
        raise TypeError(msg)
    elem_type = args[0]
    _assert_primitive_element(name, elem_type)
    return [_parse_scalar(name, elem_type, raw_value) for raw_value in entries]


def _parse_dict(name: str, hint: Any, entries: list[str | None]) -> dict[str, Any]:
    args = typing.get_args(hint)
    if len(args) != 2:
        msg = f"dict field '{name}' has incomplete type annotation"
        raise TypeError(msg)
    key_type, val_type = args[0], args[1]
    if key_type is not str:
        msg = f"dict field '{name}' key type must be str, not {key_type}"
        raise TypeError(msg)
    _assert_primitive_element(name, val_type)

    result: dict[str, Any] = {}
    for raw_value in entries:
        if raw_value is None:
            msg = f"option '{name}' requires a value in the form '{name}=key:value'"
            raise ValueError(msg)
        if ":" not in raw_value:
            msg = f"option '{name}' value '{raw_value}' must contain ':' to separate key and value"
            raise ValueError(msg)
        key, _, val = raw_value.partition(":")
        if key in result:
            msg = f"option '{name}' has duplicate key '{key}'"
            raise ValueError(msg)
        result[key] = _parse_scalar(name, val_type, val)
    return result


def _parse_scalar(name: str, hint: Any, raw_value: str | None) -> Any:
    origin = typing.get_origin(hint)

    # Unwrap `X | None` to its inner type. Combined with a
    # `None` default this yields a tri-state option: unset, true, or false.
    if origin is typing.Union or origin is types.UnionType:
        inner = [arg for arg in typing.get_args(hint) if arg is not type(None)]
        if len(inner) == 1:
            return _parse_scalar(name, inner[0], raw_value)
        msg = f"option '{name}': unsupported union type {hint}"
        raise TypeError(msg)

    if hint is bool:
        if raw_value is None:
            # Bare key — treated as True.
            return True
        lower = raw_value.lower()
        if lower == "true":
            return True
        if lower == "false":
            return False
        msg = f"option '{name}': cannot parse '{raw_value}' as bool; use 'true' or 'false'"
        raise ValueError(msg)

    # All other types require an explicit value; a bare key is an error.
    if raw_value is None:
        msg = f"option '{name}' requires a value (bare key only valid for bool fields)"
        raise ValueError(msg)

    if hint is str:
        return raw_value

    if hint is int:
        try:
            return int(raw_value)
        except ValueError:
            msg = f"option '{name}': cannot parse '{raw_value}' as int"
            raise ValueError(msg) from None

    if hint is float:
        try:
            return float(raw_value)
        except ValueError:
            msg = f"option '{name}': cannot parse '{raw_value}' as float"
            raise ValueError(msg) from None

    if origin is typing.Literal:
        allowed = typing.get_args(hint)
        if raw_value not in allowed:
            msg = f"option '{name}': '{raw_value}' is not a valid value; allowed: {', '.join(repr(a) for a in allowed)}"
            raise ValueError(msg)
        return raw_value

    if isinstance(hint, type) and issubclass(hint, str) and issubclass(hint, enum.Enum):
        lower = raw_value.lower()
        for member in hint:
            if member.name.lower() == lower or str(member.value).lower() == lower:
                return member
        allowed = ", ".join(m.name for m in hint)
        msg = f"option '{name}': '{raw_value}' is not a valid {hint.__name__}; allowed: {allowed}"
        raise ValueError(msg)

    if isinstance(hint, type) and issubclass(hint, enum.IntEnum):
        # Try by name first (case-insensitive).
        lower = raw_value.lower()
        for member in hint:
            if member.name.lower() == lower:
                return member
        # Try by integer value.
        try:
            int_val = int(raw_value)
            return hint(int_val)
        except (ValueError, KeyError):
            pass
        allowed = ", ".join(m.name for m in hint)
        msg = f"option '{name}': '{raw_value}' is not a valid {hint.__name__}; allowed names: {allowed}"
        raise ValueError(msg)

    msg = f"option '{name}': unsupported field type {hint}"
    raise TypeError(msg)


def _assert_primitive_element(name: str, elem_type: Any) -> None:
    if elem_type not in (bool, str, int, float):
        msg = f"field '{name}' element type must be one of bool, str, int, or float; got {elem_type}"
        raise TypeError(msg)
