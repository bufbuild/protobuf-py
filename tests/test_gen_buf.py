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

"""Tests for buf-generated code in gen_buf.

The proto_buf module depends on buf.build/googleapis/googleapis, which is not
generated into gen_buf. Instead, its generated code is provided by the
googleapis-googleapis-bufbuild-py package, and gen_buf is generated with
map_imports mapping google/ to the canonical import path it provides.
"""

from __future__ import annotations

from google.rpc.status_pb import Status

from tests.gen_buf.local_dep.dep_pb import Dep
from tests.gen_buf.local_import.importer_pb import Importer


def test_external_dependency_roundtrip() -> None:
    msg = Importer(dep=Dep(value="v", status=Status(code=3, message="oops")))
    decoded = Importer.from_binary(msg.to_binary())
    assert decoded.dep is not None
    assert decoded.dep.value == "v"
    assert decoded.dep.status is not None
    assert decoded.dep.status.code == 3
    assert decoded.dep.status.message == "oops"


def test_external_dependency_descriptor() -> None:
    deps = Dep.desc().file.dependencies
    assert [d.name for d in deps] == ["google/rpc/status.proto"]
