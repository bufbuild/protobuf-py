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

import importlib
from typing import TYPE_CHECKING, Any

import pytest

from bench.fleetbench.lifecycle import ProtoLifecycle

if TYPE_CHECKING:
    from pytest_benchmark.fixture import BenchmarkFixture

NUM_MESSAGES = 20


@pytest.fixture(scope="module")
def access(impl: str, setup_bufbuild: None, setup_google: None) -> Any:
    """The fleetbench Access object, wired against the active backend."""
    if impl in ("bufbuild-python", "bufbuild-rust"):
        from protobuf.wkt import FileDescriptorSet

        from bench.fleetbench.protobuf import Access

        # Round trip through descriptor bytes to get fresh message classes
        # that reflect the native vs python setup.
        files = [
            importlib.import_module(f"bench.gen.fleetbench.Message{i}_pb").desc().proto
            for i in range(NUM_MESSAGES)
        ]
        access = Access(FileDescriptorSet(file=files).to_registry())
        native = any(c.__name__ == "NativeMessage" for c in access.Message0.__mro__)
        assert native == (impl == "bufbuild-rust")
        return access

    import google.protobuf.symbol_database

    from bench.fleetbench.google import Access

    for i in range(NUM_MESSAGES):
        importlib.import_module(f"bench.gen.fleetbench.Message{i}_pb2")
    access = Access(google.protobuf.symbol_database.Default())
    descriptor_class = str(access.Message0().DESCRIPTOR.__class__)
    match impl:
        case "google-python":
            assert "google.protobuf.descriptor.Descriptor" in descriptor_class
        case "google-upb":
            assert "google._upb._message.Descriptor" in descriptor_class
    return access


@pytest.mark.parametrize("_id", ["lifecycle"])
@pytest.mark.benchmark(min_time=2)
def test_lifecycle(_id: str, access: Any, benchmark: BenchmarkFixture) -> None:
    lifecycle = ProtoLifecycle(access)

    def iteration() -> None:
        lifecycle.init()
        lifecycle.run()

    benchmark(iteration)
