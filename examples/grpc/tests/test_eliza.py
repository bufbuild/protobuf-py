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

from concurrent import futures
from typing import TYPE_CHECKING

import grpc
import pytest
from example_grpc.eliza_service import DemoElizaService
from example_grpc.eliza_service_sync import DemoElizaService as DemoElizaServiceSync
from example_grpc.gen.connectrpc.eliza.v1.eliza_pb import (
    ConverseRequest,
    IntroduceRequest,
    SayRequest,
)
from example_grpc.gen.connectrpc.eliza.v1.eliza_pb_grpc import (
    ElizaServiceClient,
    ElizaServiceClientSync,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


def test_sync_round_trip() -> None:
    """Exercise unary, server-streaming, and bidi RPCs over a sync server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    DemoElizaServiceSync().add_to_server(server)
    port = server.add_insecure_port("localhost:0")
    server.start()
    try:
        with grpc.insecure_channel(f"localhost:{port}") as channel:
            client = ElizaServiceClientSync(channel)

            # Unary.
            response = client.say(SayRequest(sentence="I need help"))
            assert response.sentence

            # Server streaming.
            intros = list(client.introduce(IntroduceRequest(name="Tester")))
            assert any("Tester" in intro.sentence for intro in intros)

            # Bidi streaming; "goodbye" terminates the conversation.
            requests = iter(
                [ConverseRequest(sentence="hello"), ConverseRequest(sentence="goodbye")]
            )
            replies = [reply.sentence for reply in client.converse(requests)]
            assert len(replies) == 2
            assert all(replies)
    finally:
        server.stop(grace=None)


@pytest.mark.asyncio
async def test_async_round_trip() -> None:
    """Exercise unary, server-streaming, and bidi RPCs over an asyncio server."""
    server = grpc.aio.server()
    DemoElizaService().add_to_server(server)
    port = server.add_insecure_port("localhost:0")
    await server.start()
    try:
        async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
            client = ElizaServiceClient(channel)

            # Unary.
            response = await client.say(SayRequest(sentence="I need help"))
            assert response.sentence

            # Server streaming.
            intros = [
                intro.sentence
                async for intro in client.introduce(IntroduceRequest(name="Tester"))
            ]
            assert any("Tester" in intro for intro in intros)

            # Bidi streaming; "goodbye" terminates the conversation.
            async def requests() -> AsyncIterator[ConverseRequest]:
                yield ConverseRequest(sentence="hello")
                yield ConverseRequest(sentence="goodbye")

            replies = [reply.sentence async for reply in client.converse(requests())]
            assert len(replies) == 2
            assert all(replies)
    finally:
        await server.stop(grace=None)
