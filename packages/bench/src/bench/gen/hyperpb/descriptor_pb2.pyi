from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf.internal import python_message as _python_message
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Edition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    EDITION_UNKNOWN: _ClassVar[Edition]
    EDITION_LEGACY: _ClassVar[Edition]
    EDITION_PROTO2: _ClassVar[Edition]
    EDITION_PROTO3: _ClassVar[Edition]
    EDITION_2023: _ClassVar[Edition]
    EDITION_2024: _ClassVar[Edition]
    EDITION_1_TEST_ONLY: _ClassVar[Edition]
    EDITION_2_TEST_ONLY: _ClassVar[Edition]
    EDITION_99997_TEST_ONLY: _ClassVar[Edition]
    EDITION_99998_TEST_ONLY: _ClassVar[Edition]
    EDITION_99999_TEST_ONLY: _ClassVar[Edition]
    EDITION_MAX: _ClassVar[Edition]
EDITION_UNKNOWN: Edition
EDITION_LEGACY: Edition
EDITION_PROTO2: Edition
EDITION_PROTO3: Edition
EDITION_2023: Edition
EDITION_2024: Edition
EDITION_1_TEST_ONLY: Edition
EDITION_2_TEST_ONLY: Edition
EDITION_99997_TEST_ONLY: Edition
EDITION_99998_TEST_ONLY: Edition
EDITION_99999_TEST_ONLY: Edition
EDITION_MAX: Edition

class FileDescriptorSet(_message.Message):
    __slots__ = ("file",)
    Extensions: _python_message._ExtensionDict
    FILE_FIELD_NUMBER: _ClassVar[int]
    file: _containers.RepeatedCompositeFieldContainer[FileDescriptorProto]
    def __init__(self, file: _Optional[_Iterable[_Union[FileDescriptorProto, _Mapping]]] = ...) -> None: ...

class FileDescriptorProto(_message.Message):
    __slots__ = ("name", "package", "dependency", "public_dependency", "weak_dependency", "message_type", "enum_type", "service", "extension", "options", "source_code_info", "syntax", "edition")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_DEPENDENCY_FIELD_NUMBER: _ClassVar[int]
    WEAK_DEPENDENCY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENUM_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CODE_INFO_FIELD_NUMBER: _ClassVar[int]
    SYNTAX_FIELD_NUMBER: _ClassVar[int]
    EDITION_FIELD_NUMBER: _ClassVar[int]
    name: str
    package: str
    dependency: _containers.RepeatedScalarFieldContainer[str]
    public_dependency: _containers.RepeatedScalarFieldContainer[int]
    weak_dependency: _containers.RepeatedScalarFieldContainer[int]
    message_type: _containers.RepeatedCompositeFieldContainer[DescriptorProto]
    enum_type: _containers.RepeatedCompositeFieldContainer[EnumDescriptorProto]
    service: _containers.RepeatedCompositeFieldContainer[ServiceDescriptorProto]
    extension: _containers.RepeatedCompositeFieldContainer[FieldDescriptorProto]
    options: FileOptions
    source_code_info: SourceCodeInfo
    syntax: str
    edition: Edition
    def __init__(self, name: _Optional[str] = ..., package: _Optional[str] = ..., dependency: _Optional[_Iterable[str]] = ..., public_dependency: _Optional[_Iterable[int]] = ..., weak_dependency: _Optional[_Iterable[int]] = ..., message_type: _Optional[_Iterable[_Union[DescriptorProto, _Mapping]]] = ..., enum_type: _Optional[_Iterable[_Union[EnumDescriptorProto, _Mapping]]] = ..., service: _Optional[_Iterable[_Union[ServiceDescriptorProto, _Mapping]]] = ..., extension: _Optional[_Iterable[_Union[FieldDescriptorProto, _Mapping]]] = ..., options: _Optional[_Union[FileOptions, _Mapping]] = ..., source_code_info: _Optional[_Union[SourceCodeInfo, _Mapping]] = ..., syntax: _Optional[str] = ..., edition: _Optional[_Union[Edition, str]] = ...) -> None: ...

class DescriptorProto(_message.Message):
    __slots__ = ("name", "field", "extension", "nested_type", "enum_type", "extension_range", "oneof_decl", "options", "reserved_range", "reserved_name")
    class ExtensionRange(_message.Message):
        __slots__ = ("start", "end", "options")
        START_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        OPTIONS_FIELD_NUMBER: _ClassVar[int]
        start: int
        end: int
        options: ExtensionRangeOptions
        def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ..., options: _Optional[_Union[ExtensionRangeOptions, _Mapping]] = ...) -> None: ...
    class ReservedRange(_message.Message):
        __slots__ = ("start", "end")
        START_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        start: int
        end: int
        def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    NESTED_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENUM_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_RANGE_FIELD_NUMBER: _ClassVar[int]
    ONEOF_DECL_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_RANGE_FIELD_NUMBER: _ClassVar[int]
    RESERVED_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    field: _containers.RepeatedCompositeFieldContainer[FieldDescriptorProto]
    extension: _containers.RepeatedCompositeFieldContainer[FieldDescriptorProto]
    nested_type: _containers.RepeatedCompositeFieldContainer[DescriptorProto]
    enum_type: _containers.RepeatedCompositeFieldContainer[EnumDescriptorProto]
    extension_range: _containers.RepeatedCompositeFieldContainer[DescriptorProto.ExtensionRange]
    oneof_decl: _containers.RepeatedCompositeFieldContainer[OneofDescriptorProto]
    options: MessageOptions
    reserved_range: _containers.RepeatedCompositeFieldContainer[DescriptorProto.ReservedRange]
    reserved_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., field: _Optional[_Iterable[_Union[FieldDescriptorProto, _Mapping]]] = ..., extension: _Optional[_Iterable[_Union[FieldDescriptorProto, _Mapping]]] = ..., nested_type: _Optional[_Iterable[_Union[DescriptorProto, _Mapping]]] = ..., enum_type: _Optional[_Iterable[_Union[EnumDescriptorProto, _Mapping]]] = ..., extension_range: _Optional[_Iterable[_Union[DescriptorProto.ExtensionRange, _Mapping]]] = ..., oneof_decl: _Optional[_Iterable[_Union[OneofDescriptorProto, _Mapping]]] = ..., options: _Optional[_Union[MessageOptions, _Mapping]] = ..., reserved_range: _Optional[_Iterable[_Union[DescriptorProto.ReservedRange, _Mapping]]] = ..., reserved_name: _Optional[_Iterable[str]] = ...) -> None: ...

class ExtensionRangeOptions(_message.Message):
    __slots__ = ("uninterpreted_option", "declaration", "features", "verification")
    Extensions: _python_message._ExtensionDict
    class VerificationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DECLARATION: _ClassVar[ExtensionRangeOptions.VerificationState]
        UNVERIFIED: _ClassVar[ExtensionRangeOptions.VerificationState]
    DECLARATION: ExtensionRangeOptions.VerificationState
    UNVERIFIED: ExtensionRangeOptions.VerificationState
    class Declaration(_message.Message):
        __slots__ = ("number", "full_name", "type", "reserved", "repeated")
        NUMBER_FIELD_NUMBER: _ClassVar[int]
        FULL_NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        RESERVED_FIELD_NUMBER: _ClassVar[int]
        REPEATED_FIELD_NUMBER: _ClassVar[int]
        number: int
        full_name: str
        type: str
        reserved: bool
        repeated: bool
        def __init__(self, number: _Optional[int] = ..., full_name: _Optional[str] = ..., type: _Optional[str] = ..., reserved: _Optional[bool] = ..., repeated: _Optional[bool] = ...) -> None: ...
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    DECLARATION_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    VERIFICATION_FIELD_NUMBER: _ClassVar[int]
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    declaration: _containers.RepeatedCompositeFieldContainer[ExtensionRangeOptions.Declaration]
    features: FeatureSet
    verification: ExtensionRangeOptions.VerificationState
    def __init__(self, uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ..., declaration: _Optional[_Iterable[_Union[ExtensionRangeOptions.Declaration, _Mapping]]] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., verification: _Optional[_Union[ExtensionRangeOptions.VerificationState, str]] = ...) -> None: ...

class FieldDescriptorProto(_message.Message):
    __slots__ = ("name", "number", "label", "type", "type_name", "extendee", "default_value", "oneof_index", "json_name", "options", "proto3_optional")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_DOUBLE: _ClassVar[FieldDescriptorProto.Type]
        TYPE_FLOAT: _ClassVar[FieldDescriptorProto.Type]
        TYPE_INT64: _ClassVar[FieldDescriptorProto.Type]
        TYPE_UINT64: _ClassVar[FieldDescriptorProto.Type]
        TYPE_INT32: _ClassVar[FieldDescriptorProto.Type]
        TYPE_FIXED64: _ClassVar[FieldDescriptorProto.Type]
        TYPE_FIXED32: _ClassVar[FieldDescriptorProto.Type]
        TYPE_BOOL: _ClassVar[FieldDescriptorProto.Type]
        TYPE_STRING: _ClassVar[FieldDescriptorProto.Type]
        TYPE_GROUP: _ClassVar[FieldDescriptorProto.Type]
        TYPE_MESSAGE: _ClassVar[FieldDescriptorProto.Type]
        TYPE_BYTES: _ClassVar[FieldDescriptorProto.Type]
        TYPE_UINT32: _ClassVar[FieldDescriptorProto.Type]
        TYPE_ENUM: _ClassVar[FieldDescriptorProto.Type]
        TYPE_SFIXED32: _ClassVar[FieldDescriptorProto.Type]
        TYPE_SFIXED64: _ClassVar[FieldDescriptorProto.Type]
        TYPE_SINT32: _ClassVar[FieldDescriptorProto.Type]
        TYPE_SINT64: _ClassVar[FieldDescriptorProto.Type]
    TYPE_DOUBLE: FieldDescriptorProto.Type
    TYPE_FLOAT: FieldDescriptorProto.Type
    TYPE_INT64: FieldDescriptorProto.Type
    TYPE_UINT64: FieldDescriptorProto.Type
    TYPE_INT32: FieldDescriptorProto.Type
    TYPE_FIXED64: FieldDescriptorProto.Type
    TYPE_FIXED32: FieldDescriptorProto.Type
    TYPE_BOOL: FieldDescriptorProto.Type
    TYPE_STRING: FieldDescriptorProto.Type
    TYPE_GROUP: FieldDescriptorProto.Type
    TYPE_MESSAGE: FieldDescriptorProto.Type
    TYPE_BYTES: FieldDescriptorProto.Type
    TYPE_UINT32: FieldDescriptorProto.Type
    TYPE_ENUM: FieldDescriptorProto.Type
    TYPE_SFIXED32: FieldDescriptorProto.Type
    TYPE_SFIXED64: FieldDescriptorProto.Type
    TYPE_SINT32: FieldDescriptorProto.Type
    TYPE_SINT64: FieldDescriptorProto.Type
    class Label(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LABEL_OPTIONAL: _ClassVar[FieldDescriptorProto.Label]
        LABEL_REPEATED: _ClassVar[FieldDescriptorProto.Label]
        LABEL_REQUIRED: _ClassVar[FieldDescriptorProto.Label]
    LABEL_OPTIONAL: FieldDescriptorProto.Label
    LABEL_REPEATED: FieldDescriptorProto.Label
    LABEL_REQUIRED: FieldDescriptorProto.Label
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    EXTENDEE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    ONEOF_INDEX_FIELD_NUMBER: _ClassVar[int]
    JSON_NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    PROTO3_OPTIONAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    number: int
    label: FieldDescriptorProto.Label
    type: FieldDescriptorProto.Type
    type_name: str
    extendee: str
    default_value: str
    oneof_index: int
    json_name: str
    options: FieldOptions
    proto3_optional: bool
    def __init__(self, name: _Optional[str] = ..., number: _Optional[int] = ..., label: _Optional[_Union[FieldDescriptorProto.Label, str]] = ..., type: _Optional[_Union[FieldDescriptorProto.Type, str]] = ..., type_name: _Optional[str] = ..., extendee: _Optional[str] = ..., default_value: _Optional[str] = ..., oneof_index: _Optional[int] = ..., json_name: _Optional[str] = ..., options: _Optional[_Union[FieldOptions, _Mapping]] = ..., proto3_optional: _Optional[bool] = ...) -> None: ...

class OneofDescriptorProto(_message.Message):
    __slots__ = ("name", "options")
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    options: OneofOptions
    def __init__(self, name: _Optional[str] = ..., options: _Optional[_Union[OneofOptions, _Mapping]] = ...) -> None: ...

class EnumDescriptorProto(_message.Message):
    __slots__ = ("name", "value", "options", "reserved_range", "reserved_name")
    class EnumReservedRange(_message.Message):
        __slots__ = ("start", "end")
        START_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        start: int
        end: int
        def __init__(self, start: _Optional[int] = ..., end: _Optional[int] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    RESERVED_RANGE_FIELD_NUMBER: _ClassVar[int]
    RESERVED_NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: _containers.RepeatedCompositeFieldContainer[EnumValueDescriptorProto]
    options: EnumOptions
    reserved_range: _containers.RepeatedCompositeFieldContainer[EnumDescriptorProto.EnumReservedRange]
    reserved_name: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., value: _Optional[_Iterable[_Union[EnumValueDescriptorProto, _Mapping]]] = ..., options: _Optional[_Union[EnumOptions, _Mapping]] = ..., reserved_range: _Optional[_Iterable[_Union[EnumDescriptorProto.EnumReservedRange, _Mapping]]] = ..., reserved_name: _Optional[_Iterable[str]] = ...) -> None: ...

class EnumValueDescriptorProto(_message.Message):
    __slots__ = ("name", "number", "options")
    NAME_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    number: int
    options: EnumValueOptions
    def __init__(self, name: _Optional[str] = ..., number: _Optional[int] = ..., options: _Optional[_Union[EnumValueOptions, _Mapping]] = ...) -> None: ...

class ServiceDescriptorProto(_message.Message):
    __slots__ = ("name", "method", "options")
    NAME_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    method: _containers.RepeatedCompositeFieldContainer[MethodDescriptorProto]
    options: ServiceOptions
    def __init__(self, name: _Optional[str] = ..., method: _Optional[_Iterable[_Union[MethodDescriptorProto, _Mapping]]] = ..., options: _Optional[_Union[ServiceOptions, _Mapping]] = ...) -> None: ...

class MethodDescriptorProto(_message.Message):
    __slots__ = ("name", "input_type", "output_type", "options", "client_streaming", "server_streaming")
    NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_TYPE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_STREAMING_FIELD_NUMBER: _ClassVar[int]
    SERVER_STREAMING_FIELD_NUMBER: _ClassVar[int]
    name: str
    input_type: str
    output_type: str
    options: MethodOptions
    client_streaming: bool
    server_streaming: bool
    def __init__(self, name: _Optional[str] = ..., input_type: _Optional[str] = ..., output_type: _Optional[str] = ..., options: _Optional[_Union[MethodOptions, _Mapping]] = ..., client_streaming: _Optional[bool] = ..., server_streaming: _Optional[bool] = ...) -> None: ...

class FileOptions(_message.Message):
    __slots__ = ("java_package", "java_outer_classname", "java_multiple_files", "java_generate_equals_and_hash", "java_string_check_utf8", "optimize_for", "go_package", "cc_generic_services", "java_generic_services", "py_generic_services", "deprecated", "cc_enable_arenas", "objc_class_prefix", "csharp_namespace", "swift_prefix", "php_class_prefix", "php_namespace", "php_metadata_namespace", "ruby_package", "features", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    class OptimizeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SPEED: _ClassVar[FileOptions.OptimizeMode]
        CODE_SIZE: _ClassVar[FileOptions.OptimizeMode]
        LITE_RUNTIME: _ClassVar[FileOptions.OptimizeMode]
    SPEED: FileOptions.OptimizeMode
    CODE_SIZE: FileOptions.OptimizeMode
    LITE_RUNTIME: FileOptions.OptimizeMode
    JAVA_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    JAVA_OUTER_CLASSNAME_FIELD_NUMBER: _ClassVar[int]
    JAVA_MULTIPLE_FILES_FIELD_NUMBER: _ClassVar[int]
    JAVA_GENERATE_EQUALS_AND_HASH_FIELD_NUMBER: _ClassVar[int]
    JAVA_STRING_CHECK_UTF8_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZE_FOR_FIELD_NUMBER: _ClassVar[int]
    GO_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    CC_GENERIC_SERVICES_FIELD_NUMBER: _ClassVar[int]
    JAVA_GENERIC_SERVICES_FIELD_NUMBER: _ClassVar[int]
    PY_GENERIC_SERVICES_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    CC_ENABLE_ARENAS_FIELD_NUMBER: _ClassVar[int]
    OBJC_CLASS_PREFIX_FIELD_NUMBER: _ClassVar[int]
    CSHARP_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SWIFT_PREFIX_FIELD_NUMBER: _ClassVar[int]
    PHP_CLASS_PREFIX_FIELD_NUMBER: _ClassVar[int]
    PHP_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PHP_METADATA_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    RUBY_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    java_package: str
    java_outer_classname: str
    java_multiple_files: bool
    java_generate_equals_and_hash: bool
    java_string_check_utf8: bool
    optimize_for: FileOptions.OptimizeMode
    go_package: str
    cc_generic_services: bool
    java_generic_services: bool
    py_generic_services: bool
    deprecated: bool
    cc_enable_arenas: bool
    objc_class_prefix: str
    csharp_namespace: str
    swift_prefix: str
    php_class_prefix: str
    php_namespace: str
    php_metadata_namespace: str
    ruby_package: str
    features: FeatureSet
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, java_package: _Optional[str] = ..., java_outer_classname: _Optional[str] = ..., java_multiple_files: _Optional[bool] = ..., java_generate_equals_and_hash: _Optional[bool] = ..., java_string_check_utf8: _Optional[bool] = ..., optimize_for: _Optional[_Union[FileOptions.OptimizeMode, str]] = ..., go_package: _Optional[str] = ..., cc_generic_services: _Optional[bool] = ..., java_generic_services: _Optional[bool] = ..., py_generic_services: _Optional[bool] = ..., deprecated: _Optional[bool] = ..., cc_enable_arenas: _Optional[bool] = ..., objc_class_prefix: _Optional[str] = ..., csharp_namespace: _Optional[str] = ..., swift_prefix: _Optional[str] = ..., php_class_prefix: _Optional[str] = ..., php_namespace: _Optional[str] = ..., php_metadata_namespace: _Optional[str] = ..., ruby_package: _Optional[str] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class MessageOptions(_message.Message):
    __slots__ = ("message_set_wire_format", "no_standard_descriptor_accessor", "deprecated", "map_entry", "deprecated_legacy_json_field_conflicts", "features", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    MESSAGE_SET_WIRE_FORMAT_FIELD_NUMBER: _ClassVar[int]
    NO_STANDARD_DESCRIPTOR_ACCESSOR_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    MAP_ENTRY_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_LEGACY_JSON_FIELD_CONFLICTS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    message_set_wire_format: bool
    no_standard_descriptor_accessor: bool
    deprecated: bool
    map_entry: bool
    deprecated_legacy_json_field_conflicts: bool
    features: FeatureSet
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, message_set_wire_format: _Optional[bool] = ..., no_standard_descriptor_accessor: _Optional[bool] = ..., deprecated: _Optional[bool] = ..., map_entry: _Optional[bool] = ..., deprecated_legacy_json_field_conflicts: _Optional[bool] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class FieldOptions(_message.Message):
    __slots__ = ("ctype", "packed", "jstype", "lazy", "unverified_lazy", "deprecated", "weak", "debug_redact", "retention", "targets", "edition_defaults", "features", "feature_support", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    class CType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STRING: _ClassVar[FieldOptions.CType]
        CORD: _ClassVar[FieldOptions.CType]
        STRING_PIECE: _ClassVar[FieldOptions.CType]
    STRING: FieldOptions.CType
    CORD: FieldOptions.CType
    STRING_PIECE: FieldOptions.CType
    class JSType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        JS_NORMAL: _ClassVar[FieldOptions.JSType]
        JS_STRING: _ClassVar[FieldOptions.JSType]
        JS_NUMBER: _ClassVar[FieldOptions.JSType]
    JS_NORMAL: FieldOptions.JSType
    JS_STRING: FieldOptions.JSType
    JS_NUMBER: FieldOptions.JSType
    class OptionRetention(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RETENTION_UNKNOWN: _ClassVar[FieldOptions.OptionRetention]
        RETENTION_RUNTIME: _ClassVar[FieldOptions.OptionRetention]
        RETENTION_SOURCE: _ClassVar[FieldOptions.OptionRetention]
    RETENTION_UNKNOWN: FieldOptions.OptionRetention
    RETENTION_RUNTIME: FieldOptions.OptionRetention
    RETENTION_SOURCE: FieldOptions.OptionRetention
    class OptionTargetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TARGET_TYPE_UNKNOWN: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_FILE: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_EXTENSION_RANGE: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_MESSAGE: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_FIELD: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_ONEOF: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_ENUM: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_ENUM_ENTRY: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_SERVICE: _ClassVar[FieldOptions.OptionTargetType]
        TARGET_TYPE_METHOD: _ClassVar[FieldOptions.OptionTargetType]
    TARGET_TYPE_UNKNOWN: FieldOptions.OptionTargetType
    TARGET_TYPE_FILE: FieldOptions.OptionTargetType
    TARGET_TYPE_EXTENSION_RANGE: FieldOptions.OptionTargetType
    TARGET_TYPE_MESSAGE: FieldOptions.OptionTargetType
    TARGET_TYPE_FIELD: FieldOptions.OptionTargetType
    TARGET_TYPE_ONEOF: FieldOptions.OptionTargetType
    TARGET_TYPE_ENUM: FieldOptions.OptionTargetType
    TARGET_TYPE_ENUM_ENTRY: FieldOptions.OptionTargetType
    TARGET_TYPE_SERVICE: FieldOptions.OptionTargetType
    TARGET_TYPE_METHOD: FieldOptions.OptionTargetType
    class EditionDefault(_message.Message):
        __slots__ = ("edition", "value")
        EDITION_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        edition: Edition
        value: str
        def __init__(self, edition: _Optional[_Union[Edition, str]] = ..., value: _Optional[str] = ...) -> None: ...
    class FeatureSupport(_message.Message):
        __slots__ = ("edition_introduced", "edition_deprecated", "deprecation_warning", "edition_removed")
        EDITION_INTRODUCED_FIELD_NUMBER: _ClassVar[int]
        EDITION_DEPRECATED_FIELD_NUMBER: _ClassVar[int]
        DEPRECATION_WARNING_FIELD_NUMBER: _ClassVar[int]
        EDITION_REMOVED_FIELD_NUMBER: _ClassVar[int]
        edition_introduced: Edition
        edition_deprecated: Edition
        deprecation_warning: str
        edition_removed: Edition
        def __init__(self, edition_introduced: _Optional[_Union[Edition, str]] = ..., edition_deprecated: _Optional[_Union[Edition, str]] = ..., deprecation_warning: _Optional[str] = ..., edition_removed: _Optional[_Union[Edition, str]] = ...) -> None: ...
    CTYPE_FIELD_NUMBER: _ClassVar[int]
    PACKED_FIELD_NUMBER: _ClassVar[int]
    JSTYPE_FIELD_NUMBER: _ClassVar[int]
    LAZY_FIELD_NUMBER: _ClassVar[int]
    UNVERIFIED_LAZY_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    WEAK_FIELD_NUMBER: _ClassVar[int]
    DEBUG_REDACT_FIELD_NUMBER: _ClassVar[int]
    RETENTION_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    EDITION_DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SUPPORT_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    ctype: FieldOptions.CType
    packed: bool
    jstype: FieldOptions.JSType
    lazy: bool
    unverified_lazy: bool
    deprecated: bool
    weak: bool
    debug_redact: bool
    retention: FieldOptions.OptionRetention
    targets: _containers.RepeatedScalarFieldContainer[FieldOptions.OptionTargetType]
    edition_defaults: _containers.RepeatedCompositeFieldContainer[FieldOptions.EditionDefault]
    features: FeatureSet
    feature_support: FieldOptions.FeatureSupport
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, ctype: _Optional[_Union[FieldOptions.CType, str]] = ..., packed: _Optional[bool] = ..., jstype: _Optional[_Union[FieldOptions.JSType, str]] = ..., lazy: _Optional[bool] = ..., unverified_lazy: _Optional[bool] = ..., deprecated: _Optional[bool] = ..., weak: _Optional[bool] = ..., debug_redact: _Optional[bool] = ..., retention: _Optional[_Union[FieldOptions.OptionRetention, str]] = ..., targets: _Optional[_Iterable[_Union[FieldOptions.OptionTargetType, str]]] = ..., edition_defaults: _Optional[_Iterable[_Union[FieldOptions.EditionDefault, _Mapping]]] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., feature_support: _Optional[_Union[FieldOptions.FeatureSupport, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class OneofOptions(_message.Message):
    __slots__ = ("features", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    features: FeatureSet
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, features: _Optional[_Union[FeatureSet, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class EnumOptions(_message.Message):
    __slots__ = ("allow_alias", "deprecated", "deprecated_legacy_json_field_conflicts", "features", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    ALLOW_ALIAS_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_LEGACY_JSON_FIELD_CONFLICTS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    allow_alias: bool
    deprecated: bool
    deprecated_legacy_json_field_conflicts: bool
    features: FeatureSet
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, allow_alias: _Optional[bool] = ..., deprecated: _Optional[bool] = ..., deprecated_legacy_json_field_conflicts: _Optional[bool] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class EnumValueOptions(_message.Message):
    __slots__ = ("deprecated", "features", "debug_redact", "feature_support", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    DEBUG_REDACT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_SUPPORT_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    deprecated: bool
    features: FeatureSet
    debug_redact: bool
    feature_support: FieldOptions.FeatureSupport
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, deprecated: _Optional[bool] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., debug_redact: _Optional[bool] = ..., feature_support: _Optional[_Union[FieldOptions.FeatureSupport, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class ServiceOptions(_message.Message):
    __slots__ = ("features", "deprecated", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    features: FeatureSet
    deprecated: bool
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, features: _Optional[_Union[FeatureSet, _Mapping]] = ..., deprecated: _Optional[bool] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class MethodOptions(_message.Message):
    __slots__ = ("deprecated", "idempotency_level", "features", "uninterpreted_option")
    Extensions: _python_message._ExtensionDict
    class IdempotencyLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IDEMPOTENCY_UNKNOWN: _ClassVar[MethodOptions.IdempotencyLevel]
        NO_SIDE_EFFECTS: _ClassVar[MethodOptions.IdempotencyLevel]
        IDEMPOTENT: _ClassVar[MethodOptions.IdempotencyLevel]
    IDEMPOTENCY_UNKNOWN: MethodOptions.IdempotencyLevel
    NO_SIDE_EFFECTS: MethodOptions.IdempotencyLevel
    IDEMPOTENT: MethodOptions.IdempotencyLevel
    DEPRECATED_FIELD_NUMBER: _ClassVar[int]
    IDEMPOTENCY_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    UNINTERPRETED_OPTION_FIELD_NUMBER: _ClassVar[int]
    deprecated: bool
    idempotency_level: MethodOptions.IdempotencyLevel
    features: FeatureSet
    uninterpreted_option: _containers.RepeatedCompositeFieldContainer[UninterpretedOption]
    def __init__(self, deprecated: _Optional[bool] = ..., idempotency_level: _Optional[_Union[MethodOptions.IdempotencyLevel, str]] = ..., features: _Optional[_Union[FeatureSet, _Mapping]] = ..., uninterpreted_option: _Optional[_Iterable[_Union[UninterpretedOption, _Mapping]]] = ...) -> None: ...

class UninterpretedOption(_message.Message):
    __slots__ = ("name", "identifier_value", "positive_int_value", "negative_int_value", "double_value", "string_value", "aggregate_value")
    class NamePart(_message.Message):
        __slots__ = ("name_part", "is_extension")
        NAME_PART_FIELD_NUMBER: _ClassVar[int]
        IS_EXTENSION_FIELD_NUMBER: _ClassVar[int]
        name_part: str
        is_extension: bool
        def __init__(self, name_part: _Optional[str] = ..., is_extension: _Optional[bool] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_VALUE_FIELD_NUMBER: _ClassVar[int]
    POSITIVE_INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    NEGATIVE_INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    AGGREGATE_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: _containers.RepeatedCompositeFieldContainer[UninterpretedOption.NamePart]
    identifier_value: str
    positive_int_value: int
    negative_int_value: int
    double_value: float
    string_value: bytes
    aggregate_value: str
    def __init__(self, name: _Optional[_Iterable[_Union[UninterpretedOption.NamePart, _Mapping]]] = ..., identifier_value: _Optional[str] = ..., positive_int_value: _Optional[int] = ..., negative_int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., string_value: _Optional[bytes] = ..., aggregate_value: _Optional[str] = ...) -> None: ...

class FeatureSet(_message.Message):
    __slots__ = ("field_presence", "enum_type", "repeated_field_encoding", "utf8_validation", "message_encoding", "json_format", "enforce_naming_style")
    Extensions: _python_message._ExtensionDict
    class FieldPresence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FIELD_PRESENCE_UNKNOWN: _ClassVar[FeatureSet.FieldPresence]
        EXPLICIT: _ClassVar[FeatureSet.FieldPresence]
        IMPLICIT: _ClassVar[FeatureSet.FieldPresence]
        LEGACY_REQUIRED: _ClassVar[FeatureSet.FieldPresence]
    FIELD_PRESENCE_UNKNOWN: FeatureSet.FieldPresence
    EXPLICIT: FeatureSet.FieldPresence
    IMPLICIT: FeatureSet.FieldPresence
    LEGACY_REQUIRED: FeatureSet.FieldPresence
    class EnumType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ENUM_TYPE_UNKNOWN: _ClassVar[FeatureSet.EnumType]
        OPEN: _ClassVar[FeatureSet.EnumType]
        CLOSED: _ClassVar[FeatureSet.EnumType]
    ENUM_TYPE_UNKNOWN: FeatureSet.EnumType
    OPEN: FeatureSet.EnumType
    CLOSED: FeatureSet.EnumType
    class RepeatedFieldEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REPEATED_FIELD_ENCODING_UNKNOWN: _ClassVar[FeatureSet.RepeatedFieldEncoding]
        PACKED: _ClassVar[FeatureSet.RepeatedFieldEncoding]
        EXPANDED: _ClassVar[FeatureSet.RepeatedFieldEncoding]
    REPEATED_FIELD_ENCODING_UNKNOWN: FeatureSet.RepeatedFieldEncoding
    PACKED: FeatureSet.RepeatedFieldEncoding
    EXPANDED: FeatureSet.RepeatedFieldEncoding
    class Utf8Validation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UTF8_VALIDATION_UNKNOWN: _ClassVar[FeatureSet.Utf8Validation]
        VERIFY: _ClassVar[FeatureSet.Utf8Validation]
        NONE: _ClassVar[FeatureSet.Utf8Validation]
    UTF8_VALIDATION_UNKNOWN: FeatureSet.Utf8Validation
    VERIFY: FeatureSet.Utf8Validation
    NONE: FeatureSet.Utf8Validation
    class MessageEncoding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MESSAGE_ENCODING_UNKNOWN: _ClassVar[FeatureSet.MessageEncoding]
        LENGTH_PREFIXED: _ClassVar[FeatureSet.MessageEncoding]
        DELIMITED: _ClassVar[FeatureSet.MessageEncoding]
    MESSAGE_ENCODING_UNKNOWN: FeatureSet.MessageEncoding
    LENGTH_PREFIXED: FeatureSet.MessageEncoding
    DELIMITED: FeatureSet.MessageEncoding
    class JsonFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        JSON_FORMAT_UNKNOWN: _ClassVar[FeatureSet.JsonFormat]
        ALLOW: _ClassVar[FeatureSet.JsonFormat]
        LEGACY_BEST_EFFORT: _ClassVar[FeatureSet.JsonFormat]
    JSON_FORMAT_UNKNOWN: FeatureSet.JsonFormat
    ALLOW: FeatureSet.JsonFormat
    LEGACY_BEST_EFFORT: FeatureSet.JsonFormat
    class EnforceNamingStyle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ENFORCE_NAMING_STYLE_UNKNOWN: _ClassVar[FeatureSet.EnforceNamingStyle]
        STYLE2024: _ClassVar[FeatureSet.EnforceNamingStyle]
        STYLE_LEGACY: _ClassVar[FeatureSet.EnforceNamingStyle]
    ENFORCE_NAMING_STYLE_UNKNOWN: FeatureSet.EnforceNamingStyle
    STYLE2024: FeatureSet.EnforceNamingStyle
    STYLE_LEGACY: FeatureSet.EnforceNamingStyle
    FIELD_PRESENCE_FIELD_NUMBER: _ClassVar[int]
    ENUM_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPEATED_FIELD_ENCODING_FIELD_NUMBER: _ClassVar[int]
    UTF8_VALIDATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ENCODING_FIELD_NUMBER: _ClassVar[int]
    JSON_FORMAT_FIELD_NUMBER: _ClassVar[int]
    ENFORCE_NAMING_STYLE_FIELD_NUMBER: _ClassVar[int]
    field_presence: FeatureSet.FieldPresence
    enum_type: FeatureSet.EnumType
    repeated_field_encoding: FeatureSet.RepeatedFieldEncoding
    utf8_validation: FeatureSet.Utf8Validation
    message_encoding: FeatureSet.MessageEncoding
    json_format: FeatureSet.JsonFormat
    enforce_naming_style: FeatureSet.EnforceNamingStyle
    def __init__(self, field_presence: _Optional[_Union[FeatureSet.FieldPresence, str]] = ..., enum_type: _Optional[_Union[FeatureSet.EnumType, str]] = ..., repeated_field_encoding: _Optional[_Union[FeatureSet.RepeatedFieldEncoding, str]] = ..., utf8_validation: _Optional[_Union[FeatureSet.Utf8Validation, str]] = ..., message_encoding: _Optional[_Union[FeatureSet.MessageEncoding, str]] = ..., json_format: _Optional[_Union[FeatureSet.JsonFormat, str]] = ..., enforce_naming_style: _Optional[_Union[FeatureSet.EnforceNamingStyle, str]] = ...) -> None: ...

class FeatureSetDefaults(_message.Message):
    __slots__ = ("defaults", "minimum_edition", "maximum_edition")
    class FeatureSetEditionDefault(_message.Message):
        __slots__ = ("edition", "overridable_features", "fixed_features")
        EDITION_FIELD_NUMBER: _ClassVar[int]
        OVERRIDABLE_FEATURES_FIELD_NUMBER: _ClassVar[int]
        FIXED_FEATURES_FIELD_NUMBER: _ClassVar[int]
        edition: Edition
        overridable_features: FeatureSet
        fixed_features: FeatureSet
        def __init__(self, edition: _Optional[_Union[Edition, str]] = ..., overridable_features: _Optional[_Union[FeatureSet, _Mapping]] = ..., fixed_features: _Optional[_Union[FeatureSet, _Mapping]] = ...) -> None: ...
    DEFAULTS_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_EDITION_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_EDITION_FIELD_NUMBER: _ClassVar[int]
    defaults: _containers.RepeatedCompositeFieldContainer[FeatureSetDefaults.FeatureSetEditionDefault]
    minimum_edition: Edition
    maximum_edition: Edition
    def __init__(self, defaults: _Optional[_Iterable[_Union[FeatureSetDefaults.FeatureSetEditionDefault, _Mapping]]] = ..., minimum_edition: _Optional[_Union[Edition, str]] = ..., maximum_edition: _Optional[_Union[Edition, str]] = ...) -> None: ...

class SourceCodeInfo(_message.Message):
    __slots__ = ("location",)
    Extensions: _python_message._ExtensionDict
    class Location(_message.Message):
        __slots__ = ("path", "span", "leading_comments", "trailing_comments", "leading_detached_comments")
        PATH_FIELD_NUMBER: _ClassVar[int]
        SPAN_FIELD_NUMBER: _ClassVar[int]
        LEADING_COMMENTS_FIELD_NUMBER: _ClassVar[int]
        TRAILING_COMMENTS_FIELD_NUMBER: _ClassVar[int]
        LEADING_DETACHED_COMMENTS_FIELD_NUMBER: _ClassVar[int]
        path: _containers.RepeatedScalarFieldContainer[int]
        span: _containers.RepeatedScalarFieldContainer[int]
        leading_comments: str
        trailing_comments: str
        leading_detached_comments: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, path: _Optional[_Iterable[int]] = ..., span: _Optional[_Iterable[int]] = ..., leading_comments: _Optional[str] = ..., trailing_comments: _Optional[str] = ..., leading_detached_comments: _Optional[_Iterable[str]] = ...) -> None: ...
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    location: _containers.RepeatedCompositeFieldContainer[SourceCodeInfo.Location]
    def __init__(self, location: _Optional[_Iterable[_Union[SourceCodeInfo.Location, _Mapping]]] = ...) -> None: ...

class GeneratedCodeInfo(_message.Message):
    __slots__ = ("annotation",)
    class Annotation(_message.Message):
        __slots__ = ("path", "source_file", "begin", "end", "semantic")
        class Semantic(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            NONE: _ClassVar[GeneratedCodeInfo.Annotation.Semantic]
            SET: _ClassVar[GeneratedCodeInfo.Annotation.Semantic]
            ALIAS: _ClassVar[GeneratedCodeInfo.Annotation.Semantic]
        NONE: GeneratedCodeInfo.Annotation.Semantic
        SET: GeneratedCodeInfo.Annotation.Semantic
        ALIAS: GeneratedCodeInfo.Annotation.Semantic
        PATH_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FILE_FIELD_NUMBER: _ClassVar[int]
        BEGIN_FIELD_NUMBER: _ClassVar[int]
        END_FIELD_NUMBER: _ClassVar[int]
        SEMANTIC_FIELD_NUMBER: _ClassVar[int]
        path: _containers.RepeatedScalarFieldContainer[int]
        source_file: str
        begin: int
        end: int
        semantic: GeneratedCodeInfo.Annotation.Semantic
        def __init__(self, path: _Optional[_Iterable[int]] = ..., source_file: _Optional[str] = ..., begin: _Optional[int] = ..., end: _Optional[int] = ..., semantic: _Optional[_Union[GeneratedCodeInfo.Annotation.Semantic, str]] = ...) -> None: ...
    ANNOTATION_FIELD_NUMBER: _ClassVar[int]
    annotation: _containers.RepeatedCompositeFieldContainer[GeneratedCodeInfo.Annotation]
    def __init__(self, annotation: _Optional[_Iterable[_Union[GeneratedCodeInfo.Annotation, _Mapping]]] = ...) -> None: ...
