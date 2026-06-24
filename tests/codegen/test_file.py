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

from protobuf import (
    DescEnum,
    DescField,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescMessage,
    DescOneof,
    ScalarType,
)
from protobuf.wkt import Edition, FeatureSet, MethodOptions
from tests.gen.enums_pb import Color, EnumMessage

if TYPE_CHECKING:
    from tests.conftest import Protoc


class TestDescFile:
    def test_proto2_syntax(self, protoc: Protoc) -> None:
        desc = protoc.compile_file('syntax = "proto2";')
        assert desc.edition == Edition.PROTO2

    def test_proto3_syntax(self, protoc: Protoc) -> None:
        desc = protoc.compile_file('syntax = "proto3";')
        assert desc.edition == Edition.PROTO3

    def test_edition_2023(self, protoc: Protoc) -> None:
        desc = protoc.compile_file('edition = "2023";')
        assert desc.edition == Edition.EDITION_2023

    def test_dependencies(self, protoc: Protoc) -> None:
        result = protoc.compile(
            {
                "a.proto": """
        syntax="proto3";
        import "b.proto";
        import "c.proto";
        message A {
          B b = 1;
          C c = 2;
        }
      """,
                "b.proto": """
        syntax="proto3";
        message B {}
      """,
                "c.proto": """
        syntax="proto3";
        message C {}
      """,
            },
            "include_imports",
            "retain_options",
            "experimental_editions",
            "include_source_info",
        )
        a_desc = result["a.proto"]
        assert len(a_desc.dependencies) == 2
        assert a_desc.dependencies == [result["b.proto"], result["c.proto"]]


class TestDescMessage:
    def test_deprecated_is_false_by_default(self, protoc: Protoc) -> None:
        desc_msg = protoc.compile_message(
            """
                syntax="proto3";
                option deprecated = true;
                message Foo {}
            """
        )
        assert desc_msg.deprecated is False

    def test_deprecated_is_true_with_option(self, protoc: Protoc) -> None:
        desc_msg = protoc.compile_message(
            """
                syntax="proto3";
                message Foo {
                option deprecated = true;
                }
            """
        )
        assert desc_msg.deprecated is True

    def test_field_contains_field_by_local_name(self, protoc: Protoc) -> None:
        desc_msg = protoc.compile_message(
            """
                    syntax="proto3";
                    message Foo {
                        int32 foo_bar = 1;
                        oneof kind {
                            int32 oneof_field = 2;
                        }
                    }
                """
        )
        assert list(desc_msg._fields_by_local_name.keys()) == ["foo_bar"]
        assert list(desc_msg._oneofs_by_local_name.keys()) == ["kind"]

    def test_members_preserves_order(self, protoc: Protoc) -> None:
        desc_msg = protoc.compile_message(
            """
                    syntax="proto3";
                    message M {
                        int32 field1 = 1;
                        oneof first {
                            bool a = 2;
                        }
                        string field2 = 3;
                        oneof second {
                            bool b = 4;
                            int32 c = 5;
                        }
                        int32 field3 = 6;
                    }
                """
        )
        assert len(desc_msg.members) == 5
        assert isinstance(desc_msg.members[0], DescField)
        assert desc_msg.members[0].local_name == "field1"
        assert isinstance(desc_msg.members[1], DescOneof)
        assert desc_msg.members[1].local_name == "first"
        assert isinstance(desc_msg.members[2], DescField)
        assert desc_msg.members[2].local_name == "field2"
        assert isinstance(desc_msg.members[3], DescOneof)
        assert desc_msg.members[3].local_name == "second"
        assert isinstance(desc_msg.members[4], DescField)
        assert desc_msg.members[4].local_name == "field3"


class TestDescEnum:
    def test_open_proto3_enum_is_open(self, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                A = 0;
            }
            """
        )
        assert desc_enum.open is True

    def test_open_proto2_enum_is_closed(self, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            """
            syntax="proto2";
            enum E {
                A = 1;
            }
            """
        )
        assert desc_enum.open is False

    def test_open_edition_2023_enum_is_open_by_default(self, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            """
            edition="2023";
            enum E {
                A = 0;
            }
            """
        )
        assert desc_enum.open is True

    def test_open_edition_2023_enum_is_closed_by_file_feature(
        self, protoc: Protoc
    ) -> None:
        desc_enum = protoc.compile_enum(
            """
            edition="2023";
            option features.enum_type = CLOSED;
            enum E {
                A = 1;
            }
            """
        )
        assert desc_enum.open is False

    def test_open_edition_2023_enum_is_closed_by_enum_feature(
        self, protoc: Protoc
    ) -> None:
        desc_enum = protoc.compile_enum(
            """
            edition="2023";
            enum E {
                option features.enum_type = CLOSED;
                A = 1;
            }
            """
        )
        assert desc_enum.open is False

    class TestStrippingEnumPrefix:
        def test_all_match_upper_snake(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum {
                    MY_ENUM_A = 0;
                    MY_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "B"]

        def test_prefix_stripping_case_sensitive(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum {
                    MY_ENUM_A = 0;
                    my_enum_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "my_enum_B"]

        def test_prefix_stripping_underscore_sensitive(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum {
                    MY_ENUM_A = 0;
                    _MY_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "pb__MY_ENUM_B"]

        def test_prefix_stripping_enum_name_leading_underscore(
            self, protoc: Protoc
        ) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum _MyEnum {
                    MY_ENUM_A = 0;
                    _MY_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["MY_ENUM_A", "B"]

        def test_prefix_stripping_enum_name_trailing_underscore(
            self, protoc: Protoc
        ) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum_ {
                    MY_ENUM__A = 0;
                    MY_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "MY_ENUM_B"]

        def test_prefix_stripping_enum_name_mid_underscore(
            self, protoc: Protoc
        ) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum My_Enum {
                    MY_ENUM_A = 0;
                    MY_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "B"]

        def test_not_stripped_if_starts_with_number(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum {
                    MY_ENUM_A = 0;
                    MY_ENUM_23_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "MY_ENUM_23_B"]

        def test_acronym_in_enum_name(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum HTTPEnum {
                    HTTP_ENUM_A = 0;
                    HTTP_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["A", "B"]

        def test_prefix_matches_untransformed_enum_name(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum {
                    MyEnum_A = 0;
                    MyEnum_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["MyEnum_A", "MyEnum_B"]

        def test_prefix_number_with_upper(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum Model3D {
                    MODEL3D_UNSPECIFIED = 0;
                    MODEL3D_CUBE = 1;
                    MODEL_3D_SPHERE = 2;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == [
                "UNSPECIFIED",
                "CUBE",
                "MODEL_3D_SPHERE",
            ]

        def test_prefix_not_pascal_case(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum m3D {
                    M3D_UNSPECIFIED = 0;
                    M3D_CUBE = 1;
                    M_3D_SPHERE = 2;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == [
                "UNSPECIFIED",
                "CUBE",
                "M_3D_SPHERE",
            ]

        def test_stripped_prefix_empty(self, protoc: Protoc) -> None:
            desc_enum = protoc.compile_enum(
                """
                syntax="proto3";
                enum MyEnum {
                    MY_ENUM_ = 0;
                    MY_ENUM_B = 1;
                }
                """
            )
            assert [v.local_name for v in desc_enum.values] == ["MY_ENUM_", "B"]

    def test_deprecated_not_deprecated_by_default(self, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                A = 0;
            }
            """
        )
        assert desc_enum.deprecated is False

    def test_deprecated_deprecated_is_deprecated(self, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                option deprecated = true;
                A = 0;
            }
            """
        )
        assert desc_enum.deprecated is True

    def test_deprecated_file_is_not_deprecated(self, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            """
            syntax="proto3";
            option deprecated = true;
            enum E {
                A = 0;
            }
            """
        )
        assert desc_enum.deprecated is False


class TestDescEnumValue:
    @pytest.mark.parametrize("name", ["MY_ENUM_A", "foo", "__proto__"])
    def test_name_is_proto_name(self, name: str, protoc: Protoc) -> None:
        desc_enum = protoc.compile_enum(
            f"""
            syntax="proto3";
            enum MyEnum {{
                {name} = 0;
            }}
            """
        )
        assert desc_enum.values[0].name == name

    def test_local_name_does_not_change_case(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                FooBAR_baz_1 = 0;
            }
            """
        ).values[0]
        assert value.local_name == "FooBAR_baz_1"

    def test_local_name_drops_shared_prefix(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum PrefixEnum {
                PREFIX_ENUM_ZERO = 0;
                PREFIX_ENUM_ONE = 1;
            }
            """
        ).values[0]
        assert value.local_name == "ZERO"

    def test_local_name_escapes_reserved_property_name(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum EnumBuiltIn {
                as = 0;
            }
            """
        ).values[0]
        assert value.local_name == "as_"

    def test_local_name_escapes_reserved_property_name_with_dropped_prefix(
        self, protoc: Protoc
    ) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum EnumBuiltInPrefixed {
                ENUM_BUILT_IN_PREFIXED_True = 0;
            }
            """
        ).values[0]
        assert value.local_name == "True_"

    def test_deprecated_not_deprecated_by_default(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                A = 0;
            }
            """
        ).values[0]
        assert value.deprecated is False

    def test_deprecated_deprecated_is_deprecated(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                A = 0 [deprecated = true];
            }
            """
        ).values[0]
        assert value.deprecated is True

    def test_deprecated_enum_is_not_deprecated(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            enum E {
                option deprecated = true;
                A = 0;
            }
            """
        ).values[0]
        assert value.deprecated is False

    def test_deprecated_file_is_not_deprecated(self, protoc: Protoc) -> None:
        value = protoc.compile_enum(
            """
            syntax="proto3";
            option deprecated = true;
            enum E {
                A = 0;
            }
            """
        ).values[0]
        assert value.deprecated is False


class TestDescOneof:
    def test_local_name_escapes_reserved_property_name(self, protoc: Protoc) -> None:
        oneof = protoc.compile_message(
            """
                syntax="proto3";
                message M {
                    oneof class {
                        bool placeholder = 1;
                    }
                }
                """
        ).oneofs[0]
        assert oneof.local_name == "class_"

    def test_fields_has_member_fields(self, protoc: Protoc) -> None:
        oneof = protoc.compile_message(
            """
            syntax="proto3";
            message M {
                oneof tst {
                    bool a = 1;
                    bool b = 2;
                }
            }
            """
        ).oneofs[0]
        assert len(oneof.fields) == 2

    def test_fields_multiple_oneofs(self, protoc: Protoc) -> None:
        msg = protoc.compile_message(
            """
            syntax="proto3";
            message M {
                oneof first {
                    bool a = 1;
                    bool b = 2;
                }
                oneof second {
                    bool p = 3;
                    bool q = 4;
                }
            }
            """
        )
        assert len(msg.oneofs) == 2
        for oneof in msg.oneofs:
            assert len(oneof.fields) == 2
        assert len(msg.members) == 2
        assert isinstance(msg.members[0], DescOneof)
        assert msg.members[0].local_name == "first"
        assert isinstance(msg.members[1], DescOneof)
        assert msg.members[1].local_name == "second"

    def test_proto3_synthetic_oneofs_are_ignored(self, protoc: Protoc) -> None:
        msg = protoc.compile_message(
            """
                syntax="proto3";
                message M {
                    optional string in = 1;
                }
                """
        )
        assert len(msg.oneofs) == 0
        assert isinstance(msg._fields_by_local_name["in_"].value, DescFieldValueScalar)
        assert msg._fields_by_local_name["in_"].value.oneof is None


class TestDescService:
    def test_type_name(self, protoc: Protoc) -> None:
        service = protoc.compile_service(
            """
            syntax="proto3";
            package test;
            service Foo {}
            """
        )
        assert service.type_name == "test.Foo"

    def test_methods(self, protoc: Protoc) -> None:
        service = protoc.compile_service(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O);
                rpc Baz(I) returns(O);
            }
            message I {}
            message O {}
            """
        )
        assert len(service.methods) == 2
        assert service.deprecated is False

    def test_deprecated_is_false_by_default(self, protoc: Protoc) -> None:
        service = protoc.compile_service(
            """
            syntax="proto3";
            service Foo {}
            """
        )
        assert service.deprecated is False

    def test_deprecated_is_true_with_option(self, protoc: Protoc) -> None:
        service = protoc.compile_service(
            """
            syntax="proto3";
            service Foo {
                option deprecated = true;
            }
            """
        )
        assert service.deprecated is True


class TestDescMethod:
    def test_method_kind_unary(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O) {}
            }
            message I {}
            message O {}
            """
        )
        assert method.method_kind == "unary"

    def test_method_kind_server_streaming(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(stream O) {}
            }
            message I {}
            message O {}
            """
        )
        assert method.method_kind == "server_streaming"

    def test_method_kind_client_streaming(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(stream I) returns(O) {}
            }
            message I {}
            message O {}
            """
        )
        assert method.method_kind == "client_streaming"

    def test_method_kind_bidi_streaming(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(stream I) returns(stream O) {}
            }
            message I {}
            message O {}
            """
        )
        assert method.method_kind == "bidi_streaming"

    def test_idempotency_is_idempotency_unknown_if_unset(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O) {}
            }
            message I {}
            message O {}
            """
        )
        assert method.idempotency == MethodOptions.IdempotencyLevel.IDEMPOTENCY_UNKNOWN

    def test_idempotency_is_idempotency_unknown_if_set(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O) {
                    option idempotency_level = IDEMPOTENCY_UNKNOWN;
                }
            }
            message I {}
            message O {}
            """
        )
        assert method.idempotency == MethodOptions.IdempotencyLevel.IDEMPOTENCY_UNKNOWN

    def test_idempotency_is_no_side_effects_if_set(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O) {
                    option idempotency_level = NO_SIDE_EFFECTS;
                }
            }
            message I {}
            message O {}
            """
        )
        assert method.idempotency == MethodOptions.IdempotencyLevel.NO_SIDE_EFFECTS

    def test_idempotency_is_idempotent_if_set(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O) {
                    option idempotency_level = IDEMPOTENT;
                }
            }
            message I {}
            message O {}
            """
        )
        assert method.idempotency == MethodOptions.IdempotencyLevel.IDEMPOTENT

    def test_deprecated_is_false_by_default(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O);
            }
            message I {}
            message O {}
            """
        )
        assert method.deprecated is False

    def test_deprecated_is_true_with_option(self, protoc: Protoc) -> None:
        method = protoc.compile_method(
            """
            syntax="proto3";
            service Foo {
                rpc Bar(I) returns(O) {
                    option deprecated = true;
                }
            }
            message I {}
            message O {}
            """
        )
        assert method.deprecated is True


@pytest.mark.parametrize(
    ("proto", "expected"),
    [
        pytest.param(
            """
            syntax="proto2";
            message M { optional int32 f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto2 optional scalar is EXPLICIT",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { optional M f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto2 optional message is EXPLICIT",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { required int32 f = 1; }
            """,
            FeatureSet.FieldPresence.LEGACY_REQUIRED,
            id="proto2 required scalar is LEGACY_REQUIRED",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { required M f = 1; }
            """,
            FeatureSet.FieldPresence.LEGACY_REQUIRED,
            id="proto2 required message is LEGACY_REQUIRED",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { repeated int32 f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto2 scalar list is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { repeated M f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto2 message list is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { map <int32, int32> f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto2 scalar map is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { map <int32, M> f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto2 message map is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto2";
            message M { oneof kind { int32 f = 1; } }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto2 oneof is EXPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { int32 f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto3 scalar is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { optional int32 f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto3 optional scalar is EXPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { repeated int32 f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto3 scalar list is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { repeated M f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto3 message list is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { map <int32, int32> f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto3 scalar map is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { map <int32, M> f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="proto3 message map is IMPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { oneof kind { int32 f = 1; } }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto3 oneof is EXPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { M f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto3 message is EXPLICIT",
        ),
        pytest.param(
            """
            syntax="proto3";
            message M { optional M f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="proto3 optional message is EXPLICIT",
        ),
        pytest.param(
            """
            edition="2023";
            message M { int32 f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="edition2023 scalar is EXPLICIT",
        ),
        pytest.param(
            """
            edition="2023";
            option features.field_presence = IMPLICIT;
            message M { int32 f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="edition2023 scalar inherits IMPLICIT",
        ),
        pytest.param(
            """
            edition="2023";
            option features.field_presence = IMPLICIT;
            message M { M f = 1; }
            """,
            FeatureSet.FieldPresence.EXPLICIT,
            id="edition2023 message is EXPLICIT (does not inherit IMPLICIT)",
        ),
        pytest.param(
            """
            edition="2023";
            message M { repeated int32 f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="edition2023 scalar list is IMPLICIT",
        ),
        pytest.param(
            """
            edition="2023";
            message M { repeated M f = 1; }
            """,
            FeatureSet.FieldPresence.IMPLICIT,
            id="edition2023 message list is IMPLICIT",
        ),
        pytest.param(
            """
            edition="2023";
            message M { int32 f = 1 [features.field_presence = LEGACY_REQUIRED]; }
            """,
            FeatureSet.FieldPresence.LEGACY_REQUIRED,
            id="edition2023 scalar with LEGACY_REQUIRED is LEGACY_REQUIRED",
        ),
        pytest.param(
            """
            edition="2023";
            message M { M f = 1 [features.field_presence = LEGACY_REQUIRED]; }
            """,
            FeatureSet.FieldPresence.LEGACY_REQUIRED,
            id="edition2023 message with LEGACY_REQUIRED is LEGACY_REQUIRED",
        ),
    ],
)
def test_desc_field_presence(
    proto: str, expected: FeatureSet.FieldPresence, protoc: Protoc
) -> None:
    assert protoc.compile_field(proto).presence == expected


class TestDescFieldDelimitedEncoding:
    def test_true_for_proto2_group(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            """
            syntax="proto2";
            message M {
                optional group GroupField = 2 {}
            }
            """
        )
        assert isinstance(field.value, DescFieldValueMessage)
        assert field.value.delimited_encoding is True

    def test_true_for_field_with_message_encoding_delimited(
        self, protoc: Protoc
    ) -> None:
        field = protoc.compile_field(
            """
            edition="2023";
            message M {
                M f = 1 [features.message_encoding = DELIMITED];
            }
            """
        )
        assert isinstance(field.value, DescFieldValueMessage)
        assert field.value.delimited_encoding is True

    def test_true_for_list_field_with_message_encoding_delimited(
        self, protoc: Protoc
    ) -> None:
        field = protoc.compile_field(
            """
            edition="2023";
            message M {
                repeated M f = 1 [features.message_encoding = DELIMITED];
            }
            """
        )
        assert isinstance(field.value, DescFieldValueList)
        assert field.value.delimited_encoding is True

    def test_true_for_file_with_message_encoding_delimited(
        self, protoc: Protoc
    ) -> None:
        field = protoc.compile_field(
            """
            edition="2023";
            option features.message_encoding = DELIMITED;
            message M {
                M f = 1;
            }
            """
        )
        assert isinstance(field.value, DescFieldValueMessage)
        assert field.value.delimited_encoding is True


class TestDescFieldRepeatedPacking:
    def test_proto2_is_unpacked_by_default(self, protoc: Protoc) -> None:
        message = protoc.compile_message(
            """
            syntax="proto2";
            message M {
                repeated int32 default = 3;
                repeated int32 explicitly_packed = 4 [packed = true];
                repeated int32 explicitly_expanded = 5 [packed = false];
            }
            """
        )
        f = message.fields[0]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is False
        f = message.fields[1]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is True
        f = message.fields[2]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is False

    def test_proto3_is_packed_by_default(self, protoc: Protoc) -> None:
        message = protoc.compile_message(
            """
            syntax="proto3";
            message M {
                repeated int32 default = 3;
                repeated int32 explicitly_packed = 4 [packed = true];
                repeated int32 explicitly_expanded = 5 [packed = false];
            }
            """
        )
        f = message.fields[0]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is True
        f = message.fields[1]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is True
        f = message.fields[2]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is False

    def test_edition2023_is_packed_by_default(self, protoc: Protoc) -> None:
        message = protoc.compile_message(
            """
            edition="2023";
            message M {
                repeated int32 default = 3;
                repeated int32 explicitly_packed = 4 [features.repeated_field_encoding = PACKED];
                repeated int32 explicitly_expanded = 5 [features.repeated_field_encoding = EXPANDED];
            }
            """
        )
        f = message.fields[0]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is True
        f = message.fields[1]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is True
        f = message.fields[2]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is False

    def test_edition2023_with_repeated_field_encoding_file_option(
        self, protoc: Protoc
    ) -> None:
        message = protoc.compile_message(
            """
            edition="2023";
            option features.repeated_field_encoding = EXPANDED;
            message M {
                repeated int32 default = 3;
                repeated int32 explicitly_packed = 4 [features.repeated_field_encoding = PACKED];
            }
            """
        )
        f = message.fields[0]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is False
        f = message.fields[1]
        assert isinstance(f.value, DescFieldValueList)
        assert f.value.packed is True


@pytest.mark.parametrize(
    ("proto", "scalar"),
    [
        ("double", ScalarType.DOUBLE),
        ("float", ScalarType.FLOAT),
        ("int32", ScalarType.INT32),
        ("int64", ScalarType.INT64),
        ("uint32", ScalarType.UINT32),
        ("uint64", ScalarType.UINT64),
        ("sint32", ScalarType.SINT32),
        ("sint64", ScalarType.SINT64),
        ("fixed32", ScalarType.FIXED32),
        ("fixed64", ScalarType.FIXED64),
        ("sfixed32", ScalarType.SFIXED32),
        ("sfixed64", ScalarType.SFIXED64),
        ("bool", ScalarType.BOOL),
        ("string", ScalarType.STRING),
        ("bytes", ScalarType.BYTES),
    ],
)
def test_desc_field_scalar_types(
    proto: str, scalar: ScalarType, protoc: Protoc
) -> None:
    field = protoc.compile_field(f'syntax="proto3";\nmessage M {{ {proto} f = 1; }}')
    assert isinstance(field.value, DescFieldValueScalar)
    assert field.value.scalar == scalar


def test_desc_field_message_type(protoc: Protoc) -> None:
    field = protoc.compile_field('syntax="proto3";\nmessage M { M nested = 1; }')
    assert isinstance(field.value, DescFieldValueMessage)
    assert isinstance(field.value.message, DescMessage)
    assert field.value.message.type_name == "M"


def test_desc_field_enum_type(protoc: Protoc) -> None:
    field = protoc.compile_field(
        'syntax="proto3";\nenum E { A = 0; }\nmessage M { E e = 1; }'
    )
    assert isinstance(field.value, DescFieldValueEnum)
    assert isinstance(field.value.enum, DescEnum)
    assert field.value.enum.type_name == "E"


class TestDescFieldListTypes:
    def test_repeated_scalar(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            'syntax="proto3";\nmessage M { repeated int32 f = 1; }'
        )
        assert isinstance(field.value, DescFieldValueList)
        assert field.value.element == ScalarType.INT32

    def test_repeated_message(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            'syntax="proto3";\nmessage M { repeated M f = 1; }'
        )
        assert isinstance(field.value, DescFieldValueList)
        assert isinstance(field.value.element, DescMessage)
        assert field.value.element.type_name == "M"

    def test_repeated_enum(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            'syntax="proto3";\nenum E { A = 0; }\nmessage M { repeated E f = 1; }'
        )
        assert isinstance(field.value, DescFieldValueList)
        assert isinstance(field.value.element, DescEnum)
        assert field.value.element.type_name == "E"


class TestDescFieldMapTypes:
    def test_map_with_scalar_value(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            'syntax="proto3";\nmessage M { map<string, int32> f = 1; }'
        )
        assert isinstance(field.value, DescFieldValueMap)
        assert field.value.key == ScalarType.STRING
        assert field.value.value == ScalarType.INT32

    def test_map_with_message_value(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            'syntax="proto3";\nmessage M { map<string, M> f = 1; }'
        )
        assert isinstance(field.value, DescFieldValueMap)
        assert field.value.key == ScalarType.STRING
        assert isinstance(field.value.value, DescMessage)
        assert field.value.value.type_name == "M"

    def test_map_with_enum_value(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            'syntax="proto3";\nenum E { A = 0; }\nmessage M { map<int32, E> f = 1; }'
        )
        assert isinstance(field.value, DescFieldValueMap)
        assert field.value.key == ScalarType.INT32
        assert isinstance(field.value.value, DescEnum)
        assert field.value.value.type_name == "E"


class TestDescField:
    def test_local_name_escapes_reserved_property_name(self, protoc: Protoc) -> None:
        field = protoc.compile_field(
            """
            syntax="proto3";
            message M {
                int32 class = 1;
            }
            """
        )
        assert field.local_name == "class_"

    def test_local_name_field_in_oneof_does_not_escape_reserved_property_name(
        self, protoc: Protoc
    ) -> None:
        field = protoc.compile_field(
            """
            syntax="proto3";
            message M {
                oneof kind {
                    int32 class = 1;
                }
            }
            """
        )
        assert field.local_name == "class"

    @pytest.mark.parametrize("name", ["field", "foo_bar", "__proto__", "class"])
    def test_json_name_returns_compiler_provided(
        self, name: str, protoc: Protoc
    ) -> None:
        field = protoc.compile_field(
            f"""
            syntax="proto3";
            message M {{
                int32 {name} = 1;
            }}
            """
        )
        assert field.json_name == field.proto.json_name

    @pytest.mark.parametrize("name", ["foo", "foo_bar", "", "@type"])
    def test_json_name_returns_custom(self, name: str, protoc: Protoc) -> None:
        field = protoc.compile_field(
            f"""
            syntax="proto3";
            message M {{
                int32 f = 1 [json_name = "{name}"];
            }}
            """
        )
        assert field.json_name == name


class TestDescExtension:
    def test_type_name(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                optional int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert ext.type_name == "ext"

    def test_type_name_with_package(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            package test;
            extend M {
                optional int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert ext.type_name == "test.ext"

    def test_type_name_for_nested_extension(self, protoc: Protoc) -> None:
        message = protoc.compile_message(
            """
            syntax="proto2";
            package test;
            message C {
                extend M {
                    optional int32 ext = 1;
                }
            }
            message M { extensions 1; }
            """
        )
        ext = message.nested_extensions[0]
        assert ext.type_name == "test.C.ext"

    def test_json_name(self, protoc: Protoc) -> None:
        message = protoc.compile_message(
            """
            syntax="proto2";
            package test;
            message C {
                extend M {
                    optional int32 ext = 1;
                }
            }
            message M { extensions 1; }
            """
        )
        ext = message.nested_extensions[0]
        assert ext.json_name == "[test.C.ext]"

    def test_extendee(self, protoc: Protoc) -> None:
        file = protoc.compile_file(
            """
            syntax="proto2";
            package test;
            extend M {
                optional int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        ext = file.extensions[0]
        msg_m = file.messages[0]
        assert ext.extendee == msg_m

    def test_parent(self, protoc: Protoc) -> None:
        message = protoc.compile_message(
            """
            syntax="proto2";
            package test;
            message C {
                extend M {
                    optional int32 ext = 1;
                }
            }
            message M { extensions 1; }
            """
        )
        ext = message.nested_extensions[0]
        assert ext.parent == message

    def test_deprecated_not_deprecated_by_default(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                optional int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert ext.deprecated is False

    def test_deprecated_deprecated_is_deprecated(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                optional int32 ext = 1 [deprecated = true];
            }
            message M { extensions 1; }
            """
        )
        assert ext.deprecated is True


class TestDescExtensionPresence:
    def test_proto2_optional_is_explicit(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                optional int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert ext.presence == FeatureSet.FieldPresence.EXPLICIT

    def test_proto2_repeated_is_implicit(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                repeated int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert ext.presence == FeatureSet.FieldPresence.IMPLICIT


class TestDescExtensionDelimitedEncoding:
    def test_true_for_proto2_group(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                optional group GroupExt = 1 {}
            }
            message M { extensions 1; }
            """
        )
        assert isinstance(ext.value, DescFieldValueMessage)
        assert ext.value.delimited_encoding is True

    def test_true_for_field_with_message_encoding_delimited(
        self, protoc: Protoc
    ) -> None:
        ext = protoc.compile_extension(
            """
            edition="2023";
            extend M {
                M f = 1 [features.message_encoding = DELIMITED];
            }
            message M { extensions 1; }
            """
        )
        assert isinstance(ext.value, DescFieldValueMessage)
        assert ext.value.delimited_encoding is True


def test_desc_extension_scalar_type(protoc: Protoc) -> None:
    ext = protoc.compile_extension(
        """
        syntax="proto2";
        extend M {
            optional int32 ext = 1;
        }
        message M { extensions 1; }
        """
    )
    assert isinstance(ext.value, DescFieldValueScalar)
    assert ext.value.scalar == ScalarType.INT32


def test_desc_extension_message_type(protoc: Protoc) -> None:
    ext = protoc.compile_extension(
        """
        syntax="proto2";
        extend M {
            optional M nested = 1;
        }
        message M { extensions 1; }
        """
    )
    assert isinstance(ext.value, DescFieldValueMessage)
    assert isinstance(ext.value.message, DescMessage)
    assert ext.value.message.type_name == "M"


def test_desc_extension_enum_type(protoc: Protoc) -> None:
    ext = protoc.compile_extension(
        """
        syntax="proto2";
        enum E { A = 0; }
        extend M {
            optional E e = 1;
        }
        message M { extensions 1; }
        """
    )
    assert isinstance(ext.value, DescFieldValueEnum)
    assert isinstance(ext.value.enum, DescEnum)
    assert ext.value.enum.type_name == "E"


class TestDescExtensionListTypes:
    def test_repeated_scalar(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                repeated int32 ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert isinstance(ext.value, DescFieldValueList)
        assert ext.value.element == ScalarType.INT32

    def test_repeated_message(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            extend M {
                repeated M ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert isinstance(ext.value, DescFieldValueList)
        assert isinstance(ext.value.element, DescMessage)
        assert ext.value.element.type_name == "M"

    def test_repeated_enum(self, protoc: Protoc) -> None:
        ext = protoc.compile_extension(
            """
            syntax="proto2";
            enum E { A = 0; }
            extend M {
                repeated E ext = 1;
            }
            message M { extensions 1; }
            """
        )
        assert isinstance(ext.value, DescFieldValueList)
        assert isinstance(ext.value.element, DescEnum)
        assert ext.value.element.type_name == "E"


@pytest.mark.parametrize(
    ("proto", "default"),
    [
        pytest.param(
            """
            syntax="proto2";
            extend M { optional int32 ext = 1 [default = 42]; }
            message M { extensions 1; }
            """,
            42,
            id="int32 positive",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional int32 ext = 1 [default = -123]; }
            message M { extensions 1; }
            """,
            -123,
            id="int32 negative",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional int64 ext = 1 [default = 9223372036854775807]; }
            message M { extensions 1; }
            """,
            9223372036854775807,
            id="int64 max",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional bool ext = 1 [default = true]; }
            message M { extensions 1; }
            """,
            True,
            id="bool true",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional bool ext = 1 [default = false]; }
            message M { extensions 1; }
            """,
            False,
            id="bool false",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional float ext = 1 [default = 3.14]; }
            message M { extensions 1; }
            """,
            3.14,
            id="float",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional double ext = 1 [default = 2.718281828]; }
            message M { extensions 1; }
            """,
            2.718281828,
            id="double",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional string ext = 1 [default = "hello"]; }
            message M { extensions 1; }
            """,
            "hello",
            id="string",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional bytes ext = 1 [default = "world"]; }
            message M { extensions 1; }
            """,
            b"world",
            id="bytes",
        ),
        pytest.param(
            """
            syntax="proto2";
            extend M { optional int32 ext = 1; }
            message M { extensions 1; }
            """,
            None,
            id="no default",
        ),
    ],
)
def test_desc_extension_scalar_default_value(
    proto: str, default: str | bool | float | bytes | None, protoc: Protoc
) -> None:
    ext = protoc.compile_extension(proto)
    assert isinstance(ext.value, DescFieldValueScalar)
    assert ext.value.default_value == default


@pytest.mark.parametrize(
    ("proto", "default"),
    [
        pytest.param(
            """
            syntax="proto2";
            enum E { ZERO = 0; ONE = 1; TWO = 2; }
            extend M { optional E ext = 1 [default = ONE]; }
            message M { extensions 1; }
            """,
            1,
            id="enum default ONE",
        ),
        pytest.param(
            """
            syntax="proto2";
            enum E { ZERO = 0; ONE = 1; }
            extend M { optional E ext = 1 [default = ZERO]; }
            message M { extensions 1; }
            """,
            0,
            id="enum default ZERO",
        ),
        pytest.param(
            """
            syntax="proto2";
            enum E { ZERO = 0; ONE = 1; }
            extend M { optional E ext = 1; }
            message M { extensions 1; }
            """,
            None,
            id="enum no default",
        ),
    ],
)
def test_desc_extension_enum_default_value(
    proto: str, default: int | None, protoc: Protoc
) -> None:
    ext = protoc.compile_extension(proto)
    assert isinstance(ext.value, DescFieldValueEnum)
    assert ext.value.default_value == default


class TestStubDescLink:
    def test_enums(self) -> None:
        assert isinstance(Color._desc, DescEnum)

    def test_messages(self) -> None:
        assert isinstance(EnumMessage._desc, DescMessage)
