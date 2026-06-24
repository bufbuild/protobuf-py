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

import dataclasses
import sys
import traceback
from typing import TYPE_CHECKING, Any, TypeVar, cast, overload

from protobuf import maximum_supported_edition, minimum_supported_edition
from protobuf.plugin._file import write
from protobuf.plugin._options import parse_options
from protobuf.plugin._schema import _Schema
from protobuf.wkt import CodeGeneratorRequest, CodeGeneratorResponse

if TYPE_CHECKING:
    from collections.abc import Callable

    from _typeshed import DataclassInstance

    from protobuf.plugin._schema import Schema

D = TypeVar("D", bound="DataclassInstance")
T = TypeVar("T")


@overload
def run(
    name: str,
    version: str,
    generate: Callable[[Schema[None]], None],
    /,
    *,
    minimum_edition: int = minimum_supported_edition,
    maximum_edition: int = maximum_supported_edition,
) -> None: ...


@overload
def run(
    name: str,
    version: str,
    options: type[D],
    generate: Callable[[Schema[D]], None],
    /,
    *,
    minimum_edition: int = minimum_supported_edition,
    maximum_edition: int = maximum_supported_edition,
) -> None: ...


@overload
def run(
    name: str,
    version: str,
    options: Callable[[str], T],
    generate: Callable[[Schema[T]], None],
    /,
    *,
    minimum_edition: int = minimum_supported_edition,
    maximum_edition: int = maximum_supported_edition,
) -> None: ...


def run(
    name: str,
    version: str,
    options_or_generate: type[DataclassInstance] | Callable[..., Any],
    generate: Callable[[Schema[Any]], None] | None = None,
    /,
    *,
    minimum_edition: int = minimum_supported_edition,
    maximum_edition: int = maximum_supported_edition,
) -> None:
    """Run a protoc plugin.

    This is the single entry point for any protoc plugin. It handles the
    full lifecycle: reading the request, parsing options, building descriptors,
    calling the generate callback, and writing the response.

    Two calling conventions are supported:

        run(name, version, generate)
        run(name, version, options, generate)

    Args:
        name: Plugin name, used for `--version` output.
        version: Plugin version, used for `--version` output.
        options_or_generate: If a dataclass type, parse key=value pairs into it.
            If a callable and `generate` is omitted, used directly as the
            generate callback. Otherwise, called with the raw parameter string.
        generate: Callback invoked with the schema.
        minimum_edition: Minimum edition supported by this plugin.
            Defaults to the runtime's minimum_supported_edition.
        maximum_edition: Maximum edition supported by this plugin.
            Defaults to the runtime's maximum_supported_edition.
    """
    if generate is None:
        generate = cast("Callable[[Schema[Any]], None]", options_or_generate)
        options: type[DataclassInstance] | Callable[[str], Any] | None = None
    else:
        options = options_or_generate

    if "--version" in sys.argv:
        sys.stdout.write(f"{name} v{version}\n")
        sys.exit(0)

    if isinstance(options, type):
        framework_fields = {f.name for f in dataclasses.fields(_FrameworkOptions)}
        plugin_fields = {f.name for f in dataclasses.fields(options)}
        conflicts = plugin_fields & framework_fields
        if conflicts:
            keys = ", ".join(sorted(conflicts))
            msg = (
                f"dataclass options type uses reserved framework option key(s): {keys}"
            )
            raise ValueError(msg)

    req = CodeGeneratorRequest.from_binary(sys.stdin.buffer.read())

    try:
        fw_opts, remaining_parameter = parse_options(_FrameworkOptions, req.parameter)

        plugin_options = _parse_plugin_options(options, remaining_parameter)

        schema = _Schema(
            req,
            plugin_options,
            minimum_edition=minimum_edition,
            maximum_edition=maximum_edition,
            name=name,
            version=version,
            escape_module_with_hash=fw_opts.escape_module_with_hash,
        )

        generate(schema)

        response_files = [
            CodeGeneratorResponse.File(
                name=path, content=write(f, path, no_fmt_off=fw_opts.no_fmt_off)
            )
            for path, f in schema._generated_files.items()
        ]

        features = (
            CodeGeneratorResponse.Feature.PROTO3_OPTIONAL
            | CodeGeneratorResponse.Feature.SUPPORTS_EDITIONS
        )
        resp = CodeGeneratorResponse(
            supported_features=int(features),
            minimum_edition=minimum_edition,
            maximum_edition=maximum_edition,
            file=response_files,
        )
        sys.stdout.buffer.write(resp.to_binary())

    except Exception:  # noqa: BLE001
        error_msg = traceback.format_exc()
        _write_error_response(error_msg)


def _parse_plugin_options(
    options: type[DataclassInstance] | Callable[[str], Any] | None, parameter: str
) -> Any:
    """Parse plugin options from the parameter string.

    Args:
        options: None, a dataclass type, or a callable.
        parameter: The remaining parameter string after framework options removed.

    Returns:
        Parsed options, or None if options is None.

    Raises:
        ValueError: If options is None but parameter is non-empty.
    """
    if options is None:
        if parameter:
            msg = f"plugin does not accept options but got parameter: {parameter!r}"
            raise ValueError(msg)
        return None
    if isinstance(options, type):
        result, unknown = parse_options(options, parameter)
        if unknown:
            msg = f"unknown option(s): {unknown}"
            raise ValueError(msg)
        return result
    return options(parameter)


def _write_error_response(error: str) -> None:
    """Write an error response to stdout."""
    resp = CodeGeneratorResponse(error=error)
    sys.stdout.buffer.write(resp.to_binary())


@dataclasses.dataclass
class _FrameworkOptions:
    no_fmt_off: bool = False
    escape_module_with_hash: bool = False
