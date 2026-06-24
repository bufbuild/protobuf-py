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
"""protoc-gen-grpc-py: a protoc plugin that generates gRPC Python stubs.

The generated stubs are fully typed and idiomatic, and use ``protobuf-py``
messages for serialization rather than the classic ``protobuf`` runtime.
"""

from __future__ import annotations

import importlib.metadata
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from protobuf._sanitization import (
    PYTHON_KEYWORDS,
    escape_identifier,
    escape_public_identifier,
)
from protobuf.plugin import File, Ident, Module, Schema, get_comments, run

if TYPE_CHECKING:
    from protobuf import DescFile, DescMethod, DescService

_RESERVED_METHOD_NAMES = PYTHON_KEYWORDS | {"add_to_server"}

_COLLECTIONS_ABC = Module("collections.abc")
_ASYNC_ITERATOR = _COLLECTIONS_ABC.ident("AsyncIterator", type_only=True)
_ITERATOR = _COLLECTIONS_ABC.ident("Iterator", type_only=True)
_SEQUENCE = _COLLECTIONS_ABC.ident("Sequence", type_only=True)

_GRPC = Module("grpc")
_STATUS_CODE = _GRPC.ident("StatusCode")
_UNARY_UNARY_HANDLER = _GRPC.ident("unary_unary_rpc_method_handler")
_UNARY_STREAM_HANDLER = _GRPC.ident("unary_stream_rpc_method_handler")
_STREAM_UNARY_HANDLER = _GRPC.ident("stream_unary_rpc_method_handler")
_STREAM_STREAM_HANDLER = _GRPC.ident("stream_stream_rpc_method_handler")
_GENERIC_HANDLER = _GRPC.ident("method_handlers_generic_handler")

_CHANNEL = _GRPC.ident("Channel", type_only=True)
_SERVER = _GRPC.ident("Server", type_only=True)
_SERVICER_CONTEXT = _GRPC.ident("ServicerContext", type_only=True)
_CALL_CREDENTIALS = _GRPC.ident("CallCredentials", type_only=True)
_COMPRESSION = _GRPC.ident("Compression", type_only=True)
_CALL_ITERATOR = _GRPC.ident("_CallIterator", type_only=True)
_AIO_METADATA = _GRPC.ident("aio.Metadata", type_only=True)
_AIO_CHANNEL = _GRPC.ident("aio.Channel", type_only=True)
_AIO_SERVER = _GRPC.ident("aio.Server", type_only=True)
_AIO_SERVICER_CONTEXT = _GRPC.ident("aio.ServicerContext", type_only=True)
_AIO_UNARY_UNARY_CALL = _GRPC.ident("aio.UnaryUnaryCall", type_only=True)
_AIO_UNARY_STREAM_CALL = _GRPC.ident("aio.UnaryStreamCall", type_only=True)
_AIO_STREAM_UNARY_CALL = _GRPC.ident("aio.StreamUnaryCall", type_only=True)
_AIO_STREAM_STREAM_CALL = _GRPC.ident("aio.StreamStreamCall", type_only=True)

_UNIMPLEMENTED_DETAILS = "Method not implemented!"


class _IOOption(str, Enum):
    """Whether to generate synchronous or asynchronous code."""

    SYNC = "sync"
    """Generates only synchronous code."""

    ASYNC = "async"
    """Generates only asynchronous code."""


@dataclass
class _Options:
    """Options for the protoc-gen-grpc-py plugin."""

    io: _IOOption | None = field(default=None)
    """The I/O mode for generated code."""


def _generate(schema: Schema[_Options]) -> None:
    for file in schema.files_to_generate:
        if not file.services:
            continue
        _generate_file(schema.generate_file(file, "_pb_grpc.py"), file, schema.options)


def _generate_file(f: File, desc: DescFile, options: _Options) -> None:
    f.preamble(desc)
    for service in desc.services:
        if not options.io or options.io == _IOOption.ASYNC:
            _generate_async_stubs(f, service)
        if not options.io or options.io == _IOOption.SYNC:
            _generate_sync_stubs(f, service)


def _generate_async_stubs(f: File, service: DescService) -> None:
    _generate_servicer(f, service, is_async=True)
    _generate_client(f, service, is_async=True)


def _generate_sync_stubs(f: File, service: DescService) -> None:
    _generate_servicer(f, service, is_async=False)
    _generate_client(f, service, is_async=False)


def _generate_servicer(f: File, service: DescService, *, is_async: bool) -> None:
    context = _AIO_SERVICER_CONTEXT if is_async else _SERVICER_CONTEXT
    with f.scope("class ", _servicer_name(service, is_async=is_async), ":"):
        _generate_docstring(f, service)
        for method in service.methods:
            # Unary-response handlers are coroutines; streaming handlers are
            # plain functions returning an (async) iterator
            prefix = "async " if is_async and not _response_stream(method) else ""
            with f.scope(
                prefix,
                "def ",
                _method_local_name(method),
                "(self, request",
                "_iterator" if _request_stream(method) else "",
                ": ",
                *_request_type(method, is_async=is_async),
                ", context: ",
                context,
                ") -> ",
                *_servicer_return_type(method, is_async=is_async),
                ":",
            ):
                _generate_docstring(f, method)
                f.print("context.set_code(", _STATUS_CODE, ".UNIMPLEMENTED)")
                f.print('context.set_details("', _UNIMPLEMENTED_DETAILS, '")')
                f.print('raise NotImplementedError("', _UNIMPLEMENTED_DETAILS, '")')
            f.print()
        _generate_add_to_server(f, service, is_async=is_async)
    f.print()


def _generate_add_to_server(f: File, service: DescService, *, is_async: bool) -> None:
    server = _AIO_SERVER if is_async else _SERVER
    with f.scope("def add_to_server(self, server: ", server, ") -> None:"):
        with f.doc("Register this servicer's RPC handlers with a grpc server."):
            pass
        with f.scope("rpc_method_handlers = {"):
            for method in service.methods:
                with f.scope('"', method.name, '": ', _handler_factory(method), "("):
                    f.print("self.", _method_local_name(method), ",")
                    f.print("request_deserializer=", method.input, ".from_binary,")
                    f.print("response_serializer=", method.output, ".to_binary,")
                f.print("),")
        f.print("}")
        with f.scope("generic_handler = ", _GENERIC_HANDLER, "("):
            f.print('"', service.type_name, '",')
            f.print("rpc_method_handlers,")
        f.print(")")
        f.print("server.add_generic_rpc_handlers((generic_handler,))")
    f.print()


def _generate_client(f: File, service: DescService, *, is_async: bool) -> None:
    channel = _AIO_CHANNEL if is_async else _CHANNEL
    with f.scope("class ", _client_name(service, is_async=is_async), ":"):
        _generate_docstring(f, service)
        with f.scope("def __init__(self, channel: ", channel, ") -> None:"):
            for method in service.methods:
                with f.scope(
                    "self._",
                    _method_local_name(method),
                    " = channel.",
                    _channel_method(method),
                    "(",
                ):
                    f.print('"', _method_url(method), '",')
                    f.print("request_serializer=", method.input, ".to_binary,")
                    f.print("response_deserializer=", method.output, ".from_binary,")
                f.print(")")
        f.print()
        for method in service.methods:
            _generate_client_method(f, method, is_async=is_async)
    f.print()


def _generate_client_method(f: File, method: DescMethod, *, is_async: bool) -> None:
    request_arg = "request_iterator" if _request_stream(method) else "request"
    with f.scope("def ", _method_local_name(method), "("):
        f.print("self,")
        f.print(request_arg, ": ", *_request_type(method, is_async=is_async), ",")
        f.print("*,")
        # These per-call options mirror grpc's *MultiCallable.__call__ methods.
        # grpc's own generated stubs type these as Any; we mirror them explicitly
        # and must keep them in sync when grpc adds parameters. As of grpcio
        # 1.81.1 the full set is: timeout, metadata, credentials, wait_for_ready,
        # compression. See the *MultiCallable.__call__ signatures (pinned to the
        # grpcio version this generator targets):
        #   sync:  https://github.com/grpc/grpc/blob/e84a8a2f04095f2772ba42a4abccde4f9243e75b/src/python/grpcio/grpc/__init__.py#L683
        #   async: https://github.com/grpc/grpc/blob/e84a8a2f04095f2772ba42a4abccde4f9243e75b/src/python/grpcio/grpc/aio/_base_channel.py#L38
        f.print("timeout: float | None = None,")
        f.print("metadata: ", *_metadata_type(is_async=is_async), " | None = None,")
        f.print("credentials: ", _CALL_CREDENTIALS, " | None = None,")
        f.print("wait_for_ready: bool | None = None,")
        f.print("compression: ", _COMPRESSION, " | None = None,")
    with f.scope(") -> ", *_client_return_type(method, is_async=is_async), ":"):
        _generate_docstring(f, method)
        f.print(
            "return self._",
            _method_local_name(method),
            "(",
            request_arg,
            ", timeout=timeout, metadata=metadata, credentials=credentials,"
            " wait_for_ready=wait_for_ready, compression=compression)",
        )
    f.print()


def _request_type(method: DescMethod, *, is_async: bool) -> list[object]:
    if _request_stream(method):
        iterator = _ASYNC_ITERATOR if is_async else _ITERATOR
        return [iterator, "[", method.input, "]"]
    return [method.input]


def _metadata_type(*, is_async: bool) -> list[object]:
    # The accepted metadata type differs between the sync and async APIs (these
    # stubs are type-checked against typeshed).
    #     https://github.com/python/typeshed/blob/3f74e6eba99eb7ce60522e044cbb5d38f4c0dd92/stubs/grpcio/grpc/__init__.pyi#L37
    #     https://github.com/python/typeshed/blob/3f74e6eba99eb7ce60522e044cbb5d38f4c0dd92/stubs/grpcio/grpc/aio/__init__.pyi#L442
    if is_async:
        return [_AIO_METADATA, " | ", _SEQUENCE, "[tuple[str, str | bytes]]"]
    return ["tuple[tuple[str, str | bytes], ...]"]


def _servicer_return_type(method: DescMethod, *, is_async: bool) -> list[object]:
    # Servicer methods are the handlers grpc invokes: streaming handlers are
    # (async) iterators/generators of the response message.
    if _response_stream(method):
        iterator = _ASYNC_ITERATOR if is_async else _ITERATOR
        return [iterator, "[", method.output, "]"]
    return [method.output]


def _client_return_type(method: DescMethod, *, is_async: bool) -> list[object]:
    # Client methods return grpc's real call objects so callers keep full
    # access to the response, status code, metadata, cancellation, etc.
    if is_async:
        return [_aio_call_ident(method), "[", method.input, ", ", method.output, "]"]
    if _response_stream(method):
        return [_CALL_ITERATOR, "[", method.output, "]"]
    return [method.output]


def _servicer_name(service: DescService, *, is_async: bool) -> str:
    suffix = "" if is_async else "Sync"
    return f"{escape_identifier(service.name)}Servicer{suffix}"


def _client_name(service: DescService, *, is_async: bool) -> str:
    suffix = "" if is_async else "Sync"
    return f"{escape_identifier(service.name)}Client{suffix}"


def _request_stream(method: DescMethod) -> bool:
    return method.method_kind in ("client_streaming", "bidi_streaming")


def _response_stream(method: DescMethod) -> bool:
    return method.method_kind in ("server_streaming", "bidi_streaming")


def _channel_method(method: DescMethod) -> str:
    request = "stream" if _request_stream(method) else "unary"
    response = "stream" if _response_stream(method) else "unary"
    return f"{request}_{response}"


def _handler_factory(method: DescMethod) -> Ident:
    match method.method_kind:
        case "unary":
            return _UNARY_UNARY_HANDLER
        case "server_streaming":
            return _UNARY_STREAM_HANDLER
        case "client_streaming":
            return _STREAM_UNARY_HANDLER
        case _:
            return _STREAM_STREAM_HANDLER


def _aio_call_ident(method: DescMethod) -> Ident:
    match method.method_kind:
        case "unary":
            return _AIO_UNARY_UNARY_CALL
        case "server_streaming":
            return _AIO_UNARY_STREAM_CALL
        case "client_streaming":
            return _AIO_STREAM_UNARY_CALL
        case _:
            return _AIO_STREAM_STREAM_CALL


def _method_local_name(method: DescMethod) -> str:
    return escape_public_identifier(
        _pascal_to_snake_case(method.name), _RESERVED_METHOD_NAMES
    )


def _method_url(method: DescMethod) -> str:
    return f"/{method.parent.type_name}/{method.name}"


_RE_UPPER_TO_LOWER = re.compile("([^_])([A-Z][a-z]+)")
_RE_LOWER_TO_UPPER = re.compile("([a-z])([A-Z])")


def _pascal_to_snake_case(text: str) -> str:
    """Convert a PascalCase RPC name to snake_case."""
    s1 = _RE_UPPER_TO_LOWER.sub(r"\1_\2", text)
    return _RE_LOWER_TO_UPPER.sub(r"\1_\2", s1).lower()


def _generate_docstring(f: File, desc: DescService | DescMethod) -> None:
    comments = get_comments(desc)
    text = ""
    if comments.leading:
        text += comments.leading.removesuffix("\n")
    if comments.trailing:
        if text:
            text += "\n\n"
        text += comments.trailing.removesuffix("\n")
    if not text:
        return
    lines = [line.removeprefix(" ") for line in text.splitlines()]
    if len(lines) == 1:
        with f.doc(lines[0]):
            pass
    else:
        with f.doc():
            for line in lines:
                f.print(line)


def main() -> None:
    """Entry point for the protoc-gen-grpc-py plugin."""
    run(
        "protoc-gen-grpc-py",
        importlib.metadata.version("protoc-gen-grpc-py"),
        _Options,
        _generate,
    )
