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

import keyword

import pytest

from protobuf._sanitization import (
    escape_class_name,
    escape_enum_attr,
    escape_extension_name,
    escape_identifier,
    escape_message_attr,
    escape_proto_module_component,
)


@pytest.mark.parametrize(
    ("ident", "expected"),
    [
        pytest.param("some_name", "some_name", id="plain"),
        pytest.param("some-name", "some_name", id="hyphen"),
        pytest.param("some🐻name", "some_name", id="unicode"),
        pytest.param("class", "class_", id="keyword"),
        pytest.param("class_", "class__", id="keyword-closure"),
        pytest.param("_private", "pb__private", id="leading-underscore"),
        pytest.param("pb_private", "pb_pb_private", id="reserved-prefix"),
        pytest.param("foo_pb", "foo_pb_", id="reserved-suffix"),
        pytest.param("foo_pb_", "foo_pb__", id="reserved-suffix-closure"),
        pytest.param("123name", "pb__123name", id="leading-digit"),
        pytest.param("name with spaces", "name_with_spaces", id="spaces"),
        pytest.param("name.with.dots", "name_with_dots", id="dots"),
    ],
)
def test_escape_proto_module_component(ident: str, expected: str) -> None:
    assert escape_proto_module_component(ident) == expected


@pytest.mark.parametrize(
    ("ident", "expected"),
    [
        pytest.param("some_name", "some_name", id="plain"),
        pytest.param("some-name", "some_name_59107c75", id="hyphen"),
        pytest.param("some🐻name", "some_name_ba04169c", id="unicode"),
        pytest.param("class", "class_", id="keyword"),
        pytest.param("class_", "class__", id="keyword-closure"),
        pytest.param("_private", "pb__private", id="leading-underscore"),
        pytest.param("pb_private", "pb_pb_private", id="reserved-prefix"),
        pytest.param("foo_pb", "foo_pb_", id="reserved-suffix"),
        pytest.param("foo_pb_", "foo_pb__", id="reserved-suffix-closure"),
        pytest.param("123name", "pb__123name", id="leading-digit"),
        pytest.param("name with spaces", "name_with_spaces_78162a09", id="spaces"),
        pytest.param("name.with.dots", "name_with_dots_3e12f374", id="dots"),
    ],
)
def test_escape_proto_module_component_hash(ident: str, expected: str) -> None:
    assert escape_proto_module_component(ident, escape_with_hash=True) == expected


@pytest.mark.parametrize(
    ("ident", "expected"),
    [
        pytest.param("some_name", "some_name", id="plain"),
        pytest.param("desc", "desc_", id="message-classmethod-desc"),
        pytest.param("desc_", "desc__", id="message-classmethod-desc-closure"),
        pytest.param("_present", "pb__present", id="message-attribute"),
        pytest.param("_unknown_fields", "pb__unknown_fields", id="message-attribute-2"),
        pytest.param("has_field", "has_field_", id="message-method-has-field"),
        pytest.param(
            "has_field_", "has_field__", id="message-method-has-field-closure"
        ),
        pytest.param("clear_field", "clear_field_", id="message-method-clear-field"),
        pytest.param(
            "clear_field_", "clear_field__", id="message-method-clear-field-closure"
        ),
        pytest.param("to_json", "to_json_", id="message-method"),
        pytest.param("to_json_", "to_json__", id="message-method-closure"),
        pytest.param("to_binary", "to_binary_", id="message-method-binary"),
        pytest.param("to_binary_", "to_binary__", id="message-method-binary-closure"),
        pytest.param("from_json", "from_json_", id="message-classmethod-from-json"),
        pytest.param(
            "from_json_", "from_json__", id="message-classmethod-from-json-closure"
        ),
        pytest.param(
            "from_binary", "from_binary_", id="message-classmethod-from-binary"
        ),
        pytest.param(
            "from_binary_",
            "from_binary__",
            id="message-classmethod-from-binary-closure",
        ),
        pytest.param("self", "self_", id="self"),
        pytest.param("self_", "self__", id="self-closure"),
        pytest.param("_", "pb__", id="underscore-only"),
        pytest.param("_private", "pb__private", id="leading-underscore"),
        pytest.param("_private_", "pb__private_", id="leading-underscore-suffixed"),
        pytest.param("pb_private", "pb_pb_private", id="reserved-prefix"),
        pytest.param("_class", "pb__class", id="leading-underscore-reserved"),
        pytest.param("__init__", "pb___init__", id="dunder"),
        # Class name collision cases
        pytest.param("int", "int", id="int-preserved"),
        pytest.param("str", "str", id="str-preserved"),
        pytest.param("bytes", "bytes", id="bytes-preserved"),
        pytest.param("float", "float", id="float-preserved"),
        pytest.param("bool", "bool", id="bool-preserved"),
        pytest.param("list", "list", id="list-preserved"),
        pytest.param("dict", "dict", id="dict-preserved"),
        pytest.param("int_", "int__", id="int_-escaped"),
        pytest.param("str_", "str__", id="str-escaped"),
        pytest.param("bytes_", "bytes__", id="bytes-escaped"),
        pytest.param("float_", "float__", id="float-escaped"),
        pytest.param("bool_", "bool__", id="bool-escaped"),
        pytest.param("list_", "list__", id="list-escaped"),
        pytest.param("dict_", "dict__", id="dict-escaped"),
    ],
)
def test_escape_message_attr(ident: str, expected: str) -> None:
    assert escape_message_attr(ident) == expected


@pytest.mark.parametrize(
    ("ident", "expected"),
    [
        pytest.param("some_name", "some_name", id="plain"),
        pytest.param("name", "name_", id="enum-name"),
        pytest.param("name_", "name__", id="enum-name-closure"),
        pytest.param("value", "value_", id="enum-value"),
        pytest.param("value_", "value__", id="enum-value-closure"),
        pytest.param("class", "class_", id="keyword"),
        pytest.param("class_", "class__", id="keyword-closure"),
        pytest.param("mro", "mro_", id="mro"),
        pytest.param("mro_", "mro__", id="mro-closure"),
        pytest.param("desc", "desc_", id="desc"),
        pytest.param("desc_", "desc__", id="desc-closure"),
        pytest.param("_private", "pb__private", id="leading-underscore"),
        pytest.param("pb_private", "pb_pb_private", id="reserved-prefix"),
    ],
)
def test_escape_enum_attr(ident: str, expected: str) -> None:
    assert escape_enum_attr(ident) == expected


@pytest.mark.parametrize(
    ("ident", "expected"),
    [
        pytest.param("SomeClass", "SomeClass", id="plain"),
        pytest.param("class", "class_", id="keyword"),
        pytest.param("to_json", "to_json_", id="message-classmethod"),
        pytest.param("ext_message", "pb_ext_message", id="extension-prefix"),
        pytest.param(
            "pb_ext_message", "pb_pb_ext_message", id="extension-reserved-prefix"
        ),
        pytest.param("int", "int_", id="built-in-int"),
        pytest.param("str", "str_", id="built-in-str"),
        pytest.param("bytes", "bytes_", id="built-in-bytes"),
        pytest.param("float", "float_", id="built-in-float"),
        pytest.param("bool", "bool_", id="built-in-bool"),
        pytest.param("list", "list_", id="built-in-list"),
        pytest.param("dict", "dict_", id="built-in-dict"),
    ],
)
def test_escape_class_name(ident: str, expected: str) -> None:
    assert escape_class_name(ident) == expected


@pytest.mark.parametrize(
    ("ident", "expected"),
    [
        pytest.param("field", "ext_field", id="simple"),
        pytest.param("ext_field", "ext_ext_field", id="prefixed"),
        pytest.param("_field", "ext__field", id="leading-underscore"),
        pytest.param("class", "ext_class", id="reserved-word"),
    ],
)
def test_escape_extension_name(ident: str, expected: str) -> None:
    assert escape_extension_name(ident) == expected


class TestEscapeIdentifier:
    @pytest.mark.parametrize(("keyword"), keyword.kwlist)
    def test_hard_keyword(self, keyword: str) -> None:
        assert escape_identifier(keyword) == f"{keyword}_"

    @pytest.mark.parametrize(("keyword"), keyword.softkwlist)
    def test_soft_keyword(self, keyword: str) -> None:
        assert escape_identifier(keyword) == keyword
