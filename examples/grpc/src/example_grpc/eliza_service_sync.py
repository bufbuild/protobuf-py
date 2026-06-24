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
"""A synchronous gRPC server implementing the Eliza service."""

from __future__ import annotations

import time
from concurrent import futures
from typing import TYPE_CHECKING

import grpc

from example_grpc import _eliza
from example_grpc.gen.connectrpc.eliza.v1.eliza_pb import (
    ConverseResponse,
    IntroduceResponse,
    SayResponse,
)
from example_grpc.gen.connectrpc.eliza.v1.eliza_pb_grpc import ElizaServiceServicerSync

if TYPE_CHECKING:
    from collections.abc import Iterator

    from example_grpc.gen.connectrpc.eliza.v1.eliza_pb import (
        ConverseRequest,
        IntroduceRequest,
        SayRequest,
    )


class DemoElizaService(ElizaServiceServicerSync):
    """A demo implementation of the Eliza service."""

    stream_delay_secs: float
    """Delay between streaming response messages."""

    def __init__(self, stream_delay_secs: float = 0) -> None:
        self.stream_delay_secs = stream_delay_secs

    def say(self, request: SayRequest, context: grpc.ServicerContext) -> SayResponse:
        reply, _ = _eliza.reply(request.sentence)
        return SayResponse(sentence=reply)

    def converse(
        self, request_iterator: Iterator[ConverseRequest], context: grpc.ServicerContext
    ) -> Iterator[ConverseResponse]:
        for request in request_iterator:
            reply, end = _eliza.reply(request.sentence)
            yield ConverseResponse(sentence=reply)
            if end:
                return

    def introduce(
        self, request: IntroduceRequest, context: grpc.ServicerContext
    ) -> Iterator[IntroduceResponse]:
        name = request.name or "Anonymous User"
        for sentence in _eliza.get_intro_responses(name):
            if self.stream_delay_secs > 0:
                time.sleep(self.stream_delay_secs)
            yield IntroduceResponse(sentence=sentence)


def serve(address: str = "[::]:50051") -> None:
    """Start the synchronous Eliza server and serve until terminated."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    DemoElizaService().add_to_server(server)
    server.add_insecure_port(address)
    server.start()
    print(f"Eliza server listening on {address}")  # noqa: T201
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
