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
"""An asyncio gRPC client for the Eliza service."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import grpc

from example_grpc.gen.connectrpc.eliza.v1.eliza_pb import (
    ConverseRequest,
    IntroduceRequest,
    SayRequest,
)
from example_grpc.gen.connectrpc.eliza.v1.eliza_pb_grpc import ElizaServiceClient

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


async def main(target: str = "localhost:50051") -> None:
    """Run a short conversation with the Eliza server."""
    async with grpc.aio.insecure_channel(target) as channel:
        client = ElizaServiceClient(channel)

        say_request = "Hello, I'm feeling anxious about my code."
        print(f"Me: {say_request}")  # noqa: T201
        response = await client.say(SayRequest(sentence=say_request))
        print(f"    Eliza: {response.sentence}")  # noqa: T201

        introduce_request = "Python Developer"
        print(f"Me: Hi, I'm a {introduce_request}.")  # noqa: T201
        async for response in client.introduce(
            IntroduceRequest(name=introduce_request)
        ):
            print(f"    Eliza: {response.sentence}")  # noqa: T201

        conversation = [
            "I've been having trouble with async programming.",
            "Sometimes I feel like my code is talking back to me.",
            "Do you think gRPC will help with my problems?",
        ]

        async def requests() -> AsyncIterator[ConverseRequest]:
            for sentence in conversation:
                print(f"Me: {sentence}")  # noqa: T201
                yield ConverseRequest(sentence=sentence)

        async for response in client.converse(requests()):
            print(f"    Eliza: {response.sentence}")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
