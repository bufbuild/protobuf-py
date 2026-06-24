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
"""Authoritative round-trip tests for the generated Haberdasher stubs.

Haberdasher exercises every RPC kind (unary, client-streaming,
server-streaming, and bidirectional-streaming), a well-known type
(``google.protobuf.Empty``), and a nested message (``Hat.Part``).
"""

from __future__ import annotations

from concurrent import futures
from typing import TYPE_CHECKING

import grpc
import pytest
import pytest_asyncio

from protobuf.wkt import Empty

from .gen.connectrpc.example.haberdasher_pb import Hat, Size
from .gen.connectrpc.example.haberdasher_pb_grpc import (
    HaberdasherClient,
    HaberdasherClientSync,
    HaberdasherServicer,
    HaberdasherServicerSync,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

_SIMILAR_HAT_COUNT = 3


class AsyncHaberdasher(HaberdasherServicer):
    """An asyncio Haberdasher implementation with deterministic behavior."""

    async def make_hat(self, request: Size, context: grpc.aio.ServicerContext) -> Hat:
        return Hat(size=request.inches, color="brown", name="bowler")

    async def make_flexible_hat(
        self, request_iterator: AsyncIterator[Size], context: grpc.aio.ServicerContext
    ) -> Hat:
        total = 0
        async for size in request_iterator:
            total += size.inches
        return Hat(size=total, color="green")

    async def make_similar_hats(
        self, request: Size, context: grpc.aio.ServicerContext
    ) -> AsyncIterator[Hat]:
        for _ in range(_SIMILAR_HAT_COUNT):
            yield Hat(size=request.inches, color="red")

    async def make_various_hats(
        self, request_iterator: AsyncIterator[Size], context: grpc.aio.ServicerContext
    ) -> AsyncIterator[Hat]:
        async for size in request_iterator:
            yield Hat(size=size.inches, color="blue")

    async def list_parts(
        self, request: Empty, context: grpc.aio.ServicerContext
    ) -> AsyncIterator[Hat.Part]:
        for part_id in ("band", "brim"):
            yield Hat.Part(id=part_id)

    async def do_nothing(
        self, request: Empty, context: grpc.aio.ServicerContext
    ) -> Empty:
        return Empty()


class SyncHaberdasher(HaberdasherServicerSync):
    """A synchronous Haberdasher implementation with deterministic behavior."""

    def make_hat(self, request: Size, context: grpc.ServicerContext) -> Hat:
        return Hat(size=request.inches, color="brown", name="bowler")

    def make_flexible_hat(
        self, request_iterator: Iterator[Size], context: grpc.ServicerContext
    ) -> Hat:
        total = sum(size.inches for size in request_iterator)
        return Hat(size=total, color="green")

    def make_similar_hats(
        self, request: Size, context: grpc.ServicerContext
    ) -> Iterator[Hat]:
        for _ in range(_SIMILAR_HAT_COUNT):
            yield Hat(size=request.inches, color="red")

    def make_various_hats(
        self, request_iterator: Iterator[Size], context: grpc.ServicerContext
    ) -> Iterator[Hat]:
        for size in request_iterator:
            yield Hat(size=size.inches, color="blue")

    def list_parts(
        self, request: Empty, context: grpc.ServicerContext
    ) -> Iterator[Hat.Part]:
        for part_id in ("band", "brim"):
            yield Hat.Part(id=part_id)

    def do_nothing(self, request: Empty, context: grpc.ServicerContext) -> Empty:
        return Empty()


@pytest.fixture(scope="module")
def sync_server_port() -> Iterator[int]:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    SyncHaberdasher().add_to_server(server)
    port = server.add_insecure_port("localhost:0")
    server.start()
    try:
        yield port
    finally:
        server.stop(grace=None)


@pytest.fixture(scope="module")
def sync_client(sync_server_port: int) -> Iterator[HaberdasherClientSync]:
    with grpc.insecure_channel(f"localhost:{sync_server_port}") as channel:
        client = HaberdasherClientSync(channel)
        yield client


def test_sync_unary(sync_client: HaberdasherClientSync) -> None:
    hat = sync_client.make_hat(Size(inches=10))
    assert hat.size == 10
    assert hat.color == "brown"
    assert hat.name == "bowler"


def test_sync_client_streaming(sync_client: HaberdasherClientSync) -> None:
    flexible = sync_client.make_flexible_hat(
        iter([Size(inches=1), Size(inches=2), Size(inches=3)])
    )
    assert flexible.size == 6


def test_sync_server_streaming(sync_client: HaberdasherClientSync) -> None:
    similar = list(sync_client.make_similar_hats(Size(inches=7)))
    assert [hat.size for hat in similar] == [7, 7, 7]


def test_sync_bidi_streaming(sync_client: HaberdasherClientSync) -> None:
    various = list(
        sync_client.make_various_hats(iter([Size(inches=4), Size(inches=5)]))
    )
    assert [hat.size for hat in various] == [4, 5]


def test_server_streaming_nested_empty(sync_client: HaberdasherClientSync) -> None:
    parts = [part.id for part in sync_client.list_parts(Empty())]
    assert parts == ["band", "brim"]


def test_unary_empty(sync_client: HaberdasherClientSync) -> None:
    assert isinstance(sync_client.do_nothing(Empty()), Empty)


@pytest_asyncio.fixture(scope="module")
async def async_server_port() -> AsyncIterator[int]:
    server = grpc.aio.server()
    AsyncHaberdasher().add_to_server(server)
    port = server.add_insecure_port("localhost:0")
    await server.start()
    try:
        yield port
    finally:
        await server.stop(grace=None)


@pytest_asyncio.fixture(scope="module")
async def async_client(async_server_port: int) -> AsyncIterator[HaberdasherClient]:
    async with grpc.aio.insecure_channel(f"localhost:{async_server_port}") as channel:
        client = HaberdasherClient(channel)
        yield client


@pytest.mark.asyncio
async def test_async_unary(async_client: HaberdasherClient) -> None:
    hat = await async_client.make_hat(Size(inches=10))
    assert hat.size == 10
    assert hat.color == "brown"
    assert hat.name == "bowler"


@pytest.mark.asyncio
async def test_async_client_streaming(async_client: HaberdasherClient) -> None:
    async def sizes() -> AsyncIterator[Size]:
        for inches in (1, 2, 3):
            yield Size(inches=inches)

    flexible = await async_client.make_flexible_hat(sizes())
    assert flexible.size == 6


@pytest.mark.asyncio
async def test_async_server_streaming(async_client: HaberdasherClient) -> None:
    similar = [hat.size async for hat in async_client.make_similar_hats(Size(inches=7))]
    assert similar == [7, 7, 7]


@pytest.mark.asyncio
async def test_async_bidi_streaming(async_client: HaberdasherClient) -> None:
    async def various_sizes() -> AsyncIterator[Size]:
        for inches in (4, 5):
            yield Size(inches=inches)

    various = [
        hat.size async for hat in async_client.make_various_hats(various_sizes())
    ]
    assert various == [4, 5]


@pytest.mark.asyncio
async def test_async_server_streaming_nested_empty(
    async_client: HaberdasherClient,
) -> None:
    parts = [part.id async for part in async_client.list_parts(Empty())]
    assert parts == ["band", "brim"]


@pytest.mark.asyncio
async def test_async_unary_empty(async_client: HaberdasherClient) -> None:
    assert isinstance(await async_client.do_nothing(Empty()), Empty)
