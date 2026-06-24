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

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Literal, TypeAlias, TypeVar

if TYPE_CHECKING:
    from protobuf import Oneof
    from protobuf.wkt import ListValue, NullValue, Struct, Value


ValueTypeParam: TypeAlias = (
    None
    | bool
    | int
    | float
    | str
    | Sequence["ValueTypeParam"]
    | Mapping[str, "ValueTypeParam"]
)
ValueTypeReturn: TypeAlias = (
    None | bool | float | str | list["ValueTypeReturn"] | dict[str, "ValueTypeReturn"]
)


SelfStruct = TypeVar("SelfStruct", bound="StructMixin")


class StructMixin:
    __slots__ = ()

    if TYPE_CHECKING:

        def __init__(self, *, fields: dict[str, Value] | None = None) -> None:
            pass

        fields: dict[str, Value]

    @classmethod
    def from_python(
        cls: type[SelfStruct], data: Mapping[str, ValueTypeParam]
    ) -> SelfStruct:
        """Create a Struct from a Python dict.

        Examples:
            >>> from protobuf.wkt import Struct
            >>> Struct.from_python({"a": 1, "b": "bear"})
            Struct(fields={'a': Value(kind=Oneof(field='number_value', value=1.0)), 'b': Value(kind=Oneof(field='string_value', value='bear'))})
        """
        from protobuf.wkt import Value  # noqa: PLC0415

        return cls(fields={k: Value.from_python(v) for k, v in data.items()})

    def to_python(self) -> dict[str, ValueTypeReturn]:
        """Convert this Struct to a Python dict.

        Examples:
            >>> from protobuf import Oneof
            >>> from protobuf.wkt import Struct, Value
            >>> Struct(
            ...     fields={
            ...         "a": Value(kind=Oneof(field="number_value", value=1.0)),
            ...         "b": Value(kind=Oneof(field="string_value", value="bear")),
            ...     }
            ... ).to_python()
            {'a': 1.0, 'b': 'bear'}
        """
        return {k: v.to_python() for k, v in self.fields.items()}


SelfValue = TypeVar("SelfValue", bound="ValueMixin")


class ValueMixin:
    __slots__ = ()

    if TYPE_CHECKING:

        def __init__(
            self,
            *,
            kind: Oneof[Literal["null_value"], NullValue]
            | Oneof[Literal["number_value"], float]
            | Oneof[Literal["string_value"], str]
            | Oneof[Literal["bool_value"], bool]
            | Oneof[Literal["struct_value"], Struct]
            | Oneof[Literal["list_value"], ListValue]
            | None = None,
        ) -> None: ...

        kind: (
            Oneof[Literal["null_value"], NullValue]
            | Oneof[Literal["number_value"], float]
            | Oneof[Literal["string_value"], str]
            | Oneof[Literal["bool_value"], bool]
            | Oneof[Literal["struct_value"], Struct]
            | Oneof[Literal["list_value"], ListValue]
            | None
        )

    @classmethod
    def from_python(cls: type[SelfValue], value: ValueTypeParam) -> SelfValue:
        """Create a Value from a Python value.

        Args:
            value: The Python value to convert. `int` values are converted to `float`.

        Returns:
            A Value representing the given Python value.

        Raises:
            TypeError: If the value is of an unsupported type, including `bytes`.

        Examples:
            >>> from protobuf.wkt import Value
            >>> Value.from_python(None)
            Value(kind=Oneof(field='null_value', value=NullValue.NULL_VALUE))
            >>> Value.from_python(True)
            Value(kind=Oneof(field='bool_value', value=True))
            >>> Value.from_python(2)
            Value(kind=Oneof(field='number_value', value=2.0))
            >>> Value.from_python(3.14)
            Value(kind=Oneof(field='number_value', value=3.14))
            >>> Value.from_python("hello")
            Value(kind=Oneof(field='string_value', value='hello'))
            >>> Value.from_python([1, "foo"])
            Value(kind=Oneof(field='list_value', value=ListValue(values=[Value(kind=Oneof(field='number_value', value=1.0)), Value(kind=Oneof(field='string_value', value='foo'))])))
            >>> Value.from_python({"a": 1, "b": "bear"})
            Value(kind=Oneof(field='struct_value', value=Struct(fields={'a': Value(kind=Oneof(field='number_value', value=1.0)), 'b': Value(kind=Oneof(field='string_value', value='bear'))})))
        """
        from protobuf import Oneof  # noqa: PLC0415
        from protobuf.wkt import ListValue, NullValue, Struct  # noqa: PLC0415

        if isinstance(value, bytes):
            msg = "unsupported type for Value: bytes"
            raise TypeError(msg)

        match value:
            case None:
                return cls(kind=Oneof(field="null_value", value=NullValue.NULL_VALUE))
            case bool():
                return cls(kind=Oneof(field="bool_value", value=value))
            case int() | float():
                return cls(kind=Oneof(field="number_value", value=float(value)))
            case str():
                return cls(kind=Oneof(field="string_value", value=value))
            case Mapping() as m:
                return cls(
                    kind=Oneof(field="struct_value", value=Struct.from_python(m))
                )
            case Sequence() as s:
                return cls(
                    kind=Oneof(field="list_value", value=ListValue.from_python(s))
                )
            case _:
                msg = f"unsupported type for Value: {type(value).__name__}"
                raise TypeError(msg)

    def to_python(self) -> ValueTypeReturn:
        """Convert this Value to a Python value.

        Examples:
            >>> from protobuf import Oneof
            >>> from protobuf.wkt import ListValue, NullValue, Struct, Value
            >>> Value(
            ...     kind=Oneof(field="null_value", value=NullValue.NULL_VALUE)
            ... ).to_python()
            >>> Value(kind=Oneof(field="bool_value", value=True)).to_python()
            True
            >>> Value(kind=Oneof(field="number_value", value=3.14)).to_python()
            3.14
            >>> Value(kind=Oneof(field="string_value", value="hello")).to_python()
            'hello'
            >>> Value(
            ...     kind=Oneof(
            ...         field="list_value",
            ...         value=ListValue(
            ...             values=[
            ...                 Value(kind=Oneof(field="number_value", value=1.0)),
            ...                 Value(kind=Oneof(field="string_value", value="foo")),
            ...             ]
            ...         ),
            ...     )
            ... ).to_python()
            [1.0, 'foo']
            >>> Value(
            ...     kind=Oneof(
            ...         field="struct_value",
            ...         value=Struct(
            ...             fields={
            ...                 "a": Value(kind=Oneof(field="number_value", value=1.0)),
            ...                 "b": Value(
            ...                     kind=Oneof(field="string_value", value="bear")
            ...                 ),
            ...             }
            ...         ),
            ...     )
            ... ).to_python()
            {'a': 1.0, 'b': 'bear'}
        """
        from protobuf import Oneof  # noqa: PLC0415

        match self.kind:
            case Oneof(
                field="null_value"  # Protobuf implementations typically ignore value
            ):
                return None
            case Oneof(field="bool_value", value=b):
                return b
            case Oneof(field="number_value", value=n):
                return n
            case Oneof(field="string_value", value=s):
                return s
            case Oneof(field="struct_value", value=s):
                return s.to_python()
            case Oneof(field="list_value", value=l):
                return l.to_python()
            case None:
                msg = "no kind set"
                raise ValueError(msg)


SelfListValue = TypeVar("SelfListValue", bound="ListValueMixin")


class ListValueMixin:
    __slots__ = ()

    if TYPE_CHECKING:

        def __init__(self, *, values: list[Value] | None = None) -> None: ...

        values: list[Value]

    @classmethod
    def from_python(
        cls: type[SelfListValue], values: Sequence[ValueTypeParam]
    ) -> SelfListValue:
        """Create a ListValue from a list of Python values.

        Examples:
            >>> from protobuf.wkt import ListValue
            >>> ListValue.from_python([1, "foo"])
            ListValue(values=[Value(kind=Oneof(field='number_value', value=1.0)), Value(kind=Oneof(field='string_value', value='foo'))])
        """
        from protobuf.wkt import Value  # noqa: PLC0415

        return cls(values=[Value.from_python(v) for v in values])

    def to_python(self) -> list[ValueTypeReturn]:
        """Convert this ListValue to a list of Python values.

        Examples:
            >>> from protobuf import Oneof
            >>> from protobuf.wkt import ListValue, Value
            >>> ListValue(
            ...     values=[
            ...         Value(kind=Oneof(field="number_value", value=1.0)),
            ...         Value(kind=Oneof(field="string_value", value="foo")),
            ...     ]
            ... ).to_python()
            [1.0, 'foo']
        """
        return [v.to_python() for v in self.values]
