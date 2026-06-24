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

"""protoc-gen-rpc: a custom protoc plugin that generates Protocol interfaces for unary RPCs.

This plugin demonstrates how to write a custom protoc plugin using the
protobuf-py plugin framework. For each service in the proto files,
it generates a Python Protocol class with typed method signatures for
unary RPCs only. Streaming methods are skipped.

The generated code depends on the base message types produced by
protoc-gen-py (the ``_pb`` files).
"""

from __future__ import annotations

import importlib.metadata
from typing import TYPE_CHECKING

from protobuf.plugin import File, Ident, Module, Schema, get_comments, run

if TYPE_CHECKING:
    from protobuf import DescFile, DescMethod, DescService

_TYPING = Module("typing")
_PROTOCOL = _TYPING.ident("Protocol")


def main() -> None:
    """Entry point for the protoc-gen-rpc plugin."""

    def generate(schema: Schema[None]) -> None:
        for desc in schema.files_to_generate:
            _generate_file(schema, desc)

    run("protoc-gen-rpc", importlib.metadata.version("example-plugin"), generate)


def _generate_file(schema: Schema[None], desc: DescFile) -> None:
    # Avoid creating an empty output file when no service has unary methods.
    has_unary = any(
        method.method_kind == "unary"
        for service in desc.services
        for method in service.methods
    )
    if not has_unary:
        return

    f = schema.generate_file(desc, "_rpc.py")
    f.preamble(desc)

    for service in desc.services:
        _generate_service(f, service)


def _generate_service(f: File, service: DescService) -> None:
    unary_methods = [m for m in service.methods if m.method_kind == "unary"]
    if not unary_methods:
        return

    with f.scope("class ", f.ident(service.name), "(", _PROTOCOL, "):"):
        with f.doc():
            _print_comments(f, service)
            f.print("Generated from service: '", service.type_name, "'.")
        for method in unary_methods:
            f.print()
            _generate_method(f, method)


def _generate_method(f: File, method: DescMethod) -> None:
    with f.scope(
        "def ",
        _to_snake_case(method.name),
        "(self, request: ",
        Ident.for_desc(method.input, type_only=True),
        ") -> ",
        Ident.for_desc(method.output, type_only=True),
        ":",
    ):
        with f.doc():
            _print_comments(f, method)
            f.print(
                "Generated from method: '",
                method.parent.type_name,
                ".",
                method.name,
                "'.",
            )
        f.print("...")


def _print_comments(f: File, desc: DescService | DescMethod) -> None:
    comments = get_comments(desc)
    if comments.leading:
        for line in comments.leading.removesuffix("\n").splitlines():
            f.print(line.removeprefix(" "))
        f.print()


def _to_snake_case(name: str) -> str:
    """Converts a PascalCase proto name to snake_case.

    Examples:
        >>> _to_snake_case("GetUser")
        'get_user'
        >>> _to_snake_case("CreateUser")
        'create_user'
    """
    return (
        name[0]
        + name[1:].translate(str.maketrans({c: f"_{c}" for c in name if c.isupper()}))
    ).lower()
