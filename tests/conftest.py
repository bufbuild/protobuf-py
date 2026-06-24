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

import dataclasses
import io
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

import pytest
from protoc import get_protoc_path

from protobuf.plugin._run import run
from protobuf.wkt import CodeGeneratorResponse, FileDescriptorSet

if TYPE_CHECKING:
    from collections.abc import Callable

    from protobuf import (
        DescEnum,
        DescExtension,
        DescField,
        DescFile,
        DescMessage,
        DescMethod,
        DescService,
    )
    from protobuf.plugin._schema import Schema


@dataclasses.dataclass
class Plugin:
    """Describes a protoc plugin for use with :meth:`Protoc.run_plugin`."""

    generate: Callable[[Schema[Any]], None]
    options: type[Any] | Callable[[str], Any] | None = None
    name: str = "protoc-gen-test"
    version: str = "1.0.0"
    minimum_edition: int | None = None
    maximum_edition: int | None = None


class Protoc:
    """Compiles protobuf sources into rich descriptors."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self._monkeypatch = monkeypatch

    def compile(
        self,
        files: dict[str, str],
        *args: Literal[
            "include_imports",
            "include_source_info",
            "experimental_editions",
            "retain_options",
        ],
    ) -> dict[str, DescFile]:
        """Compile proto files and resolve dependencies.

        Files are returned keyed by filename.  Dependencies between the
        provided files are wired up automatically based on the import graph.
        """
        desc_set = FileDescriptorSet.from_binary(
            self._compile_descriptor_set(files, *args)
        )

        reg = desc_set.to_registry()
        built: dict[str, DescFile] = {}
        for fp in desc_set.file:
            desc = reg.file(fp.name)
            assert desc is not None, f"registry missing file {fp.name}"
            built[fp.name] = desc
        return built

    def compile_set(
        self,
        files: dict[str, str],
        *args: Literal[
            "include_imports",
            "include_source_info",
            "experimental_editions",
            "retain_options",
        ],
    ) -> FileDescriptorSet:
        """Compile proto files and return the raw FileDescriptorSet."""
        return FileDescriptorSet.from_binary(self._compile_descriptor_set(files, *args))

    def compile_file(self, content: str, name: str = "input.proto") -> DescFile:
        """Compile a single proto source string."""
        return self.compile(
            {name: content},
            "include_imports",
            "retain_options",
            "experimental_editions",
            "include_source_info",
        )[name]

    def compile_message(self, content: str) -> DescMessage:
        """Compile and return the first top-level message."""
        f = self.compile_file(content)
        assert len(f.messages) > 0, "missing messages"
        return f.messages[0]

    def compile_enum(self, content: str) -> DescEnum:
        """Compile and return the first top-level enum."""
        f = self.compile_file(content)
        assert len(f.enums) == 1, f"expected 1 enum, got {len(f.enums)}"
        return f.enums[0]

    def compile_service(self, content: str) -> DescService:
        """Compile and return the first service."""
        f = self.compile_file(content)
        assert len(f.services) > 0, "missing service"
        return f.services[0]

    def compile_method(self, content: str) -> DescMethod:
        """Compile and return the first method of the first service."""
        svc = self.compile_service(content)
        assert len(svc.methods) > 0, "missing method"
        return svc.methods[0]

    def compile_field(self, content: str) -> DescField:
        """Compile and return the first field of the first message."""
        msg = self.compile_message(content)
        assert len(msg.fields) > 0, "missing field"
        return msg.fields[0]

    def compile_extension(self, content: str) -> DescExtension:
        """Compile and return the first top-level extension."""
        f = self.compile_file(content)
        assert len(f.extensions) > 0, "missing extension"
        return f.extensions[0]

    def run_plugin(
        self,
        plugin: Plugin,
        proto_files: dict[str, str],
        *,
        parameter: str = "",
        files_to_generate: list[str] | None = None,
    ) -> CodeGeneratorResponse:
        """Run a protoc plugin in-process with a real CodeGeneratorRequest.

        Uses protoc to produce the exact CodeGeneratorRequest, then calls
        ``run()`` directly with the plugin's callbacks.

        Args:
            plugin: The plugin definition to run.
            proto_files: Mapping of proto filename to source content.
            parameter: The ``--<plugin>_opt`` parameter string.
            files_to_generate: Subset of proto_files to generate.
                Defaults to all proto_files keys.
        """
        req_bytes = self._create_codegen_request(
            proto_files, parameter=parameter, files_to_generate=files_to_generate
        )
        stdin = io.BytesIO(req_bytes)
        stdout = io.BytesIO()
        self._monkeypatch.setattr(sys, "argv", [f"protoc-gen-{plugin.name}"])
        self._monkeypatch.setattr(sys, "stdin", type("stdin", (), {"buffer": stdin})())
        self._monkeypatch.setattr(
            sys, "stdout", type("stdout", (), {"buffer": stdout})()
        )
        kwargs: dict[str, int] = {}
        if plugin.minimum_edition is not None:
            kwargs["minimum_edition"] = plugin.minimum_edition
        if plugin.maximum_edition is not None:
            kwargs["maximum_edition"] = plugin.maximum_edition
        if plugin.options is not None:
            run(plugin.name, plugin.version, plugin.options, plugin.generate, **kwargs)
        else:
            run(plugin.name, plugin.version, plugin.generate, **kwargs)
        return CodeGeneratorResponse.from_binary(stdout.getvalue())

    def _create_codegen_request(
        self,
        proto_files: dict[str, str],
        *,
        parameter: str = "",
        files_to_generate: list[str] | None = None,
    ) -> bytes:
        """Run protoc with a dump plugin to capture the real CodeGeneratorRequest."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            req_path = tmp_path / "request.binpb"
            plugin_code = (
                "import sys\n"
                f"open({str(req_path)!r}, 'wb').write(sys.stdin.buffer.read())\n"
                "sys.stdout.buffer.write(b'')\n"
            )
            if platform.system().lower() == "windows":
                script_path = tmp_path / "protoc-gen-dump.py"
                script_path.write_text(plugin_code)
                dump_path = tmp_path / "protoc-gen-dump.bat"
                dump_path.write_text(f'@"{sys.executable}" "{script_path}" %*\n')
            else:
                dump_path = tmp_path / "protoc-gen-dump"
                dump_path.write_text(f"#!{sys.executable}\n" + plugin_code)
                dump_path.chmod(0o755)

            proto_dir = tmp_path / "protos"
            proto_dir.mkdir()
            for name, content in proto_files.items():
                p = proto_dir / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)

            ftg = files_to_generate or list(proto_files.keys())
            args = [
                str(get_protoc_path()),
                f"--plugin=protoc-gen-dump={dump_path}",
                f"--proto_path={proto_dir}",
                f"--dump_out={tmp_path}",
            ]
            if parameter:
                args.append(f"--dump_opt={parameter}")
            args.extend(ftg)

            subprocess.run(args, check=True, capture_output=True)  # noqa: S603
            return req_path.read_bytes()

    def _compile_descriptor_set(
        self,
        files: dict[str, str],
        *args: Literal[
            "include_imports",
            "include_source_info",
            "experimental_editions",
            "retain_options",
        ],
    ) -> bytes:
        """Compile the given proto files and return the serialized FileDescriptorSet."""
        files = files if isinstance(files, dict) else {"input.proto": files}
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir_path = Path(tmp_dir)
            for path, content in files.items():
                tmp_path = tmp_dir_path.joinpath(Path(path))
                tmp_path.parent.mkdir(parents=True, exist_ok=True)
                tmp_path.write_text(content)
            out_path = tmp_dir_path.joinpath("desc.binpb")
            compile_args = [
                *[f"--{arg}" for arg in args],
                "--descriptor_set_out",
                out_path,
                "--proto_path",
                tmp_dir,
                *files.keys(),
            ]
            subprocess.run([get_protoc_path(), *compile_args], check=True)  # noqa: S603
            return out_path.read_bytes()


@pytest.fixture
def protoc(monkeypatch: pytest.MonkeyPatch) -> Protoc:
    """Fixture providing a :class:`Protoc` for compiling proto source."""
    return Protoc(monkeypatch)
