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
"""Test configuration.

We parameterize the native and python marshaler implementations. Because generated code
gets wired to an implementation at import time, we use xdist to run tests in separate
processes for the simplest way to ensure they use the correct implementation.
"""

from __future__ import annotations

import importlib.util
import re
from typing import TYPE_CHECKING, cast, get_args

import pytest
from xdist.scheduler import EachScheduling

from tests._implementation import (
    IMPLEMENTATION_ENV,
    Implementation,
    check_implementation,
    hide_native_extension,
)

if TYPE_CHECKING:
    from xdist.remote import Producer

    from tests._protoc import Protoc

# Evaluated at import, before pytest_configure may hide the extension below.
_IMPLEMENTATIONS: tuple[Implementation, ...] = (
    get_args(Implementation)
    if importlib.util.find_spec("protobuf_ext") is not None
    else ("python",)
)


def pytest_configure(config: pytest.Config) -> None:  # noqa: ARG001
    # Runs before collection imports protobuf.
    hide_native_extension()


@pytest.fixture(params=_IMPLEMENTATIONS)
def marshaler_implementation(request: pytest.FixtureRequest) -> Implementation:
    """The marshaler implementation the current test runs against."""
    return cast("Implementation", request.param)


@pytest.fixture(autouse=True)
def _check_marshaler_implementation(marshaler_implementation: Implementation) -> None:
    check_implementation(marshaler_implementation)


_NODEID_IMPLEMENTATION = re.compile(r"\[(native|python)(?:-|\])")


def _nodeid_implementation(nodeid: str) -> Implementation:
    match = _NODEID_IMPLEMENTATION.search(nodeid)
    if match is None:
        # Unparametrized items (doctests) run once, on the native worker.
        return "native"
    return cast("Implementation", match.group(1))


class ImplementationScheduling(EachScheduling):
    """Route each implementation's tests to the worker pinned to it."""

    def schedule(self) -> None:
        for node, pending in self.node2pending.items():
            if node in self._started:
                continue
            implementation = node.gateway.spec.env.get(IMPLEMENTATION_ENV, "native")
            pending[:] = [
                index
                for index, nodeid in enumerate(self.node2collection[node])
                if _nodeid_implementation(nodeid) == implementation
            ]
            node.send_runtest_some(pending)
            node.shutdown()
            self._started.append(node)


def pytest_xdist_make_scheduler(
    config: pytest.Config, log: Producer
) -> ImplementationScheduling:
    return ImplementationScheduling(config, log)


@pytest.fixture
def protoc(monkeypatch: pytest.MonkeyPatch) -> Protoc:
    """Fixture providing a :class:`Protoc` for compiling proto source."""
    from tests._protoc import Protoc  # noqa: PLC0415

    return Protoc(monkeypatch)
