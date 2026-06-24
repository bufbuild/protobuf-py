from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Enum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENUM_UNSPECIFIED: _ClassVar[Enum]
    ENUM_1: _ClassVar[Enum]
    ENUM_2: _ClassVar[Enum]
    ENUM_3: _ClassVar[Enum]
ENUM_UNSPECIFIED: Enum
ENUM_1: Enum
ENUM_2: Enum
ENUM_3: Enum

class Scalars(_message.Message):
    __slots__ = ("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10", "a11", "a12", "a13", "a14", "a15", "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10", "b11", "b12", "b13", "b14", "b15")
    A1_FIELD_NUMBER: _ClassVar[int]
    A2_FIELD_NUMBER: _ClassVar[int]
    A3_FIELD_NUMBER: _ClassVar[int]
    A4_FIELD_NUMBER: _ClassVar[int]
    A5_FIELD_NUMBER: _ClassVar[int]
    A6_FIELD_NUMBER: _ClassVar[int]
    A7_FIELD_NUMBER: _ClassVar[int]
    A8_FIELD_NUMBER: _ClassVar[int]
    A9_FIELD_NUMBER: _ClassVar[int]
    A10_FIELD_NUMBER: _ClassVar[int]
    A11_FIELD_NUMBER: _ClassVar[int]
    A12_FIELD_NUMBER: _ClassVar[int]
    A13_FIELD_NUMBER: _ClassVar[int]
    A14_FIELD_NUMBER: _ClassVar[int]
    A15_FIELD_NUMBER: _ClassVar[int]
    B1_FIELD_NUMBER: _ClassVar[int]
    B2_FIELD_NUMBER: _ClassVar[int]
    B3_FIELD_NUMBER: _ClassVar[int]
    B4_FIELD_NUMBER: _ClassVar[int]
    B5_FIELD_NUMBER: _ClassVar[int]
    B6_FIELD_NUMBER: _ClassVar[int]
    B7_FIELD_NUMBER: _ClassVar[int]
    B8_FIELD_NUMBER: _ClassVar[int]
    B9_FIELD_NUMBER: _ClassVar[int]
    B10_FIELD_NUMBER: _ClassVar[int]
    B11_FIELD_NUMBER: _ClassVar[int]
    B12_FIELD_NUMBER: _ClassVar[int]
    B13_FIELD_NUMBER: _ClassVar[int]
    B14_FIELD_NUMBER: _ClassVar[int]
    B15_FIELD_NUMBER: _ClassVar[int]
    a1: int
    a2: int
    a3: int
    a4: int
    a5: int
    a6: int
    a7: int
    a8: int
    a9: int
    a10: int
    a11: float
    a12: float
    a13: bool
    a14: str
    a15: bytes
    b1: int
    b2: int
    b3: int
    b4: int
    b5: int
    b6: int
    b7: int
    b8: int
    b9: int
    b10: int
    b11: float
    b12: float
    b13: bool
    b14: str
    b15: bytes
    def __init__(self, a1: _Optional[int] = ..., a2: _Optional[int] = ..., a3: _Optional[int] = ..., a4: _Optional[int] = ..., a5: _Optional[int] = ..., a6: _Optional[int] = ..., a7: _Optional[int] = ..., a8: _Optional[int] = ..., a9: _Optional[int] = ..., a10: _Optional[int] = ..., a11: _Optional[float] = ..., a12: _Optional[float] = ..., a13: _Optional[bool] = ..., a14: _Optional[str] = ..., a15: _Optional[bytes] = ..., b1: _Optional[int] = ..., b2: _Optional[int] = ..., b3: _Optional[int] = ..., b4: _Optional[int] = ..., b5: _Optional[int] = ..., b6: _Optional[int] = ..., b7: _Optional[int] = ..., b8: _Optional[int] = ..., b9: _Optional[int] = ..., b10: _Optional[int] = ..., b11: _Optional[float] = ..., b12: _Optional[float] = ..., b13: _Optional[bool] = ..., b14: _Optional[str] = ..., b15: _Optional[bytes] = ...) -> None: ...

class Numbers(_message.Message):
    __slots__ = ("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "aa")
    A1_FIELD_NUMBER: _ClassVar[int]
    A2_FIELD_NUMBER: _ClassVar[int]
    A3_FIELD_NUMBER: _ClassVar[int]
    A4_FIELD_NUMBER: _ClassVar[int]
    A5_FIELD_NUMBER: _ClassVar[int]
    A6_FIELD_NUMBER: _ClassVar[int]
    A7_FIELD_NUMBER: _ClassVar[int]
    A8_FIELD_NUMBER: _ClassVar[int]
    A9_FIELD_NUMBER: _ClassVar[int]
    AA_FIELD_NUMBER: _ClassVar[int]
    a1: int
    a2: int
    a3: int
    a4: int
    a5: int
    a6: int
    a7: int
    a8: int
    a9: int
    aa: int
    def __init__(self, a1: _Optional[int] = ..., a2: _Optional[int] = ..., a3: _Optional[int] = ..., a4: _Optional[int] = ..., a5: _Optional[int] = ..., a6: _Optional[int] = ..., a7: _Optional[int] = ..., a8: _Optional[int] = ..., a9: _Optional[int] = ..., aa: _Optional[int] = ...) -> None: ...

class Repeated(_message.Message):
    __slots__ = ("r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8")
    R1_FIELD_NUMBER: _ClassVar[int]
    R2_FIELD_NUMBER: _ClassVar[int]
    R3_FIELD_NUMBER: _ClassVar[int]
    R4_FIELD_NUMBER: _ClassVar[int]
    R5_FIELD_NUMBER: _ClassVar[int]
    R6_FIELD_NUMBER: _ClassVar[int]
    R7_FIELD_NUMBER: _ClassVar[int]
    R8_FIELD_NUMBER: _ClassVar[int]
    r1: _containers.RepeatedScalarFieldContainer[int]
    r2: _containers.RepeatedScalarFieldContainer[int]
    r3: _containers.RepeatedScalarFieldContainer[int]
    r4: _containers.RepeatedScalarFieldContainer[int]
    r5: _containers.RepeatedScalarFieldContainer[int]
    r6: _containers.RepeatedScalarFieldContainer[int]
    r7: _containers.RepeatedScalarFieldContainer[str]
    r8: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, r1: _Optional[_Iterable[int]] = ..., r2: _Optional[_Iterable[int]] = ..., r3: _Optional[_Iterable[int]] = ..., r4: _Optional[_Iterable[int]] = ..., r5: _Optional[_Iterable[int]] = ..., r6: _Optional[_Iterable[int]] = ..., r7: _Optional[_Iterable[str]] = ..., r8: _Optional[_Iterable[bytes]] = ...) -> None: ...

class Graph(_message.Message):
    __slots__ = ("v", "s", "r")
    V_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    v: int
    s: Graph
    r: _containers.RepeatedCompositeFieldContainer[Graph]
    def __init__(self, v: _Optional[int] = ..., s: _Optional[_Union[Graph, _Mapping]] = ..., r: _Optional[_Iterable[_Union[Graph, _Mapping]]] = ...) -> None: ...

class Oneof(_message.Message):
    __slots__ = ("s1", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "tail")
    S1_FIELD_NUMBER: _ClassVar[int]
    M1_FIELD_NUMBER: _ClassVar[int]
    M2_FIELD_NUMBER: _ClassVar[int]
    M3_FIELD_NUMBER: _ClassVar[int]
    M4_FIELD_NUMBER: _ClassVar[int]
    M5_FIELD_NUMBER: _ClassVar[int]
    M6_FIELD_NUMBER: _ClassVar[int]
    M7_FIELD_NUMBER: _ClassVar[int]
    M8_FIELD_NUMBER: _ClassVar[int]
    M9_FIELD_NUMBER: _ClassVar[int]
    M10_FIELD_NUMBER: _ClassVar[int]
    TAIL_FIELD_NUMBER: _ClassVar[int]
    s1: int
    m1: int
    m2: int
    m3: int
    m4: int
    m5: int
    m6: int
    m7: bool
    m8: str
    m9: bytes
    m10: Oneof
    tail: int
    def __init__(self, s1: _Optional[int] = ..., m1: _Optional[int] = ..., m2: _Optional[int] = ..., m3: _Optional[int] = ..., m4: _Optional[int] = ..., m5: _Optional[int] = ..., m6: _Optional[int] = ..., m7: _Optional[bool] = ..., m8: _Optional[str] = ..., m9: _Optional[bytes] = ..., m10: _Optional[_Union[Oneof, _Mapping]] = ..., tail: _Optional[int] = ...) -> None: ...

class Maps(_message.Message):
    __slots__ = ("m10", "m11", "m12", "m13", "m14", "m15", "m16", "m17", "m18", "m19", "m1a", "m1b", "m1c", "m1d", "m1e", "m1f", "m20", "m21", "m22", "m23", "m24", "m25", "m26", "m27", "m28", "m29", "m2a", "m2b", "m2c", "m2d", "m2e", "m2f", "m30", "m31", "m32", "m33", "m34", "m35", "m36", "m37", "m38", "m39", "m3a", "m3b", "m3c", "m3d", "m3e", "m3f", "m40", "m41", "m42", "m43", "m44", "m45", "m46", "m47", "m48", "m49", "m4a", "m4b", "m4c", "m4d", "m4e", "m4f", "m50", "m51", "m52", "m53", "m54", "m55", "m56", "m57", "m58", "m59", "m5a", "m5b", "m5c", "m5d", "m5e", "m5f", "m60", "m61", "m62", "m63", "m64", "m65", "m66", "m67", "m68", "m69", "m6a", "m6b", "m6c", "m6d", "m6e", "m6f", "m70", "m71", "m72", "m73", "m74", "m75", "m76", "m77", "m78", "m79", "m7a", "m7b", "m7c", "m7d", "m7e", "m7f", "m80", "m81", "m82", "m83", "m84", "m85", "m86", "m87", "m88", "m89", "m8a", "m8b", "m8c", "m8d", "m8e", "m8f", "m90", "m91", "m92", "m93", "m94", "m95", "m96", "m97", "m98", "m99", "m9a", "m9b", "m9c", "m9d", "m9e", "m9f", "ma0", "ma1", "ma2", "ma3", "ma4", "ma5", "ma6", "ma7", "ma8", "ma9", "maa", "mab", "mac", "mad", "mae", "maf", "mb0", "mb1", "mb2", "mb3", "mb4", "mb5", "mb6", "mb7", "mb8", "mb9", "mba", "mbb", "mbc", "mbd", "mbe", "mbf", "mc0", "mc1", "mc2", "mc3", "mc4", "mc5", "mc6", "mc7", "mc8", "mc9", "mca", "mcb", "mcc", "mcd", "mce", "mcf")
    class M10Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M11Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M12Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M13Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M14Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M15Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M16Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M17Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M18Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M19Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M1aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M1bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M1cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M1dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M1eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M1fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M20Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M21Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M22Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M23Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M24Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M25Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M26Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M27Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M28Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M29Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M2aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M2bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M2cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M2dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M2eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M2fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M30Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M31Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M32Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M33Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M34Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M35Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M36Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M37Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M38Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M39Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M3aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M3bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M3cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M3dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M3eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M3fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M40Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M41Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M42Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M43Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M44Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M45Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M46Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M47Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M48Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M49Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M4aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M4bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M4cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M4dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M4eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M4fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M50Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M51Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M52Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M53Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M54Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M55Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M56Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M57Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M58Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M59Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M5aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M5bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M5cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M5dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M5eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M5fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M60Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M61Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M62Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M63Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M64Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M65Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M66Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M67Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M68Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M69Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M6aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M6bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M6cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M6dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M6eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M6fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M70Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M71Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M72Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M73Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M74Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M75Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M76Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M77Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M78Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M79Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M7aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M7bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M7cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M7dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M7eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M7fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M80Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M81Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M82Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M83Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M84Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M85Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M86Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M87Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M88Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M89Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M8aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M8bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M8cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M8dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M8eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M8fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class M90Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M91Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M92Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M93Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M94Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M95Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M96Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M97Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M98Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M99Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class M9aEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M9bEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class M9cEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class M9dEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class M9eEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class M9fEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class Ma0Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma1Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma2Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma3Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma4Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma5Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma6Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma7Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma8Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class Ma9Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    class MaaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class MabEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: float
        def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
    class MacEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bool
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bool] = ...) -> None: ...
    class MadEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: Enum
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class MaeEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    class MafEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: bytes
        def __init__(self, key: _Optional[int] = ..., value: _Optional[bytes] = ...) -> None: ...
    class Mb0Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb1Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb2Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb3Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb4Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb5Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb6Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb7Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb8Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class Mb9Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: int
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[int] = ...) -> None: ...
    class MbaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: float
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[float] = ...) -> None: ...
    class MbbEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: float
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[float] = ...) -> None: ...
    class MbcEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: bool
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[bool] = ...) -> None: ...
    class MbdEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: Enum
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class MbeEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: str
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[str] = ...) -> None: ...
    class MbfEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: bool
        value: bytes
        def __init__(self, key: _Optional[bool] = ..., value: _Optional[bytes] = ...) -> None: ...
    class Mc0Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc1Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc2Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc3Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc4Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc5Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc6Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc7Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc8Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class Mc9Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    class McaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class McbEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    class MccEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bool] = ...) -> None: ...
    class McdEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Enum
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Enum, str]] = ...) -> None: ...
    class MceEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class McfEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    M10_FIELD_NUMBER: _ClassVar[int]
    M11_FIELD_NUMBER: _ClassVar[int]
    M12_FIELD_NUMBER: _ClassVar[int]
    M13_FIELD_NUMBER: _ClassVar[int]
    M14_FIELD_NUMBER: _ClassVar[int]
    M15_FIELD_NUMBER: _ClassVar[int]
    M16_FIELD_NUMBER: _ClassVar[int]
    M17_FIELD_NUMBER: _ClassVar[int]
    M18_FIELD_NUMBER: _ClassVar[int]
    M19_FIELD_NUMBER: _ClassVar[int]
    M1A_FIELD_NUMBER: _ClassVar[int]
    M1B_FIELD_NUMBER: _ClassVar[int]
    M1C_FIELD_NUMBER: _ClassVar[int]
    M1D_FIELD_NUMBER: _ClassVar[int]
    M1E_FIELD_NUMBER: _ClassVar[int]
    M1F_FIELD_NUMBER: _ClassVar[int]
    M20_FIELD_NUMBER: _ClassVar[int]
    M21_FIELD_NUMBER: _ClassVar[int]
    M22_FIELD_NUMBER: _ClassVar[int]
    M23_FIELD_NUMBER: _ClassVar[int]
    M24_FIELD_NUMBER: _ClassVar[int]
    M25_FIELD_NUMBER: _ClassVar[int]
    M26_FIELD_NUMBER: _ClassVar[int]
    M27_FIELD_NUMBER: _ClassVar[int]
    M28_FIELD_NUMBER: _ClassVar[int]
    M29_FIELD_NUMBER: _ClassVar[int]
    M2A_FIELD_NUMBER: _ClassVar[int]
    M2B_FIELD_NUMBER: _ClassVar[int]
    M2C_FIELD_NUMBER: _ClassVar[int]
    M2D_FIELD_NUMBER: _ClassVar[int]
    M2E_FIELD_NUMBER: _ClassVar[int]
    M2F_FIELD_NUMBER: _ClassVar[int]
    M30_FIELD_NUMBER: _ClassVar[int]
    M31_FIELD_NUMBER: _ClassVar[int]
    M32_FIELD_NUMBER: _ClassVar[int]
    M33_FIELD_NUMBER: _ClassVar[int]
    M34_FIELD_NUMBER: _ClassVar[int]
    M35_FIELD_NUMBER: _ClassVar[int]
    M36_FIELD_NUMBER: _ClassVar[int]
    M37_FIELD_NUMBER: _ClassVar[int]
    M38_FIELD_NUMBER: _ClassVar[int]
    M39_FIELD_NUMBER: _ClassVar[int]
    M3A_FIELD_NUMBER: _ClassVar[int]
    M3B_FIELD_NUMBER: _ClassVar[int]
    M3C_FIELD_NUMBER: _ClassVar[int]
    M3D_FIELD_NUMBER: _ClassVar[int]
    M3E_FIELD_NUMBER: _ClassVar[int]
    M3F_FIELD_NUMBER: _ClassVar[int]
    M40_FIELD_NUMBER: _ClassVar[int]
    M41_FIELD_NUMBER: _ClassVar[int]
    M42_FIELD_NUMBER: _ClassVar[int]
    M43_FIELD_NUMBER: _ClassVar[int]
    M44_FIELD_NUMBER: _ClassVar[int]
    M45_FIELD_NUMBER: _ClassVar[int]
    M46_FIELD_NUMBER: _ClassVar[int]
    M47_FIELD_NUMBER: _ClassVar[int]
    M48_FIELD_NUMBER: _ClassVar[int]
    M49_FIELD_NUMBER: _ClassVar[int]
    M4A_FIELD_NUMBER: _ClassVar[int]
    M4B_FIELD_NUMBER: _ClassVar[int]
    M4C_FIELD_NUMBER: _ClassVar[int]
    M4D_FIELD_NUMBER: _ClassVar[int]
    M4E_FIELD_NUMBER: _ClassVar[int]
    M4F_FIELD_NUMBER: _ClassVar[int]
    M50_FIELD_NUMBER: _ClassVar[int]
    M51_FIELD_NUMBER: _ClassVar[int]
    M52_FIELD_NUMBER: _ClassVar[int]
    M53_FIELD_NUMBER: _ClassVar[int]
    M54_FIELD_NUMBER: _ClassVar[int]
    M55_FIELD_NUMBER: _ClassVar[int]
    M56_FIELD_NUMBER: _ClassVar[int]
    M57_FIELD_NUMBER: _ClassVar[int]
    M58_FIELD_NUMBER: _ClassVar[int]
    M59_FIELD_NUMBER: _ClassVar[int]
    M5A_FIELD_NUMBER: _ClassVar[int]
    M5B_FIELD_NUMBER: _ClassVar[int]
    M5C_FIELD_NUMBER: _ClassVar[int]
    M5D_FIELD_NUMBER: _ClassVar[int]
    M5E_FIELD_NUMBER: _ClassVar[int]
    M5F_FIELD_NUMBER: _ClassVar[int]
    M60_FIELD_NUMBER: _ClassVar[int]
    M61_FIELD_NUMBER: _ClassVar[int]
    M62_FIELD_NUMBER: _ClassVar[int]
    M63_FIELD_NUMBER: _ClassVar[int]
    M64_FIELD_NUMBER: _ClassVar[int]
    M65_FIELD_NUMBER: _ClassVar[int]
    M66_FIELD_NUMBER: _ClassVar[int]
    M67_FIELD_NUMBER: _ClassVar[int]
    M68_FIELD_NUMBER: _ClassVar[int]
    M69_FIELD_NUMBER: _ClassVar[int]
    M6A_FIELD_NUMBER: _ClassVar[int]
    M6B_FIELD_NUMBER: _ClassVar[int]
    M6C_FIELD_NUMBER: _ClassVar[int]
    M6D_FIELD_NUMBER: _ClassVar[int]
    M6E_FIELD_NUMBER: _ClassVar[int]
    M6F_FIELD_NUMBER: _ClassVar[int]
    M70_FIELD_NUMBER: _ClassVar[int]
    M71_FIELD_NUMBER: _ClassVar[int]
    M72_FIELD_NUMBER: _ClassVar[int]
    M73_FIELD_NUMBER: _ClassVar[int]
    M74_FIELD_NUMBER: _ClassVar[int]
    M75_FIELD_NUMBER: _ClassVar[int]
    M76_FIELD_NUMBER: _ClassVar[int]
    M77_FIELD_NUMBER: _ClassVar[int]
    M78_FIELD_NUMBER: _ClassVar[int]
    M79_FIELD_NUMBER: _ClassVar[int]
    M7A_FIELD_NUMBER: _ClassVar[int]
    M7B_FIELD_NUMBER: _ClassVar[int]
    M7C_FIELD_NUMBER: _ClassVar[int]
    M7D_FIELD_NUMBER: _ClassVar[int]
    M7E_FIELD_NUMBER: _ClassVar[int]
    M7F_FIELD_NUMBER: _ClassVar[int]
    M80_FIELD_NUMBER: _ClassVar[int]
    M81_FIELD_NUMBER: _ClassVar[int]
    M82_FIELD_NUMBER: _ClassVar[int]
    M83_FIELD_NUMBER: _ClassVar[int]
    M84_FIELD_NUMBER: _ClassVar[int]
    M85_FIELD_NUMBER: _ClassVar[int]
    M86_FIELD_NUMBER: _ClassVar[int]
    M87_FIELD_NUMBER: _ClassVar[int]
    M88_FIELD_NUMBER: _ClassVar[int]
    M89_FIELD_NUMBER: _ClassVar[int]
    M8A_FIELD_NUMBER: _ClassVar[int]
    M8B_FIELD_NUMBER: _ClassVar[int]
    M8C_FIELD_NUMBER: _ClassVar[int]
    M8D_FIELD_NUMBER: _ClassVar[int]
    M8E_FIELD_NUMBER: _ClassVar[int]
    M8F_FIELD_NUMBER: _ClassVar[int]
    M90_FIELD_NUMBER: _ClassVar[int]
    M91_FIELD_NUMBER: _ClassVar[int]
    M92_FIELD_NUMBER: _ClassVar[int]
    M93_FIELD_NUMBER: _ClassVar[int]
    M94_FIELD_NUMBER: _ClassVar[int]
    M95_FIELD_NUMBER: _ClassVar[int]
    M96_FIELD_NUMBER: _ClassVar[int]
    M97_FIELD_NUMBER: _ClassVar[int]
    M98_FIELD_NUMBER: _ClassVar[int]
    M99_FIELD_NUMBER: _ClassVar[int]
    M9A_FIELD_NUMBER: _ClassVar[int]
    M9B_FIELD_NUMBER: _ClassVar[int]
    M9C_FIELD_NUMBER: _ClassVar[int]
    M9D_FIELD_NUMBER: _ClassVar[int]
    M9E_FIELD_NUMBER: _ClassVar[int]
    M9F_FIELD_NUMBER: _ClassVar[int]
    MA0_FIELD_NUMBER: _ClassVar[int]
    MA1_FIELD_NUMBER: _ClassVar[int]
    MA2_FIELD_NUMBER: _ClassVar[int]
    MA3_FIELD_NUMBER: _ClassVar[int]
    MA4_FIELD_NUMBER: _ClassVar[int]
    MA5_FIELD_NUMBER: _ClassVar[int]
    MA6_FIELD_NUMBER: _ClassVar[int]
    MA7_FIELD_NUMBER: _ClassVar[int]
    MA8_FIELD_NUMBER: _ClassVar[int]
    MA9_FIELD_NUMBER: _ClassVar[int]
    MAA_FIELD_NUMBER: _ClassVar[int]
    MAB_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    MAD_FIELD_NUMBER: _ClassVar[int]
    MAE_FIELD_NUMBER: _ClassVar[int]
    MAF_FIELD_NUMBER: _ClassVar[int]
    MB0_FIELD_NUMBER: _ClassVar[int]
    MB1_FIELD_NUMBER: _ClassVar[int]
    MB2_FIELD_NUMBER: _ClassVar[int]
    MB3_FIELD_NUMBER: _ClassVar[int]
    MB4_FIELD_NUMBER: _ClassVar[int]
    MB5_FIELD_NUMBER: _ClassVar[int]
    MB6_FIELD_NUMBER: _ClassVar[int]
    MB7_FIELD_NUMBER: _ClassVar[int]
    MB8_FIELD_NUMBER: _ClassVar[int]
    MB9_FIELD_NUMBER: _ClassVar[int]
    MBA_FIELD_NUMBER: _ClassVar[int]
    MBB_FIELD_NUMBER: _ClassVar[int]
    MBC_FIELD_NUMBER: _ClassVar[int]
    MBD_FIELD_NUMBER: _ClassVar[int]
    MBE_FIELD_NUMBER: _ClassVar[int]
    MBF_FIELD_NUMBER: _ClassVar[int]
    MC0_FIELD_NUMBER: _ClassVar[int]
    MC1_FIELD_NUMBER: _ClassVar[int]
    MC2_FIELD_NUMBER: _ClassVar[int]
    MC3_FIELD_NUMBER: _ClassVar[int]
    MC4_FIELD_NUMBER: _ClassVar[int]
    MC5_FIELD_NUMBER: _ClassVar[int]
    MC6_FIELD_NUMBER: _ClassVar[int]
    MC7_FIELD_NUMBER: _ClassVar[int]
    MC8_FIELD_NUMBER: _ClassVar[int]
    MC9_FIELD_NUMBER: _ClassVar[int]
    MCA_FIELD_NUMBER: _ClassVar[int]
    MCB_FIELD_NUMBER: _ClassVar[int]
    MCC_FIELD_NUMBER: _ClassVar[int]
    MCD_FIELD_NUMBER: _ClassVar[int]
    MCE_FIELD_NUMBER: _ClassVar[int]
    MCF_FIELD_NUMBER: _ClassVar[int]
    m10: _containers.ScalarMap[int, int]
    m11: _containers.ScalarMap[int, int]
    m12: _containers.ScalarMap[int, int]
    m13: _containers.ScalarMap[int, int]
    m14: _containers.ScalarMap[int, int]
    m15: _containers.ScalarMap[int, int]
    m16: _containers.ScalarMap[int, int]
    m17: _containers.ScalarMap[int, int]
    m18: _containers.ScalarMap[int, int]
    m19: _containers.ScalarMap[int, int]
    m1a: _containers.ScalarMap[int, float]
    m1b: _containers.ScalarMap[int, float]
    m1c: _containers.ScalarMap[int, bool]
    m1d: _containers.ScalarMap[int, Enum]
    m1e: _containers.ScalarMap[int, str]
    m1f: _containers.ScalarMap[int, bytes]
    m20: _containers.ScalarMap[int, int]
    m21: _containers.ScalarMap[int, int]
    m22: _containers.ScalarMap[int, int]
    m23: _containers.ScalarMap[int, int]
    m24: _containers.ScalarMap[int, int]
    m25: _containers.ScalarMap[int, int]
    m26: _containers.ScalarMap[int, int]
    m27: _containers.ScalarMap[int, int]
    m28: _containers.ScalarMap[int, int]
    m29: _containers.ScalarMap[int, int]
    m2a: _containers.ScalarMap[int, float]
    m2b: _containers.ScalarMap[int, float]
    m2c: _containers.ScalarMap[int, bool]
    m2d: _containers.ScalarMap[int, Enum]
    m2e: _containers.ScalarMap[int, str]
    m2f: _containers.ScalarMap[int, bytes]
    m30: _containers.ScalarMap[int, int]
    m31: _containers.ScalarMap[int, int]
    m32: _containers.ScalarMap[int, int]
    m33: _containers.ScalarMap[int, int]
    m34: _containers.ScalarMap[int, int]
    m35: _containers.ScalarMap[int, int]
    m36: _containers.ScalarMap[int, int]
    m37: _containers.ScalarMap[int, int]
    m38: _containers.ScalarMap[int, int]
    m39: _containers.ScalarMap[int, int]
    m3a: _containers.ScalarMap[int, float]
    m3b: _containers.ScalarMap[int, float]
    m3c: _containers.ScalarMap[int, bool]
    m3d: _containers.ScalarMap[int, Enum]
    m3e: _containers.ScalarMap[int, str]
    m3f: _containers.ScalarMap[int, bytes]
    m40: _containers.ScalarMap[int, int]
    m41: _containers.ScalarMap[int, int]
    m42: _containers.ScalarMap[int, int]
    m43: _containers.ScalarMap[int, int]
    m44: _containers.ScalarMap[int, int]
    m45: _containers.ScalarMap[int, int]
    m46: _containers.ScalarMap[int, int]
    m47: _containers.ScalarMap[int, int]
    m48: _containers.ScalarMap[int, int]
    m49: _containers.ScalarMap[int, int]
    m4a: _containers.ScalarMap[int, float]
    m4b: _containers.ScalarMap[int, float]
    m4c: _containers.ScalarMap[int, bool]
    m4d: _containers.ScalarMap[int, Enum]
    m4e: _containers.ScalarMap[int, str]
    m4f: _containers.ScalarMap[int, bytes]
    m50: _containers.ScalarMap[int, int]
    m51: _containers.ScalarMap[int, int]
    m52: _containers.ScalarMap[int, int]
    m53: _containers.ScalarMap[int, int]
    m54: _containers.ScalarMap[int, int]
    m55: _containers.ScalarMap[int, int]
    m56: _containers.ScalarMap[int, int]
    m57: _containers.ScalarMap[int, int]
    m58: _containers.ScalarMap[int, int]
    m59: _containers.ScalarMap[int, int]
    m5a: _containers.ScalarMap[int, float]
    m5b: _containers.ScalarMap[int, float]
    m5c: _containers.ScalarMap[int, bool]
    m5d: _containers.ScalarMap[int, Enum]
    m5e: _containers.ScalarMap[int, str]
    m5f: _containers.ScalarMap[int, bytes]
    m60: _containers.ScalarMap[int, int]
    m61: _containers.ScalarMap[int, int]
    m62: _containers.ScalarMap[int, int]
    m63: _containers.ScalarMap[int, int]
    m64: _containers.ScalarMap[int, int]
    m65: _containers.ScalarMap[int, int]
    m66: _containers.ScalarMap[int, int]
    m67: _containers.ScalarMap[int, int]
    m68: _containers.ScalarMap[int, int]
    m69: _containers.ScalarMap[int, int]
    m6a: _containers.ScalarMap[int, float]
    m6b: _containers.ScalarMap[int, float]
    m6c: _containers.ScalarMap[int, bool]
    m6d: _containers.ScalarMap[int, Enum]
    m6e: _containers.ScalarMap[int, str]
    m6f: _containers.ScalarMap[int, bytes]
    m70: _containers.ScalarMap[int, int]
    m71: _containers.ScalarMap[int, int]
    m72: _containers.ScalarMap[int, int]
    m73: _containers.ScalarMap[int, int]
    m74: _containers.ScalarMap[int, int]
    m75: _containers.ScalarMap[int, int]
    m76: _containers.ScalarMap[int, int]
    m77: _containers.ScalarMap[int, int]
    m78: _containers.ScalarMap[int, int]
    m79: _containers.ScalarMap[int, int]
    m7a: _containers.ScalarMap[int, float]
    m7b: _containers.ScalarMap[int, float]
    m7c: _containers.ScalarMap[int, bool]
    m7d: _containers.ScalarMap[int, Enum]
    m7e: _containers.ScalarMap[int, str]
    m7f: _containers.ScalarMap[int, bytes]
    m80: _containers.ScalarMap[int, int]
    m81: _containers.ScalarMap[int, int]
    m82: _containers.ScalarMap[int, int]
    m83: _containers.ScalarMap[int, int]
    m84: _containers.ScalarMap[int, int]
    m85: _containers.ScalarMap[int, int]
    m86: _containers.ScalarMap[int, int]
    m87: _containers.ScalarMap[int, int]
    m88: _containers.ScalarMap[int, int]
    m89: _containers.ScalarMap[int, int]
    m8a: _containers.ScalarMap[int, float]
    m8b: _containers.ScalarMap[int, float]
    m8c: _containers.ScalarMap[int, bool]
    m8d: _containers.ScalarMap[int, Enum]
    m8e: _containers.ScalarMap[int, str]
    m8f: _containers.ScalarMap[int, bytes]
    m90: _containers.ScalarMap[int, int]
    m91: _containers.ScalarMap[int, int]
    m92: _containers.ScalarMap[int, int]
    m93: _containers.ScalarMap[int, int]
    m94: _containers.ScalarMap[int, int]
    m95: _containers.ScalarMap[int, int]
    m96: _containers.ScalarMap[int, int]
    m97: _containers.ScalarMap[int, int]
    m98: _containers.ScalarMap[int, int]
    m99: _containers.ScalarMap[int, int]
    m9a: _containers.ScalarMap[int, float]
    m9b: _containers.ScalarMap[int, float]
    m9c: _containers.ScalarMap[int, bool]
    m9d: _containers.ScalarMap[int, Enum]
    m9e: _containers.ScalarMap[int, str]
    m9f: _containers.ScalarMap[int, bytes]
    ma0: _containers.ScalarMap[int, int]
    ma1: _containers.ScalarMap[int, int]
    ma2: _containers.ScalarMap[int, int]
    ma3: _containers.ScalarMap[int, int]
    ma4: _containers.ScalarMap[int, int]
    ma5: _containers.ScalarMap[int, int]
    ma6: _containers.ScalarMap[int, int]
    ma7: _containers.ScalarMap[int, int]
    ma8: _containers.ScalarMap[int, int]
    ma9: _containers.ScalarMap[int, int]
    maa: _containers.ScalarMap[int, float]
    mab: _containers.ScalarMap[int, float]
    mac: _containers.ScalarMap[int, bool]
    mad: _containers.ScalarMap[int, Enum]
    mae: _containers.ScalarMap[int, str]
    maf: _containers.ScalarMap[int, bytes]
    mb0: _containers.ScalarMap[bool, int]
    mb1: _containers.ScalarMap[bool, int]
    mb2: _containers.ScalarMap[bool, int]
    mb3: _containers.ScalarMap[bool, int]
    mb4: _containers.ScalarMap[bool, int]
    mb5: _containers.ScalarMap[bool, int]
    mb6: _containers.ScalarMap[bool, int]
    mb7: _containers.ScalarMap[bool, int]
    mb8: _containers.ScalarMap[bool, int]
    mb9: _containers.ScalarMap[bool, int]
    mba: _containers.ScalarMap[bool, float]
    mbb: _containers.ScalarMap[bool, float]
    mbc: _containers.ScalarMap[bool, bool]
    mbd: _containers.ScalarMap[bool, Enum]
    mbe: _containers.ScalarMap[bool, str]
    mbf: _containers.ScalarMap[bool, bytes]
    mc0: _containers.ScalarMap[str, int]
    mc1: _containers.ScalarMap[str, int]
    mc2: _containers.ScalarMap[str, int]
    mc3: _containers.ScalarMap[str, int]
    mc4: _containers.ScalarMap[str, int]
    mc5: _containers.ScalarMap[str, int]
    mc6: _containers.ScalarMap[str, int]
    mc7: _containers.ScalarMap[str, int]
    mc8: _containers.ScalarMap[str, int]
    mc9: _containers.ScalarMap[str, int]
    mca: _containers.ScalarMap[str, float]
    mcb: _containers.ScalarMap[str, float]
    mcc: _containers.ScalarMap[str, bool]
    mcd: _containers.ScalarMap[str, Enum]
    mce: _containers.ScalarMap[str, str]
    mcf: _containers.ScalarMap[str, bytes]
    def __init__(self, m10: _Optional[_Mapping[int, int]] = ..., m11: _Optional[_Mapping[int, int]] = ..., m12: _Optional[_Mapping[int, int]] = ..., m13: _Optional[_Mapping[int, int]] = ..., m14: _Optional[_Mapping[int, int]] = ..., m15: _Optional[_Mapping[int, int]] = ..., m16: _Optional[_Mapping[int, int]] = ..., m17: _Optional[_Mapping[int, int]] = ..., m18: _Optional[_Mapping[int, int]] = ..., m19: _Optional[_Mapping[int, int]] = ..., m1a: _Optional[_Mapping[int, float]] = ..., m1b: _Optional[_Mapping[int, float]] = ..., m1c: _Optional[_Mapping[int, bool]] = ..., m1d: _Optional[_Mapping[int, Enum]] = ..., m1e: _Optional[_Mapping[int, str]] = ..., m1f: _Optional[_Mapping[int, bytes]] = ..., m20: _Optional[_Mapping[int, int]] = ..., m21: _Optional[_Mapping[int, int]] = ..., m22: _Optional[_Mapping[int, int]] = ..., m23: _Optional[_Mapping[int, int]] = ..., m24: _Optional[_Mapping[int, int]] = ..., m25: _Optional[_Mapping[int, int]] = ..., m26: _Optional[_Mapping[int, int]] = ..., m27: _Optional[_Mapping[int, int]] = ..., m28: _Optional[_Mapping[int, int]] = ..., m29: _Optional[_Mapping[int, int]] = ..., m2a: _Optional[_Mapping[int, float]] = ..., m2b: _Optional[_Mapping[int, float]] = ..., m2c: _Optional[_Mapping[int, bool]] = ..., m2d: _Optional[_Mapping[int, Enum]] = ..., m2e: _Optional[_Mapping[int, str]] = ..., m2f: _Optional[_Mapping[int, bytes]] = ..., m30: _Optional[_Mapping[int, int]] = ..., m31: _Optional[_Mapping[int, int]] = ..., m32: _Optional[_Mapping[int, int]] = ..., m33: _Optional[_Mapping[int, int]] = ..., m34: _Optional[_Mapping[int, int]] = ..., m35: _Optional[_Mapping[int, int]] = ..., m36: _Optional[_Mapping[int, int]] = ..., m37: _Optional[_Mapping[int, int]] = ..., m38: _Optional[_Mapping[int, int]] = ..., m39: _Optional[_Mapping[int, int]] = ..., m3a: _Optional[_Mapping[int, float]] = ..., m3b: _Optional[_Mapping[int, float]] = ..., m3c: _Optional[_Mapping[int, bool]] = ..., m3d: _Optional[_Mapping[int, Enum]] = ..., m3e: _Optional[_Mapping[int, str]] = ..., m3f: _Optional[_Mapping[int, bytes]] = ..., m40: _Optional[_Mapping[int, int]] = ..., m41: _Optional[_Mapping[int, int]] = ..., m42: _Optional[_Mapping[int, int]] = ..., m43: _Optional[_Mapping[int, int]] = ..., m44: _Optional[_Mapping[int, int]] = ..., m45: _Optional[_Mapping[int, int]] = ..., m46: _Optional[_Mapping[int, int]] = ..., m47: _Optional[_Mapping[int, int]] = ..., m48: _Optional[_Mapping[int, int]] = ..., m49: _Optional[_Mapping[int, int]] = ..., m4a: _Optional[_Mapping[int, float]] = ..., m4b: _Optional[_Mapping[int, float]] = ..., m4c: _Optional[_Mapping[int, bool]] = ..., m4d: _Optional[_Mapping[int, Enum]] = ..., m4e: _Optional[_Mapping[int, str]] = ..., m4f: _Optional[_Mapping[int, bytes]] = ..., m50: _Optional[_Mapping[int, int]] = ..., m51: _Optional[_Mapping[int, int]] = ..., m52: _Optional[_Mapping[int, int]] = ..., m53: _Optional[_Mapping[int, int]] = ..., m54: _Optional[_Mapping[int, int]] = ..., m55: _Optional[_Mapping[int, int]] = ..., m56: _Optional[_Mapping[int, int]] = ..., m57: _Optional[_Mapping[int, int]] = ..., m58: _Optional[_Mapping[int, int]] = ..., m59: _Optional[_Mapping[int, int]] = ..., m5a: _Optional[_Mapping[int, float]] = ..., m5b: _Optional[_Mapping[int, float]] = ..., m5c: _Optional[_Mapping[int, bool]] = ..., m5d: _Optional[_Mapping[int, Enum]] = ..., m5e: _Optional[_Mapping[int, str]] = ..., m5f: _Optional[_Mapping[int, bytes]] = ..., m60: _Optional[_Mapping[int, int]] = ..., m61: _Optional[_Mapping[int, int]] = ..., m62: _Optional[_Mapping[int, int]] = ..., m63: _Optional[_Mapping[int, int]] = ..., m64: _Optional[_Mapping[int, int]] = ..., m65: _Optional[_Mapping[int, int]] = ..., m66: _Optional[_Mapping[int, int]] = ..., m67: _Optional[_Mapping[int, int]] = ..., m68: _Optional[_Mapping[int, int]] = ..., m69: _Optional[_Mapping[int, int]] = ..., m6a: _Optional[_Mapping[int, float]] = ..., m6b: _Optional[_Mapping[int, float]] = ..., m6c: _Optional[_Mapping[int, bool]] = ..., m6d: _Optional[_Mapping[int, Enum]] = ..., m6e: _Optional[_Mapping[int, str]] = ..., m6f: _Optional[_Mapping[int, bytes]] = ..., m70: _Optional[_Mapping[int, int]] = ..., m71: _Optional[_Mapping[int, int]] = ..., m72: _Optional[_Mapping[int, int]] = ..., m73: _Optional[_Mapping[int, int]] = ..., m74: _Optional[_Mapping[int, int]] = ..., m75: _Optional[_Mapping[int, int]] = ..., m76: _Optional[_Mapping[int, int]] = ..., m77: _Optional[_Mapping[int, int]] = ..., m78: _Optional[_Mapping[int, int]] = ..., m79: _Optional[_Mapping[int, int]] = ..., m7a: _Optional[_Mapping[int, float]] = ..., m7b: _Optional[_Mapping[int, float]] = ..., m7c: _Optional[_Mapping[int, bool]] = ..., m7d: _Optional[_Mapping[int, Enum]] = ..., m7e: _Optional[_Mapping[int, str]] = ..., m7f: _Optional[_Mapping[int, bytes]] = ..., m80: _Optional[_Mapping[int, int]] = ..., m81: _Optional[_Mapping[int, int]] = ..., m82: _Optional[_Mapping[int, int]] = ..., m83: _Optional[_Mapping[int, int]] = ..., m84: _Optional[_Mapping[int, int]] = ..., m85: _Optional[_Mapping[int, int]] = ..., m86: _Optional[_Mapping[int, int]] = ..., m87: _Optional[_Mapping[int, int]] = ..., m88: _Optional[_Mapping[int, int]] = ..., m89: _Optional[_Mapping[int, int]] = ..., m8a: _Optional[_Mapping[int, float]] = ..., m8b: _Optional[_Mapping[int, float]] = ..., m8c: _Optional[_Mapping[int, bool]] = ..., m8d: _Optional[_Mapping[int, Enum]] = ..., m8e: _Optional[_Mapping[int, str]] = ..., m8f: _Optional[_Mapping[int, bytes]] = ..., m90: _Optional[_Mapping[int, int]] = ..., m91: _Optional[_Mapping[int, int]] = ..., m92: _Optional[_Mapping[int, int]] = ..., m93: _Optional[_Mapping[int, int]] = ..., m94: _Optional[_Mapping[int, int]] = ..., m95: _Optional[_Mapping[int, int]] = ..., m96: _Optional[_Mapping[int, int]] = ..., m97: _Optional[_Mapping[int, int]] = ..., m98: _Optional[_Mapping[int, int]] = ..., m99: _Optional[_Mapping[int, int]] = ..., m9a: _Optional[_Mapping[int, float]] = ..., m9b: _Optional[_Mapping[int, float]] = ..., m9c: _Optional[_Mapping[int, bool]] = ..., m9d: _Optional[_Mapping[int, Enum]] = ..., m9e: _Optional[_Mapping[int, str]] = ..., m9f: _Optional[_Mapping[int, bytes]] = ..., ma0: _Optional[_Mapping[int, int]] = ..., ma1: _Optional[_Mapping[int, int]] = ..., ma2: _Optional[_Mapping[int, int]] = ..., ma3: _Optional[_Mapping[int, int]] = ..., ma4: _Optional[_Mapping[int, int]] = ..., ma5: _Optional[_Mapping[int, int]] = ..., ma6: _Optional[_Mapping[int, int]] = ..., ma7: _Optional[_Mapping[int, int]] = ..., ma8: _Optional[_Mapping[int, int]] = ..., ma9: _Optional[_Mapping[int, int]] = ..., maa: _Optional[_Mapping[int, float]] = ..., mab: _Optional[_Mapping[int, float]] = ..., mac: _Optional[_Mapping[int, bool]] = ..., mad: _Optional[_Mapping[int, Enum]] = ..., mae: _Optional[_Mapping[int, str]] = ..., maf: _Optional[_Mapping[int, bytes]] = ..., mb0: _Optional[_Mapping[bool, int]] = ..., mb1: _Optional[_Mapping[bool, int]] = ..., mb2: _Optional[_Mapping[bool, int]] = ..., mb3: _Optional[_Mapping[bool, int]] = ..., mb4: _Optional[_Mapping[bool, int]] = ..., mb5: _Optional[_Mapping[bool, int]] = ..., mb6: _Optional[_Mapping[bool, int]] = ..., mb7: _Optional[_Mapping[bool, int]] = ..., mb8: _Optional[_Mapping[bool, int]] = ..., mb9: _Optional[_Mapping[bool, int]] = ..., mba: _Optional[_Mapping[bool, float]] = ..., mbb: _Optional[_Mapping[bool, float]] = ..., mbc: _Optional[_Mapping[bool, bool]] = ..., mbd: _Optional[_Mapping[bool, Enum]] = ..., mbe: _Optional[_Mapping[bool, str]] = ..., mbf: _Optional[_Mapping[bool, bytes]] = ..., mc0: _Optional[_Mapping[str, int]] = ..., mc1: _Optional[_Mapping[str, int]] = ..., mc2: _Optional[_Mapping[str, int]] = ..., mc3: _Optional[_Mapping[str, int]] = ..., mc4: _Optional[_Mapping[str, int]] = ..., mc5: _Optional[_Mapping[str, int]] = ..., mc6: _Optional[_Mapping[str, int]] = ..., mc7: _Optional[_Mapping[str, int]] = ..., mc8: _Optional[_Mapping[str, int]] = ..., mc9: _Optional[_Mapping[str, int]] = ..., mca: _Optional[_Mapping[str, float]] = ..., mcb: _Optional[_Mapping[str, float]] = ..., mcc: _Optional[_Mapping[str, bool]] = ..., mcd: _Optional[_Mapping[str, Enum]] = ..., mce: _Optional[_Mapping[str, str]] = ..., mcf: _Optional[_Mapping[str, bytes]] = ...) -> None: ...

class MessageMaps(_message.Message):
    __slots__ = ("scalars", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "ma", "mc")
    class M1Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M2Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M3Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M4Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M5Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M6Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M7Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M8Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class M9Entry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class MaEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: MessageMaps
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    class McEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: MessageMaps
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[MessageMaps, _Mapping]] = ...) -> None: ...
    SCALARS_FIELD_NUMBER: _ClassVar[int]
    M1_FIELD_NUMBER: _ClassVar[int]
    M2_FIELD_NUMBER: _ClassVar[int]
    M3_FIELD_NUMBER: _ClassVar[int]
    M4_FIELD_NUMBER: _ClassVar[int]
    M5_FIELD_NUMBER: _ClassVar[int]
    M6_FIELD_NUMBER: _ClassVar[int]
    M7_FIELD_NUMBER: _ClassVar[int]
    M8_FIELD_NUMBER: _ClassVar[int]
    M9_FIELD_NUMBER: _ClassVar[int]
    MA_FIELD_NUMBER: _ClassVar[int]
    MC_FIELD_NUMBER: _ClassVar[int]
    scalars: Scalars
    m1: _containers.MessageMap[int, MessageMaps]
    m2: _containers.MessageMap[int, MessageMaps]
    m3: _containers.MessageMap[int, MessageMaps]
    m4: _containers.MessageMap[int, MessageMaps]
    m5: _containers.MessageMap[int, MessageMaps]
    m6: _containers.MessageMap[int, MessageMaps]
    m7: _containers.MessageMap[int, MessageMaps]
    m8: _containers.MessageMap[int, MessageMaps]
    m9: _containers.MessageMap[int, MessageMaps]
    ma: _containers.MessageMap[int, MessageMaps]
    mc: _containers.MessageMap[str, MessageMaps]
    def __init__(self, scalars: _Optional[_Union[Scalars, _Mapping]] = ..., m1: _Optional[_Mapping[int, MessageMaps]] = ..., m2: _Optional[_Mapping[int, MessageMaps]] = ..., m3: _Optional[_Mapping[int, MessageMaps]] = ..., m4: _Optional[_Mapping[int, MessageMaps]] = ..., m5: _Optional[_Mapping[int, MessageMaps]] = ..., m6: _Optional[_Mapping[int, MessageMaps]] = ..., m7: _Optional[_Mapping[int, MessageMaps]] = ..., m8: _Optional[_Mapping[int, MessageMaps]] = ..., m9: _Optional[_Mapping[int, MessageMaps]] = ..., ma: _Optional[_Mapping[int, MessageMaps]] = ..., mc: _Optional[_Mapping[str, MessageMaps]] = ...) -> None: ...

class Pathological(_message.Message):
    __slots__ = ("x",)
    class Inner(_message.Message):
        __slots__ = ("x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "xa", "xb", "xc", "xd", "xe", "xf", "actual")
        X1_FIELD_NUMBER: _ClassVar[int]
        X2_FIELD_NUMBER: _ClassVar[int]
        X3_FIELD_NUMBER: _ClassVar[int]
        X4_FIELD_NUMBER: _ClassVar[int]
        X5_FIELD_NUMBER: _ClassVar[int]
        X6_FIELD_NUMBER: _ClassVar[int]
        X7_FIELD_NUMBER: _ClassVar[int]
        X8_FIELD_NUMBER: _ClassVar[int]
        X9_FIELD_NUMBER: _ClassVar[int]
        XA_FIELD_NUMBER: _ClassVar[int]
        XB_FIELD_NUMBER: _ClassVar[int]
        XC_FIELD_NUMBER: _ClassVar[int]
        XD_FIELD_NUMBER: _ClassVar[int]
        XE_FIELD_NUMBER: _ClassVar[int]
        XF_FIELD_NUMBER: _ClassVar[int]
        ACTUAL_FIELD_NUMBER: _ClassVar[int]
        x1: int
        x2: int
        x3: int
        x4: int
        x5: int
        x6: int
        x7: int
        x8: int
        x9: int
        xa: int
        xb: int
        xc: int
        xd: int
        xe: int
        xf: int
        actual: str
        def __init__(self, x1: _Optional[int] = ..., x2: _Optional[int] = ..., x3: _Optional[int] = ..., x4: _Optional[int] = ..., x5: _Optional[int] = ..., x6: _Optional[int] = ..., x7: _Optional[int] = ..., x8: _Optional[int] = ..., x9: _Optional[int] = ..., xa: _Optional[int] = ..., xb: _Optional[int] = ..., xc: _Optional[int] = ..., xd: _Optional[int] = ..., xe: _Optional[int] = ..., xf: _Optional[int] = ..., actual: _Optional[str] = ...) -> None: ...
    X_FIELD_NUMBER: _ClassVar[int]
    x: _containers.RepeatedCompositeFieldContainer[Pathological.Inner]
    def __init__(self, x: _Optional[_Iterable[_Union[Pathological.Inner, _Mapping]]] = ...) -> None: ...
