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

# Generated from google/protobuf/descriptor.proto. DO NOT EDIT.
# Run `uv run poe bootstrap` to regenerate.
from __future__ import annotations

from typing import TYPE_CHECKING, Final, Literal

if TYPE_CHECKING:
    from collections.abc import Mapping

# google.protobuf.FieldDescriptorProto.Type
_TYPE_STRING: Final[int] = 9
_TYPE_GROUP: Final[int] = 10
_TYPE_MESSAGE: Final[int] = 11
_TYPE_BYTES: Final[int] = 12
_TYPE_ENUM: Final[int] = 14

# google.protobuf.FieldDescriptorProto.Label
_LABEL_REQUIRED: Final[int] = 2
_LABEL_REPEATED: Final[int] = 3

# google.protobuf.Edition
_EDITION_PROTO2: Final[int] = 998
_EDITION_PROTO3: Final[int] = 999
_EDITION_UNSTABLE: Final[int] = 9999

# google.protobuf.FeatureSet.EnumType
_ENUM_TYPE_OPEN: Final[int] = 1

# google.protobuf.FeatureSet.RepeatedFieldEncoding
_REPEATED_FIELD_ENCODING_PACKED: Final[int] = 1

# google.protobuf.FeatureSet.MessageEncoding
_MESSAGE_ENCODING_DELIMITED: Final[int] = 2

# google.protobuf.MethodOptions.IdempotencyLevel
_IDEMPOTENCY_UNKNOWN: Final[int] = 0

# Minimum and maximum supported editions
_MINIMUM_EDITION: Final[int] = 998  # Edition.PROTO2
_MAXIMUM_EDITION: Final[int] = 1001  # Edition.EDITION_2024

_FeatureKey = Literal[
    "field_presence",
    "enum_type",
    "repeated_field_encoding",
    "utf8_validation",
    "message_encoding",
    "json_format",
    "enforce_naming_style",
    "default_symbol_visibility",
]

# Sourced from descriptor.proto via protoc --edition_defaults_out.
_feature_defaults: Final[Mapping[int, Mapping[_FeatureKey, int]]] = {
    # LEGACY
    900: {
        "field_presence": 1,  # EXPLICIT
        "enum_type": 2,  # CLOSED
        "repeated_field_encoding": 2,  # EXPANDED
        "utf8_validation": 3,  # NONE
        "message_encoding": 1,  # LENGTH_PREFIXED
        "json_format": 2,  # LEGACY_BEST_EFFORT
        "enforce_naming_style": 2,  # STYLE_LEGACY
        "default_symbol_visibility": 1,  # EXPORT_ALL
    },
    # PROTO3
    999: {
        "field_presence": 2,  # IMPLICIT
        "enum_type": 1,  # OPEN
        "repeated_field_encoding": 1,  # PACKED
        "utf8_validation": 2,  # VERIFY
        "message_encoding": 1,  # LENGTH_PREFIXED
        "json_format": 1,  # ALLOW
        "enforce_naming_style": 2,  # STYLE_LEGACY
        "default_symbol_visibility": 1,  # EXPORT_ALL
    },
    # EDITION_2023
    1000: {
        "field_presence": 1,  # EXPLICIT
        "enum_type": 1,  # OPEN
        "repeated_field_encoding": 1,  # PACKED
        "utf8_validation": 2,  # VERIFY
        "message_encoding": 1,  # LENGTH_PREFIXED
        "json_format": 1,  # ALLOW
        "enforce_naming_style": 2,  # STYLE_LEGACY
        "default_symbol_visibility": 1,  # EXPORT_ALL
    },
    # EDITION_2024
    1001: {
        "field_presence": 1,  # EXPLICIT
        "enum_type": 1,  # OPEN
        "repeated_field_encoding": 1,  # PACKED
        "utf8_validation": 2,  # VERIFY
        "message_encoding": 1,  # LENGTH_PREFIXED
        "json_format": 1,  # ALLOW
        "enforce_naming_style": 1,  # STYLE2024
        "default_symbol_visibility": 2,  # EXPORT_TOP_LEVEL
    },
}
