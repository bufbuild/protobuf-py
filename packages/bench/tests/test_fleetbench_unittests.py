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
"""Correctness check for the fleetbench translation."""

from __future__ import annotations

import importlib

import pytest

from bench.fleetbench.google import Access as GoogleAccess
from bench.fleetbench.protobuf import Access as ProtobufAccess

NUM_MESSAGES = 20
SETTERS_PER_MESSAGE = 4
# A long filler string and its pre-encoded bytes; Set functions slice prefixes
# of each (C++ uses a single 'a' * 1MB std::string for both string and bytes).
SAMPLE = "a" * 64
SAMPLE_BYTES = SAMPLE.encode()


@pytest.fixture(scope="module")
def google_access() -> GoogleAccess:
    import google.protobuf.symbol_database

    for i in range(NUM_MESSAGES):
        importlib.import_module(f"bench.gen.fleetbench.Message{i}_pb2")
    return GoogleAccess(google.protobuf.symbol_database.Default())


@pytest.fixture(scope="module")
def protobuf_access() -> ProtobufAccess:
    from protobuf.wkt import FileDescriptorSet

    files = [
        importlib.import_module(f"bench.gen.fleetbench.Message{i}_pb").desc().proto
        for i in range(NUM_MESSAGES)
    ]
    return ProtobufAccess(FileDescriptorSet(file=files).to_registry())


@pytest.mark.parametrize("msg_id", range(NUM_MESSAGES))
@pytest.mark.parametrize("setter", range(1, SETTERS_PER_MESSAGE + 1))
def test_set_bytes_match(
    msg_id: int,
    setter: int,
    google_access: GoogleAccess,
    protobuf_access: ProtobufAccess,
) -> None:
    google_msg = getattr(google_access, f"Message{msg_id}")()
    protobuf_msg = getattr(protobuf_access, f"Message{msg_id}")()

    getattr(google_access, f"message{msg_id}_set_{setter}")(
        google_msg, SAMPLE, SAMPLE_BYTES
    )
    getattr(protobuf_access, f"message{msg_id}_set_{setter}")(
        protobuf_msg, SAMPLE, SAMPLE_BYTES
    )

    assert google_access.serialize(google_msg) == protobuf_access.serialize(
        protobuf_msg
    )
