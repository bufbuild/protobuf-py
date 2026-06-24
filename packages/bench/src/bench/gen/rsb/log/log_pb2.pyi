from ...rsb import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Address(_message.Message):
    __slots__ = ("x0", "x1", "x2", "x3")
    X0_FIELD_NUMBER: _ClassVar[int]
    X1_FIELD_NUMBER: _ClassVar[int]
    X2_FIELD_NUMBER: _ClassVar[int]
    X3_FIELD_NUMBER: _ClassVar[int]
    x0: int
    x1: int
    x2: int
    x3: int
    def __init__(self, x0: _Optional[int] = ..., x1: _Optional[int] = ..., x2: _Optional[int] = ..., x3: _Optional[int] = ...) -> None: ...

class Log(_message.Message):
    __slots__ = ("address", "identity", "userid", "date", "request", "code", "size")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    address: Address
    identity: str
    userid: str
    date: str
    request: str
    code: int
    size: int
    def __init__(self, address: _Optional[_Union[Address, _Mapping]] = ..., identity: _Optional[str] = ..., userid: _Optional[str] = ..., date: _Optional[str] = ..., request: _Optional[str] = ..., code: _Optional[int] = ..., size: _Optional[int] = ...) -> None: ...

class Logs(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[Log]
    def __init__(self, logs: _Optional[_Iterable[_Union[Log, _Mapping]]] = ...) -> None: ...
