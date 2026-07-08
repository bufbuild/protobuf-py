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

"""Protobuf core primitives and features."""

from __future__ import annotations

from ._descriptors import (
    DescComments,
    DescEnum,
    DescEnumValue,
    DescExtension,
    DescField,
    DescFieldValue,
    DescFieldValueEnum,
    DescFieldValueList,
    DescFieldValueMap,
    DescFieldValueMessage,
    DescFieldValueScalar,
    DescFieldValueSingular,
    DescFile,
    DescMessage,
    DescMethod,
    DescOneof,
    DescService,
    DescUnknownField,
    ScalarType,
)
from ._enum import Enum, enum_is_unknown
from ._extension import Extension
from ._from_binary import merge_from_binary
from ._from_json import merge_from_json, message_from_json_value
from ._merge import merge_from
from ._message import Message
from ._oneof import Oneof
from ._registry import Registry
from ._supported_editions import maximum_supported_edition, minimum_supported_edition
from ._to_json import message_to_json_value

__all__ = [
    "DescComments",
    "DescEnum",
    "DescEnumValue",
    "DescExtension",
    "DescField",
    "DescFieldValue",
    "DescFieldValueEnum",
    "DescFieldValueList",
    "DescFieldValueMap",
    "DescFieldValueMessage",
    "DescFieldValueScalar",
    "DescFieldValueSingular",
    "DescFile",
    "DescMessage",
    "DescMethod",
    "DescOneof",
    "DescService",
    "DescUnknownField",
    "Enum",
    "Extension",
    "Message",
    "Oneof",
    "Registry",
    "ScalarType",
    "enum_is_unknown",
    "maximum_supported_edition",
    "merge_from",
    "merge_from_binary",
    "merge_from_json",
    "message_from_json_value",
    "message_to_json_value",
    "minimum_supported_edition",
]
