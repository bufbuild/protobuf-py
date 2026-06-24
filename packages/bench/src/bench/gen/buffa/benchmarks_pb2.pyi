from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BenchmarkDataset(_message.Message):
    __slots__ = ("name", "message_name", "payload")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    name: str
    message_name: str
    payload: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, name: _Optional[str] = ..., message_name: _Optional[str] = ..., payload: _Optional[_Iterable[bytes]] = ...) -> None: ...
