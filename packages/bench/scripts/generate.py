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

import base64
import contextlib
import json
import os
import shutil
import subprocess
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote
from urllib.request import urlopen
from zipfile import ZipFile

import yaml
from fix_protobuf_imports.fix_protobuf_imports import fix_protobuf_imports

from bench.gen.buffa.benchmarks_pb import BenchmarkDataset
from bench.gen.suite_pb import Case, Suite

from . import _fleetbench

if TYPE_CHECKING:
    from http.client import HTTPResponse

VER_BUFFA = "0.6.0"
VER_HYPERPB = "0.1.3"
# fleetbench has no recent release with the 20-message benchmark; pin a commit.
VER_FLEETBENCH = "0f5548c4d83ddb210b02bf131b0ed610ce857404"

# Real Reddit post bodies for the home page timeline benchmark. webis-TLDR-17 has
# no score/popularity field, so we just take the first set of rows.
HOME_TIMELINE_DATASET = "webis/tldr-17"
HOME_TIMELINE_ROWS = 100

tests_root = Path(__file__).parent.parent / "tests"


def _fetch_repo(org: str, repo: str, ver: str, *, commit: bool = False) -> Path:
    temp_dir = Path(__file__).parent.parent.parent.parent / ".tmp"
    temp_dir.mkdir(exist_ok=True)
    # GitHub names the subfolder `{repo}-{ref}`, stripping a leading `v` from
    # tags; for a commit the subfolder is `{repo}-{sha}`.
    dest_dir = temp_dir / f"{repo}-{ver}"
    if dest_dir.exists():
        return dest_dir
    archive = ver if commit else f"refs/tags/v{ver}"
    with contextlib.closing(
        urlopen(f"https://github.com/{org}/{repo}/archive/{archive}.zip")
    ) as resp:
        resp: HTTPResponse
        if resp.status != 200:
            msg = f"bad HTTP response status {resp.status} for {org}/{repo}:{ver}"
            raise RuntimeError(msg)
        ZipFile(BytesIO(resp.read())).extractall(temp_dir)
    return dest_dir


def _update_hyperpb(suite: Suite) -> None:
    print("Updating hyperpb benchmarks...")  # noqa: T201
    repo_root = _fetch_repo("bufbuild", "hyperpb-go", VER_HYPERPB)
    for dir, _, files in os.walk(repo_root / "internal" / "testdata"):
        for file in files:
            if not file.endswith(".yaml"):
                continue
            data: dict[str, Any] = yaml.safe_load((Path(dir) / file).read_text())
            if not data.get("benchmark"):
                continue
            for i, payload in enumerate(_extract_hyperpb_payload(file, data)):
                name = f"hyperpb:{file}:{i}"
                suite.cases.append(
                    Case(name=name, typename=data["type"], payload=payload)
                )


def _extract_hyperpb_payload(filename: str, data: dict[str, Any]) -> list[bytes]:
    if payloads := data.get("hex"):
        if not isinstance(payloads, list):
            msg = f"benchmark {filename} has hex field but is not a list"
            raise RuntimeError(msg)
        return [bytes.fromhex(p) for p in payloads]
    if payloads := data.get("protoscope"):
        if not isinstance(payloads, list):
            msg = f"benchmark {filename} has protoscope field but is not a list"
            raise RuntimeError(msg)
        res: list[bytes] = []
        for payload in payloads:
            if not isinstance(payload, str):
                msg = f"benchmark {filename} has non-string protoscope payload"
                raise TypeError(msg)
            proc = subprocess.run(
                [  # noqa: S607
                    "go",
                    "run",
                    "github.com/protocolbuffers/protoscope/cmd/protoscope@8e7a6aafa2c9958527b1e0747e66e1bfff045819",
                    "-s",
                ],
                input=payload.encode(),
                capture_output=True,
                check=True,
            )
            res.append(proc.stdout)
        return res
    if payloads := data.get("textproto"):
        if not isinstance(payloads, list):
            msg = f"benchmark {filename} has textproto field but is not a list"
            raise RuntimeError(msg)
        res: list[bytes] = []
        for payload in payloads:
            if not isinstance(payload, str):
                msg = f"benchmark {filename} has non-string textproto payload"
                raise TypeError(msg)
            proc = subprocess.run(  # noqa: S603
                [  # noqa: S607
                    "buf",
                    "convert",
                    "--from",
                    "-#format=txtpb",
                    "--type",
                    data["type"],
                    "--to",
                    "-#format=binpb",
                ],
                input=payload.encode(),
                capture_output=True,
                check=True,
            )
            res.append(proc.stdout)
        return res

    msg = f"benchmark {filename} is missing one of hex, protoscope, textproto"
    raise RuntimeError(msg)


def _update_buffa(suite: Suite) -> None:
    print("Updating buffa benchmarks...")  # noqa: T201
    repo_root = _fetch_repo("anthropics", "buffa", VER_BUFFA)
    for root, _, files in os.walk(repo_root / "benchmarks" / "datasets"):
        for file in files:
            if not file.endswith(".pb"):
                continue
            data = BenchmarkDataset.from_binary((Path(root) / file).read_bytes())
            for i, payload in enumerate(data.payload):
                name = f"buffa:{file}:{data.name}:{i}"
                suite.cases.append(
                    Case(name=name, typename=data.message_name, payload=payload)
                )


def _update_fleetbench() -> None:
    print("Updating fleetbench benchmarks...")  # noqa: T201
    repo_root = _fetch_repo("google", "fleetbench", VER_FLEETBENCH, commit=True)
    _fleetbench.translate(repo_root)


def protos() -> None:
    out_dir = tests_root.parent / "proto"

    hyperpb_root = _fetch_repo("bufbuild", "hyperpb-go", VER_HYPERPB)
    shutil.copytree(
        hyperpb_root / "internal" / "proto" / "test" / "test",
        out_dir / "hyperpb",
        dirs_exist_ok=True,
    )
    shutil.copytree(
        hyperpb_root / "internal" / "proto" / "rsb" / "rsb",
        out_dir / "rsb",
        dirs_exist_ok=True,
    )

    buffa_root = _fetch_repo("anthropics", "buffa", VER_BUFFA)
    shutil.copytree(
        buffa_root / "benchmarks" / "proto",
        out_dir / "buffa",
        dirs_exist_ok=True,
    )

    fleetbench_root = _fetch_repo("google", "fleetbench", VER_FLEETBENCH, commit=True)
    fleetbench_dst = out_dir / "fleetbench"
    fleetbench_dst.mkdir(exist_ok=True)
    for proto in sorted((fleetbench_root / "fleetbench" / "proto").glob("*.proto")):
        shutil.copy(proto, fleetbench_dst / proto.name)

    subprocess.run(["buf", "generate"], check=True, cwd=out_dir.parent)

    fix_protobuf_imports.callback(tests_root.parent / "src" / "bench" / "gen", False)  # type: ignore


def suite() -> None:
    suite = Suite()
    _update_hyperpb(suite)
    _update_buffa(suite)
    (tests_root / "suite.binpb").write_bytes(suite.to_binary())
    _update_fleetbench()


def home_timeline() -> None:
    print("Updating home timeline content...")  # noqa: T201
    # Fetch real Reddit post bodies via the Hugging Face datasets-server rows API.
    # We store the content column, as a base64-encoded JSON array of strings.
    # Using base64 encoding allows colorful Reddit content to stay opaque within
    # the contents of this source code.
    url = (
        "https://datasets-server.huggingface.co/rows"
        f"?dataset={quote(HOME_TIMELINE_DATASET, safe='')}"
        f"&config=default&split=train&offset=0&length={HOME_TIMELINE_ROWS}"
    )
    with contextlib.closing(urlopen(url)) as resp:  # noqa: S310
        resp: HTTPResponse
        if resp.status != 200:
            msg = f"bad HTTP response status {resp.status} for {url}"
            raise RuntimeError(msg)
        data = json.load(resp)
    contents = [row["row"]["content"] for row in data["rows"]]
    blob = base64.b64encode(json.dumps(contents).encode())
    (tests_root / "home_timeline.json.b64").write_bytes(blob)


if __name__ == "__main__":
    protos()
    suite()
    home_timeline()
