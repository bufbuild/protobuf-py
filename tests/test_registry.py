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

from typing import TYPE_CHECKING

import pytest

from protobuf._descriptors import DescFile
from protobuf._registry import Registry

if TYPE_CHECKING:
    from .conftest import Protoc


def test_empty_registry() -> None:
    reg = Registry()
    assert reg.file("foo.proto") is None
    assert reg.message("foo") is None
    assert reg.enum("foo") is None
    assert reg.extension("foo") is None
    assert reg.service("foo") is None
    assert reg.extension_for("foo", 1) is None


@pytest.fixture
def file(protoc: Protoc) -> DescFile:
    return protoc.compile_file(
        """\
        syntax = "proto2";
        package P;
        message M {
            extensions 100 to 101;
        }
        extend M {
            optional string ext = 100;
        }
        enum E {
            E_UNSPECIFIED = 0;
        }
        service S {
            rpc GetFoo(M) returns (M);
        }
        message M2 {
            message M3 {
                message M4 {}
            }
            extend M {
                optional int32 ext2 = 101;
            }
            enum E2 {
                E2_UNSPECIFIED = 0;
            }
        }
""",
        name="file.proto",
    )


def test_init(file: DescFile) -> None:
    assert_all(file, Registry(file))


def test_add(file: DescFile) -> None:
    reg = Registry()
    reg.add(file)
    assert_all(file, reg)


def test_other_registry(file: DescFile) -> None:
    assert_all(file, Registry(Registry(file)))


def test_with_types(file: DescFile) -> None:
    assert_all(
        file,
        Registry(
            file,
            *file.services,
            *[msg.type for msg in file.messages],
            *[enum.type for enum in file.enums],
            *[ext.type for ext in file.extensions],
        ),
    )


def test_extension_without_message(file: DescFile) -> None:
    reg = Registry(*file.extensions)
    assert reg.message("P.M") is None
    assert reg.extension_for("P.M", 100) is file.extensions[0]
    assert reg.extension_for(file.messages[0], 100) is file.extensions[0]


def test_multiple(protoc: Protoc, file: DescFile) -> None:
    other = protoc.compile_file(
        """\
    syntax = "proto2";
    package O;
    message M {
        extensions 100 to 101;
    }
    extend M {
        optional string ext = 100;
    }
    enum E {
        E_UNSPECIFIED = 0;
    }
    service S {
        rpc GetFoo(M) returns (M);
    }
""",
        name="other.proto",
    )
    reg = Registry(other, file)
    assert_all(file, reg)
    assert reg.file("other.proto") is other
    assert reg.message("O.M") is other.messages[0]
    assert reg.service("O.S") is other.services[0]
    assert reg.enum("O.E") is other.enums[0]
    assert reg.extension("O.ext") is other.extensions[0]
    assert reg.extension_for("O.M", 100) is other.extensions[0]


def test_last_win(protoc: Protoc, file: DescFile) -> None:
    other = protoc.compile_file(
        # Same as the "file.proto" fixture
        """\
    syntax = "proto2";
    package P;
    message M {
        extensions 100 to 101;
    }
    extend M {
        optional string ext = 100;
    }
    enum E {
        E_UNSPECIFIED = 0;
    }
    service S {
        rpc GetFoo(M) returns (M);
    }
""",
        name="file.proto",
    )
    assert_all(file, Registry(other, Registry(file)))


def test_iter(file: DescFile) -> None:
    expected = {
        "file.proto": file,
        "P.M": file.messages[0],
        "P.S": file.services[0],
        "P.E": file.enums[0],
        "P.ext": file.extensions[0],
        "P.M2": file.messages[1],
        "P.M2.M3": file.messages[1].nested_messages[0],
        "P.M2.M3.M4": file.messages[1].nested_messages[0].nested_messages[0],
        "P.M2.E2": file.messages[1].nested_enums[0],
        "P.M2.ext2": file.messages[1].nested_extensions[0],
    }
    registry_dict = {
        desc.name if isinstance(desc, DescFile) else desc.type_name: desc
        for desc in Registry(file)
    }
    assert registry_dict == expected


def assert_all(file: DescFile, reg: Registry) -> None:
    assert reg.file("file.proto") is file
    assert reg.message("P.M") is file.messages[0]
    assert reg.service("P.S") is file.services[0]
    assert reg.enum("P.E") is file.enums[0]
    assert reg.extension("P.ext") is file.extensions[0]
    assert reg.extension_for("P.M", 100) is file.extensions[0]
