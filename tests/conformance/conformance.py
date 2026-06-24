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

import struct
import sys
from typing import Literal

from protobuf import Oneof, Registry
from protobuf.wkt import (
    any_pb,
    duration_pb,
    empty_pb,
    field_mask_pb,
    struct_pb,
    timestamp_pb,
    wrappers_pb,
)

from .gen.conformance.conformance_pb import (
    ConformanceRequest,
    ConformanceResponse,
    TestCategory,
    WireFormat,
)
from .gen.conformance.messages import (
    test_messages_edition2023_pb,
    test_messages_edition_unstable_pb,
    test_messages_proto2_editions_pb,
    test_messages_proto2_pb,
    test_messages_proto3_editions_pb,
    test_messages_proto3_pb,
)

REGISTRY: Registry = Registry(
    test_messages_proto2_pb.desc(),
    test_messages_proto3_pb.desc(),
    test_messages_edition_unstable_pb.desc(),
    test_messages_proto2_editions_pb.desc(),
    test_messages_proto3_editions_pb.desc(),
    test_messages_edition2023_pb.desc(),
    any_pb.desc(),
    duration_pb.desc(),
    empty_pb.desc(),
    field_mask_pb.desc(),
    struct_pb.desc(),
    timestamp_pb.desc(),
    wrappers_pb.desc(),
)


Result = (
    Oneof[Literal["parse_error"], str]
    | Oneof[Literal["serialize_error"], str]
    | Oneof[Literal["timeout_error"], str]
    | Oneof[Literal["runtime_error"], str]
    | Oneof[Literal["protobuf_payload"], bytes]
    | Oneof[Literal["json_payload"], str]
    | Oneof[Literal["skipped"], str]
    | Oneof[Literal["jspb_payload"], str]
    | Oneof[Literal["text_payload"], str]
)


def do_test(request: ConformanceRequest) -> Result:
    if request.requested_output_format == WireFormat.TEXT_FORMAT:
        return Oneof(field="skipped", value="text output not supported")

    desc = REGISTRY.message(request.message_type)
    if desc is None:
        return Oneof(field="runtime_error", value="message not supported")
    message_type = desc.type
    assert request.payload

    match request.payload:
        case Oneof(field="protobuf_payload", value=v):
            try:
                message = message_type.from_binary(v)
                # We parse extensions lazily. To exercise the conformance tests for
                # UTF-8 validation, we eagerly parse all recognized extensions.
                if uf := message._unknown_fields:
                    for field_number in uf:
                        if ext := REGISTRY.extension_for(message, field_number):
                            message[ext.type]
            except AssertionError as e:
                return Oneof(
                    field="runtime_error",
                    value="Unexpected assertion error in from_binary: " + repr(e),
                )
            except Exception as e:  # noqa: BLE001
                return Oneof(field="parse_error", value=repr(e))
        case Oneof(field="json_payload", value=v):
            try:
                ignore_unknown_fields = (
                    request.test_category
                    == TestCategory.JSON_IGNORE_UNKNOWN_PARSING_TEST
                )
                message = message_type.from_json(
                    v, ignore_unknown_fields=ignore_unknown_fields, registry=REGISTRY
                )
            except AssertionError as e:
                return Oneof(
                    field="runtime_error",
                    value="Unexpected assertion error in from_json: " + repr(e),
                )
            except NotImplementedError:
                return Oneof(field="runtime_error", value="not implemented")
            except Exception as e:  # noqa: BLE001
                return Oneof(field="parse_error", value=repr(e))
        case _:
            return Oneof(field="skipped", value="only protobuf or json input supported")

    if request.requested_output_format == WireFormat.PROTOBUF:
        try:
            return Oneof(field="protobuf_payload", value=message.to_binary())
        except AssertionError as e:
            return Oneof(
                field="runtime_error",
                value="Unexpected assertion error in to_binary: " + repr(e),
            )
        except Exception as e:  # noqa: BLE001
            return Oneof(field="serialize_error", value=repr(e))

    if request.requested_output_format == WireFormat.JSON:
        try:
            return Oneof(field="json_payload", value=message.to_json(registry=REGISTRY))
        except AssertionError as e:
            return Oneof(
                field="runtime_error",
                value="Unexpected assertion error in to_json: " + repr(e),
            )
        except Exception as e:  # noqa: BLE001
            return Oneof(field="serialize_error", value=repr(e))

    return Oneof(field="skipped", value="only protobuf or json output supported")


def do_test_io() -> bool:
    length_bytes = sys.stdin.buffer.read(4)
    if len(length_bytes) == 0:
        return False  # EOF
    if len(length_bytes) != 4:
        msg = "I/O error"
        raise OSError(msg)

    length = struct.unpack("<I", length_bytes)[0]
    serialized_request = sys.stdin.buffer.read(length)
    if len(serialized_request) != length:
        msg = "I/O error"
        raise OSError(msg)

    request = ConformanceRequest.from_binary(serialized_request)
    result = do_test(request)
    serialized_response = ConformanceResponse(result=result).to_binary()

    sys.stdout.buffer.write(struct.pack("<I", len(serialized_response)))
    sys.stdout.buffer.write(serialized_response)
    sys.stdout.buffer.flush()

    return True


def main() -> None:
    while do_test_io():
        pass


if __name__ == "__main__":
    main()
