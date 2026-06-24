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

import os
import sys
import sysconfig
from typing import Iterator, Literal, TypeAlias, get_args

import pytest
from protobuf import _native_message

Impl: TypeAlias = Literal[
    "bufbuild-python", "bufbuild-rust", "google-python", "google-upb"
]


@pytest.fixture(params=get_args(Impl), scope="module")
def impl(request: pytest.FixtureRequest) -> Impl:
    return request.param


@pytest.fixture(scope="module")
def setup_bufbuild(impl: Impl) -> Iterator[None]:
    if impl not in ("bufbuild-python", "bufbuild-rust"):
        yield
        return

    sys.modules.pop("protobuf._message", None)

    match impl:
        case "bufbuild-python":
            if _native_message.NativeMessageClass is None:
                yield
            else:
                _NativeMessageClass = _native_message.NativeMessageClass
                _native_message.NativeMessageClass = None
                yield
                _native_message.NativeMessageClass = _NativeMessageClass
        case "bufbuild-rust":
            if _native_message.NativeMessageClass is None:
                pytest.skip("Native marshaler not available")
            yield


def _unload_google_modules() -> None:
    # Generally upstream protobuf implementation can only be controlled per process, but
    # completely removing traces of it from sys.modules seems to allow us to switch within
    # a pytest invocation. This makes sure our benchmark reporting works as-is.
    for name in list(sys.modules):
        if name.endswith("_pb2"):
            sys.modules.pop(name, None)
        if name.startswith("google."):
            sys.modules.pop(name, None)


@pytest.fixture(scope="module")
def setup_google(impl: Impl) -> Iterator[None]:
    if impl not in ("google-python", "google-upb"):
        yield
        return

    match impl:
        case "google-python":
            os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
        case "google-upb":
            if sys.implementation.name != "cpython" or sysconfig.get_config_var(
                "Py_GIL_DISABLED"
            ):
                pytest.skip("upb is not available on this Python implementation")
            os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "upb"
    _unload_google_modules()
    yield
    os.environ.pop("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", None)
    _unload_google_modules()
