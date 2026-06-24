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
"""Translate the fleetbench C++ proto benchmark harness to Python.

The fleetbench `access_message*.cc`/`lifecycle.cc` sources are C++ code
auto-generated from production workloads, which mean they themselves have a
simple, machine-generated structure. We take advantage of this to translate
to Python with string smashing rather than manual translation or using
an AST parser.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

OUT_ROOT = Path(__file__).parent.parent / "src" / "bench" / "fleetbench"
IMPLS = ("google", "protobuf")
PROTO_PACKAGE = "fleetbench.proto"

LICENSE = """\
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
"""

HEADER = (
    LICENSE
    + """
# Generated from fleetbench {cc} by _fleetbench.py. DO NOT EDIT.
#
# Derived from github.com/google/fleetbench
# Copyright 2025 The Fleetbench Authors
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: F841
# pyright: reportUnusedExpression=false
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bench.gen.fleetbench.{module} import {top}
"""
)


_PROTO_FIELD_RE = re.compile(
    r"^\s*(?:optional|repeated|required)\s+(\S+)\s+(f_\d+)\s*=\s*\d+"
)
_PROTO_MESSAGE_RE = re.compile(r"^\s*message\s+(\w+)\s*\{")
_PROTO_ENUM_RE = re.compile(r"^\s*enum\s+(\w+)\s*\{")


# We find all the bytes fields in a proto since unlike the original C++,
# we cannot assign a string field to them. While it would be possible to
# use gencode descriptors for this, it's simple enough to stick to the
# string smashing we use throughout the file.
def parse_bytes_fields(proto: Path) -> set[tuple[str, str]]:
    bytes_fields: set[tuple[str, str]] = set()
    stack: list[str] = []  # message-name frames only
    kinds: list[str] = []  # "msg" or "enum" for every brace frame
    for line in proto.read_text().splitlines():
        if m := _PROTO_MESSAGE_RE.match(line):
            stack.append(m.group(1))
            kinds.append("msg")
            continue
        if _PROTO_ENUM_RE.match(line):
            kinds.append("enum")
            continue
        if "}" in line and kinds:
            if kinds.pop() == "msg":
                stack.pop()
            continue
        if (m := _PROTO_FIELD_RE.match(line)) and m.group(1) == "bytes":
            bytes_fields.add((".".join(stack), m.group(2)))
    return bytes_fields


_SUBSTR_RE = re.compile(r"^s->substr\(0,\s*(\d+)\)$")
_ENUM_MEMBER_RE = re.compile(r"^(E\d+)_(.+)$")


@dataclass
class UsedTypes:
    """Type paths (dotted, package-less) referenced by translated code.

    Message classes and enum classes must be resolved at runtime from a
    registry / symbol database (the classes differ per backend), so every
    referenced type becomes an attribute wired in ``Access.__init__``.
    """

    messages: set[str] = field(default_factory=set)
    enums: set[str] = field(default_factory=set)

    def update(self, other: UsedTypes) -> None:
        self.messages |= other.messages
        self.enums |= other.enums

    def all_dotted(self) -> list[str]:
        return sorted(self.messages | self.enums, key=_flat)

    def all_flat(self) -> list[str]:
        return [_flat(t) for t in self.all_dotted()]


def _flat(dotted: str) -> str:
    """Dotted type path -> flat attribute name (Message0.M1.E2 -> Message0_M1_E2)."""
    return dotted.replace(".", "_")


def translate_enum(token: str, impl: str, used: UsedTypes) -> str:
    """`A::B::E2_CONST_1` -> google `A_B.E2_CONST_1`, buf `A_B_E2.CONST_1`.

    Google enum constants are attributes of the containing message class;
    Buf enum members are attributes of the enum class. Either way the class
    is referenced through its flat local name and recorded in `used`.
    """
    parts = token.split("::")
    container = ".".join(parts[:-1])
    m = _ENUM_MEMBER_RE.match(parts[-1])
    assert m, f"unexpected enum constant {token!r}"
    if impl == "protobuf":
        enum_path = f"{container}.{m.group(1)}"
        used.enums.add(enum_path)
        return f"{_flat(enum_path)}.{m.group(2)}"
    used.messages.add(container)
    return f"{_flat(container)}.{parts[-1]}"


def translate_value(val: str, *, is_bytes: bool, impl: str, used: UsedTypes) -> str:
    val = val.strip()
    if val == "true":
        return "True"
    if val == "false":
        return "False"
    if m := _SUBSTR_RE.match(val):
        n = m.group(1)
        return f"b[0:{n}]" if is_bytes else f"s[0:{n}]"
    if "::" in val:
        return translate_enum(val, impl, used)
    return val  # hex / int / float literal, valid as-is in Python


@dataclass
class Func:
    name: str  # e.g. Message0_Set_1
    kind: str  # "Set" or "Get"
    body: list[str]  # raw C++ body lines (between the braces)


_FUNC_START = re.compile(r"^void (Message\d+_(Set|Get)_\d+)\(")
_LINE_COMMENT_RE = re.compile(r"\s*//.*$")
_SCOPE_RE = re.compile(r"\s*::\s*")


def logical_lines(body: list[str]) -> list[str]:
    """Join clang-wrapped physical lines into whole statements.

    A statement is complete when a physical line ends with `;`, `{`, or `}`
    (block delimiters and array-literal terminators). Continuations (a line
    ending in `=`, `(`, `,`, an operand, ...) are joined with a single space.
    """
    out: list[str] = []
    buf = ""
    for raw in body:
        line = _LINE_COMMENT_RE.sub("", raw).strip()  # drop trailing line comments
        if not line:
            continue
        buf = line if not buf else f"{buf} {line}"
        if line.endswith((";", "{", "}")):
            # Long C++ type paths wrap only at `::`; drop any space the join
            # introduced around a scope-resolution operator.
            out.append(_SCOPE_RE.sub("::", buf))
            buf = ""
    if buf:
        out.append(buf)
    return out


def extract_funcs(cc: Path) -> list[Func]:
    funcs: list[Func] = []
    lines = cc.read_text().splitlines()
    i = 0
    while i < len(lines):
        if m := _FUNC_START.match(lines[i]):
            name, kind = m.group(1), m.group(2)
            body: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("}"):
                body.append(lines[i])
                i += 1
            funcs.append(Func(name=name, kind=kind, body=body))
        i += 1
    return funcs


_DECL_RE = re.compile(
    r"^(?P<type>[\w:]+)\*\s*(?P<var>\w+)\s*=\s*"
    r"(?P<recv>\w+)->(?P<method>add|mutable)_(?P<field>f_\d+)\(\);$"
)
_SET_RE = re.compile(r"^(?P<recv>\w+)->set_(?P<field>f_\d+)\((?P<val>.*)\);$")
_ADD_RE = re.compile(r"^(?P<recv>\w+)->add_(?P<field>f_\d+)\((?P<val>.*)\);$")
_ARRAY_START = re.compile(r"^[\w:]+\s+(?P<name>array_\d+)\[\d*\]\s*=\s*\{(?P<rest>.*)$")
_FOR_ARRAY = re.compile(r"^for \(auto v : (?P<name>array_\d+)\) \{$")
_FOR_COUNT = re.compile(r"^for \(size_t i = 0; i < \d+; \+\+i\) \{$")
_COUNT_BODY = re.compile(
    r"^(?P<recv>\w+)->add_(?P<field>f_\d+)\(s->substr\(0, (?P<arr>array_\d+)\[i\]\)\);$"
)
_VOID = re.compile(r"^\(void\)(?P<var>\w+);")


@dataclass
class _SetState:
    var2type: dict[str, str]
    arrays: dict[str, list[str]] = field(default_factory=dict)
    cur_array: str = ""  # array name currently being collected
    # ("bulk", array_name) or ("count", "") while inside a for-loop, else None.
    loop: tuple[str, str] | None = None


def _cls(cpp_type: str) -> str:
    """C++ type path -> Python class path (Message0::M1 -> Message0.M1)."""
    return cpp_type.replace("::", ".")


def translate_set(
    func: Func,
    top: str,
    bytes_fields: set[tuple[str, str]],
    impl: str,
    used: UsedTypes,
) -> list[str]:
    st = _SetState(var2type={"message": top})
    out: list[str] = []

    def is_bytes(recv: str, fieldname: str) -> bool:
        # Both var2type paths and bytes_fields keys include the top message
        # component (e.g. "Message1.M2.M4"), so they compare directly.
        return (st.var2type.get(recv, top), fieldname) in bytes_fields

    pending_decl: list[str] = []
    lines = logical_lines(func.body)
    # A `(void)v;` line marks a mutable submessage that never has a field set on
    # it. Those are the only ones google needs SetInParent for (see below).
    void_vars = {m.group("var") for line in lines if (m := _VOID.match(line))}
    for line in lines:
        if _VOID.match(line):
            continue

        # Multi-line C array literal: collect until the closing `};`.
        if pending_decl:
            pending_decl.append(line)
        elif m := _ARRAY_START.match(line):
            st.cur_array = m.group("name")
            pending_decl = [m.group("rest")]
        if pending_decl:
            if "}" in pending_decl[-1]:
                blob = " ".join(pending_decl)
                blob = blob[: blob.rindex("}")]
                st.arrays[st.cur_array] = [
                    v.strip() for v in blob.split(",") if v.strip()
                ]
                pending_decl = []
            continue

        if m := _FOR_ARRAY.match(line):
            st.loop = ("bulk", m.group("name"))
            continue
        if _FOR_COUNT.match(line):
            st.loop = ("count", "")
            continue

        if st.loop is not None:
            if line == "}":
                st.loop = None
                continue
            kind, arr = st.loop
            if kind == "bulk":
                m = _ADD_RE.match(line)
                assert m and m.group("val") == "v", f"bad bulk body: {line}"
                recv, fld = m.group("recv"), m.group("field")
                elems = [
                    translate_value(v, is_bytes=False, impl=impl, used=used)
                    for v in st.arrays[arr]
                ]
                out.append(f"    {recv}.{fld}.extend([{', '.join(elems)}])")
            else:  # count loop appending variable-length substrings
                m = _COUNT_BODY.match(line)
                assert m, f"bad count body: {line}"
                recv, fld = m.group("recv"), m.group("field")
                lengths = ", ".join(st.arrays[m.group("arr")])
                src = "b" if is_bytes(recv, fld) else "s"
                out.append(f"    for n in [{lengths}]:")
                out.append(f"        {recv}.{fld}.append({src}[0:n])")
            continue

        if m := _DECL_RE.match(line):
            var, recv = m.group("var"), m.group("recv")
            fld, method = m.group("field"), m.group("method")
            st.var2type[var] = _cls(m.group("type"))
            cls = st.var2type[var]
            if method == "mutable":
                if impl == "google":
                    out.append(f"    {var} = {recv}.{fld}")
                    # Only an empty submessage needs explicit presence. If a
                    # field is later set on `var` (or any descendant), that
                    # marks the whole chain present for free.
                    if var in void_vars:
                        out.append(f"    {var}.SetInParent()")
                else:
                    used.messages.add(cls)
                    out.append(f"    {var} = {_flat(cls)}()")
                    out.append(f"    {recv}.{fld} = {var}")
            else:  # repeated message add
                if impl == "google":
                    out.append(f"    {var} = {recv}.{fld}.add()")
                else:
                    used.messages.add(cls)
                    out.append(f"    {var} = {_flat(cls)}()")
                    out.append(f"    {recv}.{fld}.append({var})")
            continue

        if m := _SET_RE.match(line):
            recv, fld, val = m.group("recv"), m.group("field"), m.group("val")
            py = translate_value(
                val, is_bytes=is_bytes(recv, fld), impl=impl, used=used
            )
            out.append(f"    {recv}.{fld} = {py}")
            continue

        if m := _ADD_RE.match(line):
            recv, fld, val = m.group("recv"), m.group("field"), m.group("val")
            py = translate_value(
                val, is_bytes=is_bytes(recv, fld), impl=impl, used=used
            )
            out.append(f"    {recv}.{fld}.append({py})")
            continue

        raise AssertionError(f"unhandled Set line in {func.name}: {line!r}")

    return out or ["    pass"]


_FOR_EACH = re.compile(r"^for \(const auto& (?P<var>\w+) : (?P<expr>.+)\) \{$")
_BIND = re.compile(r"^const (?P<type>[\w:]+)& (?P<var>\w+) = (?P<expr>.+);$")
_RECEIVE = re.compile(r"^Receive\((?P<expr>.+)\);$")
_FOR_SIZE = re.compile(r"^for \(int i = 0; i < (?P<expr>.+)_size\(\); \+\+i\) \{$")
_GET_INDEXED_RE = re.compile(r"\.(f_\d+)\(i\)")
_GET_CALL_RE = re.compile(r"\.(f_\d+)\(\)")


def _get_expr(expr: str) -> str:
    expr = expr.replace("(*message)", "message")
    expr = _GET_INDEXED_RE.sub(r".\1[i]", expr)
    expr = _GET_CALL_RE.sub(r".\1", expr)
    return expr


def translate_get(func: Func, impl: str, used: UsedTypes) -> list[str]:
    out: list[str] = []
    depth = 1
    for line in logical_lines(func.body):
        if line == "}":
            depth -= 1
            continue
        indent = "    " * depth
        if m := _FOR_EACH.match(line):
            out.append(f"{indent}for {m.group('var')} in {_get_expr(m.group('expr'))}:")
            depth += 1
        elif m := _FOR_SIZE.match(line):
            out.append(f"{indent}for i in range(len({_get_expr(m.group('expr'))})):")
            depth += 1
        elif m := _BIND.match(line):
            expr = _get_expr(m.group("expr"))
            # C++ reads an unset singular message as a read-only default. The
            # google API matches that; the Buf API returns None, so substitute
            # a default instance to keep the read-only traversal total.
            if impl == "protobuf":
                cls = _cls(m.group("type"))
                used.messages.add(cls)
                expr = f"{expr} or {_flat(cls)}()"
            out.append(f"{indent}{m.group('var')} = {expr}")
        elif m := _RECEIVE.match(line):
            # C++ `Receive(x)` defeats dead-code elimination; in Python the
            # bare field access is the read we want to measure, with no
            # extra call-frame overhead to add noise.
            out.append(f"{indent}{_get_expr(m.group('expr'))}")
        else:
            raise AssertionError(f"unhandled Get line in {func.name}: {line!r}")
    return out or ["    pass"]


def py_name(cpp_name: str) -> str:
    """Message0_Set_1 -> message0_set_1."""
    return cpp_name.lower()


def generate_access(msg_id: int, impl: str, src: Path) -> tuple[str, UsedTypes]:
    cc = src / f"access_message{msg_id}.cc"
    top = f"Message{msg_id}"
    module = f"{top}_pb" if impl == "protobuf" else f"{top}_pb2"
    bytes_fields = parse_bytes_fields(src / f"{top}.proto")
    funcs = extract_funcs(cc)

    methods: list[str] = []
    file_used = UsedTypes()
    for f in funcs:
        used = UsedTypes()
        name = py_name(f.name)
        if f.kind == "Set":
            lines = translate_set(f, top, bytes_fields, impl, used)
            sig = f"def {name}(self, message: {top}, s: str, b: bytes) -> None:"
        else:
            lines = translate_get(f, impl, used)
            sig = f"def {name}(self, message: {top}) -> None:"
        # Bind each backend-wired class used by this method to a local once,
        # so the body pays one attribute lookup per type rather than per use.
        prelude = [f"    {n} = self.{n}" for n in used.all_flat()]
        body = "\n".join("    " + ln for ln in (*prelude, *lines))
        methods.append(f"\n\n    {sig}\n{body}")
        file_used.update(used)

    chunks = [HEADER.format(cc=cc.name, module=module, top=top)]
    chunks.append(f"\n\nclass {top}Access:")
    if dotted := file_used.all_dotted():
        chunks.append("\n    if TYPE_CHECKING:")
        chunks.append("\n        # Provided by the Access subclass, which wires the")
        chunks.append(
            "\n        # backend's classes; never assigned on the mixin itself."
        )
        chunks.extend(f"\n        {_flat(t)}: type[{t}]" for t in dotted)
    chunks.extend(methods)
    return "".join(chunks) + "\n", file_used


_INIT_HELPERS = """


def _message_type(registry: Registry, name: str) -> Any:
    desc = registry.message(name)
    if desc is None:
        msg = f"message {name} not found in registry"
        raise ValueError(msg)
    return desc.type


def _enum_type(registry: Registry, name: str) -> Any:
    desc = registry.enum(name)
    if desc is None:
        msg = f"enum {name} not found in registry"
        raise ValueError(msg)
    return desc.type
"""


def generate_init(impl: str, num_messages: int, used: UsedTypes) -> str:
    messages = sorted(used.messages | {f"Message{k}" for k in range(num_messages)})
    enums = sorted(used.enums)
    lines = [
        LICENSE.rstrip("\n"),
        "",
        "# Generated by _fleetbench.py. DO NOT EDIT.",
        "from __future__ import annotations",
        "",
        "from typing import TYPE_CHECKING, Any"
        if impl == "protobuf"
        else "from typing import Any",
        "",
        f"from bench.fleetbench.{impl}.receiver import Ops",
    ]
    lines.extend(
        f"from bench.fleetbench.{impl}.access_message{i} import Message{i}Access"
        for i in range(num_messages)
    )
    if impl == "protobuf":
        lines += ["", "if TYPE_CHECKING:", "    from protobuf import Registry"]
        lines.append(_INIT_HELPERS.rstrip("\n"))
    bases = ", ".join(["Ops", *(f"Message{i}Access" for i in range(num_messages))])
    lines += [
        "",
        "",
        f"class Access({bases}):",
        '    """Message classes and operations, resolved per backend.',
        "",
        "    The message types are wired as attributes so the same access code",
        "    runs against whichever backend produced them.",
        '    """',
        "",
    ]
    if impl == "protobuf":
        lines.append("    def __init__(self, registry: Registry) -> None:")
        lines.extend(
            f'        self.{_flat(name)} = _message_type(registry, "{PROTO_PACKAGE}.{name}")'
            for name in messages
        )
        lines.extend(
            f'        self.{_flat(name)} = _enum_type(registry, "{PROTO_PACKAGE}.{name}")'
            for name in enums
        )
    else:
        lines.append("    def __init__(self, symbol_database: Any) -> None:")
        lines.append("        get_symbol = symbol_database.GetSymbol")
        lines.extend(
            f'        self.{_flat(name)} = get_symbol("{PROTO_PACKAGE}.{name}")'
            for name in messages
        )
    lines += ["", "", '__all__ = ["Access"]', ""]
    return "\n".join(lines)


_RUN_SLOT_RE = re.compile(r"message(\d+)_")


def _run_expr(e: str) -> str:
    """Translate a Run-body operand: messageK_.x[i] -> m[K].x[i], drop `&`."""
    return _RUN_SLOT_RE.sub(r"m[\1]", e.strip().lstrip("&"))


_SLOT = r"message(\d+)_\.(message|other_message)\[i\]"

_RUN_RULES: list[tuple[re.Pattern[str], object]] = [
    # Construct a fresh message (C++ arena reallocation, and Create below). The
    # idiomatic Python equivalent is simply calling the message constructor.
    (
        re.compile(
            rf"^{_SLOT} = google::protobuf::Arena::Create<Message\d+>\(arena_\);$"
        ),
        lambda m: f"m[{m.group(1)}].{m.group(2)}[i] = a.Message{m.group(1)}()",
    ),
    (
        # C++ `Create` does `*message = M()` to reuse an arena slot. Real user
        # code just constructs a new message, so we do the same.
        re.compile(rf"^Create\({_SLOT}\);$"),
        lambda m: f"m[{m.group(1)}].{m.group(2)}[i] = a.Message{m.group(1)}()",
    ),
    (
        re.compile(r"^Message(\d+)_Set_(\d+)\((?P<x>.+), &s_\);$"),
        lambda m: (
            f"a.message{m.group(1)}_set_{m.group(2)}({_run_expr(m.group('x'))}, s, b)"
        ),
    ),
    (
        re.compile(r"^Message(\d+)_Get_(\d+)\((?P<x>.+)\);$"),
        lambda m: f"a.message{m.group(1)}_get_{m.group(2)}({_run_expr(m.group('x'))})",
    ),
    (
        re.compile(r"^Serialize\((?P<m>.+), (?P<s>&.+)\);$"),
        lambda m: f"{_run_expr(m.group('s'))} = a.serialize({_run_expr(m.group('m'))})",
    ),
    (
        # Parse into a freshly constructed message, the idiomatic Python form.
        re.compile(rf"^Deserialize\({_SLOT}, (?P<s>&.+)\);$"),
        lambda m: (
            f"m[{m.group(1)}].{m.group(2)}[i] = "
            f"a.parse(a.Message{m.group(1)}, {_run_expr(m.group('s'))})"
        ),
    ),
    (
        re.compile(r"^Merge\((?P<a>.+), (?P<b>.+)\);$"),
        lambda m: f"a.merge({_run_expr(m.group('a'))}, {_run_expr(m.group('b'))})",
    ),
    (
        # C++ CopyFrom; the idiomatic Python deep copy is copy.deepcopy.
        re.compile(r"^Copy\((?P<a>.+), (?P<b>.+)\);$"),
        lambda m: f"{_run_expr(m.group('a'))} = deepcopy({_run_expr(m.group('b'))})",
    ),
    (
        # C++ Swap exchanges contents in O(1); the idiomatic Python equivalent
        # is swapping the two references.
        re.compile(r"^Swap\((?P<a>.+), (?P<b>.+)\);$"),
        lambda m: (
            f"{_run_expr(m.group('a'))}, {_run_expr(m.group('b'))} = "
            f"{_run_expr(m.group('b'))}, {_run_expr(m.group('a'))}"
        ),
    ),
    (
        # C++-only or non-user-relevant operations, dropped entirely.
        re.compile(
            r"^(ByteSize|Reflection|Descriptor|SpaceUsed|Destroy)\((?P<x>.+)\);$"
        ),
        lambda m: None,
    ),
]


def translate_run_body(cc: Path) -> list[str]:
    funcs_text = cc.read_text().splitlines()
    # Slice out the Run() body between its inner for-loop braces.
    run_at = next(i for i, line in enumerate(funcs_text) if "::Run()" in line)
    start = next(
        i
        for i, line in enumerate(funcs_text[run_at:], run_at)
        if "for (size_t i = 0;" in line
    )
    body = funcs_text[start + 1 :]
    out: list[str] = []
    for line in logical_lines(body):
        if line == "}":  # closes the for-loop (the rest is file tail)
            break
        for pat, fn in _RUN_RULES:
            if m := pat.match(line):
                stmt = fn(m)  # type: ignore[operator]
                if stmt is not None:  # some ops are dropped, not translated
                    out.append("            " + stmt)
                break
        else:
            raise AssertionError(f"unhandled Run line: {line!r}")
    return out


LIFECYCLE_TEMPLATE = (
    LICENSE
    + '''
# Generated from fleetbench lifecycle.cc by _fleetbench.py. DO NOT EDIT.
#
# Derived from github.com/google/fleetbench
# Copyright 2025 The Fleetbench Authors
# SPDX-License-Identifier: Apache-2.0
#
# Shared by both the google and protobuf implementations: the message classes,
# access functions, and message operations are all resolved on the `Access`
# object passed at construction.
# ruff: noqa: F841
from __future__ import annotations

from copy import deepcopy
from typing import Any

WORKING_SET_SIZE = 10  # C++ kIterations
MAX_VALUE_STRING_SIZE = 1 << 20


class _Holder:
    """One message type's working set: live messages, peers, and buffers."""

    __slots__ = ("message", "other_message", "string")

    def __init__(self, n: int) -> None:
        self.message: list = [None] * n
        self.other_message: list = [None] * n
        self.string: list[bytes] = [b""] * n


class ProtoLifecycle:
    """Port of fleetbench `ProtoLifecycle`, parameterized by implementation."""

    def __init__(self, access: Any, working_set_size: int = WORKING_SET_SIZE) -> None:
        self._a = access
        self.n = working_set_size
        self.s = "a" * MAX_VALUE_STRING_SIZE
        self.b = self.s.encode()  # pre-encoded so bytes fields don't re-encode
        self.holders = [_Holder(working_set_size) for _ in range({num_messages})]

    def _init_messages(self, holder: _Holder, message_cls: type) -> None:
        """Allocate one message type's working set (C++ `InitMessages`)."""
        for i in range(self.n):
            holder.message[i] = message_cls()
            holder.other_message[i] = message_cls()
            holder.string[i] = b""

    def init(self) -> None:
        a, m, s, b = self._a, self.holders, self.s, self.b
{init_body}

    def run(self) -> None:
        a, m, s, b = self._a, self.holders, self.s, self.b
        for i in range(self.n):
{run_body}
'''
)


def generate_lifecycle(src: Path, num_messages: int) -> str:
    run_body = "\n".join(translate_run_body(src / "lifecycle.cc"))
    # Mirror the C++ Init: an InitMessages call per message, then a loop with a
    # first-setter call per message. The message and setter names match across
    # impls, so we emit them explicitly rather than looping.
    init_lines = [
        f"        self._init_messages(m[{k}], a.Message{k})"
        for k in range(num_messages)
    ]
    init_lines.append("        for i in range(self.n):")
    init_lines += [
        f"            a.message{k}_set_1(m[{k}].other_message[i], s, b)"
        for k in range(num_messages)
    ]
    init_body = "\n".join(init_lines)
    return (
        LIFECYCLE_TEMPLATE.replace("{num_messages}", str(num_messages))
        .replace("{init_body}", init_body)
        .replace("{run_body}", run_body)
    )


def translate(repo_root: Path) -> None:
    """Translate the fleetbench C++ proto benchmark harness to Python.

    Reads the C++ sources from a fleetbench checkout (``repo_root`` is the
    extracted repository root) and writes the google and protobuf access
    modules, package ``__init__``s, and the shared lifecycle, then formats them.
    """
    src = repo_root / "fleetbench" / "proto"
    # Messages are Message0..MessageN-1, one Message{i}.proto per message.
    num_messages = len(list(src.glob("Message*.proto")))
    for impl in IMPLS:
        out_dir = OUT_ROOT / impl
        out_dir.mkdir(parents=True, exist_ok=True)
        used = UsedTypes()
        for msg_id in range(num_messages):
            text, file_used = generate_access(msg_id, impl, src)
            (out_dir / f"access_message{msg_id}.py").write_text(text)
            used.update(file_used)
        (out_dir / "__init__.py").write_text(generate_init(impl, num_messages, used))
    (OUT_ROOT / "lifecycle.py").write_text(generate_lifecycle(src, num_messages))
    subprocess.run(["ruff", "format", str(OUT_ROOT)], check=True)  # noqa: S607
    print(f"translated {num_messages} fleetbench messages")  # noqa: T201
