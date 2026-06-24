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
"""Enforce that error messages start with a lowercase letter.

See: https://github.com/bufbuild/protobuf-py/issues/498
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import TypeAlias

_REPO_ROOT = Path(__file__).parent.parent
_SOURCE_DIRS = (_REPO_ROOT / "src", _REPO_ROOT / "packages")

# Maps variable name -> [(lineno, value_node)] for all simple string assignments.
# Used to resolve the message string when raise uses a variable: msg = "..."; raise Error(msg)
_StrAssignments: TypeAlias = dict[str, list[tuple[int, ast.expr]]]


def _first_str_char(node: ast.expr) -> str | None:
    """Return the first character of a string literal or f-string, or None."""
    match node:
        case ast.Constant(value=str(s)) if s:
            return s[0]
        case ast.JoinedStr(values=[ast.Constant(value=str(s)), *_]) if s:
            # f-strings starting with a variable expression (e.g. f"{var}: ...")
            # have a FormattedValue as their first value, not a Constant, so they
            # fall through and return None — we can't inspect runtime values statically.
            return s[0]
    return None


def _collect_str_assignments(tree: ast.AST) -> _StrAssignments:
    """Collect string assignments for resolving variable-based error messages."""
    result: _StrAssignments = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        if _first_str_char(node.value) is not None:
            result.setdefault(node.targets[0].id, []).append((node.lineno, node.value))
    return result


def _check_msg_arg(
    arg: ast.expr, usage_lineno: int, assignments: _StrAssignments
) -> tuple[int, str] | None:
    """Return (lineno, repr) if the message starts with uppercase, else None."""
    if isinstance(arg, ast.Name):
        # Resolve the variable to its most recent string assignment before this
        # raise — the same name may be reused with different values in one scope.
        before = [t for t in assignments.get(arg.id, []) if t[0] < usage_lineno]
        if before:
            ln, value_node = max(before, key=lambda t: t[0])
            ch = _first_str_char(value_node)
            if ch and ch.isupper():
                return ln, ast.unparse(value_node)
        return None
    ch = _first_str_char(arg)
    if ch and ch.isupper():
        return usage_lineno, ast.unparse(arg)
    return None


def _check_file(path: Path) -> list[tuple[int, str]]:
    """Return (lineno, repr) for error messages starting with uppercase."""
    source = path.read_text(encoding="utf-8")
    if "DO NOT EDIT" in source:
        return []

    tree = ast.parse(source)
    assignments = _collect_str_assignments(tree)

    violations: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Raise)
            and isinstance(node.exc, ast.Call)
            and node.exc.args
        ):
            if result := _check_msg_arg(node.exc.args[0], node.lineno, assignments):
                violations.append(result)
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "_assert"  # raise-wrapper used in _file_registry.py
            and len(node.args) >= 2
            and (result := _check_msg_arg(node.args[1], node.lineno, assignments))
        ):
            violations.append(result)

    return violations


def test_error_messages_start_with_lowercase() -> None:
    """Error messages passed to exceptions must start with a lowercase letter."""
    failures: list[str] = []
    for source_dir in _SOURCE_DIRS:
        for path in sorted(source_dir.rglob("*.py")):
            rel = path.relative_to(_REPO_ROOT)
            for lineno, snippet in _check_file(path):
                failures.append(f"  {rel}:{lineno}: {snippet}")

    assert not failures, "error messages must start with lowercase:\n" + "\n".join(
        failures
    )
