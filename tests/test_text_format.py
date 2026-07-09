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

import math
import re

import pytest

from protobuf import Oneof, Registry
from protobuf.txtpb import merge_from_text, message_from_text, message_to_text
from protobuf.wkt import Any, any_pb

from .conformance.gen.conformance.messages import (
    test_messages_proto2_pb,
    test_messages_proto3_pb,
)
from .conformance.gen.conformance.messages.test_messages_edition2023_pb import (
    TestAllTypesEdition2023 as Edition2023,
)
from .conformance.gen.conformance.messages.test_messages_proto2_pb import (
    TestAllTypesProto2 as Proto2,
)
from .conformance.gen.conformance.messages.test_messages_proto3_pb import (
    TestAllTypesProto3 as Proto3,
)
from .gen import extensions_proto2_pb
from .gen.extensions_proto2_pb import (
    GroupExt,
    Proto2Extendee,
    Proto2ExtMessage,
    ext_groupext,
    ext_repeated_message_ext,
    ext_string_ext,
)


class TestRoundTrip:
    def test_proto3(self) -> None:
        want = Proto3(
            optional_int32=-42,
            optional_int64=-9223372036854775808,
            optional_uint32=4294967295,
            optional_uint64=18446744073709551615,
            optional_sint64=-1,
            optional_fixed32=7,
            optional_float=0.5,
            optional_double=12345.6789,
            optional_bool=True,
            optional_string='a "quote", tab\t, newline\n, é 🎉',
            optional_bytes=bytes([0, 1, 2, 0x7F, 0x80, 0xFF]),
            optional_nested_message=Proto3.NestedMessage(a=17),
            optional_nested_enum=Proto3.NestedEnum.BAZ,
            repeated_int32=[1, 2, 3],
            repeated_string=["x", "y"],
            repeated_nested_message=[
                Proto3.NestedMessage(a=1),
                Proto3.NestedMessage(a=2),
            ],
            map_string_string={"one": "1", "two": "2"},
            map_int32_int32={1: 10, 2: 20},
            map_string_nested_message={"k": Proto3.NestedMessage(a=5)},
            oneof_field=Oneof("oneof_uint32", 123),
        )
        text = message_to_text(want)
        got = message_from_text(Proto3, text)
        assert got == want, text
        assert message_to_text(got) == text

    def test_proto2(self) -> None:
        # proto3 has no groups, required fields, closed enums, or explicit
        # defaults, so a proto2 message covers what proto3 cannot.
        want = Proto2(
            optional_int32=-7,
            optional_int64=9223372036854775807,
            optional_string="hello",
            optional_nested_enum=Proto2.NestedEnum.NEG,
            data=Proto2.Data(group_int32=5, group_uint32=6),
            repeated_nested_enum=[Proto2.NestedEnum.FOO, Proto2.NestedEnum.BAZ],
        )
        text = message_to_text(want)
        got = message_from_text(Proto2, text)
        assert got == want, text
        assert message_to_text(got) == text

    @pytest.mark.parametrize(
        ("default_int32", "default_string"),
        [
            pytest.param(5, "x", id="non-default values"),
            pytest.param(-123456789, "Rosebud", id="values equal to the default"),
        ],
    )
    def test_proto2_explicit_defaults(
        self, default_int32: int, default_string: str
    ) -> None:
        # Explicit presence means a field set even to its default value is
        # emitted and round-trips; an unset one is omitted.
        want = Proto2(default_int32=default_int32, default_string=default_string)
        text = message_to_text(want)
        assert "default_int32:" in text
        assert message_from_text(Proto2, text) == want, text

    def test_unset_defaults(self) -> None:
        assert message_to_text(Proto2()) == ""
        assert message_from_text(Proto2, "").default_string == "Rosebud"


class TestToTextFormatting:
    def test_basic_formatting(self) -> None:
        msg = Proto3(
            optional_int32=1,
            optional_nested_message=Proto3.NestedMessage(a=2),
            repeated_int32=[3, 4],
        )
        assert message_to_text(msg) == (
            "optional_int32: 1\n"
            "optional_nested_message {\n  a: 2\n}\n"
            "repeated_int32: 3\n"
            "repeated_int32: 4\n"
        )

    def test_declaration_order(self) -> None:
        # Fields are emitted in declaration order. In this proto declaration
        # order happens to equal field-number order, so a regression to sorting
        # by number is caught instead by the extension-ordering test below,
        # where the two orders disagree.
        msg = Proto3(optional_int32=1, recursive_message=Proto3(optional_int32=2))
        assert message_to_text(msg) == (
            "optional_int32: 1\nrecursive_message {\n  optional_int32: 2\n}\n"
        )

    def test_empty_submessage(self) -> None:
        msg = Proto3(optional_nested_message=Proto3.NestedMessage())
        assert message_to_text(msg) == "optional_nested_message {}\n"

    def test_empty_message(self) -> None:
        assert message_to_text(Proto3()) == ""

    def test_no_colon_before_brace(self) -> None:
        # The colon is optional for message-valued fields per the text format
        # spec, and the canonical google.protobuf.text_format writer omits it
        # (verified directly against google.protobuf.text_format.MessageToString).
        # protobuf-es's writer always includes it; we deliberately match the
        # canonical C++/Python behavior instead.
        msg = Proto3(optional_nested_message=Proto3.NestedMessage(a=1))
        assert ": {" not in message_to_text(msg)
        assert "optional_nested_message {" in message_to_text(msg)

    def test_string_escaping(self) -> None:
        # Controls, quotes, C1 controls (\x85 is NEL, U+0085), and raw UTF-8.
        msg = Proto3(optional_string='tab\tnl\n"q"\\b\x7f\x85é')
        assert (
            message_to_text(msg)
            == 'optional_string: "tab\\tnl\\n\\"q\\"\\\\b\\x7f\\u0085é"\n'
        )

    def test_bytes_escaping(self) -> None:
        # 0x00 -> \x00, A raw, 0xc3 0xa9 is valid UTF-8 "é" raw, 0xff invalid.
        msg = Proto3(optional_bytes=bytes([0x00, 0x41, 0xC3, 0xA9, 0xFF]))
        assert message_to_text(msg) == 'optional_bytes: "\\x00Aé\\xff"\n'

    def test_non_mnemonic_c0_controls(self) -> None:
        # 0x07/0x08/0x0b/0x0c have C mnemonics (\a \b \v \f) but the write path
        # deliberately does not use them; only \n \r \t are mnemonics. This
        # matches protobuf-go.
        msg = Proto3(optional_bytes=bytes([0x07, 0x08, 0x0B, 0x0C]))
        assert message_to_text(msg) == 'optional_bytes: "\\x07\\x08\\x0b\\x0c"\n'

    @pytest.mark.parametrize(
        ("value", "repr_"),
        [
            pytest.param(math.inf, "inf", id="inf"),
            pytest.param(-math.inf, "-inf", id="-inf"),
            pytest.param(math.nan, "nan", id="nan"),
            pytest.param(-0.0, "-0", id="-0"),
        ],
    )
    def test_float_special_values(self, value: float, repr_: str) -> None:
        # -0.0 is not the zero value, so it counts as set even with implicit
        # presence, and its sign must survive.
        msg = Proto3(optional_double=value)
        assert message_to_text(msg) == f"optional_double: {repr_}\n"

    def test_float32_shortest_decimal(self) -> None:
        parsed = message_from_text(Proto3, "optional_float: 0.1")
        assert parsed.optional_float == 0.10000000149011612
        assert message_to_text(parsed) == "optional_float: 0.1\n"
        # float overflow prints inf.
        overflowed = message_from_text(Proto3, "optional_float: 1e50")
        assert message_to_text(overflowed) == "optional_float: inf\n"
        # float underflow to negative zero keeps its sign.
        underflowed = Proto3(optional_float=-1e-50)
        assert message_to_text(underflowed) == "optional_float: -0\n"

    def test_enum_names(self) -> None:
        named = Proto3(optional_nested_enum=Proto3.NestedEnum.BAZ)
        assert message_to_text(named) == "optional_nested_enum: BAZ\n"
        # 99 is an open-enum value outside the known set.
        unknown = Proto3(optional_nested_enum=Proto3.NestedEnum(99))
        assert message_to_text(unknown) == "optional_nested_enum: 99\n"

    def test_enum_aliases(self) -> None:
        # AliasedEnum declares ALIAS_BAZ = 2 first, then MOO, moo, and bAz as
        # aliases. The first declaration wins, matching protobuf-go.
        msg = Proto3(optional_aliased_enum=Proto3.AliasedEnum.MOO)
        assert message_to_text(msg) == "optional_aliased_enum: ALIAS_BAZ\n"

    def test_enum_int_or_member(self) -> None:
        by_member = Proto3(optional_nested_enum=Proto3.NestedEnum.BAZ)
        by_int = Proto3()
        # Assign a plain int; the runtime accepts it in place of an Enum.
        setattr(by_int, "optional_nested_enum", 2)  # noqa: B010
        assert (
            message_to_text(by_member)
            == message_to_text(by_int)
            == "optional_nested_enum: BAZ\n"
        )


class TestFromTextScalars:
    @pytest.mark.parametrize(
        ("text", "field", "expected"),
        [
            pytest.param("optional_int32: 0x7fffffff", "optional_int32", 2147483647),
            pytest.param("optional_int32: -010", "optional_int32", -8),
            pytest.param("optional_uint32: 0xff", "optional_uint32", 255),
            pytest.param(
                "optional_int64: -9223372036854775808",
                "optional_int64",
                -9223372036854775808,
            ),
            pytest.param(
                "optional_uint64: 18446744073709551615",
                "optional_uint64",
                18446744073709551615,
            ),
        ],
    )
    def test_int_bases(self, text: str, field: str, expected: int) -> None:
        assert getattr(message_from_text(Proto3, text), field) == expected

    def test_float_literals(self) -> None:
        assert message_from_text(Proto3, "optional_float: 1.5f").optional_float == 1.5
        assert (
            message_from_text(Proto3, "optional_float: 1e50").optional_float == math.inf
        )
        assert math.isnan(
            message_from_text(Proto3, "optional_float: NaN").optional_float
        )
        assert (
            message_from_text(Proto3, "optional_double: -Infinity").optional_double
            == -math.inf
        )

    @pytest.mark.parametrize("bad", [".e5", ".E5", "-.e5", "1.e", ".", "-."])
    def test_rejects_no_significand(self, bad: str) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, f"optional_float: {bad}")

    @pytest.mark.parametrize(
        ("literal", "expected"),
        [
            *[pytest.param(t, True, id=t) for t in ("true", "True", "t", "1")],
            *[pytest.param(f, False, id=f) for f in ("false", "False", "f", "0")],
        ],
    )
    def test_bool_literals(self, literal: str, expected: bool) -> None:
        msg = message_from_text(Proto3, f"optional_bool: {literal}")
        assert msg.optional_bool is expected

    def test_adjacent_string_literals(self) -> None:
        msg = message_from_text(Proto3, 'optional_string: "foo" \'bar\' "baz"')
        assert msg.optional_string == "foobarbaz"

    def test_escape_sequences(self) -> None:
        msg = message_from_text(Proto3, 'optional_string: "\\u0041\\x42\\103"')
        assert msg.optional_string == "ABC"
        msg = message_from_text(Proto3, 'optional_bytes: "\\xde\\xad"')
        assert msg.optional_bytes == b"\xde\xad"

    def test_rejects_invalid_utf8(self) -> None:
        # The same escaped byte is legal for a bytes field (see above), but a
        # string field must hold valid UTF-8.
        with pytest.raises(ValueError, match="invalid UTF-8"):
            message_from_text(Proto3, 'optional_string: "\\xff"')


class TestSignMatrix:
    def test_sign_whitespace(self) -> None:
        assert message_from_text(Proto3, "optional_int32: - 42").optional_int32 == -42
        assert (
            message_from_text(Proto3, "optional_double: -inf").optional_double
            == -math.inf
        )

    def test_rejects_minus_nan(self) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, "optional_double: -nan")

    def test_sign_glued_to_inf(self) -> None:
        # Whitespace may separate the sign from digits, but not from a float
        # literal: "-inf" is negative infinity, "- inf" is an error. This
        # matches protobuf-go.
        assert (
            message_from_text(Proto3, "optional_double: -infinity").optional_double
            == -math.inf
        )
        for bad in (
            "optional_double: - inf",
            "optional_double: - infinity",
            "optional_double: - nan",
        ):
            with pytest.raises(ValueError):  # noqa: PT011
                message_from_text(Proto3, bad)

    @pytest.mark.parametrize(
        "bad",
        [
            "optional_uint32: -1",
            "optional_uint32: -0",
            "optional_uint64: -1",
            "optional_bool: -1",
            "optional_bool: -0",
        ],
    )
    def test_rejects_sign_on_unsigned_and_bool(self, bad: str) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, bad)

    def test_sign_on_enum(self) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto2, "optional_nested_enum: -BAZ")
        # A sign on an enum number is fine.
        msg = message_from_text(Proto3, "optional_nested_enum: -1")
        assert msg.optional_nested_enum == -1


class TestFromTextStructure:
    def test_colon_optional_for_messages(self) -> None:
        msg = message_from_text(Proto3, "optional_nested_message { a: 1 }")
        assert msg.optional_nested_message is not None
        assert msg.optional_nested_message.a == 1
        with pytest.raises(ValueError, match="expected"):
            message_from_text(Proto3, "optional_int32 1")

    def test_angle_brackets(self) -> None:
        msg = message_from_text(Proto3, "optional_nested_message < a: 7 >")
        assert msg.optional_nested_message is not None
        assert msg.optional_nested_message.a == 7

    def test_repeated_and_list_syntax(self) -> None:
        msg = message_from_text(
            Proto3, "repeated_int32: 1 repeated_int32: 2 repeated_int32: 3"
        )
        assert msg.repeated_int32 == [1, 2, 3]
        msg = message_from_text(Proto3, "repeated_int32: [4, 5, 6]")
        assert msg.repeated_int32 == [4, 5, 6]

    def test_comments_and_separators(self) -> None:
        msg = message_from_text(
            Proto3, "# a comment\noptional_int32: 1, # trailing\noptional_int64: 2;"
        )
        assert msg.optional_int32 == 1
        assert msg.optional_int64 == 2

    def test_leading_bom(self) -> None:
        assert message_from_text(Proto3, "﻿optional_int32: 1").optional_int32 == 1

    @pytest.mark.parametrize(
        "text",
        [
            pytest.param("  # nothing here\n", id="comment only"),
            pytest.param("", id="empty"),
        ],
    )
    def test_empty_input(self, text: str) -> None:
        assert message_from_text(Proto3, text) == Proto3()


class TestSeparators:
    @pytest.mark.parametrize("sep", [",", ";"])
    def test_trailing_separator(self, sep: str) -> None:
        msg = message_from_text(Proto3, f"optional_int32: 1{sep}")
        assert msg.optional_int32 == 1

    @pytest.mark.parametrize(
        "bad",
        [
            "optional_int32: 1;;",
            "optional_int32: 1,,",
            "repeated_int32: [1,]",
            "repeated_int32: [1,,2]",
            "optional_nested_message { a: 1,, }",
        ],
    )
    def test_rejects_doubled_separators(self, bad: str) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, bad)

    def test_list_separator(self) -> None:
        # Non-string list elements need a separator.
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, "repeated_int32: [1 2]")
        # Adjacent string literals concatenate into a single element.
        msg = message_from_text(Proto3, 'repeated_string: ["a" "b"]')
        assert msg.repeated_string == ["ab"]
        msg = message_from_text(Proto3, 'repeated_string: ["a", "b"]')
        assert msg.repeated_string == ["a", "b"]

    def test_rejects_trailing_tokens(self) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, "optional_int32: 1 }")


class TestMaps:
    def test_insertion_order(self) -> None:
        msg = message_from_text(
            Proto3,
            'map_string_string { key: "a" value: "b" }'
            ' map_string_string { key: "c" value: "d" }',
        )
        assert msg.map_string_string == {"a": "b", "c": "d"}

    def test_duplicate_key_across_entries(self) -> None:
        msg = message_from_text(
            Proto3,
            "map_int32_int32 { key: 1 value: 2 } map_int32_int32 { key: 1 value: 3 }",
        )
        assert msg.map_int32_int32 == {1: 3}

    @pytest.mark.parametrize(
        "bad",
        [
            pytest.param("map_int32_int32 { key: 1 key: 2 value: 3 }", id="key"),
            pytest.param("map_int32_int32 { key: 1 value: 2 value: 3 }", id="value"),
        ],
    )
    def test_rejects_duplicate_key_or_value(self, bad: str) -> None:
        with pytest.raises(ValueError, match="already set"):
            message_from_text(Proto3, bad)

    def test_missing_key_or_value(self) -> None:
        msg = message_from_text(Proto3, 'map_string_string { value: "v" }')
        assert msg.map_string_string == {"": "v"}
        msg = message_from_text(Proto3, "map_int32_int32 { key: 7 }")
        assert msg.map_int32_int32 == {7: 0}

    def test_output_insertion_order(self) -> None:
        # We emit entries in insertion order; protobuf-go would sort them to
        # a, b, c. This is a deliberate divergence shared with protobuf-es.
        msg = Proto3(map_string_string={"b": "1", "a": "2", "c": "3"})
        keys = re.findall(r'key: "(\w)"', message_to_text(msg))
        assert keys == ["b", "a", "c"]

    def test_bool_and_int64_keys(self) -> None:
        msg = message_from_text(
            Proto3,
            "map_bool_bool { key: true value: false }"
            " map_int64_int64 { key: -9223372036854775808 value: 1 }",
        )
        assert msg.map_bool_bool == {True: False}
        assert msg.map_int64_int64 == {-9223372036854775808: 1}
        assert message_from_text(Proto3, message_to_text(msg)) == msg


class TestFromTextErrors:
    def test_unknown_field(self) -> None:
        with pytest.raises(ValueError, match="unknown field"):
            message_from_text(Proto3, "no_such_field: 1")

    def test_reserved_field(self) -> None:
        msg = message_from_text(Proto3, "reserved_field: 123 optional_int32: 7")
        assert msg.optional_int32 == 7

    def test_repeated_singular_and_oneof(self) -> None:
        with pytest.raises(ValueError, match="repeated"):
            message_from_text(Proto3, "optional_int32: 1 optional_int32: 2")
        with pytest.raises(ValueError, match="oneof"):
            message_from_text(Proto3, 'oneof_uint32: 1 oneof_string: "x"')

    def test_field_by_number(self) -> None:
        with pytest.raises(ValueError, match="by number"):
            message_from_text(Proto3, "5: 1")

    def test_out_of_range_int(self) -> None:
        with pytest.raises(OverflowError, match="out of range"):
            message_from_text(Proto3, "optional_int32: 2147483648")

    def test_octal(self) -> None:
        assert message_from_text(Proto3, "optional_int32: 010").optional_int32 == 8
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, "optional_int32: 08")
        # Octal and hexadecimal are not valid for float fields.
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, "optional_float: 010")

    @pytest.mark.parametrize("bad", ["\\ud800", "\\ud801\\udc37", "\\U00110000"])
    def test_surrogate_escapes(self, bad: str) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto3, f"optional_string: '{bad}'")

    def test_recursion_limit(self) -> None:
        nested = "optional_int32: 1"
        for _ in range(200):
            nested = f"recursive_message {{ {nested} }}"
        with pytest.raises(RecursionError, match="recursion"):
            message_from_text(Proto3, nested)

    def test_recursion_limit_reserved_skip(self) -> None:
        # A reserved field whose value is a deeply nested message must not
        # bypass the limit.
        skip = "reserved_field { " + "a { " * 200
        with pytest.raises(RecursionError, match="recursion"):
            message_from_text(Proto3, skip)

    def test_recursion_limit_map_entry(self) -> None:
        # Nesting through map entry values must not bypass the limit.
        nested = "optional_int32: 1"
        for _ in range(100):
            nested = (
                'map_string_nested_message { key: "k"'
                f" value {{ corecursive {{ {nested} }} }} }}"
            )
        with pytest.raises(RecursionError, match="recursion"):
            message_from_text(Proto3, nested)


class TestIgnoreUnknownFields:
    def test_unknown_field_skipped(self) -> None:
        msg = message_from_text(
            Proto3, "no_such_field: 1 optional_int32: 7", ignore_unknown_fields=True
        )
        assert msg.optional_int32 == 7

    def test_unknown_extension_skipped(self) -> None:
        registry = Registry(extensions_proto2_pb.desc())
        msg = message_from_text(
            Proto2Extendee,
            "[proto2ext.nope]: 1 own_field: 7",
            registry=registry,
            ignore_unknown_fields=True,
        )
        assert msg.own_field == 7

    def test_default_still_raises(self) -> None:
        with pytest.raises(ValueError, match="unknown field"):
            message_from_text(Proto3, "no_such_field: 1")

    def test_merge_from_text_skips(self) -> None:
        msg = Proto3()
        merge_from_text(
            msg, "no_such_field: 1 optional_int32: 7", ignore_unknown_fields=True
        )
        assert msg.optional_int32 == 7


class TestClosedVersusOpenEnums:
    def test_closed_enum(self) -> None:
        msg = message_from_text(Proto2, "optional_nested_enum: BAZ")
        assert msg.optional_nested_enum == 2
        with pytest.raises(ValueError):  # noqa: PT011
            message_from_text(Proto2, "optional_nested_enum: 99")

    def test_open_enum(self) -> None:
        msg = message_from_text(Proto3, "optional_nested_enum: 99")
        assert msg.optional_nested_enum == 99

    def test_negative_closed_enum(self) -> None:
        want = Proto2(optional_nested_enum=Proto2.NestedEnum.NEG)
        text = message_to_text(want)
        assert text == "optional_nested_enum: NEG\n"
        assert message_from_text(Proto2, text) == want


class TestGroups:
    def test_group_name_and_lowercase_alias(self) -> None:
        msg = Proto2(data=Proto2.Data(group_int32=5))
        assert message_to_text(msg) == "Data {\n  group_int32: 5\n}\n"
        for name in ("Data", "data"):
            parsed = message_from_text(Proto2, f"{name} {{ group_int32: 9 }}")
            assert parsed.data is not None
            assert parsed.data.group_int32 == 9

    def test_group_extension(self) -> None:
        # A group declared as an extension is addressed by its extension field
        # full name (lowercase), never by the group message name — the
        # opposite of a regular group field above. (conformance
        # GroupFieldExtension / GroupFieldExtensionGroupName.)
        registry = Registry(extensions_proto2_pb.desc())
        msg = Proto2Extendee()
        msg[ext_groupext] = GroupExt(a=7)
        text = message_to_text(msg, registry=registry)
        assert "[proto2ext.groupext]" in text
        assert "GroupExt" not in text
        got = message_from_text(Proto2Extendee, text, registry=registry)
        assert got[ext_groupext] == GroupExt(a=7)
        # Addressing it by the GroupExt message name is rejected.
        with pytest.raises(ValueError, match="unknown extension"):
            message_from_text(
                Proto2Extendee, "[proto2ext.GroupExt] { a: 1 }", registry=registry
            )


class TestEditionsDelimited:
    # delimited_encoding here comes from [features.message_encoding=DELIMITED],
    # not the proto2 `group` keyword — group_like_message must treat them
    # identically.

    def test_group_like(self) -> None:
        want = Edition2023(groupliketype=Edition2023.GroupLikeType(group_int32=5))
        text = message_to_text(want)
        assert text.startswith("GroupLikeType {")
        assert message_from_text(Edition2023, text) == want
        for name in ("GroupLikeType", "groupliketype"):
            parsed = message_from_text(Edition2023, f"{name} {{ group_int32: 9 }}")
            assert parsed.groupliketype is not None
            assert parsed.groupliketype.group_int32 == 9

    def test_non_group_like(self) -> None:
        want = Edition2023(delimited_field=Edition2023.GroupLikeType())
        text = message_to_text(want)
        assert text.startswith("delimited_field {}")
        assert message_from_text(Edition2023, text) == want


class TestExtensions:
    registry = Registry(extensions_proto2_pb.desc())

    def test_sorted_after_regular_fields(self) -> None:
        msg = Proto2Extendee(own_field=1)
        msg[ext_string_ext] = "hello"
        msg[ext_repeated_message_ext] = [
            Proto2ExtMessage(string_field="x"),
            Proto2ExtMessage(string_field="y"),
        ]
        text = message_to_text(msg, registry=self.registry)
        assert '[proto2ext.string_ext]: "hello"' in text
        # Regular fields come first, then extensions sorted by full name.
        own_index = text.index("own_field")
        repeated_index = text.index("[proto2ext.repeated_message_ext]")
        string_index = text.index("[proto2ext.string_ext]")
        assert own_index < repeated_index < string_index, text
        got = message_from_text(Proto2Extendee, text, registry=self.registry)
        assert got[ext_string_ext] == "hello"
        assert len(got[ext_repeated_message_ext]) == 2

    def test_no_registry(self) -> None:
        msg = Proto2Extendee(own_field=1)
        msg[ext_string_ext] = "hello"
        assert message_to_text(msg) == "own_field: 1\n"

    def test_unknown_extension(self) -> None:
        with pytest.raises(ValueError, match="unknown extension"):
            message_from_text(
                Proto2Extendee, "[proto2ext.nope]: 1", registry=self.registry
            )

    def test_repeated_singular_extension(self) -> None:
        with pytest.raises(ValueError, match=re.escape("[proto2ext.string_ext]")):
            message_from_text(
                Proto2Extendee,
                '[proto2ext.string_ext]: "a" [proto2ext.string_ext]: "b"',
                registry=self.registry,
            )

    def test_wrong_extendee(self) -> None:
        # string_ext extends Proto2Extendee, not Proto2ExtMessage.
        with pytest.raises(ValueError, match="unknown extension"):
            message_from_text(
                Proto2ExtMessage, '[proto2ext.string_ext]: "x"', registry=self.registry
            )


class TestAny:
    registry = Registry(test_messages_proto3_pb.desc(), any_pb.desc())

    def test_expanded_form(self) -> None:
        payload = Proto3(optional_int32=42)
        any_ = Any.pack(payload)
        text = message_to_text(any_, registry=self.registry)
        assert text == (
            "[type.googleapis.com/protobuf_test_messages.proto3.TestAllTypesProto3]"
            " {\n  optional_int32: 42\n}\n"
        )
        assert message_from_text(Any, text, registry=self.registry) == any_

    def test_no_registry(self) -> None:
        any_ = Any.pack(Proto3(optional_int32=1))
        text = message_to_text(any_)
        assert text.startswith("type_url: ")
        assert "\nvalue: " in text

    def test_expanded_then_raw(self) -> None:
        # The expansion marks type_url and value as seen, so a following raw
        # field trips the duplicate-field check.
        with pytest.raises(ValueError, match="repeated"):
            message_from_text(
                Any,
                "[type.googleapis.com/protobuf_test_messages.proto3"
                '.TestAllTypesProto3] {} type_url: "x"',
                registry=self.registry,
            )

    def test_raw_then_expanded(self) -> None:
        with pytest.raises(ValueError, match="expanded form"):
            message_from_text(
                Any,
                'type_url: "x" [type.googleapis.com/protobuf_test_messages.proto3'
                ".TestAllTypesProto3] {}",
                registry=self.registry,
            )

    def test_unresolvable_type_url(self) -> None:
        with pytest.raises(ValueError, match="unable to resolve"):
            message_from_text(
                Any, "[type.googleapis.com/no.such.Type] {}", registry=self.registry
            )

    def test_invalid_percent_escape(self) -> None:
        with pytest.raises(ValueError, match="percent-escape"):
            message_from_text(
                Any, "[type.googleapis.com/%ZZ/foo.Bar] {}", registry=self.registry
            )


class TestLoneSurrogates:
    def test_lone_surrogate(self) -> None:
        msg = Proto3(optional_string="\ud800")
        back = message_from_text(Proto3, message_to_text(msg))
        assert back.optional_string == "�"


class TestMergeFromText:
    def test_repeated_and_message_merge(self) -> None:
        msg = Proto3(
            repeated_int32=[1], optional_nested_message=Proto3.NestedMessage(a=1)
        )
        merge_from_text(
            msg,
            "repeated_int32: 2"
            " optional_nested_message { corecursive { optional_int32: 9 } }",
        )
        assert msg.repeated_int32 == [1, 2]
        assert msg.optional_nested_message is not None
        assert msg.optional_nested_message.a == 1
        assert msg.optional_nested_message.corecursive is not None
        assert msg.optional_nested_message.corecursive.optional_int32 == 9

    def test_singular_and_map_overwrite(self) -> None:
        msg = Proto3(optional_int32=1, map_string_string={"k": "old", "keep": "me"})
        merge_from_text(
            msg, 'optional_int32: 2 map_string_string { key: "k" value: "new" }'
        )
        assert msg.optional_int32 == 2
        assert msg.map_string_string == {"k": "new", "keep": "me"}

    def test_repeated_extension(self) -> None:
        registry = Registry(extensions_proto2_pb.desc())
        msg = Proto2Extendee()
        msg[ext_repeated_message_ext] = [Proto2ExtMessage(string_field="x")]
        merge_from_text(
            msg,
            '[proto2ext.repeated_message_ext] { string_field: "y" }',
            registry=registry,
        )
        assert [m.string_field for m in msg[ext_repeated_message_ext]] == ["x", "y"]


class TestUnknownFields:
    def test_default_omitted_opt_in_printed(self) -> None:
        data = Proto3(optional_int32=1).to_binary()
        # Append an unknown varint field 999 = 5. Tag = (999 << 3) | 0.
        msg = Proto3.from_binary(data + bytes([0xB8, 0x3E, 0x05]))
        assert message_to_text(msg) == "optional_int32: 1\n"
        assert (
            message_to_text(msg, print_unknown_fields=True)
            == "optional_int32: 1\n999: 5\n"
        )

    def test_numbered_output_unparseable(self) -> None:
        with pytest.raises(ValueError, match="by number"):
            message_from_text(Proto3, "999: 5")

    def test_fixed_width_hex(self) -> None:
        # Field 999 as fixed32 (wire type 5) and fixed64 (wire type 1).
        fixed32 = bytes([0xBD, 0x3E]) + (0xDEADBEEF).to_bytes(4, "little")
        fixed64 = bytes([0xB9, 0x3E]) + (0xDEADBEEF).to_bytes(8, "little")
        msg = Proto3.from_binary(fixed32 + fixed64)
        assert message_to_text(msg, print_unknown_fields=True) == (
            "999: 0xdeadbeef\n999: 0x00000000deadbeef\n"
        )

    def test_length_delimited(self) -> None:
        # Field 999 length-delimited (tag 0xba 0x3e). b"\x08\x01" parses as
        # field 1 varint 1; b"\xff" does not parse and prints as quoted bytes.
        # A parsed-as-message unknown field has no colon before its brace,
        # matching the same rule as a named message-valued field.
        nested = bytes([0xBA, 0x3E, 0x02, 0x08, 0x01])
        opaque = bytes([0xBA, 0x3E, 0x01, 0xFF])
        assert (
            message_to_text(Proto3.from_binary(nested), print_unknown_fields=True)
            == "999 {\n  1: 1\n}\n"
        )
        assert (
            message_to_text(Proto3.from_binary(opaque), print_unknown_fields=True)
            == '999: "\\xff"\n'
        )

    def test_group(self) -> None:
        # Field 999 as a group (start 0xbb 0x3e ... end 0xbc 0x3e) holding
        # field 1 varint 1, and an empty group. Groups are message-valued, so
        # no colon before the brace, same as above.
        group = bytes([0xBB, 0x3E, 0x08, 0x01, 0xBC, 0x3E])
        empty = bytes([0xBB, 0x3E, 0xBC, 0x3E])
        assert (
            message_to_text(Proto3.from_binary(group), print_unknown_fields=True)
            == "999 {\n  1: 1\n}\n"
        )
        assert (
            message_to_text(Proto3.from_binary(empty), print_unknown_fields=True)
            == "999 {}\n"
        )


class TestPythonInput:
    @pytest.mark.parametrize(
        "text",
        [
            pytest.param(b"optional_int32: 1", id="bytes"),
            pytest.param(bytearray(b"optional_int32: 1"), id="bytearray"),
            pytest.param(b"\xef\xbb\xbfoptional_int32: 1", id="bytes with BOM"),
        ],
    )
    def test_bytes_input(self, text: bytes | bytearray) -> None:
        assert message_from_text(Proto3, text).optional_int32 == 1

    def test_no_required_field_validation(self) -> None:
        # Unlike to_binary and to_json, text serialization intentionally
        # accepts a message with unset required fields, like protobuf-es.
        msg = test_messages_proto2_pb.TestAllRequiredTypesProto2()
        assert message_to_text(msg) == ""

    def test_multi_word_group_name(self) -> None:
        msg = Proto2(multiwordgroupfield=Proto2.MultiWordGroupField(group_int32=1))
        text = message_to_text(msg)
        assert text.startswith("MultiWordGroupField {")
        assert message_from_text(Proto2, text) == msg
        # An arbitrary case variation of the group name is not accepted.
        with pytest.raises(ValueError, match="unknown field"):
            message_from_text(Proto2, "MULTIWORDGROUPFIELD { group_int32: 1 }")
