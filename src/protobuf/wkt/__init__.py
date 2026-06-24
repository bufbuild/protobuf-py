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
"""Protobuf Well-Known types."""

from __future__ import annotations

from ._gen import (
    any_pb,
    api_pb,
    c_sharp_features_pb,
    cpp_features_pb,
    descriptor_pb,
    duration_pb,
    empty_pb,
    field_mask_pb,
    go_features_pb,
    java_features_pb,
    source_context_pb,
    struct_pb,
    timestamp_pb,
    type_pb,
    wrappers_pb,
)
from ._gen.any_pb import Any
from ._gen.api_pb import Api, Method, Mixin
from ._gen.c_sharp_features_pb import CSharpFeatures, ext_csharp
from ._gen.compiler import plugin_pb
from ._gen.compiler.plugin_pb import (
    CodeGeneratorRequest,
    CodeGeneratorResponse,
    Version,
)
from ._gen.cpp_features_pb import CppFeatures, ext_cpp
from ._gen.descriptor_pb import (
    DescriptorProto,
    Edition,
    EnumDescriptorProto,
    EnumOptions,
    EnumValueDescriptorProto,
    EnumValueOptions,
    ExtensionRangeOptions,
    FeatureSet,
    FeatureSetDefaults,
    FieldDescriptorProto,
    FieldOptions,
    FileDescriptorProto,
    FileDescriptorSet,
    FileOptions,
    GeneratedCodeInfo,
    MessageOptions,
    MethodDescriptorProto,
    MethodOptions,
    OneofDescriptorProto,
    OneofOptions,
    ServiceDescriptorProto,
    ServiceOptions,
    SourceCodeInfo,
    SymbolVisibility,
    UninterpretedOption,
)
from ._gen.duration_pb import Duration
from ._gen.empty_pb import Empty
from ._gen.field_mask_pb import FieldMask
from ._gen.go_features_pb import GoFeatures, ext_go
from ._gen.java_features_pb import JavaFeatures, ext_java
from ._gen.source_context_pb import SourceContext
from ._gen.struct_pb import ListValue, NullValue, Struct, Value
from ._gen.timestamp_pb import Timestamp
from ._gen.type_pb import Enum, EnumValue, Field, Option, Syntax, Type
from ._gen.wrappers_pb import (
    BoolValue,
    BytesValue,
    DoubleValue,
    FloatValue,
    Int32Value,
    Int64Value,
    StringValue,
    UInt32Value,
    UInt64Value,
)

__all__ = [
    "Any",
    "Api",
    "BoolValue",
    "BytesValue",
    "CSharpFeatures",
    "CodeGeneratorRequest",
    "CodeGeneratorResponse",
    "CppFeatures",
    "DescriptorProto",
    "DoubleValue",
    "Duration",
    "Edition",
    "Empty",
    "Enum",
    "EnumDescriptorProto",
    "EnumOptions",
    "EnumValue",
    "EnumValueDescriptorProto",
    "EnumValueOptions",
    "ExtensionRangeOptions",
    "FeatureSet",
    "FeatureSetDefaults",
    "Field",
    "FieldDescriptorProto",
    "FieldMask",
    "FieldOptions",
    "FileDescriptorProto",
    "FileDescriptorSet",
    "FileOptions",
    "FloatValue",
    "GeneratedCodeInfo",
    "GoFeatures",
    "Int32Value",
    "Int64Value",
    "JavaFeatures",
    "ListValue",
    "MessageOptions",
    "Method",
    "MethodDescriptorProto",
    "MethodOptions",
    "Mixin",
    "NullValue",
    "OneofDescriptorProto",
    "OneofOptions",
    "Option",
    "ServiceDescriptorProto",
    "ServiceOptions",
    "SourceCodeInfo",
    "SourceContext",
    "StringValue",
    "Struct",
    "SymbolVisibility",
    "Syntax",
    "Timestamp",
    "Type",
    "UInt32Value",
    "UInt64Value",
    "UninterpretedOption",
    "Value",
    "Version",
    "any_pb",
    "api_pb",
    "c_sharp_features_pb",
    "cpp_features_pb",
    "descriptor_pb",
    "duration_pb",
    "empty_pb",
    "ext_cpp",
    "ext_csharp",
    "ext_go",
    "ext_java",
    "field_mask_pb",
    "go_features_pb",
    "java_features_pb",
    "plugin_pb",
    "source_context_pb",
    "struct_pb",
    "timestamp_pb",
    "type_pb",
    "wrappers_pb",
]
