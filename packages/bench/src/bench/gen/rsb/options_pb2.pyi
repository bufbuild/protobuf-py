from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
M_FIELD_NUMBER: _ClassVar[int]
m: _descriptor.FieldDescriptor
F_FIELD_NUMBER: _ClassVar[int]
f: _descriptor.FieldDescriptor

class MessageOptions(_message.Message):
    __slots__ = ("max_depth",)
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    max_depth: int
    def __init__(self, max_depth: _Optional[int] = ...) -> None: ...

class FieldOptions(_message.Message):
    __slots__ = ("p", "int", "uint", "len")
    class Int(_message.Message):
        __slots__ = ("min", "max")
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class Uint(_message.Message):
        __slots__ = ("min", "max")
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class Len(_message.Message):
        __slots__ = ("min", "max")
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    P_FIELD_NUMBER: _ClassVar[int]
    INT_FIELD_NUMBER: _ClassVar[int]
    UINT_FIELD_NUMBER: _ClassVar[int]
    LEN_FIELD_NUMBER: _ClassVar[int]
    p: float
    int: FieldOptions.Int
    uint: FieldOptions.Uint
    len: FieldOptions.Len
    def __init__(self, p: _Optional[float] = ..., int: _Optional[_Union[FieldOptions.Int, _Mapping]] = ..., uint: _Optional[_Union[FieldOptions.Uint, _Mapping]] = ..., len: _Optional[_Union[FieldOptions.Len, _Mapping]] = ...) -> None: ...
