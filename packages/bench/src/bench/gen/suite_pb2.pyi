from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Case(_message.Message):
    __slots__ = ("name", "typename", "payload")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPENAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    name: str
    typename: str
    payload: bytes
    def __init__(self, name: _Optional[str] = ..., typename: _Optional[str] = ..., payload: _Optional[bytes] = ...) -> None: ...

class Suite(_message.Message):
    __slots__ = ("cases",)
    CASES_FIELD_NUMBER: _ClassVar[int]
    cases: _containers.RepeatedCompositeFieldContainer[Case]
    def __init__(self, cases: _Optional[_Iterable[_Union[Case, _Mapping]]] = ...) -> None: ...
