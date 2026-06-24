from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message2(_message.Message):
    __slots__ = ("f_0", "f_4", "f_5", "f_6", "f_7", "f_8", "f_11", "f_13", "f_15")
    class M1(_message.Message):
        __slots__ = ("f_0", "f_2", "f_3", "f_4", "f_5")
        class M9(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
        class M12(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, f_0: _Optional[_Iterable[int]] = ...) -> None: ...
        class M16(_message.Message):
            __slots__ = ("f_0", "f_2")
            class M23(_message.Message):
                __slots__ = ("f_0", "f_1", "f_4", "f_5", "f_6", "f_7", "f_9", "f_10", "f_11", "f_12", "f_14")
                class M27(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                class M30(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class E13(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E13_UNSPECIFIED: _ClassVar[Message2.M1.M16.M23.M30.E13]
                        E13_CONST_1: _ClassVar[Message2.M1.M16.M23.M30.E13]
                        E13_CONST_2: _ClassVar[Message2.M1.M16.M23.M30.E13]
                        E13_CONST_3: _ClassVar[Message2.M1.M16.M23.M30.E13]
                        E13_CONST_4: _ClassVar[Message2.M1.M16.M23.M30.E13]
                        E13_CONST_5: _ClassVar[Message2.M1.M16.M23.M30.E13]
                    E13_UNSPECIFIED: Message2.M1.M16.M23.M30.E13
                    E13_CONST_1: Message2.M1.M16.M23.M30.E13
                    E13_CONST_2: Message2.M1.M16.M23.M30.E13
                    E13_CONST_3: Message2.M1.M16.M23.M30.E13
                    E13_CONST_4: Message2.M1.M16.M23.M30.E13
                    E13_CONST_5: Message2.M1.M16.M23.M30.E13
                    class M58(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message2.M1.M16.M23.M30.E13
                    f_2: _containers.RepeatedCompositeFieldContainer[Message2.M1.M16.M23.M30.M58]
                    def __init__(self, f_0: _Optional[_Union[Message2.M1.M16.M23.M30.E13, str]] = ..., f_2: _Optional[_Iterable[_Union[Message2.M1.M16.M23.M30.M58, _Mapping]]] = ...) -> None: ...
                class M32(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                class M34(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M50(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: bytes
                        def __init__(self, f_0: _Optional[bytes] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: bytes
                    f_2: Message2.M1.M16.M23.M34.M50
                    def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Union[Message2.M1.M16.M23.M34.M50, _Mapping]] = ...) -> None: ...
                class M38(_message.Message):
                    __slots__ = ("f_0",)
                    class E17(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E17_UNSPECIFIED: _ClassVar[Message2.M1.M16.M23.M38.E17]
                        E17_CONST_1: _ClassVar[Message2.M1.M16.M23.M38.E17]
                        E17_CONST_2: _ClassVar[Message2.M1.M16.M23.M38.E17]
                        E17_CONST_3: _ClassVar[Message2.M1.M16.M23.M38.E17]
                        E17_CONST_4: _ClassVar[Message2.M1.M16.M23.M38.E17]
                        E17_CONST_5: _ClassVar[Message2.M1.M16.M23.M38.E17]
                    E17_UNSPECIFIED: Message2.M1.M16.M23.M38.E17
                    E17_CONST_1: Message2.M1.M16.M23.M38.E17
                    E17_CONST_2: Message2.M1.M16.M23.M38.E17
                    E17_CONST_3: Message2.M1.M16.M23.M38.E17
                    E17_CONST_4: Message2.M1.M16.M23.M38.E17
                    E17_CONST_5: Message2.M1.M16.M23.M38.E17
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message2.M1.M16.M23.M38.E17
                    def __init__(self, f_0: _Optional[_Union[Message2.M1.M16.M23.M38.E17, str]] = ...) -> None: ...
                class M40(_message.Message):
                    __slots__ = ("f_0", "f_2", "f_4")
                    class M61(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_5")
                        class M71(_message.Message):
                            __slots__ = ("f_0",)
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        f_1: int
                        f_5: Message2.M1.M16.M23.M40.M61.M71
                        def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_5: _Optional[_Union[Message2.M1.M16.M23.M40.M61.M71, _Mapping]] = ...) -> None: ...
                    class M62(_message.Message):
                        __slots__ = ("f_0", "f_1")
                        class E23(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E23_UNSPECIFIED: _ClassVar[Message2.M1.M16.M23.M40.M62.E23]
                            E23_CONST_1: _ClassVar[Message2.M1.M16.M23.M40.M62.E23]
                            E23_CONST_2: _ClassVar[Message2.M1.M16.M23.M40.M62.E23]
                            E23_CONST_3: _ClassVar[Message2.M1.M16.M23.M40.M62.E23]
                            E23_CONST_4: _ClassVar[Message2.M1.M16.M23.M40.M62.E23]
                            E23_CONST_5: _ClassVar[Message2.M1.M16.M23.M40.M62.E23]
                        E23_UNSPECIFIED: Message2.M1.M16.M23.M40.M62.E23
                        E23_CONST_1: Message2.M1.M16.M23.M40.M62.E23
                        E23_CONST_2: Message2.M1.M16.M23.M40.M62.E23
                        E23_CONST_3: Message2.M1.M16.M23.M40.M62.E23
                        E23_CONST_4: Message2.M1.M16.M23.M40.M62.E23
                        E23_CONST_5: Message2.M1.M16.M23.M40.M62.E23
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message2.M1.M16.M23.M40.M62.E23
                        f_1: float
                        def __init__(self, f_0: _Optional[_Union[Message2.M1.M16.M23.M40.M62.E23, str]] = ..., f_1: _Optional[float] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_2: Message2.M1.M16.M23.M40.M61
                    f_4: _containers.RepeatedCompositeFieldContainer[Message2.M1.M16.M23.M40.M62]
                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M1.M16.M23.M40.M61, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message2.M1.M16.M23.M40.M62, _Mapping]]] = ...) -> None: ...
                class M43(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class E18(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E18_UNSPECIFIED: _ClassVar[Message2.M1.M16.M23.M43.E18]
                        E18_CONST_1: _ClassVar[Message2.M1.M16.M23.M43.E18]
                        E18_CONST_2: _ClassVar[Message2.M1.M16.M23.M43.E18]
                        E18_CONST_3: _ClassVar[Message2.M1.M16.M23.M43.E18]
                        E18_CONST_4: _ClassVar[Message2.M1.M16.M23.M43.E18]
                        E18_CONST_5: _ClassVar[Message2.M1.M16.M23.M43.E18]
                    E18_UNSPECIFIED: Message2.M1.M16.M23.M43.E18
                    E18_CONST_1: Message2.M1.M16.M23.M43.E18
                    E18_CONST_2: Message2.M1.M16.M23.M43.E18
                    E18_CONST_3: Message2.M1.M16.M23.M43.E18
                    E18_CONST_4: Message2.M1.M16.M23.M43.E18
                    E18_CONST_5: Message2.M1.M16.M23.M43.E18
                    class M65(_message.Message):
                        __slots__ = ("f_0",)
                        class E24(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E24_UNSPECIFIED: _ClassVar[Message2.M1.M16.M23.M43.M65.E24]
                            E24_CONST_1: _ClassVar[Message2.M1.M16.M23.M43.M65.E24]
                            E24_CONST_2: _ClassVar[Message2.M1.M16.M23.M43.M65.E24]
                            E24_CONST_3: _ClassVar[Message2.M1.M16.M23.M43.M65.E24]
                            E24_CONST_4: _ClassVar[Message2.M1.M16.M23.M43.M65.E24]
                            E24_CONST_5: _ClassVar[Message2.M1.M16.M23.M43.M65.E24]
                        E24_UNSPECIFIED: Message2.M1.M16.M23.M43.M65.E24
                        E24_CONST_1: Message2.M1.M16.M23.M43.M65.E24
                        E24_CONST_2: Message2.M1.M16.M23.M43.M65.E24
                        E24_CONST_3: Message2.M1.M16.M23.M43.M65.E24
                        E24_CONST_4: Message2.M1.M16.M23.M43.M65.E24
                        E24_CONST_5: Message2.M1.M16.M23.M43.M65.E24
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message2.M1.M16.M23.M43.M65.E24
                        def __init__(self, f_0: _Optional[_Union[Message2.M1.M16.M23.M43.M65.E24, str]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message2.M1.M16.M23.M43.E18
                    f_2: Message2.M1.M16.M23.M43.M65
                    def __init__(self, f_0: _Optional[_Union[Message2.M1.M16.M23.M43.E18, str]] = ..., f_2: _Optional[_Union[Message2.M1.M16.M23.M43.M65, _Mapping]] = ...) -> None: ...
                class M44(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                class M46(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_1_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                F_6_FIELD_NUMBER: _ClassVar[int]
                F_7_FIELD_NUMBER: _ClassVar[int]
                F_9_FIELD_NUMBER: _ClassVar[int]
                F_10_FIELD_NUMBER: _ClassVar[int]
                F_11_FIELD_NUMBER: _ClassVar[int]
                F_12_FIELD_NUMBER: _ClassVar[int]
                F_14_FIELD_NUMBER: _ClassVar[int]
                f_0: str
                f_1: float
                f_4: _containers.RepeatedCompositeFieldContainer[Message2.M1.M16.M23.M27]
                f_5: _containers.RepeatedCompositeFieldContainer[Message2.M1.M16.M23.M30]
                f_6: Message2.M1.M16.M23.M32
                f_7: Message2.M1.M16.M23.M34
                f_9: Message2.M1.M16.M23.M38
                f_10: Message2.M1.M16.M23.M40
                f_11: _containers.RepeatedCompositeFieldContainer[Message2.M1.M16.M23.M43]
                f_12: Message2.M1.M16.M23.M44
                f_14: Message2.M1.M16.M23.M46
                def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[float] = ..., f_4: _Optional[_Iterable[_Union[Message2.M1.M16.M23.M27, _Mapping]]] = ..., f_5: _Optional[_Iterable[_Union[Message2.M1.M16.M23.M30, _Mapping]]] = ..., f_6: _Optional[_Union[Message2.M1.M16.M23.M32, _Mapping]] = ..., f_7: _Optional[_Union[Message2.M1.M16.M23.M34, _Mapping]] = ..., f_9: _Optional[_Union[Message2.M1.M16.M23.M38, _Mapping]] = ..., f_10: _Optional[_Union[Message2.M1.M16.M23.M40, _Mapping]] = ..., f_11: _Optional[_Iterable[_Union[Message2.M1.M16.M23.M43, _Mapping]]] = ..., f_12: _Optional[_Union[Message2.M1.M16.M23.M44, _Mapping]] = ..., f_14: _Optional[_Union[Message2.M1.M16.M23.M46, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            f_0: bytes
            f_2: _containers.RepeatedCompositeFieldContainer[Message2.M1.M16.M23]
            def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Iterable[_Union[Message2.M1.M16.M23, _Mapping]]] = ...) -> None: ...
        class M19(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5")
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_1_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_4_FIELD_NUMBER: _ClassVar[int]
            F_5_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_1: int
            f_2: int
            f_3: int
            f_4: _containers.RepeatedScalarFieldContainer[int]
            f_5: str
            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[_Iterable[int]] = ..., f_5: _Optional[str] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        F_5_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_2: Message2.M1.M9
        f_3: Message2.M1.M12
        f_4: Message2.M1.M16
        f_5: _containers.RepeatedCompositeFieldContainer[Message2.M1.M19]
        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M1.M9, _Mapping]] = ..., f_3: _Optional[_Union[Message2.M1.M12, _Mapping]] = ..., f_4: _Optional[_Union[Message2.M1.M16, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message2.M1.M19, _Mapping]]] = ...) -> None: ...
    class M2(_message.Message):
        __slots__ = ("f_0",)
        F_0_FIELD_NUMBER: _ClassVar[int]
        f_0: float
        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
    class M3(_message.Message):
        __slots__ = ("f_0", "f_2")
        class M13(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: float
            def __init__(self, f_0: _Optional[float] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        f_0: str
        f_2: Message2.M3.M13
        def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message2.M3.M13, _Mapping]] = ...) -> None: ...
    class M4(_message.Message):
        __slots__ = ("f_0",)
        F_0_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
    class M5(_message.Message):
        __slots__ = ("f_0", "f_2", "f_3")
        class M20(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2")
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_1_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_1: int
            f_2: float
            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[float] = ...) -> None: ...
        class M22(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9")
            class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E2_UNSPECIFIED: _ClassVar[Message2.M5.M22.E2]
                E2_CONST_1: _ClassVar[Message2.M5.M22.E2]
                E2_CONST_2: _ClassVar[Message2.M5.M22.E2]
                E2_CONST_3: _ClassVar[Message2.M5.M22.E2]
                E2_CONST_4: _ClassVar[Message2.M5.M22.E2]
                E2_CONST_5: _ClassVar[Message2.M5.M22.E2]
            E2_UNSPECIFIED: Message2.M5.M22.E2
            E2_CONST_1: Message2.M5.M22.E2
            E2_CONST_2: Message2.M5.M22.E2
            E2_CONST_3: Message2.M5.M22.E2
            E2_CONST_4: Message2.M5.M22.E2
            E2_CONST_5: Message2.M5.M22.E2
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_1_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_4_FIELD_NUMBER: _ClassVar[int]
            F_5_FIELD_NUMBER: _ClassVar[int]
            F_6_FIELD_NUMBER: _ClassVar[int]
            F_7_FIELD_NUMBER: _ClassVar[int]
            F_8_FIELD_NUMBER: _ClassVar[int]
            F_9_FIELD_NUMBER: _ClassVar[int]
            f_0: float
            f_1: _containers.RepeatedScalarFieldContainer[int]
            f_2: int
            f_3: _containers.RepeatedScalarFieldContainer[Message2.M5.M22.E2]
            f_4: int
            f_5: int
            f_6: int
            f_7: bytes
            f_8: str
            f_9: bool
            def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[_Iterable[int]] = ..., f_2: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message2.M5.M22.E2, str]]] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[int] = ..., f_7: _Optional[bytes] = ..., f_8: _Optional[str] = ..., f_9: _Optional[bool] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        f_0: str
        f_2: Message2.M5.M20
        f_3: Message2.M5.M22
        def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message2.M5.M20, _Mapping]] = ..., f_3: _Optional[_Union[Message2.M5.M22, _Mapping]] = ...) -> None: ...
    class M6(_message.Message):
        __slots__ = ("f_0", "f_2", "f_3", "f_4")
        class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E1_UNSPECIFIED: _ClassVar[Message2.M6.E1]
            E1_CONST_1: _ClassVar[Message2.M6.E1]
            E1_CONST_2: _ClassVar[Message2.M6.E1]
            E1_CONST_3: _ClassVar[Message2.M6.E1]
            E1_CONST_4: _ClassVar[Message2.M6.E1]
            E1_CONST_5: _ClassVar[Message2.M6.E1]
        E1_UNSPECIFIED: Message2.M6.E1
        E1_CONST_1: Message2.M6.E1
        E1_CONST_2: Message2.M6.E1
        E1_CONST_3: Message2.M6.E1
        E1_CONST_4: Message2.M6.E1
        E1_CONST_5: Message2.M6.E1
        class M11(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
        class M15(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, f_0: _Optional[_Iterable[int]] = ...) -> None: ...
        class M18(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        f_0: Message2.M6.E1
        f_2: _containers.RepeatedCompositeFieldContainer[Message2.M6.M11]
        f_3: _containers.RepeatedCompositeFieldContainer[Message2.M6.M15]
        f_4: Message2.M6.M18
        def __init__(self, f_0: _Optional[_Union[Message2.M6.E1, str]] = ..., f_2: _Optional[_Iterable[_Union[Message2.M6.M11, _Mapping]]] = ..., f_3: _Optional[_Iterable[_Union[Message2.M6.M15, _Mapping]]] = ..., f_4: _Optional[_Union[Message2.M6.M18, _Mapping]] = ...) -> None: ...
    class M7(_message.Message):
        __slots__ = ("f_0", "f_1", "f_2", "f_5")
        class M17(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_1_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_5_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_1: bytes
        f_2: int
        f_5: _containers.RepeatedCompositeFieldContainer[Message2.M7.M17]
        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[int] = ..., f_5: _Optional[_Iterable[_Union[Message2.M7.M17, _Mapping]]] = ...) -> None: ...
    class M8(_message.Message):
        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_10", "f_11", "f_12")
        class M10(_message.Message):
            __slots__ = ("f_0", "f_3", "f_4")
            class M24(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_8", "f_9", "f_10", "f_11", "f_12", "f_15", "f_17", "f_19", "f_20", "f_21")
                class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E3_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.E3]
                    E3_CONST_1: _ClassVar[Message2.M8.M10.M24.E3]
                    E3_CONST_2: _ClassVar[Message2.M8.M10.M24.E3]
                    E3_CONST_3: _ClassVar[Message2.M8.M10.M24.E3]
                    E3_CONST_4: _ClassVar[Message2.M8.M10.M24.E3]
                    E3_CONST_5: _ClassVar[Message2.M8.M10.M24.E3]
                E3_UNSPECIFIED: Message2.M8.M10.M24.E3
                E3_CONST_1: Message2.M8.M10.M24.E3
                E3_CONST_2: Message2.M8.M10.M24.E3
                E3_CONST_3: Message2.M8.M10.M24.E3
                E3_CONST_4: Message2.M8.M10.M24.E3
                E3_CONST_5: Message2.M8.M10.M24.E3
                class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E4_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.E4]
                    E4_CONST_1: _ClassVar[Message2.M8.M10.M24.E4]
                    E4_CONST_2: _ClassVar[Message2.M8.M10.M24.E4]
                    E4_CONST_3: _ClassVar[Message2.M8.M10.M24.E4]
                    E4_CONST_4: _ClassVar[Message2.M8.M10.M24.E4]
                    E4_CONST_5: _ClassVar[Message2.M8.M10.M24.E4]
                E4_UNSPECIFIED: Message2.M8.M10.M24.E4
                E4_CONST_1: Message2.M8.M10.M24.E4
                E4_CONST_2: Message2.M8.M10.M24.E4
                E4_CONST_3: Message2.M8.M10.M24.E4
                E4_CONST_4: Message2.M8.M10.M24.E4
                E4_CONST_5: Message2.M8.M10.M24.E4
                class M26(_message.Message):
                    __slots__ = ("f_0", "f_3", "f_4", "f_5", "f_6")
                    class M53(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M70(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19")
                            class E31(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E31_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E31]
                                E31_CONST_1: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E31]
                                E31_CONST_2: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E31]
                                E31_CONST_3: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E31]
                                E31_CONST_4: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E31]
                                E31_CONST_5: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E31]
                            E31_UNSPECIFIED: Message2.M8.M10.M24.M26.M53.M70.E31
                            E31_CONST_1: Message2.M8.M10.M24.M26.M53.M70.E31
                            E31_CONST_2: Message2.M8.M10.M24.M26.M53.M70.E31
                            E31_CONST_3: Message2.M8.M10.M24.M26.M53.M70.E31
                            E31_CONST_4: Message2.M8.M10.M24.M26.M53.M70.E31
                            E31_CONST_5: Message2.M8.M10.M24.M26.M53.M70.E31
                            class E32(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E32_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E32]
                                E32_CONST_1: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E32]
                                E32_CONST_2: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E32]
                                E32_CONST_3: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E32]
                                E32_CONST_4: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E32]
                                E32_CONST_5: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E32]
                            E32_UNSPECIFIED: Message2.M8.M10.M24.M26.M53.M70.E32
                            E32_CONST_1: Message2.M8.M10.M24.M26.M53.M70.E32
                            E32_CONST_2: Message2.M8.M10.M24.M26.M53.M70.E32
                            E32_CONST_3: Message2.M8.M10.M24.M26.M53.M70.E32
                            E32_CONST_4: Message2.M8.M10.M24.M26.M53.M70.E32
                            E32_CONST_5: Message2.M8.M10.M24.M26.M53.M70.E32
                            class E33(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E33_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E33]
                                E33_CONST_1: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E33]
                                E33_CONST_2: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E33]
                                E33_CONST_3: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E33]
                                E33_CONST_4: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E33]
                                E33_CONST_5: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E33]
                            E33_UNSPECIFIED: Message2.M8.M10.M24.M26.M53.M70.E33
                            E33_CONST_1: Message2.M8.M10.M24.M26.M53.M70.E33
                            E33_CONST_2: Message2.M8.M10.M24.M26.M53.M70.E33
                            E33_CONST_3: Message2.M8.M10.M24.M26.M53.M70.E33
                            E33_CONST_4: Message2.M8.M10.M24.M26.M53.M70.E33
                            E33_CONST_5: Message2.M8.M10.M24.M26.M53.M70.E33
                            class E34(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E34_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E34]
                                E34_CONST_1: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E34]
                                E34_CONST_2: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E34]
                                E34_CONST_3: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E34]
                                E34_CONST_4: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E34]
                                E34_CONST_5: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E34]
                            E34_UNSPECIFIED: Message2.M8.M10.M24.M26.M53.M70.E34
                            E34_CONST_1: Message2.M8.M10.M24.M26.M53.M70.E34
                            E34_CONST_2: Message2.M8.M10.M24.M26.M53.M70.E34
                            E34_CONST_3: Message2.M8.M10.M24.M26.M53.M70.E34
                            E34_CONST_4: Message2.M8.M10.M24.M26.M53.M70.E34
                            E34_CONST_5: Message2.M8.M10.M24.M26.M53.M70.E34
                            class E35(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E35_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E35]
                                E35_CONST_1: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E35]
                                E35_CONST_2: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E35]
                                E35_CONST_3: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E35]
                                E35_CONST_4: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E35]
                                E35_CONST_5: _ClassVar[Message2.M8.M10.M24.M26.M53.M70.E35]
                            E35_UNSPECIFIED: Message2.M8.M10.M24.M26.M53.M70.E35
                            E35_CONST_1: Message2.M8.M10.M24.M26.M53.M70.E35
                            E35_CONST_2: Message2.M8.M10.M24.M26.M53.M70.E35
                            E35_CONST_3: Message2.M8.M10.M24.M26.M53.M70.E35
                            E35_CONST_4: Message2.M8.M10.M24.M26.M53.M70.E35
                            E35_CONST_5: Message2.M8.M10.M24.M26.M53.M70.E35
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            F_5_FIELD_NUMBER: _ClassVar[int]
                            F_6_FIELD_NUMBER: _ClassVar[int]
                            F_7_FIELD_NUMBER: _ClassVar[int]
                            F_8_FIELD_NUMBER: _ClassVar[int]
                            F_9_FIELD_NUMBER: _ClassVar[int]
                            F_10_FIELD_NUMBER: _ClassVar[int]
                            F_11_FIELD_NUMBER: _ClassVar[int]
                            F_12_FIELD_NUMBER: _ClassVar[int]
                            F_13_FIELD_NUMBER: _ClassVar[int]
                            F_14_FIELD_NUMBER: _ClassVar[int]
                            F_15_FIELD_NUMBER: _ClassVar[int]
                            F_16_FIELD_NUMBER: _ClassVar[int]
                            F_17_FIELD_NUMBER: _ClassVar[int]
                            F_18_FIELD_NUMBER: _ClassVar[int]
                            F_19_FIELD_NUMBER: _ClassVar[int]
                            f_0: Message2.M8.M10.M24.M26.M53.M70.E31
                            f_1: int
                            f_2: Message2.M8.M10.M24.M26.M53.M70.E32
                            f_3: _containers.RepeatedScalarFieldContainer[bytes]
                            f_4: str
                            f_5: int
                            f_6: Message2.M8.M10.M24.M26.M53.M70.E33
                            f_7: Message2.M8.M10.M24.M26.M53.M70.E34
                            f_8: bool
                            f_9: Message2.M8.M10.M24.M26.M53.M70.E35
                            f_10: int
                            f_11: bool
                            f_12: str
                            f_13: int
                            f_14: int
                            f_15: int
                            f_16: bytes
                            f_17: bool
                            f_18: int
                            f_19: int
                            def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M24.M26.M53.M70.E31, str]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M26.M53.M70.E32, str]] = ..., f_3: _Optional[_Iterable[bytes]] = ..., f_4: _Optional[str] = ..., f_5: _Optional[int] = ..., f_6: _Optional[_Union[Message2.M8.M10.M24.M26.M53.M70.E33, str]] = ..., f_7: _Optional[_Union[Message2.M8.M10.M24.M26.M53.M70.E34, str]] = ..., f_8: _Optional[bool] = ..., f_9: _Optional[_Union[Message2.M8.M10.M24.M26.M53.M70.E35, str]] = ..., f_10: _Optional[int] = ..., f_11: _Optional[bool] = ..., f_12: _Optional[str] = ..., f_13: _Optional[int] = ..., f_14: _Optional[int] = ..., f_15: _Optional[int] = ..., f_16: _Optional[bytes] = ..., f_17: _Optional[bool] = ..., f_18: _Optional[int] = ..., f_19: _Optional[int] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: bytes
                        f_2: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M26.M53.M70]
                        def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M26.M53.M70, _Mapping]]] = ...) -> None: ...
                    class M54(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                    class M57(_message.Message):
                        __slots__ = ("f_0", "f_4")
                        class M68(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4")
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            f_0: str
                            f_1: int
                            f_2: int
                            f_3: bytes
                            f_4: int
                            def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[bytes] = ..., f_4: _Optional[int] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        f_4: Message2.M8.M10.M24.M26.M57.M68
                        def __init__(self, f_0: _Optional[float] = ..., f_4: _Optional[_Union[Message2.M8.M10.M24.M26.M57.M68, _Mapping]] = ...) -> None: ...
                    class M60(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_3: Message2.M8.M10.M24.M26.M53
                    f_4: Message2.M8.M10.M24.M26.M54
                    f_5: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M26.M57]
                    f_6: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M26.M60]
                    def __init__(self, f_0: _Optional[str] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24.M26.M53, _Mapping]] = ..., f_4: _Optional[_Union[Message2.M8.M10.M24.M26.M54, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M26.M57, _Mapping]]] = ..., f_6: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M26.M60, _Mapping]]] = ...) -> None: ...
                class M28(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_9")
                    class M63(_message.Message):
                        __slots__ = ("f_0", "f_4")
                        class M67(_message.Message):
                            __slots__ = ("f_0", "f_2", "f_3")
                            class E28(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E28_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.E28]
                                E28_CONST_1: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.E28]
                                E28_CONST_2: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.E28]
                                E28_CONST_3: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.E28]
                                E28_CONST_4: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.E28]
                                E28_CONST_5: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.E28]
                            E28_UNSPECIFIED: Message2.M8.M10.M24.M28.M63.M67.E28
                            E28_CONST_1: Message2.M8.M10.M24.M28.M63.M67.E28
                            E28_CONST_2: Message2.M8.M10.M24.M28.M63.M67.E28
                            E28_CONST_3: Message2.M8.M10.M24.M28.M63.M67.E28
                            E28_CONST_4: Message2.M8.M10.M24.M28.M63.M67.E28
                            E28_CONST_5: Message2.M8.M10.M24.M28.M63.M67.E28
                            class M73(_message.Message):
                                __slots__ = ("f_0", "f_2")
                                class M83(_message.Message):
                                    __slots__ = ("f_0", "f_2")
                                    class M86(_message.Message):
                                        __slots__ = ("f_0", "f_4")
                                        class M93(_message.Message):
                                            __slots__ = ("f_0", "f_1", "f_2", "f_4", "f_6")
                                            class M95(_message.Message):
                                                __slots__ = ("f_0", "f_3")
                                                class M99(_message.Message):
                                                    __slots__ = ("f_0", "f_2", "f_3")
                                                    class M100(_message.Message):
                                                        __slots__ = ("f_0", "f_3")
                                                        class M102(_message.Message):
                                                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_11", "f_12")
                                                            class E42(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                                __slots__ = ()
                                                                E42_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42]
                                                                E42_CONST_1: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42]
                                                                E42_CONST_2: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42]
                                                                E42_CONST_3: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42]
                                                                E42_CONST_4: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42]
                                                                E42_CONST_5: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42]
                                                            E42_UNSPECIFIED: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            E42_CONST_1: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            E42_CONST_2: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            E42_CONST_3: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            E42_CONST_4: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            E42_CONST_5: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            class M103(_message.Message):
                                                                __slots__ = ("f_0",)
                                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                                f_0: int
                                                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                                            class M104(_message.Message):
                                                                __slots__ = ("f_0", "f_2")
                                                                class M105(_message.Message):
                                                                    __slots__ = ("f_0", "f_1", "f_2", "f_5", "f_6")
                                                                    class E43(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                                        __slots__ = ()
                                                                        E43_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43]
                                                                        E43_CONST_1: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43]
                                                                        E43_CONST_2: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43]
                                                                        E43_CONST_3: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43]
                                                                        E43_CONST_4: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43]
                                                                        E43_CONST_5: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43]
                                                                    E43_UNSPECIFIED: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    E43_CONST_1: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    E43_CONST_2: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    E43_CONST_3: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    E43_CONST_4: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    E43_CONST_5: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    class M106(_message.Message):
                                                                        __slots__ = ("f_0",)
                                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                                        f_0: str
                                                                        def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                                                                    class M107(_message.Message):
                                                                        __slots__ = ("f_0",)
                                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                                        f_0: str
                                                                        def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                                                    F_5_FIELD_NUMBER: _ClassVar[int]
                                                                    F_6_FIELD_NUMBER: _ClassVar[int]
                                                                    f_0: int
                                                                    f_1: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43
                                                                    f_2: int
                                                                    f_5: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.M106
                                                                    f_6: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.M107]
                                                                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.E43, str]] = ..., f_2: _Optional[int] = ..., f_5: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.M106, _Mapping]] = ..., f_6: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105.M107, _Mapping]]] = ...) -> None: ...
                                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                                F_2_FIELD_NUMBER: _ClassVar[int]
                                                                f_0: bytes
                                                                f_2: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105
                                                                def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104.M105, _Mapping]] = ...) -> None: ...
                                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                                            F_1_FIELD_NUMBER: _ClassVar[int]
                                                            F_2_FIELD_NUMBER: _ClassVar[int]
                                                            F_3_FIELD_NUMBER: _ClassVar[int]
                                                            F_4_FIELD_NUMBER: _ClassVar[int]
                                                            F_5_FIELD_NUMBER: _ClassVar[int]
                                                            F_6_FIELD_NUMBER: _ClassVar[int]
                                                            F_7_FIELD_NUMBER: _ClassVar[int]
                                                            F_11_FIELD_NUMBER: _ClassVar[int]
                                                            F_12_FIELD_NUMBER: _ClassVar[int]
                                                            f_0: int
                                                            f_1: int
                                                            f_2: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42
                                                            f_3: int
                                                            f_4: int
                                                            f_5: int
                                                            f_6: float
                                                            f_7: str
                                                            f_11: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M103
                                                            f_12: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104
                                                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.E42, str]] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[float] = ..., f_7: _Optional[str] = ..., f_11: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M103, _Mapping]] = ..., f_12: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102.M104, _Mapping]] = ...) -> None: ...
                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                        F_3_FIELD_NUMBER: _ClassVar[int]
                                                        f_0: float
                                                        f_3: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102]
                                                        def __init__(self, f_0: _Optional[float] = ..., f_3: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100.M102, _Mapping]]] = ...) -> None: ...
                                                    class M101(_message.Message):
                                                        __slots__ = ("f_0",)
                                                        class E41(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                            __slots__ = ()
                                                            E41_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41]
                                                            E41_CONST_1: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41]
                                                            E41_CONST_2: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41]
                                                            E41_CONST_3: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41]
                                                            E41_CONST_4: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41]
                                                            E41_CONST_5: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41]
                                                        E41_UNSPECIFIED: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        E41_CONST_1: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        E41_CONST_2: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        E41_CONST_3: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        E41_CONST_4: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        E41_CONST_5: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                        f_0: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41
                                                        def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101.E41, str]] = ...) -> None: ...
                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                                    f_0: float
                                                    f_2: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100]
                                                    f_3: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101
                                                    def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M100, _Mapping]]] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99.M101, _Mapping]] = ...) -> None: ...
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                F_3_FIELD_NUMBER: _ClassVar[int]
                                                f_0: int
                                                f_3: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99
                                                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95.M99, _Mapping]] = ...) -> None: ...
                                            class M97(_message.Message):
                                                __slots__ = ("f_0",)
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                f_0: int
                                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            F_1_FIELD_NUMBER: _ClassVar[int]
                                            F_2_FIELD_NUMBER: _ClassVar[int]
                                            F_4_FIELD_NUMBER: _ClassVar[int]
                                            F_6_FIELD_NUMBER: _ClassVar[int]
                                            f_0: bytes
                                            f_1: int
                                            f_2: int
                                            f_4: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95]
                                            f_6: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M97
                                            def __init__(self, f_0: _Optional[bytes] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_4: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M95, _Mapping]]] = ..., f_6: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93.M97, _Mapping]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_4_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        f_4: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93
                                        def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86.M93, _Mapping]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: bool
                                    f_2: Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86
                                    def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83.M86, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                f_2: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M73.M83]
                                def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M73.M83, _Mapping]]] = ...) -> None: ...
                            class M75(_message.Message):
                                __slots__ = ("f_0", "f_2", "f_4", "f_5", "f_6")
                                class M76(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                class M78(_message.Message):
                                    __slots__ = ("f_0", "f_2", "f_3")
                                    class M88(_message.Message):
                                        __slots__ = ("f_0", "f_3")
                                        class M92(_message.Message):
                                            __slots__ = ("f_0",)
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            f_0: str
                                            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_3_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        f_3: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75.M78.M88.M92]
                                        def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M78.M88.M92, _Mapping]]] = ...) -> None: ...
                                    class M89(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: str
                                        def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: float
                                    f_2: Message2.M8.M10.M24.M28.M63.M67.M75.M78.M88
                                    f_3: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75.M78.M89]
                                    def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M78.M88, _Mapping]] = ..., f_3: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M78.M89, _Mapping]]] = ...) -> None: ...
                                class M81(_message.Message):
                                    __slots__ = ("f_0", "f_2")
                                    class M90(_message.Message):
                                        __slots__ = ("f_0",)
                                        class E40(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                            __slots__ = ()
                                            E40_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40]
                                            E40_CONST_1: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40]
                                            E40_CONST_2: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40]
                                            E40_CONST_3: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40]
                                            E40_CONST_4: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40]
                                            E40_CONST_5: _ClassVar[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40]
                                        E40_UNSPECIFIED: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        E40_CONST_1: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        E40_CONST_2: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        E40_CONST_3: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        E40_CONST_4: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        E40_CONST_5: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40
                                        def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90.E40, str]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    f_2: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90]
                                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M81.M90, _Mapping]]] = ...) -> None: ...
                                class M82(_message.Message):
                                    __slots__ = ("f_0", "f_2", "f_3")
                                    class M84(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                    class M91(_message.Message):
                                        __slots__ = ("f_0", "f_5")
                                        class M94(_message.Message):
                                            __slots__ = ("f_0", "f_1", "f_4")
                                            class M96(_message.Message):
                                                __slots__ = ("f_0", "f_2")
                                                class M98(_message.Message):
                                                    __slots__ = ("f_0",)
                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                    f_0: int
                                                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                F_2_FIELD_NUMBER: _ClassVar[int]
                                                f_0: int
                                                f_2: Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91.M94.M96.M98
                                                def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91.M94.M96.M98, _Mapping]] = ...) -> None: ...
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            F_1_FIELD_NUMBER: _ClassVar[int]
                                            F_4_FIELD_NUMBER: _ClassVar[int]
                                            f_0: int
                                            f_1: int
                                            f_4: Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91.M94.M96
                                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_4: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91.M94.M96, _Mapping]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_5_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        f_5: Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91.M94
                                        def __init__(self, f_0: _Optional[int] = ..., f_5: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91.M94, _Mapping]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: bytes
                                    f_2: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75.M82.M84]
                                    f_3: Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91
                                    def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M82.M84, _Mapping]]] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M82.M91, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                F_4_FIELD_NUMBER: _ClassVar[int]
                                F_5_FIELD_NUMBER: _ClassVar[int]
                                F_6_FIELD_NUMBER: _ClassVar[int]
                                f_0: str
                                f_2: Message2.M8.M10.M24.M28.M63.M67.M75.M76
                                f_4: Message2.M8.M10.M24.M28.M63.M67.M75.M78
                                f_5: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75.M81]
                                f_6: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75.M82]
                                def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M76, _Mapping]] = ..., f_4: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M78, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M81, _Mapping]]] = ..., f_6: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75.M82, _Mapping]]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            f_0: Message2.M8.M10.M24.M28.M63.M67.E28
                            f_2: Message2.M8.M10.M24.M28.M63.M67.M73
                            f_3: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67.M75]
                            def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.E28, str]] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M28.M63.M67.M73, _Mapping]] = ..., f_3: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67.M75, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_4: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63.M67]
                        def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63.M67, _Mapping]]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_9_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: bool
                    f_2: int
                    f_3: str
                    f_4: bool
                    f_9: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28.M63]
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[bool] = ..., f_2: _Optional[int] = ..., f_3: _Optional[str] = ..., f_4: _Optional[bool] = ..., f_9: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28.M63, _Mapping]]] = ...) -> None: ...
                class M29(_message.Message):
                    __slots__ = ("f_0", "f_3")
                    class M52(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_3: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M29.M52]
                    def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M29.M52, _Mapping]]] = ...) -> None: ...
                class M35(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2")
                    class E15(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E15_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M35.E15]
                        E15_CONST_1: _ClassVar[Message2.M8.M10.M24.M35.E15]
                        E15_CONST_2: _ClassVar[Message2.M8.M10.M24.M35.E15]
                        E15_CONST_3: _ClassVar[Message2.M8.M10.M24.M35.E15]
                        E15_CONST_4: _ClassVar[Message2.M8.M10.M24.M35.E15]
                        E15_CONST_5: _ClassVar[Message2.M8.M10.M24.M35.E15]
                    E15_UNSPECIFIED: Message2.M8.M10.M24.M35.E15
                    E15_CONST_1: Message2.M8.M10.M24.M35.E15
                    E15_CONST_2: Message2.M8.M10.M24.M35.E15
                    E15_CONST_3: Message2.M8.M10.M24.M35.E15
                    E15_CONST_4: Message2.M8.M10.M24.M35.E15
                    E15_CONST_5: Message2.M8.M10.M24.M35.E15
                    class E16(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E16_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M35.E16]
                        E16_CONST_1: _ClassVar[Message2.M8.M10.M24.M35.E16]
                        E16_CONST_2: _ClassVar[Message2.M8.M10.M24.M35.E16]
                        E16_CONST_3: _ClassVar[Message2.M8.M10.M24.M35.E16]
                        E16_CONST_4: _ClassVar[Message2.M8.M10.M24.M35.E16]
                        E16_CONST_5: _ClassVar[Message2.M8.M10.M24.M35.E16]
                    E16_UNSPECIFIED: Message2.M8.M10.M24.M35.E16
                    E16_CONST_1: Message2.M8.M10.M24.M35.E16
                    E16_CONST_2: Message2.M8.M10.M24.M35.E16
                    E16_CONST_3: Message2.M8.M10.M24.M35.E16
                    E16_CONST_4: Message2.M8.M10.M24.M35.E16
                    E16_CONST_5: Message2.M8.M10.M24.M35.E16
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message2.M8.M10.M24.M35.E15
                    f_1: _containers.RepeatedScalarFieldContainer[str]
                    f_2: _containers.RepeatedScalarFieldContainer[Message2.M8.M10.M24.M35.E16]
                    def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M24.M35.E15, str]] = ..., f_1: _Optional[_Iterable[str]] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M35.E16, str]]] = ...) -> None: ...
                class M39(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                class M41(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: bool
                    def __init__(self, f_0: _Optional[bool] = ...) -> None: ...
                class M42(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M55(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_2: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M42.M55]
                    def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M42.M55, _Mapping]]] = ...) -> None: ...
                class M45(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: int
                    f_2: str
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[str] = ...) -> None: ...
                class M47(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M59(_message.Message):
                        __slots__ = ("f_0", "f_3")
                        class E22(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E22_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M47.M59.E22]
                            E22_CONST_1: _ClassVar[Message2.M8.M10.M24.M47.M59.E22]
                            E22_CONST_2: _ClassVar[Message2.M8.M10.M24.M47.M59.E22]
                            E22_CONST_3: _ClassVar[Message2.M8.M10.M24.M47.M59.E22]
                            E22_CONST_4: _ClassVar[Message2.M8.M10.M24.M47.M59.E22]
                            E22_CONST_5: _ClassVar[Message2.M8.M10.M24.M47.M59.E22]
                        E22_UNSPECIFIED: Message2.M8.M10.M24.M47.M59.E22
                        E22_CONST_1: Message2.M8.M10.M24.M47.M59.E22
                        E22_CONST_2: Message2.M8.M10.M24.M47.M59.E22
                        E22_CONST_3: Message2.M8.M10.M24.M47.M59.E22
                        E22_CONST_4: Message2.M8.M10.M24.M47.M59.E22
                        E22_CONST_5: Message2.M8.M10.M24.M47.M59.E22
                        class M72(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4")
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            f_0: _containers.RepeatedScalarFieldContainer[int]
                            f_1: int
                            f_2: int
                            f_3: int
                            f_4: int
                            def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message2.M8.M10.M24.M47.M59.E22
                        f_3: Message2.M8.M10.M24.M47.M59.M72
                        def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M24.M47.M59.E22, str]] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24.M47.M59.M72, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_2: Message2.M8.M10.M24.M47.M59
                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M8.M10.M24.M47.M59, _Mapping]] = ...) -> None: ...
                class M49(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9")
                    class E19(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E19_UNSPECIFIED: _ClassVar[Message2.M8.M10.M24.M49.E19]
                        E19_CONST_1: _ClassVar[Message2.M8.M10.M24.M49.E19]
                        E19_CONST_2: _ClassVar[Message2.M8.M10.M24.M49.E19]
                        E19_CONST_3: _ClassVar[Message2.M8.M10.M24.M49.E19]
                        E19_CONST_4: _ClassVar[Message2.M8.M10.M24.M49.E19]
                        E19_CONST_5: _ClassVar[Message2.M8.M10.M24.M49.E19]
                    E19_UNSPECIFIED: Message2.M8.M10.M24.M49.E19
                    E19_CONST_1: Message2.M8.M10.M24.M49.E19
                    E19_CONST_2: Message2.M8.M10.M24.M49.E19
                    E19_CONST_3: Message2.M8.M10.M24.M49.E19
                    E19_CONST_4: Message2.M8.M10.M24.M49.E19
                    E19_CONST_5: Message2.M8.M10.M24.M49.E19
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    F_7_FIELD_NUMBER: _ClassVar[int]
                    F_8_FIELD_NUMBER: _ClassVar[int]
                    F_9_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_1: int
                    f_2: float
                    f_3: float
                    f_4: bytes
                    f_5: int
                    f_6: int
                    f_7: float
                    f_8: Message2.M8.M10.M24.M49.E19
                    f_9: int
                    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[float] = ..., f_3: _Optional[float] = ..., f_4: _Optional[bytes] = ..., f_5: _Optional[int] = ..., f_6: _Optional[int] = ..., f_7: _Optional[float] = ..., f_8: _Optional[_Union[Message2.M8.M10.M24.M49.E19, str]] = ..., f_9: _Optional[int] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_1_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_8_FIELD_NUMBER: _ClassVar[int]
                F_9_FIELD_NUMBER: _ClassVar[int]
                F_10_FIELD_NUMBER: _ClassVar[int]
                F_11_FIELD_NUMBER: _ClassVar[int]
                F_12_FIELD_NUMBER: _ClassVar[int]
                F_15_FIELD_NUMBER: _ClassVar[int]
                F_17_FIELD_NUMBER: _ClassVar[int]
                F_19_FIELD_NUMBER: _ClassVar[int]
                F_20_FIELD_NUMBER: _ClassVar[int]
                F_21_FIELD_NUMBER: _ClassVar[int]
                f_0: bool
                f_1: _containers.RepeatedScalarFieldContainer[bytes]
                f_2: str
                f_3: Message2.M8.M10.M24.E3
                f_4: Message2.M8.M10.M24.E4
                f_8: Message2.M8.M10.M24.M26
                f_9: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M28]
                f_10: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M29]
                f_11: Message2.M8.M10.M24.M35
                f_12: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M39]
                f_15: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M24.M41]
                f_17: Message2.M8.M10.M24.M42
                f_19: Message2.M8.M10.M24.M45
                f_20: Message2.M8.M10.M24.M47
                f_21: Message2.M8.M10.M24.M49
                def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[_Iterable[bytes]] = ..., f_2: _Optional[str] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24.E3, str]] = ..., f_4: _Optional[_Union[Message2.M8.M10.M24.E4, str]] = ..., f_8: _Optional[_Union[Message2.M8.M10.M24.M26, _Mapping]] = ..., f_9: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M28, _Mapping]]] = ..., f_10: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M29, _Mapping]]] = ..., f_11: _Optional[_Union[Message2.M8.M10.M24.M35, _Mapping]] = ..., f_12: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M39, _Mapping]]] = ..., f_15: _Optional[_Iterable[_Union[Message2.M8.M10.M24.M41, _Mapping]]] = ..., f_17: _Optional[_Union[Message2.M8.M10.M24.M42, _Mapping]] = ..., f_19: _Optional[_Union[Message2.M8.M10.M24.M45, _Mapping]] = ..., f_20: _Optional[_Union[Message2.M8.M10.M24.M47, _Mapping]] = ..., f_21: _Optional[_Union[Message2.M8.M10.M24.M49, _Mapping]] = ...) -> None: ...
            class M25(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_31", "f_32", "f_33", "f_34", "f_35", "f_36", "f_37", "f_38", "f_39", "f_40", "f_41", "f_42", "f_43", "f_44", "f_45", "f_46", "f_47", "f_48", "f_49", "f_50", "f_51", "f_52", "f_53", "f_54", "f_55", "f_56", "f_57", "f_58", "f_59", "f_60", "f_61", "f_62", "f_63", "f_64", "f_65", "f_66", "f_67", "f_68", "f_69", "f_70", "f_71", "f_72", "f_73", "f_101", "f_102", "f_103", "f_104", "f_105")
                class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E5_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E5]
                    E5_CONST_1: _ClassVar[Message2.M8.M10.M25.E5]
                    E5_CONST_2: _ClassVar[Message2.M8.M10.M25.E5]
                    E5_CONST_3: _ClassVar[Message2.M8.M10.M25.E5]
                    E5_CONST_4: _ClassVar[Message2.M8.M10.M25.E5]
                    E5_CONST_5: _ClassVar[Message2.M8.M10.M25.E5]
                E5_UNSPECIFIED: Message2.M8.M10.M25.E5
                E5_CONST_1: Message2.M8.M10.M25.E5
                E5_CONST_2: Message2.M8.M10.M25.E5
                E5_CONST_3: Message2.M8.M10.M25.E5
                E5_CONST_4: Message2.M8.M10.M25.E5
                E5_CONST_5: Message2.M8.M10.M25.E5
                class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E6_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E6]
                    E6_CONST_1: _ClassVar[Message2.M8.M10.M25.E6]
                    E6_CONST_2: _ClassVar[Message2.M8.M10.M25.E6]
                    E6_CONST_3: _ClassVar[Message2.M8.M10.M25.E6]
                    E6_CONST_4: _ClassVar[Message2.M8.M10.M25.E6]
                    E6_CONST_5: _ClassVar[Message2.M8.M10.M25.E6]
                E6_UNSPECIFIED: Message2.M8.M10.M25.E6
                E6_CONST_1: Message2.M8.M10.M25.E6
                E6_CONST_2: Message2.M8.M10.M25.E6
                E6_CONST_3: Message2.M8.M10.M25.E6
                E6_CONST_4: Message2.M8.M10.M25.E6
                E6_CONST_5: Message2.M8.M10.M25.E6
                class E7(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E7_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E7]
                    E7_CONST_1: _ClassVar[Message2.M8.M10.M25.E7]
                    E7_CONST_2: _ClassVar[Message2.M8.M10.M25.E7]
                    E7_CONST_3: _ClassVar[Message2.M8.M10.M25.E7]
                    E7_CONST_4: _ClassVar[Message2.M8.M10.M25.E7]
                    E7_CONST_5: _ClassVar[Message2.M8.M10.M25.E7]
                E7_UNSPECIFIED: Message2.M8.M10.M25.E7
                E7_CONST_1: Message2.M8.M10.M25.E7
                E7_CONST_2: Message2.M8.M10.M25.E7
                E7_CONST_3: Message2.M8.M10.M25.E7
                E7_CONST_4: Message2.M8.M10.M25.E7
                E7_CONST_5: Message2.M8.M10.M25.E7
                class E8(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E8_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E8]
                    E8_CONST_1: _ClassVar[Message2.M8.M10.M25.E8]
                    E8_CONST_2: _ClassVar[Message2.M8.M10.M25.E8]
                    E8_CONST_3: _ClassVar[Message2.M8.M10.M25.E8]
                    E8_CONST_4: _ClassVar[Message2.M8.M10.M25.E8]
                    E8_CONST_5: _ClassVar[Message2.M8.M10.M25.E8]
                E8_UNSPECIFIED: Message2.M8.M10.M25.E8
                E8_CONST_1: Message2.M8.M10.M25.E8
                E8_CONST_2: Message2.M8.M10.M25.E8
                E8_CONST_3: Message2.M8.M10.M25.E8
                E8_CONST_4: Message2.M8.M10.M25.E8
                E8_CONST_5: Message2.M8.M10.M25.E8
                class E9(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E9_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E9]
                    E9_CONST_1: _ClassVar[Message2.M8.M10.M25.E9]
                    E9_CONST_2: _ClassVar[Message2.M8.M10.M25.E9]
                    E9_CONST_3: _ClassVar[Message2.M8.M10.M25.E9]
                    E9_CONST_4: _ClassVar[Message2.M8.M10.M25.E9]
                    E9_CONST_5: _ClassVar[Message2.M8.M10.M25.E9]
                E9_UNSPECIFIED: Message2.M8.M10.M25.E9
                E9_CONST_1: Message2.M8.M10.M25.E9
                E9_CONST_2: Message2.M8.M10.M25.E9
                E9_CONST_3: Message2.M8.M10.M25.E9
                E9_CONST_4: Message2.M8.M10.M25.E9
                E9_CONST_5: Message2.M8.M10.M25.E9
                class E10(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E10_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E10]
                    E10_CONST_1: _ClassVar[Message2.M8.M10.M25.E10]
                    E10_CONST_2: _ClassVar[Message2.M8.M10.M25.E10]
                    E10_CONST_3: _ClassVar[Message2.M8.M10.M25.E10]
                    E10_CONST_4: _ClassVar[Message2.M8.M10.M25.E10]
                    E10_CONST_5: _ClassVar[Message2.M8.M10.M25.E10]
                E10_UNSPECIFIED: Message2.M8.M10.M25.E10
                E10_CONST_1: Message2.M8.M10.M25.E10
                E10_CONST_2: Message2.M8.M10.M25.E10
                E10_CONST_3: Message2.M8.M10.M25.E10
                E10_CONST_4: Message2.M8.M10.M25.E10
                E10_CONST_5: Message2.M8.M10.M25.E10
                class E11(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E11_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E11]
                    E11_CONST_1: _ClassVar[Message2.M8.M10.M25.E11]
                    E11_CONST_2: _ClassVar[Message2.M8.M10.M25.E11]
                    E11_CONST_3: _ClassVar[Message2.M8.M10.M25.E11]
                    E11_CONST_4: _ClassVar[Message2.M8.M10.M25.E11]
                    E11_CONST_5: _ClassVar[Message2.M8.M10.M25.E11]
                E11_UNSPECIFIED: Message2.M8.M10.M25.E11
                E11_CONST_1: Message2.M8.M10.M25.E11
                E11_CONST_2: Message2.M8.M10.M25.E11
                E11_CONST_3: Message2.M8.M10.M25.E11
                E11_CONST_4: Message2.M8.M10.M25.E11
                E11_CONST_5: Message2.M8.M10.M25.E11
                class E12(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E12_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.E12]
                    E12_CONST_1: _ClassVar[Message2.M8.M10.M25.E12]
                    E12_CONST_2: _ClassVar[Message2.M8.M10.M25.E12]
                    E12_CONST_3: _ClassVar[Message2.M8.M10.M25.E12]
                    E12_CONST_4: _ClassVar[Message2.M8.M10.M25.E12]
                    E12_CONST_5: _ClassVar[Message2.M8.M10.M25.E12]
                E12_UNSPECIFIED: Message2.M8.M10.M25.E12
                E12_CONST_1: Message2.M8.M10.M25.E12
                E12_CONST_2: Message2.M8.M10.M25.E12
                E12_CONST_3: Message2.M8.M10.M25.E12
                E12_CONST_4: Message2.M8.M10.M25.E12
                E12_CONST_5: Message2.M8.M10.M25.E12
                class M31(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                class M33(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_14")
                    class E14(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E14_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M33.E14]
                        E14_CONST_1: _ClassVar[Message2.M8.M10.M25.M33.E14]
                        E14_CONST_2: _ClassVar[Message2.M8.M10.M25.M33.E14]
                        E14_CONST_3: _ClassVar[Message2.M8.M10.M25.M33.E14]
                        E14_CONST_4: _ClassVar[Message2.M8.M10.M25.M33.E14]
                        E14_CONST_5: _ClassVar[Message2.M8.M10.M25.M33.E14]
                    E14_UNSPECIFIED: Message2.M8.M10.M25.M33.E14
                    E14_CONST_1: Message2.M8.M10.M25.M33.E14
                    E14_CONST_2: Message2.M8.M10.M25.M33.E14
                    E14_CONST_3: Message2.M8.M10.M25.M33.E14
                    E14_CONST_4: Message2.M8.M10.M25.M33.E14
                    E14_CONST_5: Message2.M8.M10.M25.M33.E14
                    class M64(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12")
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        F_6_FIELD_NUMBER: _ClassVar[int]
                        F_7_FIELD_NUMBER: _ClassVar[int]
                        F_8_FIELD_NUMBER: _ClassVar[int]
                        F_9_FIELD_NUMBER: _ClassVar[int]
                        F_10_FIELD_NUMBER: _ClassVar[int]
                        F_11_FIELD_NUMBER: _ClassVar[int]
                        F_12_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_1: int
                        f_2: int
                        f_3: float
                        f_4: int
                        f_5: str
                        f_6: float
                        f_7: str
                        f_8: int
                        f_9: float
                        f_10: int
                        f_11: int
                        f_12: str
                        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[float] = ..., f_4: _Optional[int] = ..., f_5: _Optional[str] = ..., f_6: _Optional[float] = ..., f_7: _Optional[str] = ..., f_8: _Optional[int] = ..., f_9: _Optional[float] = ..., f_10: _Optional[int] = ..., f_11: _Optional[int] = ..., f_12: _Optional[str] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    F_7_FIELD_NUMBER: _ClassVar[int]
                    F_8_FIELD_NUMBER: _ClassVar[int]
                    F_14_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: str
                    f_2: int
                    f_3: float
                    f_4: str
                    f_5: bool
                    f_6: float
                    f_7: bool
                    f_8: Message2.M8.M10.M25.M33.E14
                    f_14: Message2.M8.M10.M25.M33.M64
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[str] = ..., f_2: _Optional[int] = ..., f_3: _Optional[float] = ..., f_4: _Optional[str] = ..., f_5: _Optional[bool] = ..., f_6: _Optional[float] = ..., f_7: _Optional[bool] = ..., f_8: _Optional[_Union[Message2.M8.M10.M25.M33.E14, str]] = ..., f_14: _Optional[_Union[Message2.M8.M10.M25.M33.M64, _Mapping]] = ...) -> None: ...
                class M36(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: bytes
                    f_2: int
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[int] = ...) -> None: ...
                class M37(_message.Message):
                    __slots__ = ("f_0", "f_3")
                    class M51(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_3: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M25.M37.M51]
                    def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message2.M8.M10.M25.M37.M51, _Mapping]]] = ...) -> None: ...
                class M48(_message.Message):
                    __slots__ = ("f_0", "f_3", "f_4")
                    class M56(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13")
                        class E20(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E20_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M56.E20]
                            E20_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M56.E20]
                            E20_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M56.E20]
                            E20_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M56.E20]
                            E20_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M56.E20]
                            E20_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M56.E20]
                        E20_UNSPECIFIED: Message2.M8.M10.M25.M48.M56.E20
                        E20_CONST_1: Message2.M8.M10.M25.M48.M56.E20
                        E20_CONST_2: Message2.M8.M10.M25.M48.M56.E20
                        E20_CONST_3: Message2.M8.M10.M25.M48.M56.E20
                        E20_CONST_4: Message2.M8.M10.M25.M48.M56.E20
                        E20_CONST_5: Message2.M8.M10.M25.M48.M56.E20
                        class E21(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E21_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M56.E21]
                            E21_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M56.E21]
                            E21_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M56.E21]
                            E21_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M56.E21]
                            E21_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M56.E21]
                            E21_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M56.E21]
                        E21_UNSPECIFIED: Message2.M8.M10.M25.M48.M56.E21
                        E21_CONST_1: Message2.M8.M10.M25.M48.M56.E21
                        E21_CONST_2: Message2.M8.M10.M25.M48.M56.E21
                        E21_CONST_3: Message2.M8.M10.M25.M48.M56.E21
                        E21_CONST_4: Message2.M8.M10.M25.M48.M56.E21
                        E21_CONST_5: Message2.M8.M10.M25.M48.M56.E21
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        F_6_FIELD_NUMBER: _ClassVar[int]
                        F_7_FIELD_NUMBER: _ClassVar[int]
                        F_8_FIELD_NUMBER: _ClassVar[int]
                        F_9_FIELD_NUMBER: _ClassVar[int]
                        F_10_FIELD_NUMBER: _ClassVar[int]
                        F_11_FIELD_NUMBER: _ClassVar[int]
                        F_12_FIELD_NUMBER: _ClassVar[int]
                        F_13_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message2.M8.M10.M25.M48.M56.E20
                        f_1: str
                        f_2: _containers.RepeatedScalarFieldContainer[str]
                        f_3: bool
                        f_4: int
                        f_5: int
                        f_6: str
                        f_7: int
                        f_8: int
                        f_9: int
                        f_10: int
                        f_11: Message2.M8.M10.M25.M48.M56.E21
                        f_12: int
                        f_13: bytes
                        def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M25.M48.M56.E20, str]] = ..., f_1: _Optional[str] = ..., f_2: _Optional[_Iterable[str]] = ..., f_3: _Optional[bool] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[str] = ..., f_7: _Optional[int] = ..., f_8: _Optional[int] = ..., f_9: _Optional[int] = ..., f_10: _Optional[int] = ..., f_11: _Optional[_Union[Message2.M8.M10.M25.M48.M56.E21, str]] = ..., f_12: _Optional[int] = ..., f_13: _Optional[bytes] = ...) -> None: ...
                    class M66(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_15")
                        class E25(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E25_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.E25]
                            E25_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.E25]
                            E25_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.E25]
                            E25_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.E25]
                            E25_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.E25]
                            E25_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.E25]
                        E25_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.E25
                        E25_CONST_1: Message2.M8.M10.M25.M48.M66.E25
                        E25_CONST_2: Message2.M8.M10.M25.M48.M66.E25
                        E25_CONST_3: Message2.M8.M10.M25.M48.M66.E25
                        E25_CONST_4: Message2.M8.M10.M25.M48.M66.E25
                        E25_CONST_5: Message2.M8.M10.M25.M48.M66.E25
                        class E26(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E26_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.E26]
                            E26_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.E26]
                            E26_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.E26]
                            E26_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.E26]
                            E26_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.E26]
                            E26_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.E26]
                        E26_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.E26
                        E26_CONST_1: Message2.M8.M10.M25.M48.M66.E26
                        E26_CONST_2: Message2.M8.M10.M25.M48.M66.E26
                        E26_CONST_3: Message2.M8.M10.M25.M48.M66.E26
                        E26_CONST_4: Message2.M8.M10.M25.M48.M66.E26
                        E26_CONST_5: Message2.M8.M10.M25.M48.M66.E26
                        class E27(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E27_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.E27]
                            E27_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.E27]
                            E27_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.E27]
                            E27_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.E27]
                            E27_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.E27]
                            E27_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.E27]
                        E27_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.E27
                        E27_CONST_1: Message2.M8.M10.M25.M48.M66.E27
                        E27_CONST_2: Message2.M8.M10.M25.M48.M66.E27
                        E27_CONST_3: Message2.M8.M10.M25.M48.M66.E27
                        E27_CONST_4: Message2.M8.M10.M25.M48.M66.E27
                        E27_CONST_5: Message2.M8.M10.M25.M48.M66.E27
                        class M69(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_21")
                            class E29(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E29_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E29]
                                E29_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E29]
                                E29_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E29]
                                E29_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E29]
                                E29_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E29]
                                E29_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E29]
                            E29_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.M69.E29
                            E29_CONST_1: Message2.M8.M10.M25.M48.M66.M69.E29
                            E29_CONST_2: Message2.M8.M10.M25.M48.M66.M69.E29
                            E29_CONST_3: Message2.M8.M10.M25.M48.M66.M69.E29
                            E29_CONST_4: Message2.M8.M10.M25.M48.M66.M69.E29
                            E29_CONST_5: Message2.M8.M10.M25.M48.M66.M69.E29
                            class E30(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E30_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E30]
                                E30_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E30]
                                E30_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E30]
                                E30_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E30]
                                E30_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E30]
                                E30_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.E30]
                            E30_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.M69.E30
                            E30_CONST_1: Message2.M8.M10.M25.M48.M66.M69.E30
                            E30_CONST_2: Message2.M8.M10.M25.M48.M66.M69.E30
                            E30_CONST_3: Message2.M8.M10.M25.M48.M66.M69.E30
                            E30_CONST_4: Message2.M8.M10.M25.M48.M66.M69.E30
                            E30_CONST_5: Message2.M8.M10.M25.M48.M66.M69.E30
                            class M74(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_37", "f_38", "f_39")
                                class E36(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E36_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.E36]
                                    E36_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.E36]
                                    E36_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.E36]
                                    E36_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.E36]
                                    E36_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.E36]
                                    E36_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.E36]
                                E36_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                E36_CONST_1: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                E36_CONST_2: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                E36_CONST_3: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                E36_CONST_4: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                E36_CONST_5: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                class M77(_message.Message):
                                    __slots__ = ("f_0", "f_3")
                                    class M85(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    f_3: Message2.M8.M10.M25.M48.M66.M69.M74.M77.M85
                                    def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M77.M85, _Mapping]] = ...) -> None: ...
                                class M79(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_2")
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: float
                                    f_1: int
                                    f_2: int
                                    def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ...) -> None: ...
                                class M80(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_14")
                                    class E37(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E37_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37]
                                        E37_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37]
                                        E37_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37]
                                        E37_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37]
                                        E37_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37]
                                        E37_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37]
                                    E37_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    E37_CONST_1: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    E37_CONST_2: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    E37_CONST_3: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    E37_CONST_4: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    E37_CONST_5: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    class M87(_message.Message):
                                        __slots__ = ("f_0", "f_1", "f_2", "f_3")
                                        class E38(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                            __slots__ = ()
                                            E38_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38]
                                            E38_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38]
                                            E38_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38]
                                            E38_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38]
                                            E38_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38]
                                            E38_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38]
                                        E38_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        E38_CONST_1: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        E38_CONST_2: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        E38_CONST_3: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        E38_CONST_4: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        E38_CONST_5: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        class E39(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                            __slots__ = ()
                                            E39_UNSPECIFIED: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39]
                                            E39_CONST_1: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39]
                                            E39_CONST_2: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39]
                                            E39_CONST_3: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39]
                                            E39_CONST_4: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39]
                                            E39_CONST_5: _ClassVar[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39]
                                        E39_UNSPECIFIED: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        E39_CONST_1: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        E39_CONST_2: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        E39_CONST_3: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        E39_CONST_4: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        E39_CONST_5: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_1_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        F_3_FIELD_NUMBER: _ClassVar[int]
                                        f_0: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38
                                        f_1: bytes
                                        f_2: _containers.RepeatedScalarFieldContainer[float]
                                        f_3: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39
                                        def __init__(self, f_0: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E38, str]] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[_Iterable[float]] = ..., f_3: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87.E39, str]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    F_4_FIELD_NUMBER: _ClassVar[int]
                                    F_5_FIELD_NUMBER: _ClassVar[int]
                                    F_6_FIELD_NUMBER: _ClassVar[int]
                                    F_7_FIELD_NUMBER: _ClassVar[int]
                                    F_8_FIELD_NUMBER: _ClassVar[int]
                                    F_9_FIELD_NUMBER: _ClassVar[int]
                                    F_14_FIELD_NUMBER: _ClassVar[int]
                                    f_0: float
                                    f_1: int
                                    f_2: Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37
                                    f_3: int
                                    f_4: int
                                    f_5: int
                                    f_6: int
                                    f_7: int
                                    f_8: _containers.RepeatedScalarFieldContainer[int]
                                    f_9: int
                                    f_14: Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87
                                    def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M80.E37, str]] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[int] = ..., f_7: _Optional[int] = ..., f_8: _Optional[_Iterable[int]] = ..., f_9: _Optional[int] = ..., f_14: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M80.M87, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                F_4_FIELD_NUMBER: _ClassVar[int]
                                F_5_FIELD_NUMBER: _ClassVar[int]
                                F_6_FIELD_NUMBER: _ClassVar[int]
                                F_7_FIELD_NUMBER: _ClassVar[int]
                                F_8_FIELD_NUMBER: _ClassVar[int]
                                F_9_FIELD_NUMBER: _ClassVar[int]
                                F_10_FIELD_NUMBER: _ClassVar[int]
                                F_11_FIELD_NUMBER: _ClassVar[int]
                                F_12_FIELD_NUMBER: _ClassVar[int]
                                F_13_FIELD_NUMBER: _ClassVar[int]
                                F_14_FIELD_NUMBER: _ClassVar[int]
                                F_15_FIELD_NUMBER: _ClassVar[int]
                                F_16_FIELD_NUMBER: _ClassVar[int]
                                F_17_FIELD_NUMBER: _ClassVar[int]
                                F_18_FIELD_NUMBER: _ClassVar[int]
                                F_19_FIELD_NUMBER: _ClassVar[int]
                                F_20_FIELD_NUMBER: _ClassVar[int]
                                F_21_FIELD_NUMBER: _ClassVar[int]
                                F_22_FIELD_NUMBER: _ClassVar[int]
                                F_23_FIELD_NUMBER: _ClassVar[int]
                                F_24_FIELD_NUMBER: _ClassVar[int]
                                F_25_FIELD_NUMBER: _ClassVar[int]
                                F_37_FIELD_NUMBER: _ClassVar[int]
                                F_38_FIELD_NUMBER: _ClassVar[int]
                                F_39_FIELD_NUMBER: _ClassVar[int]
                                f_0: bytes
                                f_1: int
                                f_2: Message2.M8.M10.M25.M48.M66.M69.M74.E36
                                f_3: int
                                f_4: int
                                f_5: str
                                f_6: int
                                f_7: _containers.RepeatedScalarFieldContainer[str]
                                f_8: int
                                f_9: float
                                f_10: int
                                f_11: _containers.RepeatedScalarFieldContainer[int]
                                f_12: int
                                f_13: bytes
                                f_14: int
                                f_15: int
                                f_16: int
                                f_17: int
                                f_18: int
                                f_19: int
                                f_20: float
                                f_21: int
                                f_22: int
                                f_23: bytes
                                f_24: int
                                f_25: int
                                f_37: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M25.M48.M66.M69.M74.M77]
                                f_38: Message2.M8.M10.M25.M48.M66.M69.M74.M79
                                f_39: Message2.M8.M10.M25.M48.M66.M69.M74.M80
                                def __init__(self, f_0: _Optional[bytes] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.E36, str]] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[str] = ..., f_6: _Optional[int] = ..., f_7: _Optional[_Iterable[str]] = ..., f_8: _Optional[int] = ..., f_9: _Optional[float] = ..., f_10: _Optional[int] = ..., f_11: _Optional[_Iterable[int]] = ..., f_12: _Optional[int] = ..., f_13: _Optional[bytes] = ..., f_14: _Optional[int] = ..., f_15: _Optional[int] = ..., f_16: _Optional[int] = ..., f_17: _Optional[int] = ..., f_18: _Optional[int] = ..., f_19: _Optional[int] = ..., f_20: _Optional[float] = ..., f_21: _Optional[int] = ..., f_22: _Optional[int] = ..., f_23: _Optional[bytes] = ..., f_24: _Optional[int] = ..., f_25: _Optional[int] = ..., f_37: _Optional[_Iterable[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M77, _Mapping]]] = ..., f_38: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M79, _Mapping]] = ..., f_39: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74.M80, _Mapping]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            F_5_FIELD_NUMBER: _ClassVar[int]
                            F_6_FIELD_NUMBER: _ClassVar[int]
                            F_7_FIELD_NUMBER: _ClassVar[int]
                            F_8_FIELD_NUMBER: _ClassVar[int]
                            F_9_FIELD_NUMBER: _ClassVar[int]
                            F_10_FIELD_NUMBER: _ClassVar[int]
                            F_11_FIELD_NUMBER: _ClassVar[int]
                            F_12_FIELD_NUMBER: _ClassVar[int]
                            F_13_FIELD_NUMBER: _ClassVar[int]
                            F_21_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_1: Message2.M8.M10.M25.M48.M66.M69.E29
                            f_2: str
                            f_3: int
                            f_4: float
                            f_5: str
                            f_6: int
                            f_7: float
                            f_8: int
                            f_9: str
                            f_10: int
                            f_11: _containers.RepeatedScalarFieldContainer[str]
                            f_12: bytes
                            f_13: Message2.M8.M10.M25.M48.M66.M69.E30
                            f_21: Message2.M8.M10.M25.M48.M66.M69.M74
                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.E29, str]] = ..., f_2: _Optional[str] = ..., f_3: _Optional[int] = ..., f_4: _Optional[float] = ..., f_5: _Optional[str] = ..., f_6: _Optional[int] = ..., f_7: _Optional[float] = ..., f_8: _Optional[int] = ..., f_9: _Optional[str] = ..., f_10: _Optional[int] = ..., f_11: _Optional[_Iterable[str]] = ..., f_12: _Optional[bytes] = ..., f_13: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.E30, str]] = ..., f_21: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69.M74, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        F_6_FIELD_NUMBER: _ClassVar[int]
                        F_7_FIELD_NUMBER: _ClassVar[int]
                        F_8_FIELD_NUMBER: _ClassVar[int]
                        F_9_FIELD_NUMBER: _ClassVar[int]
                        F_10_FIELD_NUMBER: _ClassVar[int]
                        F_11_FIELD_NUMBER: _ClassVar[int]
                        F_15_FIELD_NUMBER: _ClassVar[int]
                        f_0: _containers.RepeatedScalarFieldContainer[Message2.M8.M10.M25.M48.M66.E25]
                        f_1: Message2.M8.M10.M25.M48.M66.E26
                        f_2: str
                        f_3: str
                        f_4: int
                        f_5: bytes
                        f_6: _containers.RepeatedScalarFieldContainer[Message2.M8.M10.M25.M48.M66.E27]
                        f_7: _containers.RepeatedScalarFieldContainer[str]
                        f_8: str
                        f_9: int
                        f_10: int
                        f_11: int
                        f_15: Message2.M8.M10.M25.M48.M66.M69
                        def __init__(self, f_0: _Optional[_Iterable[_Union[Message2.M8.M10.M25.M48.M66.E25, str]]] = ..., f_1: _Optional[_Union[Message2.M8.M10.M25.M48.M66.E26, str]] = ..., f_2: _Optional[str] = ..., f_3: _Optional[str] = ..., f_4: _Optional[int] = ..., f_5: _Optional[bytes] = ..., f_6: _Optional[_Iterable[_Union[Message2.M8.M10.M25.M48.M66.E27, str]]] = ..., f_7: _Optional[_Iterable[str]] = ..., f_8: _Optional[str] = ..., f_9: _Optional[int] = ..., f_10: _Optional[int] = ..., f_11: _Optional[int] = ..., f_15: _Optional[_Union[Message2.M8.M10.M25.M48.M66.M69, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_3: Message2.M8.M10.M25.M48.M56
                    f_4: Message2.M8.M10.M25.M48.M66
                    def __init__(self, f_0: _Optional[float] = ..., f_3: _Optional[_Union[Message2.M8.M10.M25.M48.M56, _Mapping]] = ..., f_4: _Optional[_Union[Message2.M8.M10.M25.M48.M66, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_1_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                F_6_FIELD_NUMBER: _ClassVar[int]
                F_7_FIELD_NUMBER: _ClassVar[int]
                F_8_FIELD_NUMBER: _ClassVar[int]
                F_9_FIELD_NUMBER: _ClassVar[int]
                F_10_FIELD_NUMBER: _ClassVar[int]
                F_11_FIELD_NUMBER: _ClassVar[int]
                F_12_FIELD_NUMBER: _ClassVar[int]
                F_13_FIELD_NUMBER: _ClassVar[int]
                F_14_FIELD_NUMBER: _ClassVar[int]
                F_15_FIELD_NUMBER: _ClassVar[int]
                F_16_FIELD_NUMBER: _ClassVar[int]
                F_17_FIELD_NUMBER: _ClassVar[int]
                F_18_FIELD_NUMBER: _ClassVar[int]
                F_19_FIELD_NUMBER: _ClassVar[int]
                F_20_FIELD_NUMBER: _ClassVar[int]
                F_21_FIELD_NUMBER: _ClassVar[int]
                F_22_FIELD_NUMBER: _ClassVar[int]
                F_23_FIELD_NUMBER: _ClassVar[int]
                F_24_FIELD_NUMBER: _ClassVar[int]
                F_25_FIELD_NUMBER: _ClassVar[int]
                F_26_FIELD_NUMBER: _ClassVar[int]
                F_27_FIELD_NUMBER: _ClassVar[int]
                F_28_FIELD_NUMBER: _ClassVar[int]
                F_29_FIELD_NUMBER: _ClassVar[int]
                F_30_FIELD_NUMBER: _ClassVar[int]
                F_31_FIELD_NUMBER: _ClassVar[int]
                F_32_FIELD_NUMBER: _ClassVar[int]
                F_33_FIELD_NUMBER: _ClassVar[int]
                F_34_FIELD_NUMBER: _ClassVar[int]
                F_35_FIELD_NUMBER: _ClassVar[int]
                F_36_FIELD_NUMBER: _ClassVar[int]
                F_37_FIELD_NUMBER: _ClassVar[int]
                F_38_FIELD_NUMBER: _ClassVar[int]
                F_39_FIELD_NUMBER: _ClassVar[int]
                F_40_FIELD_NUMBER: _ClassVar[int]
                F_41_FIELD_NUMBER: _ClassVar[int]
                F_42_FIELD_NUMBER: _ClassVar[int]
                F_43_FIELD_NUMBER: _ClassVar[int]
                F_44_FIELD_NUMBER: _ClassVar[int]
                F_45_FIELD_NUMBER: _ClassVar[int]
                F_46_FIELD_NUMBER: _ClassVar[int]
                F_47_FIELD_NUMBER: _ClassVar[int]
                F_48_FIELD_NUMBER: _ClassVar[int]
                F_49_FIELD_NUMBER: _ClassVar[int]
                F_50_FIELD_NUMBER: _ClassVar[int]
                F_51_FIELD_NUMBER: _ClassVar[int]
                F_52_FIELD_NUMBER: _ClassVar[int]
                F_53_FIELD_NUMBER: _ClassVar[int]
                F_54_FIELD_NUMBER: _ClassVar[int]
                F_55_FIELD_NUMBER: _ClassVar[int]
                F_56_FIELD_NUMBER: _ClassVar[int]
                F_57_FIELD_NUMBER: _ClassVar[int]
                F_58_FIELD_NUMBER: _ClassVar[int]
                F_59_FIELD_NUMBER: _ClassVar[int]
                F_60_FIELD_NUMBER: _ClassVar[int]
                F_61_FIELD_NUMBER: _ClassVar[int]
                F_62_FIELD_NUMBER: _ClassVar[int]
                F_63_FIELD_NUMBER: _ClassVar[int]
                F_64_FIELD_NUMBER: _ClassVar[int]
                F_65_FIELD_NUMBER: _ClassVar[int]
                F_66_FIELD_NUMBER: _ClassVar[int]
                F_67_FIELD_NUMBER: _ClassVar[int]
                F_68_FIELD_NUMBER: _ClassVar[int]
                F_69_FIELD_NUMBER: _ClassVar[int]
                F_70_FIELD_NUMBER: _ClassVar[int]
                F_71_FIELD_NUMBER: _ClassVar[int]
                F_72_FIELD_NUMBER: _ClassVar[int]
                F_73_FIELD_NUMBER: _ClassVar[int]
                F_101_FIELD_NUMBER: _ClassVar[int]
                F_102_FIELD_NUMBER: _ClassVar[int]
                F_103_FIELD_NUMBER: _ClassVar[int]
                F_104_FIELD_NUMBER: _ClassVar[int]
                F_105_FIELD_NUMBER: _ClassVar[int]
                f_0: str
                f_1: _containers.RepeatedScalarFieldContainer[int]
                f_2: int
                f_3: int
                f_4: bytes
                f_5: int
                f_6: bytes
                f_7: bool
                f_8: Message2.M8.M10.M25.E5
                f_9: int
                f_10: str
                f_11: str
                f_12: int
                f_13: str
                f_14: _containers.RepeatedScalarFieldContainer[float]
                f_15: int
                f_16: int
                f_17: Message2.M8.M10.M25.E6
                f_18: int
                f_19: int
                f_20: int
                f_21: str
                f_22: bytes
                f_23: int
                f_24: bool
                f_25: float
                f_26: int
                f_27: int
                f_28: float
                f_29: int
                f_30: float
                f_31: float
                f_32: Message2.M8.M10.M25.E7
                f_33: int
                f_34: bool
                f_35: int
                f_36: _containers.RepeatedScalarFieldContainer[Message2.M8.M10.M25.E8]
                f_37: int
                f_38: int
                f_39: int
                f_40: int
                f_41: Message2.M8.M10.M25.E9
                f_42: float
                f_43: int
                f_44: Message2.M8.M10.M25.E10
                f_45: bytes
                f_46: int
                f_47: bool
                f_48: int
                f_49: int
                f_50: int
                f_51: bool
                f_52: int
                f_53: float
                f_54: float
                f_55: Message2.M8.M10.M25.E11
                f_56: str
                f_57: _containers.RepeatedScalarFieldContainer[int]
                f_58: str
                f_59: int
                f_60: int
                f_61: int
                f_62: int
                f_63: str
                f_64: float
                f_65: int
                f_66: int
                f_67: bytes
                f_68: int
                f_69: float
                f_70: Message2.M8.M10.M25.E12
                f_71: bytes
                f_72: int
                f_73: int
                f_101: Message2.M8.M10.M25.M31
                f_102: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M25.M33]
                f_103: Message2.M8.M10.M25.M36
                f_104: Message2.M8.M10.M25.M37
                f_105: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M25.M48]
                def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[_Iterable[int]] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[bytes] = ..., f_5: _Optional[int] = ..., f_6: _Optional[bytes] = ..., f_7: _Optional[bool] = ..., f_8: _Optional[_Union[Message2.M8.M10.M25.E5, str]] = ..., f_9: _Optional[int] = ..., f_10: _Optional[str] = ..., f_11: _Optional[str] = ..., f_12: _Optional[int] = ..., f_13: _Optional[str] = ..., f_14: _Optional[_Iterable[float]] = ..., f_15: _Optional[int] = ..., f_16: _Optional[int] = ..., f_17: _Optional[_Union[Message2.M8.M10.M25.E6, str]] = ..., f_18: _Optional[int] = ..., f_19: _Optional[int] = ..., f_20: _Optional[int] = ..., f_21: _Optional[str] = ..., f_22: _Optional[bytes] = ..., f_23: _Optional[int] = ..., f_24: _Optional[bool] = ..., f_25: _Optional[float] = ..., f_26: _Optional[int] = ..., f_27: _Optional[int] = ..., f_28: _Optional[float] = ..., f_29: _Optional[int] = ..., f_30: _Optional[float] = ..., f_31: _Optional[float] = ..., f_32: _Optional[_Union[Message2.M8.M10.M25.E7, str]] = ..., f_33: _Optional[int] = ..., f_34: _Optional[bool] = ..., f_35: _Optional[int] = ..., f_36: _Optional[_Iterable[_Union[Message2.M8.M10.M25.E8, str]]] = ..., f_37: _Optional[int] = ..., f_38: _Optional[int] = ..., f_39: _Optional[int] = ..., f_40: _Optional[int] = ..., f_41: _Optional[_Union[Message2.M8.M10.M25.E9, str]] = ..., f_42: _Optional[float] = ..., f_43: _Optional[int] = ..., f_44: _Optional[_Union[Message2.M8.M10.M25.E10, str]] = ..., f_45: _Optional[bytes] = ..., f_46: _Optional[int] = ..., f_47: _Optional[bool] = ..., f_48: _Optional[int] = ..., f_49: _Optional[int] = ..., f_50: _Optional[int] = ..., f_51: _Optional[bool] = ..., f_52: _Optional[int] = ..., f_53: _Optional[float] = ..., f_54: _Optional[float] = ..., f_55: _Optional[_Union[Message2.M8.M10.M25.E11, str]] = ..., f_56: _Optional[str] = ..., f_57: _Optional[_Iterable[int]] = ..., f_58: _Optional[str] = ..., f_59: _Optional[int] = ..., f_60: _Optional[int] = ..., f_61: _Optional[int] = ..., f_62: _Optional[int] = ..., f_63: _Optional[str] = ..., f_64: _Optional[float] = ..., f_65: _Optional[int] = ..., f_66: _Optional[int] = ..., f_67: _Optional[bytes] = ..., f_68: _Optional[int] = ..., f_69: _Optional[float] = ..., f_70: _Optional[_Union[Message2.M8.M10.M25.E12, str]] = ..., f_71: _Optional[bytes] = ..., f_72: _Optional[int] = ..., f_73: _Optional[int] = ..., f_101: _Optional[_Union[Message2.M8.M10.M25.M31, _Mapping]] = ..., f_102: _Optional[_Iterable[_Union[Message2.M8.M10.M25.M33, _Mapping]]] = ..., f_103: _Optional[_Union[Message2.M8.M10.M25.M36, _Mapping]] = ..., f_104: _Optional[_Union[Message2.M8.M10.M25.M37, _Mapping]] = ..., f_105: _Optional[_Iterable[_Union[Message2.M8.M10.M25.M48, _Mapping]]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_4_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_3: Message2.M8.M10.M24
            f_4: _containers.RepeatedCompositeFieldContainer[Message2.M8.M10.M25]
            def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message2.M8.M10.M24, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message2.M8.M10.M25, _Mapping]]] = ...) -> None: ...
        class M14(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
        class M21(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_1_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        F_10_FIELD_NUMBER: _ClassVar[int]
        F_11_FIELD_NUMBER: _ClassVar[int]
        F_12_FIELD_NUMBER: _ClassVar[int]
        f_0: str
        f_1: int
        f_2: bytes
        f_3: int
        f_4: str
        f_10: Message2.M8.M10
        f_11: Message2.M8.M14
        f_12: Message2.M8.M21
        def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[bytes] = ..., f_3: _Optional[int] = ..., f_4: _Optional[str] = ..., f_10: _Optional[_Union[Message2.M8.M10, _Mapping]] = ..., f_11: _Optional[_Union[Message2.M8.M14, _Mapping]] = ..., f_12: _Optional[_Union[Message2.M8.M21, _Mapping]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_4_FIELD_NUMBER: _ClassVar[int]
    F_5_FIELD_NUMBER: _ClassVar[int]
    F_6_FIELD_NUMBER: _ClassVar[int]
    F_7_FIELD_NUMBER: _ClassVar[int]
    F_8_FIELD_NUMBER: _ClassVar[int]
    F_11_FIELD_NUMBER: _ClassVar[int]
    F_13_FIELD_NUMBER: _ClassVar[int]
    F_15_FIELD_NUMBER: _ClassVar[int]
    f_0: int
    f_4: _containers.RepeatedCompositeFieldContainer[Message2.M1]
    f_5: _containers.RepeatedCompositeFieldContainer[Message2.M2]
    f_6: Message2.M3
    f_7: _containers.RepeatedCompositeFieldContainer[Message2.M4]
    f_8: Message2.M5
    f_11: Message2.M6
    f_13: Message2.M7
    f_15: Message2.M8
    def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Iterable[_Union[Message2.M1, _Mapping]]] = ..., f_5: _Optional[_Iterable[_Union[Message2.M2, _Mapping]]] = ..., f_6: _Optional[_Union[Message2.M3, _Mapping]] = ..., f_7: _Optional[_Iterable[_Union[Message2.M4, _Mapping]]] = ..., f_8: _Optional[_Union[Message2.M5, _Mapping]] = ..., f_11: _Optional[_Union[Message2.M6, _Mapping]] = ..., f_13: _Optional[_Union[Message2.M7, _Mapping]] = ..., f_15: _Optional[_Union[Message2.M8, _Mapping]] = ...) -> None: ...
