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
"""Message operations for the Buf ``protobuf`` API.

Port of the subset of fleetbench ``receiver.h`` that maps to idiomatic
end-user code, as the base class of the generated ``Access``. Several C++
operations are intentionally omitted (see the note at the bottom): they
measure C++ runtime internals or arena mechanics rather than the user-facing
message code this benchmark compares.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from protobuf import merge_from

if TYPE_CHECKING:
    from protobuf import Message


class Ops:
    """Idiomatic message operations (C++ ``receiver.h``) for the Buf API."""

    def merge(self, message: Message, other_message: Message) -> None:
        merge_from(message, other_message)

    def serialize(self, message: Message) -> bytes:
        return message.to_binary()

    def parse(self, message_cls: type[Message], serialized: bytes) -> Message:
        return message_cls.from_binary(serialized)


# Operations from receiver.h handled idiomatically inline by the lifecycle, or
# omitted as not representative of user code:
#
# - Receive:     a bare field-access expression in the Get functions; the C++
#                copy-to-defeat-optimization helper would only add call noise.
# - Create:      message constructor (`MessageType()`); C++ reuses arena slots.
# - Copy:        copy.deepcopy; C++ CopyFrom mutates in place.
# - Swap:        reference swap; C++ swaps contents in place.
# - Destroy:     no-op; Python frees via garbage collection.
# - ByteSize:    a cheap non-allocating count in C++/google; Buf protobuf does
#                not implement it (users don't need it), so omitted to keep the
#                comparison meaningful.
# - Descriptor / EnumDescriptor / IsInitialized / Reflection / SpaceUsed:
#                C++ reflection and arena-accounting internals.
