from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiResponse(_message.Message):
    __slots__ = ("request_id", "status_code", "message", "latency_ms", "cached", "trace_id", "retry_after_ms", "tags")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    CACHED_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    RETRY_AFTER_MS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    request_id: int
    status_code: int
    message: str
    latency_ms: float
    cached: bool
    trace_id: str
    retry_after_ms: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, request_id: _Optional[int] = ..., status_code: _Optional[int] = ..., message: _Optional[str] = ..., latency_ms: _Optional[float] = ..., cached: _Optional[bool] = ..., trace_id: _Optional[str] = ..., retry_after_ms: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class LogRecord(_message.Message):
    __slots__ = ("timestamp_nanos", "service_name", "instance_id", "severity", "message", "labels", "trace_id", "span_id", "source")
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        UNSPECIFIED: _ClassVar[LogRecord.Severity]
        DEBUG: _ClassVar[LogRecord.Severity]
        INFO: _ClassVar[LogRecord.Severity]
        WARN: _ClassVar[LogRecord.Severity]
        ERROR: _ClassVar[LogRecord.Severity]
    UNSPECIFIED: LogRecord.Severity
    DEBUG: LogRecord.Severity
    INFO: LogRecord.Severity
    WARN: LogRecord.Severity
    ERROR: LogRecord.Severity
    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class Context(_message.Message):
        __slots__ = ("file", "line", "function")
        FILE_FIELD_NUMBER: _ClassVar[int]
        LINE_FIELD_NUMBER: _ClassVar[int]
        FUNCTION_FIELD_NUMBER: _ClassVar[int]
        file: str
        line: int
        function: str
        def __init__(self, file: _Optional[str] = ..., line: _Optional[int] = ..., function: _Optional[str] = ...) -> None: ...
    TIMESTAMP_NANOS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    TRACE_ID_FIELD_NUMBER: _ClassVar[int]
    SPAN_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    timestamp_nanos: int
    service_name: str
    instance_id: str
    severity: LogRecord.Severity
    message: str
    labels: _containers.ScalarMap[str, str]
    trace_id: str
    span_id: str
    source: LogRecord.Context
    def __init__(self, timestamp_nanos: _Optional[int] = ..., service_name: _Optional[str] = ..., instance_id: _Optional[str] = ..., severity: _Optional[_Union[LogRecord.Severity, str]] = ..., message: _Optional[str] = ..., labels: _Optional[_Mapping[str, str]] = ..., trace_id: _Optional[str] = ..., span_id: _Optional[str] = ..., source: _Optional[_Union[LogRecord.Context, _Mapping]] = ...) -> None: ...

class AnalyticsEvent(_message.Message):
    __slots__ = ("event_id", "timestamp", "user_id", "properties", "sections")
    class Property(_message.Message):
        __slots__ = ("key", "string_value", "int_value", "double_value", "bool_value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
        INT_VALUE_FIELD_NUMBER: _ClassVar[int]
        DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
        BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        string_value: str
        int_value: int
        double_value: float
        bool_value: bool
        def __init__(self, key: _Optional[str] = ..., string_value: _Optional[str] = ..., int_value: _Optional[int] = ..., double_value: _Optional[float] = ..., bool_value: _Optional[bool] = ...) -> None: ...
    class Nested(_message.Message):
        __slots__ = ("name", "attributes", "children")
        NAME_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        CHILDREN_FIELD_NUMBER: _ClassVar[int]
        name: str
        attributes: _containers.RepeatedCompositeFieldContainer[AnalyticsEvent.Property]
        children: _containers.RepeatedCompositeFieldContainer[AnalyticsEvent.Nested]
        def __init__(self, name: _Optional[str] = ..., attributes: _Optional[_Iterable[_Union[AnalyticsEvent.Property, _Mapping]]] = ..., children: _Optional[_Iterable[_Union[AnalyticsEvent.Nested, _Mapping]]] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    timestamp: int
    user_id: str
    properties: _containers.RepeatedCompositeFieldContainer[AnalyticsEvent.Property]
    sections: _containers.RepeatedCompositeFieldContainer[AnalyticsEvent.Nested]
    def __init__(self, event_id: _Optional[str] = ..., timestamp: _Optional[int] = ..., user_id: _Optional[str] = ..., properties: _Optional[_Iterable[_Union[AnalyticsEvent.Property, _Mapping]]] = ..., sections: _Optional[_Iterable[_Union[AnalyticsEvent.Nested, _Mapping]]] = ...) -> None: ...

class MediaFrame(_message.Message):
    __slots__ = ("frame_id", "timestamp_nanos", "content_type", "body", "chunks", "attachments")
    class AttachmentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_NANOS_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    CHUNKS_FIELD_NUMBER: _ClassVar[int]
    ATTACHMENTS_FIELD_NUMBER: _ClassVar[int]
    frame_id: str
    timestamp_nanos: int
    content_type: str
    body: bytes
    chunks: _containers.RepeatedScalarFieldContainer[bytes]
    attachments: _containers.ScalarMap[str, bytes]
    def __init__(self, frame_id: _Optional[str] = ..., timestamp_nanos: _Optional[int] = ..., content_type: _Optional[str] = ..., body: _Optional[bytes] = ..., chunks: _Optional[_Iterable[bytes]] = ..., attachments: _Optional[_Mapping[str, bytes]] = ...) -> None: ...
