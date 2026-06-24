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
"""Pytest configuration for the protoc-gen-grpc-py stub tests."""

from __future__ import annotations

import importlib.util

# grpcio ships no wheels for some interpreters (PyPy, free-threaded CPython) and
# we deliberately do not build it from source there. When it is unavailable,
# skip collecting the stub tests entirely: collect_ignore prevents importing the
# module, which would otherwise fail on the generated stubs' ``import grpc``.
collect_ignore: list[str] = []
if importlib.util.find_spec("grpc") is None:
    collect_ignore.append("test_haberdasher.py")
