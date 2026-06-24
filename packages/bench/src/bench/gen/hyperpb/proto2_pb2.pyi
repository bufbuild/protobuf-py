from google.protobuf.internal import containers as _containers
from google.protobuf.internal import python_message as _python_message
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
B1_FIELD_NUMBER: _ClassVar[int]
b1: _descriptor.FieldDescriptor
B2_FIELD_NUMBER: _ClassVar[int]
b2: _descriptor.FieldDescriptor
B3_FIELD_NUMBER: _ClassVar[int]
b3: _descriptor.FieldDescriptor
B4_FIELD_NUMBER: _ClassVar[int]
b4: _descriptor.FieldDescriptor
B5_FIELD_NUMBER: _ClassVar[int]
b5: _descriptor.FieldDescriptor
B6_FIELD_NUMBER: _ClassVar[int]
b6: _descriptor.FieldDescriptor
B7_FIELD_NUMBER: _ClassVar[int]
b7: _descriptor.FieldDescriptor
B8_FIELD_NUMBER: _ClassVar[int]
b8: _descriptor.FieldDescriptor
B9_FIELD_NUMBER: _ClassVar[int]
b9: _descriptor.FieldDescriptor
B10_FIELD_NUMBER: _ClassVar[int]
b10: _descriptor.FieldDescriptor
B11_FIELD_NUMBER: _ClassVar[int]
b11: _descriptor.FieldDescriptor
B12_FIELD_NUMBER: _ClassVar[int]
b12: _descriptor.FieldDescriptor
B13_FIELD_NUMBER: _ClassVar[int]
b13: _descriptor.FieldDescriptor
B14_FIELD_NUMBER: _ClassVar[int]
b14: _descriptor.FieldDescriptor
B15_FIELD_NUMBER: _ClassVar[int]
b15: _descriptor.FieldDescriptor
Z_FIELD_NUMBER: _ClassVar[int]
z: _descriptor.FieldDescriptor

class Extensions(_message.Message):
    __slots__ = ()
    Extensions: _python_message._ExtensionDict
    def __init__(self) -> None: ...

class Required(_message.Message):
    __slots__ = ("x", "y", "z")
    class Empty(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: Required
    z: Required.Empty
    def __init__(self, x: _Optional[int] = ..., y: _Optional[_Union[Required, _Mapping]] = ..., z: _Optional[_Union[Required.Empty, _Mapping]] = ...) -> None: ...

class DependsOnRequired(_message.Message):
    __slots__ = ("a", "b", "c")
    class CEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Required
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Required, _Mapping]] = ...) -> None: ...
    A_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    C_FIELD_NUMBER: _ClassVar[int]
    a: Required
    b: _containers.RepeatedCompositeFieldContainer[Required]
    c: _containers.MessageMap[int, Required]
    def __init__(self, a: _Optional[_Union[Required, _Mapping]] = ..., b: _Optional[_Iterable[_Union[Required, _Mapping]]] = ..., c: _Optional[_Mapping[int, Required]] = ...) -> None: ...

class Groups(_message.Message):
    __slots__ = ("singular", "repeated")
    class Singular(_message.Message):
        __slots__ = ("a", "b", "g", "nested")
        class Nested(_message.Message):
            __slots__ = ("a",)
            A_FIELD_NUMBER: _ClassVar[int]
            a: int
            def __init__(self, a: _Optional[int] = ...) -> None: ...
        A_FIELD_NUMBER: _ClassVar[int]
        B_FIELD_NUMBER: _ClassVar[int]
        G_FIELD_NUMBER: _ClassVar[int]
        NESTED_FIELD_NUMBER: _ClassVar[int]
        a: int
        b: int
        g: Groups
        nested: Groups.Singular.Nested
        def __init__(self, a: _Optional[int] = ..., b: _Optional[int] = ..., g: _Optional[_Union[Groups, _Mapping]] = ..., nested: _Optional[_Union[Groups.Singular.Nested, _Mapping]] = ...) -> None: ...
    class Repeated(_message.Message):
        __slots__ = ("a", "b")
        A_FIELD_NUMBER: _ClassVar[int]
        B_FIELD_NUMBER: _ClassVar[int]
        a: int
        b: int
        def __init__(self, a: _Optional[int] = ..., b: _Optional[int] = ...) -> None: ...
    SINGULAR_FIELD_NUMBER: _ClassVar[int]
    REPEATED_FIELD_NUMBER: _ClassVar[int]
    singular: Groups.Singular
    repeated: _containers.RepeatedCompositeFieldContainer[Groups.Repeated]
    def __init__(self, singular: _Optional[_Union[Groups.Singular, _Mapping]] = ..., repeated: _Optional[_Iterable[_Union[Groups.Repeated, _Mapping]]] = ...) -> None: ...
