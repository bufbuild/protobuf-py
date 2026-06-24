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

"""Script for building protoc-runner package."""

from __future__ import annotations

import contextlib
import importlib.metadata
import platform
import shutil
import subprocess
import sys
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.request import urlopen
from zipfile import ZipFile

if TYPE_CHECKING:
    from http.client import HTTPResponse


package_root = Path(__file__).parent.parent
package_dir = package_root / "src" / "protoc"
bin_dir = package_dir / "_bin"
protos_dir = package_dir / "include"

ver = importlib.metadata.version("protoc-runner")


def _fetch_repo(org: str, repo: str, ver: str) -> Path:
    temp_dir = package_root.parent.parent / ".tmp"
    temp_dir.mkdir(exist_ok=True)
    # GitHub archives always strip `v` from the subfolder.
    dest_dir = temp_dir / f"{repo}-{ver}"
    if dest_dir.exists():
        return dest_dir
    with contextlib.closing(
        urlopen(f"https://github.com/{org}/{repo}/archive/refs/tags/v{ver}.zip")
    ) as resp:
        resp: HTTPResponse
        if resp.status != 200:
            msg = f"bad HTTP response status {resp.status} for {org}/{repo}:{ver}"
            raise RuntimeError(msg)
        ZipFile(BytesIO(resp.read())).extractall(temp_dir)
    return dest_dir


def build_conformance_runner() -> Path:
    """Downloads the protocolbuffers repository and uses Bazel to build the conformance runner."""
    print(f"Fetching protobuf version {ver}", file=sys.stderr)  # noqa: T201
    repo_dir = _fetch_repo("protocolbuffers", "protobuf", ver)

    if sys.platform == "win32":
        print(  # noqa: T201
            "Conformance runner is not supported on Windows, skipping build.",
            file=sys.stderr,
        )
        return repo_dir

    bazel_cmd = ["bazel", "build", "//conformance:conformance_test_runner"]
    if sys.platform == "darwin":
        # Avoid Xcode requirement
        bazel_cmd.append("--repo_env=BAZEL_NO_APPLE_CPP_TOOLCHAIN=1")
        bazel_cmd.append("--macos_minimum_os=12.0")
    subprocess.run(bazel_cmd, cwd=repo_dir, check=True)  # noqa: S603

    shutil.copy2(
        repo_dir / "bazel-bin" / "conformance" / "conformance_test_runner",
        bin_dir / "conformance_test_runner",
    )
    return repo_dir


def _protoc_release_suffix() -> str:
    match sys.platform:
        case "win32":
            return "win64"
        case "darwin":
            suffix = "osx-"
        case "linux":
            suffix = "linux-"
        case _:
            msg = f"unsupported platform {sys.platform}"
            raise RuntimeError(msg)
    match platform.machine().lower():
        case "amd64" | "x86_64":
            suffix += "x86_64"
        case "aarch64" | "arm64":
            suffix += "aarch_64"
        case _:
            msg = f"unsupported architecture {platform.machine()}"
            raise RuntimeError(msg)
    return suffix


def download_protoc() -> Path:
    """Downloads release artifact with protoc."""
    archive_name = f"protoc-{ver}-{_protoc_release_suffix()}"

    temp_dir = package_root.parent.parent / ".tmp" / archive_name
    temp_dir.mkdir(parents=True, exist_ok=True)

    with contextlib.closing(
        urlopen(
            f"https://github.com/protocolbuffers/protobuf/releases/download/v{ver}/{archive_name}.zip"
        )
    ) as resp:
        resp: HTTPResponse
        if resp.status != 200:
            msg = f"bad HTTP response status {resp.status}"
            raise RuntimeError(msg)
        ZipFile(BytesIO(resp.read())).extractall(temp_dir)

    protoc_filename = "protoc.exe" if sys.platform == "win32" else "protoc"
    protoc_path = bin_dir / protoc_filename
    shutil.copy2(temp_dir / "bin" / protoc_filename, protoc_path)
    protoc_path.chmod(0o755)
    return temp_dir


def extract_protos(conformance_runner_dir: Path | None, protoc_dir: Path) -> None:
    """Extracts include protos from conformance runner and protoc."""
    if conformance_runner_dir is not None:
        conformance_proto_dir = protos_dir / "conformance"
        conformance_proto_dir.mkdir()
        shutil.copy2(
            conformance_runner_dir / "conformance" / "conformance.proto",
            conformance_proto_dir / "conformance.proto",
        )
        test_messages_dir = conformance_proto_dir / "messages"
        test_messages_dir.mkdir()
        for proto in [
            *(conformance_runner_dir / "conformance" / "test_protos").glob("*.proto"),
            *(conformance_runner_dir / "src" / "google" / "protobuf").glob(
                "test_messages_*.proto"
            ),
            *(conformance_runner_dir / "editions" / "golden").glob(
                "test_messages_*.proto"
            ),
        ]:
            shutil.copy2(proto, test_messages_dir / proto.name)

    shutil.copytree(protoc_dir / "include", protos_dir, dirs_exist_ok=True)


def _platform_tag() -> str:
    match sys.platform:
        case "win32":
            return "win_amd64"
        case "darwin":
            match platform.machine().lower():
                case "amd64" | "x86_64":
                    return "macosx_12_0_x86_64"
                case "aarch64" | "arm64":
                    return "macosx_12_0_arm64"
                case _:
                    msg = f"unsupported architecture {platform.machine()}"
                    raise RuntimeError(msg)
        case "linux":
            # Statically linked, we can use same wheel for manylinux and musllinux
            match platform.machine().lower():
                case "amd64" | "x86_64":
                    return "manylinux_2_17_x86_64.manylinux2014_x86_64.musllinux_1_1_x86_64"
                case "aarch64" | "arm64":
                    return "manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64"
                case _:
                    msg = f"unsupported architecture {platform.machine()}"
                    raise RuntimeError(msg)
        case _:
            msg = f"unsupported platform {sys.platform}"
            raise RuntimeError(msg)


def extract_licenses(protobuf_dir: Path) -> None:
    """Extracts license files from dependencies."""
    licenses_dir = package_root / "vendor-licenses"
    shutil.copy2(protobuf_dir / "LICENSE", licenses_dir / "protobuf.txt")


def main() -> None:  # noqa: D103
    shutil.rmtree(bin_dir, ignore_errors=True)
    bin_dir.mkdir(parents=True)
    protobuf_dir = build_conformance_runner()
    protoc_dir = download_protoc()

    shutil.rmtree(protos_dir, ignore_errors=True)
    protos_dir.mkdir(parents=True)
    extract_protos(protobuf_dir, protoc_dir)
    extract_licenses(protobuf_dir)

    subprocess.run(["uv", "build", "--wheel"], cwd=package_root, check=True)  # noqa: S607
    built_wheel = next((package_root / "dist").glob("*-py3-none-any.whl"))
    subprocess.run(  # noqa: PLW1510, S603
        [
            sys.executable,
            "-m",
            "wheel",
            "tags",
            "--remove",
            "--platform-tag",
            _platform_tag(),
            built_wheel,
        ]
    )


if __name__ == "__main__":
    main()
