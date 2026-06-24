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
"""License header generation, detection, and modification."""

from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class CommentStyle:
    """Comment style for a file type."""

    prefix: str  # e.g. "# ", "## ", "// "
    blank: str  # e.g. "#", "##", "//"
    wrap: bool  # whether to add blank-prefix lines before/after body


HASH = CommentStyle(prefix="# ", blank="#", wrap=False)
DOUBLE_HASH = CommentStyle(prefix="## ", blank="##", wrap=False)
DOUBLE_SLASH = CommentStyle(prefix="// ", blank="//", wrap=False)

STYLES: dict[str, CommentStyle] = {
    ".py": HASH,
    ".pyi": HASH,
    ".sh": DOUBLE_HASH,
    ".go": DOUBLE_SLASH,
    ".proto": DOUBLE_SLASH,
}

_APACHE_2_0_TEMPLATE = """\
Copyright (c) {year_range} {copyright_holder}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""


def make_header(copyright_holder: str, year_range: str, style: CommentStyle) -> str:
    """Generate a formatted license header comment block."""
    body = _APACHE_2_0_TEMPLATE.format(
        year_range=year_range, copyright_holder=copyright_holder
    )
    lines: list[str] = []
    if style.wrap:
        lines.append(style.blank)
    for line in body.splitlines():
        if line:
            lines.append(f"{style.prefix}{line}")
        else:
            lines.append(style.blank)
    if style.wrap:
        lines.append(style.blank)
    return "\n".join(lines) + "\n"


def modify(content: str, header: str, style: CommentStyle) -> str:
    """Add or replace the license header in file content.

    Returns the modified content. If the header is already correct,
    returns the original content unchanged.
    """
    if not content:
        return header

    lines = content.splitlines(keepends=True)
    skip_until = _count_skip_lines(lines)
    start, end = _find_existing_header(lines, skip_until, style)

    if start >= 0:
        existing = "".join(lines[start:end])
        if existing == header:
            return content
        return "".join(lines[:start]) + header + "".join(lines[end:])

    prefix = "".join(lines[:skip_until])
    rest = "".join(lines[skip_until:])
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    # Ensure a blank line between the header and adjacent comment lines
    # so they aren't detected as a single block on re-runs.
    if rest and _is_comment_line(rest.splitlines()[0] + "\n", style):
        header += "\n"
    return prefix + header + rest


def _count_skip_lines(lines: list[str]) -> int:
    """Count lines to preserve at the top (shebang, encoding)."""
    idx = 0
    if idx < len(lines) and lines[idx].startswith("#!"):
        idx += 1
    if idx < len(lines) and _is_encoding_line(lines[idx]):
        idx += 1
    return idx


def _is_encoding_line(line: str) -> bool:
    """Check if a line is a PEP 263 encoding declaration."""
    stripped = line.strip()
    return stripped.startswith(("# -*- coding:", "# coding:"))


def _find_existing_header(
    lines: list[str], start_from: int, style: CommentStyle
) -> tuple[int, int]:
    """Find the bounds of an existing license header comment block.

    Returns (start, end) indices where lines[start:end] is the header.
    Returns (-1, -1) if no header is found.

    The header block is a contiguous run of comment lines (no blank lines)
    that contains "copyright". A blank line between the license header and
    subsequent comments (e.g. "# DO NOT EDIT") acts as the delimiter.
    """
    n = len(lines)
    idx = start_from

    while idx < n and lines[idx].strip() == "":
        idx += 1

    if idx >= n or not _is_comment_line(lines[idx], style):
        return (-1, -1)

    block_start = idx
    has_copyright = False

    while idx < n and _is_comment_line(lines[idx], style):
        if "copyright" in lines[idx].lower():
            has_copyright = True
        idx += 1

    if not has_copyright:
        return (-1, -1)

    return (block_start, idx)


def _is_comment_line(line: str, style: CommentStyle) -> bool:
    """Check if a line is a comment in the given style."""
    stripped = line.strip()
    return stripped == style.blank or stripped.startswith(style.prefix)
