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

import pytest

from protobuf import __version__
from protobuf._codegen import _version
from protobuf._codegen._version import _convert_version, check_version


@pytest.fixture
def runtime_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pins the runtime to 1.4.0 with a minimum codegen version of 1.0.0."""
    monkeypatch.setattr(_version, "__version__", "1.4.0")
    monkeypatch.setattr(_version, "_version_tuple", _convert_version("1.4.0"))
    monkeypatch.setattr(_version, "_min_codegen_version", _convert_version("1.0.0"))


class TestConvertVersion:
    @pytest.mark.parametrize(
        ("version", "expected"),
        [
            pytest.param("1.2.3", (1, 2, 3, 1, 0), id="release"),
            pytest.param("0.7.0", (0, 7, 0, 1, 0), id="zero_major"),
            pytest.param("1.2.3rc1", (1, 2, 3, 0, 1), id="rc"),
            pytest.param("10.20.30rc40", (10, 20, 30, 0, 40), id="multi_digit"),
        ],
    )
    def test_convert(self, version: str, expected: tuple[int, ...]) -> None:
        assert _convert_version(version) == expected

    @pytest.mark.parametrize(
        "version",
        [
            pytest.param("1.2", id="two_parts"),
            pytest.param("1.2.3.4", id="four_parts"),
            pytest.param("v1.2.3", id="v_prefix"),
            pytest.param("1.2.3a1", id="alpha"),
            pytest.param("1.2.3b1", id="beta"),
            pytest.param("1.2.3.dev1", id="dev"),
            pytest.param("1.2.3.post1", id="post"),
            pytest.param("1.2.3rc1+local", id="local"),
            pytest.param("1.2.3-rc1", id="hyphen_rc"),
            pytest.param("1.2.3rc", id="rc_without_number"),
            pytest.param("", id="empty"),
        ],
    )
    def test_unsupported(self, version: str) -> None:
        with pytest.raises(ValueError, match="unsupported version format"):
            _convert_version(version)

    def test_ordering(self) -> None:
        versions = [
            "1.0.1",
            "1.0.0",
            "1.0.1rc1",
            "1.0.0rc2",
            "0.9.9",
            "1.0.0rc1",
            "2.0.0rc1",
        ]
        assert sorted(versions, key=_convert_version) == [
            "0.9.9",
            "1.0.0rc1",
            "1.0.0rc2",
            "1.0.0",
            "1.0.1rc1",
            "1.0.1",
            "2.0.0rc1",
        ]


@pytest.mark.usefixtures("runtime_version")
class TestCheckVersion:
    @pytest.mark.parametrize(
        "codegen_version",
        [
            pytest.param("1.4.0", id="same"),
            pytest.param("1.4.0rc1", id="same_rc"),
            pytest.param("1.3.9", id="older_patch"),
            pytest.param("1.2.0", id="older_minor"),
            pytest.param("1.0.0", id="minimum"),
        ],
    )
    def test_compatible(self, codegen_version: str) -> None:
        check_version(codegen_version)

    @pytest.mark.parametrize(
        "codegen_version",
        [
            pytest.param("1.4.1", id="newer_patch"),
            pytest.param("1.5.0", id="newer_minor"),
            pytest.param("1.5.0rc1", id="newer_minor_rc"),
            pytest.param("2.0.0", id="newer_major"),
            pytest.param("2.0.0rc1", id="newer_major_rc"),
        ],
    )
    def test_newer_than_runtime(self, codegen_version: str) -> None:
        with pytest.raises(
            RuntimeError,
            match=rf"codegen version {codegen_version} is newer than the installed protobuf-py version 1\.4\.0",
        ):
            check_version(codegen_version)

    @pytest.mark.parametrize(
        "codegen_version",
        [
            pytest.param("0.9.9", id="older_minor"),
            pytest.param("0.0.0", id="zero"),
            pytest.param("1.0.0rc1", id="minimum_rc"),
        ],
    )
    def test_older_than_minimum(self, codegen_version: str) -> None:
        with pytest.raises(
            RuntimeError,
            match=rf"codegen version {codegen_version} is older than the minimum required version",
        ):
            check_version(codegen_version)

    def test_unsupported_format(self) -> None:
        with pytest.raises(ValueError, match="unsupported version format"):
            check_version("1.4.0.dev1")


class TestRuntimeRc:
    @pytest.fixture(autouse=True)
    def runtime_rc_version(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(_version, "__version__", "1.4.0rc1")
        monkeypatch.setattr(_version, "_version_tuple", _convert_version("1.4.0rc1"))
        monkeypatch.setattr(_version, "_min_codegen_version", _convert_version("1.0.0"))

    @pytest.mark.parametrize(
        "codegen_version",
        [
            pytest.param("1.4.0rc1", id="same_rc"),
            pytest.param("1.3.0", id="older_release"),
        ],
    )
    def test_compatible(self, codegen_version: str) -> None:
        check_version(codegen_version)

    @pytest.mark.parametrize(
        "codegen_version",
        [
            pytest.param("1.4.0", id="release_of_same_version"),
            pytest.param("1.4.0rc2", id="later_rc"),
        ],
    )
    def test_newer_than_runtime(self, codegen_version: str) -> None:
        with pytest.raises(
            RuntimeError,
            match=r"is newer than the installed protobuf-py version 1\.4\.0rc1",
        ):
            check_version(codegen_version)


def test_minimum_rc_is_older_than_minimum() -> None:
    """An rc of the minimum version is older than the minimum, whatever it is."""
    major, minor, patch, *_ = _version._min_codegen_version
    with pytest.raises(
        RuntimeError, match="is older than the minimum required version"
    ):
        check_version(f"{major}.{minor}.{patch}rc1")


def test_installed_version_is_compatible() -> None:
    """Code generated by the release matching the runtime always imports."""
    check_version(__version__)
