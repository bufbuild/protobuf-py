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

from types import MappingProxyType
from typing import TYPE_CHECKING, cast

import pytest

from protobuf import Oneof
from protobuf.wkt import ListValue, NullValue, Struct, Value

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from protobuf.wkt._mixin._struct import ValueTypeParam, ValueTypeReturn


class TestStruct:
    @pytest.mark.parametrize(
        ("proto", "python"),
        [
            pytest.param(Struct(), {}, id="empty"),
            pytest.param(
                Struct(
                    fields={
                        "null": Value(
                            kind=Oneof(field="null_value", value=NullValue.NULL_VALUE)
                        ),
                        "bool": Value(kind=Oneof(field="bool_value", value=True)),
                        "number": Value(kind=Oneof(field="number_value", value=1.5)),
                        "string": Value(
                            kind=Oneof(field="string_value", value="hello")
                        ),
                    }
                ),
                {"null": None, "bool": True, "number": 1.5, "string": "hello"},
                id="scalar_fields",
            ),
            pytest.param(
                Struct(
                    fields={
                        "list": Value(
                            kind=Oneof(
                                field="list_value",
                                value=ListValue(
                                    values=[
                                        Value(
                                            kind=Oneof(
                                                field="null_value",
                                                value=NullValue.NULL_VALUE,
                                            )
                                        ),
                                        Value(
                                            kind=Oneof(field="bool_value", value=False)
                                        ),
                                        Value(
                                            kind=Oneof(field="number_value", value=2.0)
                                        ),
                                        Value(
                                            kind=Oneof(
                                                field="string_value", value="nested"
                                            )
                                        ),
                                    ]
                                ),
                            )
                        ),
                        "struct": Value(
                            kind=Oneof(
                                field="struct_value",
                                value=Struct(
                                    fields={
                                        "nested": Value(
                                            kind=Oneof(
                                                field="string_value", value="field"
                                            )
                                        )
                                    }
                                ),
                            )
                        ),
                    }
                ),
                {"list": [None, False, 2.0, "nested"], "struct": {"nested": "field"}},
                id="nested_fields",
            ),
        ],
    )
    def test_roundtrip(self, proto: Struct, python: dict[str, ValueTypeReturn]) -> None:
        assert proto.to_python() == python
        assert Struct.from_python(python) == proto

    def test_from_python_mapping(self) -> None:
        data = cast(
            "Mapping[str, ValueTypeParam]", MappingProxyType({"a": 1, "b": ("x", None)})
        )

        assert Struct.from_python(data) == Struct(
            fields={
                "a": Value(kind=Oneof(field="number_value", value=1.0)),
                "b": Value(
                    kind=Oneof(
                        field="list_value",
                        value=ListValue(
                            values=[
                                Value(kind=Oneof(field="string_value", value="x")),
                                Value(
                                    kind=Oneof(
                                        field="null_value", value=NullValue.NULL_VALUE
                                    )
                                ),
                            ]
                        ),
                    )
                ),
            }
        )


class TestValue:
    @pytest.mark.parametrize(
        ("proto", "python"),
        [
            pytest.param(
                Value(kind=Oneof(field="null_value", value=NullValue.NULL_VALUE)),
                None,
                id="null_value",
            ),
            pytest.param(
                Value(kind=Oneof(field="bool_value", value=True)), True, id="bool_value"
            ),
            pytest.param(
                Value(kind=Oneof(field="number_value", value=1.0)),
                1.0,
                id="number_value",
            ),
            pytest.param(
                Value(kind=Oneof(field="string_value", value="hello")),
                "hello",
                id="string_value",
            ),
            pytest.param(
                Value(
                    kind=Oneof(
                        field="struct_value",
                        value=Struct(
                            fields={
                                "a": Value(kind=Oneof(field="number_value", value=1.0)),
                                "b": Value(
                                    kind=Oneof(field="string_value", value="bear")
                                ),
                            }
                        ),
                    )
                ),
                {"a": 1.0, "b": "bear"},
                id="struct_value",
            ),
            pytest.param(
                Value(
                    kind=Oneof(
                        field="list_value",
                        value=ListValue(
                            values=[
                                Value(kind=Oneof(field="number_value", value=1.0)),
                                Value(kind=Oneof(field="string_value", value="foo")),
                            ]
                        ),
                    )
                ),
                [1.0, "foo"],
                id="list_value",
            ),
        ],
    )
    def test_roundtrip(self, proto: Value, python: ValueTypeReturn) -> None:
        assert proto.to_python() == python
        assert Value.from_python(python) == proto

    def test_unknown_null_value(self) -> None:
        assert (
            Value(kind=Oneof(field="null_value", value=NullValue(99))).to_python()
            is None
        )

    @pytest.mark.parametrize(
        ("proto", "python"),
        [
            pytest.param(
                Value(kind=Oneof(field="number_value", value=1.0)), 1, id="positive"
            ),
            pytest.param(
                Value(kind=Oneof(field="number_value", value=-2.0)), -2, id="negative"
            ),
        ],
    )
    def test_from_python_int(self, proto: Value, python: int) -> None:
        assert Value.from_python(python) == proto

    def test_from_python_mapping(self) -> None:
        data = cast(
            "Mapping[str, ValueTypeParam]", MappingProxyType({"a": 1, "b": True})
        )

        assert Value.from_python(data) == Value(
            kind=Oneof(
                field="struct_value",
                value=Struct(
                    fields={
                        "a": Value(kind=Oneof(field="number_value", value=1.0)),
                        "b": Value(kind=Oneof(field="bool_value", value=True)),
                    }
                ),
            )
        )

    def test_from_python_sequence(self) -> None:
        assert Value.from_python(("x", 1, False)) == Value(
            kind=Oneof(
                field="list_value",
                value=ListValue(
                    values=[
                        Value(kind=Oneof(field="string_value", value="x")),
                        Value(kind=Oneof(field="number_value", value=1.0)),
                        Value(kind=Oneof(field="bool_value", value=False)),
                    ]
                ),
            )
        )

    def test_to_python_without_kind(self) -> None:
        with pytest.raises(ValueError, match="no kind set"):
            Value().to_python()

    def test_from_python_bytes(self) -> None:
        with pytest.raises(TypeError, match="unsupported type for Value: bytes"):
            Value.from_python(b"bytes")

    def test_from_python_unsupported_type(self) -> None:
        with pytest.raises(TypeError, match="unsupported type for Value: object"):
            Value.from_python(cast("ValueTypeParam", object()))


class TestListValue:
    @pytest.mark.parametrize(
        ("proto", "python"),
        [
            pytest.param(ListValue(), [], id="empty"),
            pytest.param(
                ListValue(
                    values=[
                        Value(
                            kind=Oneof(field="null_value", value=NullValue.NULL_VALUE)
                        ),
                        Value(kind=Oneof(field="bool_value", value=True)),
                        Value(kind=Oneof(field="number_value", value=1.0)),
                        Value(kind=Oneof(field="string_value", value="hello")),
                        Value(
                            kind=Oneof(
                                field="struct_value",
                                value=Struct(
                                    fields={
                                        "a": Value(
                                            kind=Oneof(field="number_value", value=2.0)
                                        )
                                    }
                                ),
                            )
                        ),
                        Value(
                            kind=Oneof(
                                field="list_value",
                                value=ListValue(
                                    values=[
                                        Value(
                                            kind=Oneof(field="bool_value", value=False)
                                        )
                                    ]
                                ),
                            )
                        ),
                    ]
                ),
                [None, True, 1.0, "hello", {"a": 2.0}, [False]],
                id="mixed_values",
            ),
            pytest.param(
                ListValue(values=[Value(kind=Oneof(field="number_value", value=1.0))]),
                [1.0],
                id="single_value",
            ),
        ],
    )
    def test_roundtrip(self, proto: ListValue, python: list[ValueTypeReturn]) -> None:
        assert proto.to_python() == python
        assert ListValue.from_python(python) == proto

    def test_from_python_sequence(self) -> None:
        data = cast("Sequence[ValueTypeParam]", (None, "x", 1))

        assert ListValue.from_python(data) == ListValue(
            values=[
                Value(kind=Oneof(field="null_value", value=NullValue.NULL_VALUE)),
                Value(kind=Oneof(field="string_value", value="x")),
                Value(kind=Oneof(field="number_value", value=1.0)),
            ]
        )
