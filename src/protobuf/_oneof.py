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

from contextlib import suppress
from typing import Final, Generic, TypeVar, final

__all__ = ["Oneof"]

C = TypeVar("C", bound=str)
V = TypeVar("V")


@final
class Oneof(Generic[C, V]):  # noqa: PLW1641
    """A oneof value with a field name and typed value.

    This class represents a oneof field value in protobuf messages. It combines
    a field name (the field name within the oneof) with its typed value, enabling
    type-safe pattern matching.

    Attributes:
        field: The name of the active oneof field
        value: The typed value for this field

    Examples:
        ```python
        a = Oneof(field="a", value="hello")
        match a:
            case Oneof(field="a", value=v):
                print(f"Got string: {v}")
            case Oneof(field="b", value=v):
                print(f"Got int: {v}")
        # Got string: hello
        ```
    """

    __slots__ = ("field", "value")
    __match_args__ = ("field", "value")

    field: Final[C]
    value: Final[V]

    def __init__(self, field: C, value: V) -> None:
        """Initializes a new Oneof.

        Args:
            field: The name of the active oneof field
            value: The typed value for this field
        """
        self.field = field
        self.value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Oneof):
            return self.field == other.field and self.value == other.value
        return False

    def __repr__(self) -> str:
        return f"Oneof(field={self.field!r}, value={self.value!r})"


with suppress(ImportError):
    import protobuf_ext

    # Assigning to globals ensures docs / type checking pick up the rich Python type
    # while runtime uses the native implementation.
    globals()["Oneof"] = protobuf_ext.Oneof
