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

import re

from protobuf._version import __version__

_VERSION_RE = re.compile(r"(\d+)\.(\d+)\.(\d+)(?:rc(\d+))?")


def _convert_version(version: str) -> tuple[int, ...]:
    m = _VERSION_RE.fullmatch(version)
    if m is None:
        msg = f"unsupported version format: {version!r}"
        raise ValueError(msg)
    major, minor, patch, rc = m.groups()
    # Sort rc before released versions.
    pre = (0, int(rc)) if rc is not None else (1, 0)
    return (int(major), int(minor), int(patch), *pre)


_version_tuple = _convert_version(__version__)

_min_codegen_version = _convert_version("0.6.0")


def check_version(codegen_version: str) -> None:
    """Checks the protoc-gen-py version used to generate code is compatible with the current runtime."""
    codegen_version_tuple = _convert_version(codegen_version)
    if codegen_version_tuple < _min_codegen_version:
        msg = f"codegen version {codegen_version} is older than the minimum required version {_min_codegen_version}. Update protoc-gen-py."
        raise RuntimeError(msg)
    if codegen_version_tuple > _version_tuple:
        msg = f"codegen version {codegen_version} is newer than the installed protobuf-py version {__version__}. Update protobuf-py."
        raise RuntimeError(msg)
