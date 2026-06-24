from ...rsb import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vector3(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Triangle(_message.Message):
    __slots__ = ("v0", "v1", "v2", "normal")
    V0_FIELD_NUMBER: _ClassVar[int]
    V1_FIELD_NUMBER: _ClassVar[int]
    V2_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    v0: Vector3
    v1: Vector3
    v2: Vector3
    normal: Vector3
    def __init__(self, v0: _Optional[_Union[Vector3, _Mapping]] = ..., v1: _Optional[_Union[Vector3, _Mapping]] = ..., v2: _Optional[_Union[Vector3, _Mapping]] = ..., normal: _Optional[_Union[Vector3, _Mapping]] = ...) -> None: ...

class Mesh(_message.Message):
    __slots__ = ("triangles",)
    TRIANGLES_FIELD_NUMBER: _ClassVar[int]
    triangles: _containers.RepeatedCompositeFieldContainer[Triangle]
    def __init__(self, triangles: _Optional[_Iterable[_Union[Triangle, _Mapping]]] = ...) -> None: ...
