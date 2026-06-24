from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Proto2Strings(_message.Message):
    __slots__ = ("s1", "s2", "s3", "s4", "z")
    class S3Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    S1_FIELD_NUMBER: _ClassVar[int]
    S2_FIELD_NUMBER: _ClassVar[int]
    S3_FIELD_NUMBER: _ClassVar[int]
    S4_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    s1: str
    s2: _containers.RepeatedScalarFieldContainer[str]
    s3: _containers.ScalarMap[str, str]
    s4: str
    z: int
    def __init__(self, s1: _Optional[str] = ..., s2: _Optional[_Iterable[str]] = ..., s3: _Optional[_Mapping[str, str]] = ..., s4: _Optional[str] = ..., z: _Optional[int] = ...) -> None: ...
