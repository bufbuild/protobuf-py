from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message8(_message.Message):
    __slots__ = ("f_0", "f_2", "f_4", "f_5", "f_6")
    class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        E1_UNSPECIFIED: _ClassVar[Message8.E1]
        E1_CONST_1: _ClassVar[Message8.E1]
        E1_CONST_2: _ClassVar[Message8.E1]
        E1_CONST_3: _ClassVar[Message8.E1]
        E1_CONST_4: _ClassVar[Message8.E1]
        E1_CONST_5: _ClassVar[Message8.E1]
    E1_UNSPECIFIED: Message8.E1
    E1_CONST_1: Message8.E1
    E1_CONST_2: Message8.E1
    E1_CONST_3: Message8.E1
    E1_CONST_4: Message8.E1
    E1_CONST_5: Message8.E1
    class M1(_message.Message):
        __slots__ = ("f_0", "f_2")
        class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E2_UNSPECIFIED: _ClassVar[Message8.M1.E2]
            E2_CONST_1: _ClassVar[Message8.M1.E2]
            E2_CONST_2: _ClassVar[Message8.M1.E2]
            E2_CONST_3: _ClassVar[Message8.M1.E2]
            E2_CONST_4: _ClassVar[Message8.M1.E2]
            E2_CONST_5: _ClassVar[Message8.M1.E2]
        E2_UNSPECIFIED: Message8.M1.E2
        E2_CONST_1: Message8.M1.E2
        E2_CONST_2: Message8.M1.E2
        E2_CONST_3: Message8.M1.E2
        E2_CONST_4: Message8.M1.E2
        E2_CONST_5: Message8.M1.E2
        class M5(_message.Message):
            __slots__ = ("f_0", "f_3", "f_5", "f_6")
            class M16(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
            class M17(_message.Message):
                __slots__ = ("f_0", "f_3")
                class M25(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M44(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: _containers.RepeatedScalarFieldContainer[int]
                        def __init__(self, f_0: _Optional[_Iterable[int]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: bool
                    f_2: Message8.M1.M5.M17.M25.M44
                    def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Union[Message8.M1.M5.M17.M25.M44, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_3: _containers.RepeatedCompositeFieldContainer[Message8.M1.M5.M17.M25]
                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message8.M1.M5.M17.M25, _Mapping]]] = ...) -> None: ...
            class M21(_message.Message):
                __slots__ = ("f_0", "f_2", "f_3")
                class M24(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M42(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_11")
                        class M47(_message.Message):
                            __slots__ = ("f_0", "f_2", "f_3", "f_4", "f_6")
                            class M49(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                            class M50(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                            class M51(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_2", "f_3")
                                class E30(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E30_UNSPECIFIED: _ClassVar[Message8.M1.M5.M21.M24.M42.M47.M51.E30]
                                    E30_CONST_1: _ClassVar[Message8.M1.M5.M21.M24.M42.M47.M51.E30]
                                    E30_CONST_2: _ClassVar[Message8.M1.M5.M21.M24.M42.M47.M51.E30]
                                    E30_CONST_3: _ClassVar[Message8.M1.M5.M21.M24.M42.M47.M51.E30]
                                    E30_CONST_4: _ClassVar[Message8.M1.M5.M21.M24.M42.M47.M51.E30]
                                    E30_CONST_5: _ClassVar[Message8.M1.M5.M21.M24.M42.M47.M51.E30]
                                E30_UNSPECIFIED: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                E30_CONST_1: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                E30_CONST_2: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                E30_CONST_3: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                E30_CONST_4: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                E30_CONST_5: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                f_0: Message8.M1.M5.M21.M24.M42.M47.M51.E30
                                f_1: bytes
                                f_2: int
                                f_3: str
                                def __init__(self, f_0: _Optional[_Union[Message8.M1.M5.M21.M24.M42.M47.M51.E30, str]] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[int] = ..., f_3: _Optional[str] = ...) -> None: ...
                            class M52(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: float
                                def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            F_6_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_2: Message8.M1.M5.M21.M24.M42.M47.M49
                            f_3: _containers.RepeatedCompositeFieldContainer[Message8.M1.M5.M21.M24.M42.M47.M50]
                            f_4: Message8.M1.M5.M21.M24.M42.M47.M51
                            f_6: _containers.RepeatedCompositeFieldContainer[Message8.M1.M5.M21.M24.M42.M47.M52]
                            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message8.M1.M5.M21.M24.M42.M47.M49, _Mapping]] = ..., f_3: _Optional[_Iterable[_Union[Message8.M1.M5.M21.M24.M42.M47.M50, _Mapping]]] = ..., f_4: _Optional[_Union[Message8.M1.M5.M21.M24.M42.M47.M51, _Mapping]] = ..., f_6: _Optional[_Iterable[_Union[Message8.M1.M5.M21.M24.M42.M47.M52, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_11_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        f_1: bool
                        f_2: int
                        f_3: str
                        f_4: int
                        f_11: Message8.M1.M5.M21.M24.M42.M47
                        def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[bool] = ..., f_2: _Optional[int] = ..., f_3: _Optional[str] = ..., f_4: _Optional[int] = ..., f_11: _Optional[_Union[Message8.M1.M5.M21.M24.M42.M47, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_2: Message8.M1.M5.M21.M24.M42
                    def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message8.M1.M5.M21.M24.M42, _Mapping]] = ...) -> None: ...
                class M30(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class E13(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E13_UNSPECIFIED: _ClassVar[Message8.M1.M5.M21.M30.E13]
                        E13_CONST_1: _ClassVar[Message8.M1.M5.M21.M30.E13]
                        E13_CONST_2: _ClassVar[Message8.M1.M5.M21.M30.E13]
                        E13_CONST_3: _ClassVar[Message8.M1.M5.M21.M30.E13]
                        E13_CONST_4: _ClassVar[Message8.M1.M5.M21.M30.E13]
                        E13_CONST_5: _ClassVar[Message8.M1.M5.M21.M30.E13]
                    E13_UNSPECIFIED: Message8.M1.M5.M21.M30.E13
                    E13_CONST_1: Message8.M1.M5.M21.M30.E13
                    E13_CONST_2: Message8.M1.M5.M21.M30.E13
                    E13_CONST_3: Message8.M1.M5.M21.M30.E13
                    E13_CONST_4: Message8.M1.M5.M21.M30.E13
                    E13_CONST_5: Message8.M1.M5.M21.M30.E13
                    class M37(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message8.M1.M5.M21.M30.E13
                    f_2: Message8.M1.M5.M21.M30.M37
                    def __init__(self, f_0: _Optional[_Union[Message8.M1.M5.M21.M30.E13, str]] = ..., f_2: _Optional[_Union[Message8.M1.M5.M21.M30.M37, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_2: Message8.M1.M5.M21.M24
                f_3: Message8.M1.M5.M21.M30
                def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message8.M1.M5.M21.M24, _Mapping]] = ..., f_3: _Optional[_Union[Message8.M1.M5.M21.M30, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_5_FIELD_NUMBER: _ClassVar[int]
            F_6_FIELD_NUMBER: _ClassVar[int]
            f_0: bool
            f_3: Message8.M1.M5.M16
            f_5: _containers.RepeatedCompositeFieldContainer[Message8.M1.M5.M17]
            f_6: Message8.M1.M5.M21
            def __init__(self, f_0: _Optional[bool] = ..., f_3: _Optional[_Union[Message8.M1.M5.M16, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message8.M1.M5.M17, _Mapping]]] = ..., f_6: _Optional[_Union[Message8.M1.M5.M21, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        f_0: Message8.M1.E2
        f_2: _containers.RepeatedCompositeFieldContainer[Message8.M1.M5]
        def __init__(self, f_0: _Optional[_Union[Message8.M1.E2, str]] = ..., f_2: _Optional[_Iterable[_Union[Message8.M1.M5, _Mapping]]] = ...) -> None: ...
    class M2(_message.Message):
        __slots__ = ("f_0", "f_2", "f_4")
        class M6(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: _containers.RepeatedScalarFieldContainer[int]
            def __init__(self, f_0: _Optional[_Iterable[int]] = ...) -> None: ...
        class M11(_message.Message):
            __slots__ = ("f_0", "f_1", "f_3", "f_4")
            class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E4_UNSPECIFIED: _ClassVar[Message8.M2.M11.E4]
                E4_CONST_1: _ClassVar[Message8.M2.M11.E4]
                E4_CONST_2: _ClassVar[Message8.M2.M11.E4]
                E4_CONST_3: _ClassVar[Message8.M2.M11.E4]
                E4_CONST_4: _ClassVar[Message8.M2.M11.E4]
                E4_CONST_5: _ClassVar[Message8.M2.M11.E4]
            E4_UNSPECIFIED: Message8.M2.M11.E4
            E4_CONST_1: Message8.M2.M11.E4
            E4_CONST_2: Message8.M2.M11.E4
            E4_CONST_3: Message8.M2.M11.E4
            E4_CONST_4: Message8.M2.M11.E4
            E4_CONST_5: Message8.M2.M11.E4
            class M13(_message.Message):
                __slots__ = ("f_0", "f_4", "f_5", "f_6")
                class M31(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                class M34(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                class M36(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14")
                    class E14(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E14_UNSPECIFIED: _ClassVar[Message8.M2.M11.M13.M36.E14]
                        E14_CONST_1: _ClassVar[Message8.M2.M11.M13.M36.E14]
                        E14_CONST_2: _ClassVar[Message8.M2.M11.M13.M36.E14]
                        E14_CONST_3: _ClassVar[Message8.M2.M11.M13.M36.E14]
                        E14_CONST_4: _ClassVar[Message8.M2.M11.M13.M36.E14]
                        E14_CONST_5: _ClassVar[Message8.M2.M11.M13.M36.E14]
                    E14_UNSPECIFIED: Message8.M2.M11.M13.M36.E14
                    E14_CONST_1: Message8.M2.M11.M13.M36.E14
                    E14_CONST_2: Message8.M2.M11.M13.M36.E14
                    E14_CONST_3: Message8.M2.M11.M13.M36.E14
                    E14_CONST_4: Message8.M2.M11.M13.M36.E14
                    E14_CONST_5: Message8.M2.M11.M13.M36.E14
                    class E15(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E15_UNSPECIFIED: _ClassVar[Message8.M2.M11.M13.M36.E15]
                        E15_CONST_1: _ClassVar[Message8.M2.M11.M13.M36.E15]
                        E15_CONST_2: _ClassVar[Message8.M2.M11.M13.M36.E15]
                        E15_CONST_3: _ClassVar[Message8.M2.M11.M13.M36.E15]
                        E15_CONST_4: _ClassVar[Message8.M2.M11.M13.M36.E15]
                        E15_CONST_5: _ClassVar[Message8.M2.M11.M13.M36.E15]
                    E15_UNSPECIFIED: Message8.M2.M11.M13.M36.E15
                    E15_CONST_1: Message8.M2.M11.M13.M36.E15
                    E15_CONST_2: Message8.M2.M11.M13.M36.E15
                    E15_CONST_3: Message8.M2.M11.M13.M36.E15
                    E15_CONST_4: Message8.M2.M11.M13.M36.E15
                    E15_CONST_5: Message8.M2.M11.M13.M36.E15
                    class E16(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E16_UNSPECIFIED: _ClassVar[Message8.M2.M11.M13.M36.E16]
                        E16_CONST_1: _ClassVar[Message8.M2.M11.M13.M36.E16]
                        E16_CONST_2: _ClassVar[Message8.M2.M11.M13.M36.E16]
                        E16_CONST_3: _ClassVar[Message8.M2.M11.M13.M36.E16]
                        E16_CONST_4: _ClassVar[Message8.M2.M11.M13.M36.E16]
                        E16_CONST_5: _ClassVar[Message8.M2.M11.M13.M36.E16]
                    E16_UNSPECIFIED: Message8.M2.M11.M13.M36.E16
                    E16_CONST_1: Message8.M2.M11.M13.M36.E16
                    E16_CONST_2: Message8.M2.M11.M13.M36.E16
                    E16_CONST_3: Message8.M2.M11.M13.M36.E16
                    E16_CONST_4: Message8.M2.M11.M13.M36.E16
                    E16_CONST_5: Message8.M2.M11.M13.M36.E16
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
                    f_0: Message8.M2.M11.M13.M36.E14
                    f_1: int
                    f_2: int
                    f_3: Message8.M2.M11.M13.M36.E15
                    f_4: str
                    f_5: int
                    f_6: int
                    f_7: str
                    f_8: Message8.M2.M11.M13.M36.E16
                    f_9: int
                    f_10: str
                    f_11: int
                    f_12: int
                    f_13: int
                    f_14: _containers.RepeatedScalarFieldContainer[int]
                    def __init__(self, f_0: _Optional[_Union[Message8.M2.M11.M13.M36.E14, str]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[_Union[Message8.M2.M11.M13.M36.E15, str]] = ..., f_4: _Optional[str] = ..., f_5: _Optional[int] = ..., f_6: _Optional[int] = ..., f_7: _Optional[str] = ..., f_8: _Optional[_Union[Message8.M2.M11.M13.M36.E16, str]] = ..., f_9: _Optional[int] = ..., f_10: _Optional[str] = ..., f_11: _Optional[int] = ..., f_12: _Optional[int] = ..., f_13: _Optional[int] = ..., f_14: _Optional[_Iterable[int]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                F_6_FIELD_NUMBER: _ClassVar[int]
                f_0: bytes
                f_4: Message8.M2.M11.M13.M31
                f_5: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M13.M34]
                f_6: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M13.M36]
                def __init__(self, f_0: _Optional[bytes] = ..., f_4: _Optional[_Union[Message8.M2.M11.M13.M31, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message8.M2.M11.M13.M34, _Mapping]]] = ..., f_6: _Optional[_Iterable[_Union[Message8.M2.M11.M13.M36, _Mapping]]] = ...) -> None: ...
            class M23(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_7", "f_8")
                class M26(_message.Message):
                    __slots__ = ("f_0", "f_2", "f_3")
                    class M38(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M48(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_31", "f_32", "f_33", "f_34", "f_35", "f_36", "f_37", "f_38", "f_39", "f_40", "f_41", "f_42", "f_43", "f_44", "f_45", "f_46", "f_62", "f_64", "f_66", "f_68")
                            class E22(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E22_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E22]
                                E22_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E22]
                                E22_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E22]
                                E22_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E22]
                                E22_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E22]
                                E22_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E22]
                            E22_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E22
                            E22_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E22
                            E22_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E22
                            E22_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E22
                            E22_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E22
                            E22_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E22
                            class E23(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E23_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E23]
                                E23_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E23]
                                E23_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E23]
                                E23_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E23]
                                E23_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E23]
                                E23_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E23]
                            E23_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E23
                            E23_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E23
                            E23_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E23
                            E23_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E23
                            E23_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E23
                            E23_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E23
                            class E24(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E24_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E24]
                                E24_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E24]
                                E24_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E24]
                                E24_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E24]
                                E24_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E24]
                                E24_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E24]
                            E24_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E24
                            E24_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E24
                            E24_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E24
                            E24_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E24
                            E24_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E24
                            E24_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E24
                            class E25(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E25_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E25]
                                E25_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E25]
                                E25_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E25]
                                E25_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E25]
                                E25_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E25]
                                E25_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E25]
                            E25_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E25
                            E25_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E25
                            E25_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E25
                            E25_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E25
                            E25_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E25
                            E25_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E25
                            class E26(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E26_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E26]
                                E26_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E26]
                                E26_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E26]
                                E26_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E26]
                                E26_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E26]
                                E26_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E26]
                            E26_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E26
                            E26_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E26
                            E26_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E26
                            E26_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E26
                            E26_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E26
                            E26_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E26
                            class E27(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E27_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E27]
                                E27_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E27]
                                E27_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E27]
                                E27_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E27]
                                E27_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E27]
                                E27_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E27]
                            E27_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E27
                            E27_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E27
                            E27_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E27
                            E27_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E27
                            E27_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E27
                            E27_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E27
                            class E28(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E28_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E28]
                                E28_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E28]
                                E28_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E28]
                                E28_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E28]
                                E28_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E28]
                                E28_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E28]
                            E28_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E28
                            E28_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E28
                            E28_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E28
                            E28_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E28
                            E28_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E28
                            E28_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E28
                            class E29(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E29_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E29]
                                E29_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E29]
                                E29_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E29]
                                E29_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E29]
                                E29_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E29]
                                E29_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.E29]
                            E29_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.E29
                            E29_CONST_1: Message8.M2.M11.M23.M26.M38.M48.E29
                            E29_CONST_2: Message8.M2.M11.M23.M26.M38.M48.E29
                            E29_CONST_3: Message8.M2.M11.M23.M26.M38.M48.E29
                            E29_CONST_4: Message8.M2.M11.M23.M26.M38.M48.E29
                            E29_CONST_5: Message8.M2.M11.M23.M26.M38.M48.E29
                            class M53(_message.Message):
                                __slots__ = ("f_0",)
                                class E31(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E31_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                    E31_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                    E31_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                    E31_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                    E31_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                    E31_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                E31_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M53.E31
                                E31_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M53.E31
                                E31_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M53.E31
                                E31_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M53.E31
                                E31_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M53.E31
                                E31_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M53.E31
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: _containers.RepeatedScalarFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M53.E31]
                                def __init__(self, f_0: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M53.E31, str]]] = ...) -> None: ...
                            class M54(_message.Message):
                                __slots__ = ("f_0", "f_4", "f_5", "f_6", "f_7", "f_9")
                                class M57(_message.Message):
                                    __slots__ = ("f_0",)
                                    class E33(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E33_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33]
                                        E33_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33]
                                        E33_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33]
                                        E33_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33]
                                        E33_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33]
                                        E33_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33]
                                    E33_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    E33_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    E33_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    E33_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    E33_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    E33_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33
                                    def __init__(self, f_0: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M57.E33, str]] = ...) -> None: ...
                                class M58(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: str
                                    def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                                class M59(_message.Message):
                                    __slots__ = ("f_0", "f_2", "f_3")
                                    class M63(_message.Message):
                                        __slots__ = ("f_0", "f_1", "f_2", "f_5")
                                        class E36(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                            __slots__ = ()
                                            E36_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36]
                                            E36_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36]
                                            E36_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36]
                                            E36_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36]
                                            E36_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36]
                                            E36_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36]
                                        E36_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        E36_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        E36_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        E36_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        E36_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        E36_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        class M68(_message.Message):
                                            __slots__ = ("f_0", "f_1", "f_3")
                                            class E38(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                __slots__ = ()
                                                E38_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38]
                                                E38_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38]
                                                E38_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38]
                                                E38_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38]
                                                E38_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38]
                                                E38_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38]
                                            E38_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            E38_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            E38_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            E38_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            E38_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            E38_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            class M69(_message.Message):
                                                __slots__ = ("f_0", "f_1", "f_4")
                                                class M70(_message.Message):
                                                    __slots__ = ("f_0", "f_2")
                                                    class M71(_message.Message):
                                                        __slots__ = ("f_0", "f_2")
                                                        class M72(_message.Message):
                                                            __slots__ = ("f_0", "f_3")
                                                            class M73(_message.Message):
                                                                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_12")
                                                                class E39(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                                    __slots__ = ()
                                                                    E39_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39]
                                                                    E39_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39]
                                                                    E39_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39]
                                                                    E39_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39]
                                                                    E39_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39]
                                                                    E39_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39]
                                                                E39_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                E39_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                E39_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                E39_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                E39_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                E39_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                class M74(_message.Message):
                                                                    __slots__ = ("f_0",)
                                                                    class E40(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                                        __slots__ = ()
                                                                        E40_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                        E40_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                        E40_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                        E40_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                        E40_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                        E40_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                    E40_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40
                                                                    E40_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40
                                                                    E40_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40
                                                                    E40_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40
                                                                    E40_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40
                                                                    E40_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40
                                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                                    f_0: _containers.RepeatedScalarFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40]
                                                                    def __init__(self, f_0: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74.E40, str]]] = ...) -> None: ...
                                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                                F_1_FIELD_NUMBER: _ClassVar[int]
                                                                F_2_FIELD_NUMBER: _ClassVar[int]
                                                                F_3_FIELD_NUMBER: _ClassVar[int]
                                                                F_4_FIELD_NUMBER: _ClassVar[int]
                                                                F_5_FIELD_NUMBER: _ClassVar[int]
                                                                F_6_FIELD_NUMBER: _ClassVar[int]
                                                                F_7_FIELD_NUMBER: _ClassVar[int]
                                                                F_12_FIELD_NUMBER: _ClassVar[int]
                                                                f_0: int
                                                                f_1: int
                                                                f_2: int
                                                                f_3: int
                                                                f_4: str
                                                                f_5: _containers.RepeatedScalarFieldContainer[int]
                                                                f_6: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39
                                                                f_7: str
                                                                f_12: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74
                                                                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[str] = ..., f_5: _Optional[_Iterable[int]] = ..., f_6: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.E39, str]] = ..., f_7: _Optional[str] = ..., f_12: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73.M74, _Mapping]] = ...) -> None: ...
                                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                                            F_3_FIELD_NUMBER: _ClassVar[int]
                                                            f_0: str
                                                            f_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73
                                                            def __init__(self, f_0: _Optional[str] = ..., f_3: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72.M73, _Mapping]] = ...) -> None: ...
                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                                        f_0: bool
                                                        f_2: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72]
                                                        def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71.M72, _Mapping]]] = ...) -> None: ...
                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                                    f_0: bool
                                                    f_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71
                                                    def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70.M71, _Mapping]] = ...) -> None: ...
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                F_1_FIELD_NUMBER: _ClassVar[int]
                                                F_4_FIELD_NUMBER: _ClassVar[int]
                                                f_0: bytes
                                                f_1: float
                                                f_4: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70
                                                def __init__(self, f_0: _Optional[bytes] = ..., f_1: _Optional[float] = ..., f_4: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69.M70, _Mapping]] = ...) -> None: ...
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            F_1_FIELD_NUMBER: _ClassVar[int]
                                            F_3_FIELD_NUMBER: _ClassVar[int]
                                            f_0: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38
                                            f_1: str
                                            f_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69
                                            def __init__(self, f_0: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.E38, str]] = ..., f_1: _Optional[str] = ..., f_3: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68.M69, _Mapping]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_1_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        F_5_FIELD_NUMBER: _ClassVar[int]
                                        f_0: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36
                                        f_1: int
                                        f_2: int
                                        f_5: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68]
                                        def __init__(self, f_0: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.E36, str]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_5: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63.M68, _Mapping]]] = ...) -> None: ...
                                    class M65(_message.Message):
                                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_8")
                                        class E37(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                            __slots__ = ()
                                            E37_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37]
                                            E37_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37]
                                            E37_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37]
                                            E37_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37]
                                            E37_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37]
                                            E37_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37]
                                        E37_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        E37_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        E37_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        E37_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        E37_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        E37_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        class M66(_message.Message):
                                            __slots__ = ("f_0",)
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            f_0: int
                                            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_1_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        F_3_FIELD_NUMBER: _ClassVar[int]
                                        F_4_FIELD_NUMBER: _ClassVar[int]
                                        F_8_FIELD_NUMBER: _ClassVar[int]
                                        f_0: float
                                        f_1: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37
                                        f_2: int
                                        f_3: int
                                        f_4: int
                                        f_8: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.M66]
                                        def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.E37, str]] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_8: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65.M66, _Mapping]]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    f_2: Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63
                                    f_3: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65]
                                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M63, _Mapping]] = ..., f_3: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59.M65, _Mapping]]] = ...) -> None: ...
                                class M60(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                class M62(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_2", "f_3")
                                    class E34(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E34_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34]
                                        E34_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34]
                                        E34_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34]
                                        E34_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34]
                                        E34_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34]
                                        E34_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34]
                                    E34_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    E34_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    E34_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    E34_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    E34_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    E34_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    class E35(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E35_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35]
                                        E35_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35]
                                        E35_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35]
                                        E35_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35]
                                        E35_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35]
                                        E35_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35]
                                    E35_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    E35_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    E35_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    E35_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    E35_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    E35_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34
                                    f_1: str
                                    f_2: float
                                    f_3: Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35
                                    def __init__(self, f_0: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E34, str]] = ..., f_1: _Optional[str] = ..., f_2: _Optional[float] = ..., f_3: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M62.E35, str]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_4_FIELD_NUMBER: _ClassVar[int]
                                F_5_FIELD_NUMBER: _ClassVar[int]
                                F_6_FIELD_NUMBER: _ClassVar[int]
                                F_7_FIELD_NUMBER: _ClassVar[int]
                                F_9_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                f_4: Message8.M2.M11.M23.M26.M38.M48.M54.M57
                                f_5: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M58]
                                f_6: Message8.M2.M11.M23.M26.M38.M48.M54.M59
                                f_7: Message8.M2.M11.M23.M26.M38.M48.M54.M60
                                f_9: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M54.M62]
                                def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M57, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M58, _Mapping]]] = ..., f_6: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M59, _Mapping]] = ..., f_7: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M60, _Mapping]] = ..., f_9: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M54.M62, _Mapping]]] = ...) -> None: ...
                            class M55(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: str
                                def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                            class M56(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_4")
                                class E32(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E32_UNSPECIFIED: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M56.E32]
                                    E32_CONST_1: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M56.E32]
                                    E32_CONST_2: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M56.E32]
                                    E32_CONST_3: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M56.E32]
                                    E32_CONST_4: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M56.E32]
                                    E32_CONST_5: _ClassVar[Message8.M2.M11.M23.M26.M38.M48.M56.E32]
                                E32_UNSPECIFIED: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                E32_CONST_1: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                E32_CONST_2: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                E32_CONST_3: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                E32_CONST_4: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                E32_CONST_5: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                class M61(_message.Message):
                                    __slots__ = ("f_0", "f_4")
                                    class M64(_message.Message):
                                        __slots__ = ("f_0", "f_2")
                                        class M67(_message.Message):
                                            __slots__ = ("f_0",)
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            f_0: _containers.RepeatedScalarFieldContainer[str]
                                            def __init__(self, f_0: _Optional[_Iterable[str]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        f_2: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M56.M61.M64.M67]
                                        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M56.M61.M64.M67, _Mapping]]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_4_FIELD_NUMBER: _ClassVar[int]
                                    f_0: _containers.RepeatedScalarFieldContainer[int]
                                    f_4: Message8.M2.M11.M23.M26.M38.M48.M56.M61.M64
                                    def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_4: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M56.M61.M64, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_4_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                f_1: Message8.M2.M11.M23.M26.M38.M48.M56.E32
                                f_4: Message8.M2.M11.M23.M26.M38.M48.M56.M61
                                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M56.E32, str]] = ..., f_4: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M56.M61, _Mapping]] = ...) -> None: ...
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
                            F_62_FIELD_NUMBER: _ClassVar[int]
                            F_64_FIELD_NUMBER: _ClassVar[int]
                            F_66_FIELD_NUMBER: _ClassVar[int]
                            F_68_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_1: bytes
                            f_2: _containers.RepeatedScalarFieldContainer[int]
                            f_3: str
                            f_4: Message8.M2.M11.M23.M26.M38.M48.E22
                            f_5: _containers.RepeatedScalarFieldContainer[Message8.M2.M11.M23.M26.M38.M48.E23]
                            f_6: int
                            f_7: int
                            f_8: bytes
                            f_9: str
                            f_10: float
                            f_11: int
                            f_12: bytes
                            f_13: str
                            f_14: bytes
                            f_15: int
                            f_16: int
                            f_17: float
                            f_18: int
                            f_19: Message8.M2.M11.M23.M26.M38.M48.E24
                            f_20: int
                            f_21: int
                            f_22: float
                            f_23: str
                            f_24: str
                            f_25: _containers.RepeatedScalarFieldContainer[int]
                            f_26: int
                            f_27: Message8.M2.M11.M23.M26.M38.M48.E25
                            f_28: float
                            f_29: bytes
                            f_30: str
                            f_31: int
                            f_32: _containers.RepeatedScalarFieldContainer[int]
                            f_33: str
                            f_34: Message8.M2.M11.M23.M26.M38.M48.E26
                            f_35: int
                            f_36: Message8.M2.M11.M23.M26.M38.M48.E27
                            f_37: int
                            f_38: int
                            f_39: Message8.M2.M11.M23.M26.M38.M48.E28
                            f_40: int
                            f_41: float
                            f_42: str
                            f_43: str
                            f_44: _containers.RepeatedScalarFieldContainer[int]
                            f_45: Message8.M2.M11.M23.M26.M38.M48.E29
                            f_46: int
                            f_62: Message8.M2.M11.M23.M26.M38.M48.M53
                            f_64: Message8.M2.M11.M23.M26.M38.M48.M54
                            f_66: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38.M48.M55]
                            f_68: Message8.M2.M11.M23.M26.M38.M48.M56
                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[_Iterable[int]] = ..., f_3: _Optional[str] = ..., f_4: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E22, str]] = ..., f_5: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.E23, str]]] = ..., f_6: _Optional[int] = ..., f_7: _Optional[int] = ..., f_8: _Optional[bytes] = ..., f_9: _Optional[str] = ..., f_10: _Optional[float] = ..., f_11: _Optional[int] = ..., f_12: _Optional[bytes] = ..., f_13: _Optional[str] = ..., f_14: _Optional[bytes] = ..., f_15: _Optional[int] = ..., f_16: _Optional[int] = ..., f_17: _Optional[float] = ..., f_18: _Optional[int] = ..., f_19: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E24, str]] = ..., f_20: _Optional[int] = ..., f_21: _Optional[int] = ..., f_22: _Optional[float] = ..., f_23: _Optional[str] = ..., f_24: _Optional[str] = ..., f_25: _Optional[_Iterable[int]] = ..., f_26: _Optional[int] = ..., f_27: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E25, str]] = ..., f_28: _Optional[float] = ..., f_29: _Optional[bytes] = ..., f_30: _Optional[str] = ..., f_31: _Optional[int] = ..., f_32: _Optional[_Iterable[int]] = ..., f_33: _Optional[str] = ..., f_34: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E26, str]] = ..., f_35: _Optional[int] = ..., f_36: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E27, str]] = ..., f_37: _Optional[int] = ..., f_38: _Optional[int] = ..., f_39: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E28, str]] = ..., f_40: _Optional[int] = ..., f_41: _Optional[float] = ..., f_42: _Optional[str] = ..., f_43: _Optional[str] = ..., f_44: _Optional[_Iterable[int]] = ..., f_45: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.E29, str]] = ..., f_46: _Optional[int] = ..., f_62: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M53, _Mapping]] = ..., f_64: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M54, _Mapping]] = ..., f_66: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38.M48.M55, _Mapping]]] = ..., f_68: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48.M56, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        f_2: Message8.M2.M11.M23.M26.M38.M48
                        def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message8.M2.M11.M23.M26.M38.M48, _Mapping]] = ...) -> None: ...
                    class M39(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_2: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M38]
                    f_3: _containers.RepeatedCompositeFieldContainer[Message8.M2.M11.M23.M26.M39]
                    def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M38, _Mapping]]] = ..., f_3: _Optional[_Iterable[_Union[Message8.M2.M11.M23.M26.M39, _Mapping]]] = ...) -> None: ...
                class M27(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_1_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_7_FIELD_NUMBER: _ClassVar[int]
                F_8_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_1: int
                f_2: int
                f_3: int
                f_7: Message8.M2.M11.M23.M26
                f_8: Message8.M2.M11.M23.M27
                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_7: _Optional[_Union[Message8.M2.M11.M23.M26, _Mapping]] = ..., f_8: _Optional[_Union[Message8.M2.M11.M23.M27, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_1_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_4_FIELD_NUMBER: _ClassVar[int]
            f_0: Message8.M2.M11.E4
            f_1: int
            f_3: Message8.M2.M11.M13
            f_4: Message8.M2.M11.M23
            def __init__(self, f_0: _Optional[_Union[Message8.M2.M11.E4, str]] = ..., f_1: _Optional[int] = ..., f_3: _Optional[_Union[Message8.M2.M11.M13, _Mapping]] = ..., f_4: _Optional[_Union[Message8.M2.M11.M23, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_2: Message8.M2.M6
        f_4: Message8.M2.M11
        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message8.M2.M6, _Mapping]] = ..., f_4: _Optional[_Union[Message8.M2.M11, _Mapping]] = ...) -> None: ...
    class M3(_message.Message):
        __slots__ = ("f_0", "f_3", "f_6", "f_7")
        class M8(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
        class M9(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
        class M10(_message.Message):
            __slots__ = ("f_0", "f_3", "f_5", "f_8")
            class M18(_message.Message):
                __slots__ = ("f_0", "f_3", "f_4")
                class M29(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    F_7_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: int
                    f_2: str
                    f_3: int
                    f_4: bool
                    f_5: float
                    f_6: int
                    f_7: bool
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[str] = ..., f_3: _Optional[int] = ..., f_4: _Optional[bool] = ..., f_5: _Optional[float] = ..., f_6: _Optional[int] = ..., f_7: _Optional[bool] = ...) -> None: ...
                class M35(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_3: Message8.M3.M10.M18.M29
                f_4: Message8.M3.M10.M18.M35
                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message8.M3.M10.M18.M29, _Mapping]] = ..., f_4: _Optional[_Union[Message8.M3.M10.M18.M35, _Mapping]] = ...) -> None: ...
            class M20(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
            class M22(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7")
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_1_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                F_6_FIELD_NUMBER: _ClassVar[int]
                F_7_FIELD_NUMBER: _ClassVar[int]
                f_0: float
                f_1: int
                f_2: str
                f_3: str
                f_4: float
                f_5: int
                f_6: str
                f_7: int
                def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_2: _Optional[str] = ..., f_3: _Optional[str] = ..., f_4: _Optional[float] = ..., f_5: _Optional[int] = ..., f_6: _Optional[str] = ..., f_7: _Optional[int] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_5_FIELD_NUMBER: _ClassVar[int]
            F_8_FIELD_NUMBER: _ClassVar[int]
            f_0: bool
            f_3: Message8.M3.M10.M18
            f_5: Message8.M3.M10.M20
            f_8: Message8.M3.M10.M22
            def __init__(self, f_0: _Optional[bool] = ..., f_3: _Optional[_Union[Message8.M3.M10.M18, _Mapping]] = ..., f_5: _Optional[_Union[Message8.M3.M10.M20, _Mapping]] = ..., f_8: _Optional[_Union[Message8.M3.M10.M22, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_6_FIELD_NUMBER: _ClassVar[int]
        F_7_FIELD_NUMBER: _ClassVar[int]
        f_0: str
        f_3: Message8.M3.M8
        f_6: Message8.M3.M9
        f_7: _containers.RepeatedCompositeFieldContainer[Message8.M3.M10]
        def __init__(self, f_0: _Optional[str] = ..., f_3: _Optional[_Union[Message8.M3.M8, _Mapping]] = ..., f_6: _Optional[_Union[Message8.M3.M9, _Mapping]] = ..., f_7: _Optional[_Iterable[_Union[Message8.M3.M10, _Mapping]]] = ...) -> None: ...
    class M4(_message.Message):
        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_9", "f_10")
        class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E3_UNSPECIFIED: _ClassVar[Message8.M4.E3]
            E3_CONST_1: _ClassVar[Message8.M4.E3]
            E3_CONST_2: _ClassVar[Message8.M4.E3]
            E3_CONST_3: _ClassVar[Message8.M4.E3]
            E3_CONST_4: _ClassVar[Message8.M4.E3]
            E3_CONST_5: _ClassVar[Message8.M4.E3]
        E3_UNSPECIFIED: Message8.M4.E3
        E3_CONST_1: Message8.M4.E3
        E3_CONST_2: Message8.M4.E3
        E3_CONST_3: Message8.M4.E3
        E3_CONST_4: Message8.M4.E3
        E3_CONST_5: Message8.M4.E3
        class M7(_message.Message):
            __slots__ = ("f_0", "f_3")
            class M14(_message.Message):
                __slots__ = ("f_0", "f_5", "f_8")
                class M32(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_4", "f_5")
                    class M40(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: _containers.RepeatedScalarFieldContainer[int]
                        def __init__(self, f_0: _Optional[_Iterable[int]] = ...) -> None: ...
                    class M46(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5")
                        class E20(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E20_UNSPECIFIED: _ClassVar[Message8.M4.M7.M14.M32.M46.E20]
                            E20_CONST_1: _ClassVar[Message8.M4.M7.M14.M32.M46.E20]
                            E20_CONST_2: _ClassVar[Message8.M4.M7.M14.M32.M46.E20]
                            E20_CONST_3: _ClassVar[Message8.M4.M7.M14.M32.M46.E20]
                            E20_CONST_4: _ClassVar[Message8.M4.M7.M14.M32.M46.E20]
                            E20_CONST_5: _ClassVar[Message8.M4.M7.M14.M32.M46.E20]
                        E20_UNSPECIFIED: Message8.M4.M7.M14.M32.M46.E20
                        E20_CONST_1: Message8.M4.M7.M14.M32.M46.E20
                        E20_CONST_2: Message8.M4.M7.M14.M32.M46.E20
                        E20_CONST_3: Message8.M4.M7.M14.M32.M46.E20
                        E20_CONST_4: Message8.M4.M7.M14.M32.M46.E20
                        E20_CONST_5: Message8.M4.M7.M14.M32.M46.E20
                        class E21(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E21_UNSPECIFIED: _ClassVar[Message8.M4.M7.M14.M32.M46.E21]
                            E21_CONST_1: _ClassVar[Message8.M4.M7.M14.M32.M46.E21]
                            E21_CONST_2: _ClassVar[Message8.M4.M7.M14.M32.M46.E21]
                            E21_CONST_3: _ClassVar[Message8.M4.M7.M14.M32.M46.E21]
                            E21_CONST_4: _ClassVar[Message8.M4.M7.M14.M32.M46.E21]
                            E21_CONST_5: _ClassVar[Message8.M4.M7.M14.M32.M46.E21]
                        E21_UNSPECIFIED: Message8.M4.M7.M14.M32.M46.E21
                        E21_CONST_1: Message8.M4.M7.M14.M32.M46.E21
                        E21_CONST_2: Message8.M4.M7.M14.M32.M46.E21
                        E21_CONST_3: Message8.M4.M7.M14.M32.M46.E21
                        E21_CONST_4: Message8.M4.M7.M14.M32.M46.E21
                        E21_CONST_5: Message8.M4.M7.M14.M32.M46.E21
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message8.M4.M7.M14.M32.M46.E20
                        f_1: str
                        f_2: int
                        f_3: float
                        f_4: Message8.M4.M7.M14.M32.M46.E21
                        f_5: _containers.RepeatedScalarFieldContainer[int]
                        def __init__(self, f_0: _Optional[_Union[Message8.M4.M7.M14.M32.M46.E20, str]] = ..., f_1: _Optional[str] = ..., f_2: _Optional[int] = ..., f_3: _Optional[float] = ..., f_4: _Optional[_Union[Message8.M4.M7.M14.M32.M46.E21, str]] = ..., f_5: _Optional[_Iterable[int]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_1: str
                    f_4: Message8.M4.M7.M14.M32.M40
                    f_5: Message8.M4.M7.M14.M32.M46
                    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[str] = ..., f_4: _Optional[_Union[Message8.M4.M7.M14.M32.M40, _Mapping]] = ..., f_5: _Optional[_Union[Message8.M4.M7.M14.M32.M46, _Mapping]] = ...) -> None: ...
                class M33(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                F_8_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_5: Message8.M4.M7.M14.M32
                f_8: _containers.RepeatedCompositeFieldContainer[Message8.M4.M7.M14.M33]
                def __init__(self, f_0: _Optional[int] = ..., f_5: _Optional[_Union[Message8.M4.M7.M14.M32, _Mapping]] = ..., f_8: _Optional[_Iterable[_Union[Message8.M4.M7.M14.M33, _Mapping]]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_3: Message8.M4.M7.M14
            def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message8.M4.M7.M14, _Mapping]] = ...) -> None: ...
        class M12(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_31", "f_32", "f_33", "f_34", "f_35", "f_36", "f_37", "f_38", "f_39", "f_40", "f_41", "f_42", "f_43", "f_44", "f_45", "f_46", "f_47", "f_48", "f_49", "f_50", "f_51", "f_52", "f_53", "f_54", "f_55", "f_56", "f_57", "f_58", "f_59", "f_60", "f_61", "f_62", "f_63", "f_64", "f_65", "f_66", "f_67", "f_68", "f_69", "f_93", "f_95")
            class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E5_UNSPECIFIED: _ClassVar[Message8.M4.M12.E5]
                E5_CONST_1: _ClassVar[Message8.M4.M12.E5]
                E5_CONST_2: _ClassVar[Message8.M4.M12.E5]
                E5_CONST_3: _ClassVar[Message8.M4.M12.E5]
                E5_CONST_4: _ClassVar[Message8.M4.M12.E5]
                E5_CONST_5: _ClassVar[Message8.M4.M12.E5]
            E5_UNSPECIFIED: Message8.M4.M12.E5
            E5_CONST_1: Message8.M4.M12.E5
            E5_CONST_2: Message8.M4.M12.E5
            E5_CONST_3: Message8.M4.M12.E5
            E5_CONST_4: Message8.M4.M12.E5
            E5_CONST_5: Message8.M4.M12.E5
            class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E6_UNSPECIFIED: _ClassVar[Message8.M4.M12.E6]
                E6_CONST_1: _ClassVar[Message8.M4.M12.E6]
                E6_CONST_2: _ClassVar[Message8.M4.M12.E6]
                E6_CONST_3: _ClassVar[Message8.M4.M12.E6]
                E6_CONST_4: _ClassVar[Message8.M4.M12.E6]
                E6_CONST_5: _ClassVar[Message8.M4.M12.E6]
            E6_UNSPECIFIED: Message8.M4.M12.E6
            E6_CONST_1: Message8.M4.M12.E6
            E6_CONST_2: Message8.M4.M12.E6
            E6_CONST_3: Message8.M4.M12.E6
            E6_CONST_4: Message8.M4.M12.E6
            E6_CONST_5: Message8.M4.M12.E6
            class E7(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E7_UNSPECIFIED: _ClassVar[Message8.M4.M12.E7]
                E7_CONST_1: _ClassVar[Message8.M4.M12.E7]
                E7_CONST_2: _ClassVar[Message8.M4.M12.E7]
                E7_CONST_3: _ClassVar[Message8.M4.M12.E7]
                E7_CONST_4: _ClassVar[Message8.M4.M12.E7]
                E7_CONST_5: _ClassVar[Message8.M4.M12.E7]
            E7_UNSPECIFIED: Message8.M4.M12.E7
            E7_CONST_1: Message8.M4.M12.E7
            E7_CONST_2: Message8.M4.M12.E7
            E7_CONST_3: Message8.M4.M12.E7
            E7_CONST_4: Message8.M4.M12.E7
            E7_CONST_5: Message8.M4.M12.E7
            class E8(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E8_UNSPECIFIED: _ClassVar[Message8.M4.M12.E8]
                E8_CONST_1: _ClassVar[Message8.M4.M12.E8]
                E8_CONST_2: _ClassVar[Message8.M4.M12.E8]
                E8_CONST_3: _ClassVar[Message8.M4.M12.E8]
                E8_CONST_4: _ClassVar[Message8.M4.M12.E8]
                E8_CONST_5: _ClassVar[Message8.M4.M12.E8]
            E8_UNSPECIFIED: Message8.M4.M12.E8
            E8_CONST_1: Message8.M4.M12.E8
            E8_CONST_2: Message8.M4.M12.E8
            E8_CONST_3: Message8.M4.M12.E8
            E8_CONST_4: Message8.M4.M12.E8
            E8_CONST_5: Message8.M4.M12.E8
            class E9(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E9_UNSPECIFIED: _ClassVar[Message8.M4.M12.E9]
                E9_CONST_1: _ClassVar[Message8.M4.M12.E9]
                E9_CONST_2: _ClassVar[Message8.M4.M12.E9]
                E9_CONST_3: _ClassVar[Message8.M4.M12.E9]
                E9_CONST_4: _ClassVar[Message8.M4.M12.E9]
                E9_CONST_5: _ClassVar[Message8.M4.M12.E9]
            E9_UNSPECIFIED: Message8.M4.M12.E9
            E9_CONST_1: Message8.M4.M12.E9
            E9_CONST_2: Message8.M4.M12.E9
            E9_CONST_3: Message8.M4.M12.E9
            E9_CONST_4: Message8.M4.M12.E9
            E9_CONST_5: Message8.M4.M12.E9
            class E10(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E10_UNSPECIFIED: _ClassVar[Message8.M4.M12.E10]
                E10_CONST_1: _ClassVar[Message8.M4.M12.E10]
                E10_CONST_2: _ClassVar[Message8.M4.M12.E10]
                E10_CONST_3: _ClassVar[Message8.M4.M12.E10]
                E10_CONST_4: _ClassVar[Message8.M4.M12.E10]
                E10_CONST_5: _ClassVar[Message8.M4.M12.E10]
            E10_UNSPECIFIED: Message8.M4.M12.E10
            E10_CONST_1: Message8.M4.M12.E10
            E10_CONST_2: Message8.M4.M12.E10
            E10_CONST_3: Message8.M4.M12.E10
            E10_CONST_4: Message8.M4.M12.E10
            E10_CONST_5: Message8.M4.M12.E10
            class E11(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E11_UNSPECIFIED: _ClassVar[Message8.M4.M12.E11]
                E11_CONST_1: _ClassVar[Message8.M4.M12.E11]
                E11_CONST_2: _ClassVar[Message8.M4.M12.E11]
                E11_CONST_3: _ClassVar[Message8.M4.M12.E11]
                E11_CONST_4: _ClassVar[Message8.M4.M12.E11]
                E11_CONST_5: _ClassVar[Message8.M4.M12.E11]
            E11_UNSPECIFIED: Message8.M4.M12.E11
            E11_CONST_1: Message8.M4.M12.E11
            E11_CONST_2: Message8.M4.M12.E11
            E11_CONST_3: Message8.M4.M12.E11
            E11_CONST_4: Message8.M4.M12.E11
            E11_CONST_5: Message8.M4.M12.E11
            class E12(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E12_UNSPECIFIED: _ClassVar[Message8.M4.M12.E12]
                E12_CONST_1: _ClassVar[Message8.M4.M12.E12]
                E12_CONST_2: _ClassVar[Message8.M4.M12.E12]
                E12_CONST_3: _ClassVar[Message8.M4.M12.E12]
                E12_CONST_4: _ClassVar[Message8.M4.M12.E12]
                E12_CONST_5: _ClassVar[Message8.M4.M12.E12]
            E12_UNSPECIFIED: Message8.M4.M12.E12
            E12_CONST_1: Message8.M4.M12.E12
            E12_CONST_2: Message8.M4.M12.E12
            E12_CONST_3: Message8.M4.M12.E12
            E12_CONST_4: Message8.M4.M12.E12
            E12_CONST_5: Message8.M4.M12.E12
            class M15(_message.Message):
                __slots__ = ("f_0", "f_2")
                class M28(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_5", "f_7", "f_8")
                    class M41(_message.Message):
                        __slots__ = ("f_0",)
                        class E17(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E17_UNSPECIFIED: _ClassVar[Message8.M4.M12.M15.M28.M41.E17]
                            E17_CONST_1: _ClassVar[Message8.M4.M12.M15.M28.M41.E17]
                            E17_CONST_2: _ClassVar[Message8.M4.M12.M15.M28.M41.E17]
                            E17_CONST_3: _ClassVar[Message8.M4.M12.M15.M28.M41.E17]
                            E17_CONST_4: _ClassVar[Message8.M4.M12.M15.M28.M41.E17]
                            E17_CONST_5: _ClassVar[Message8.M4.M12.M15.M28.M41.E17]
                        E17_UNSPECIFIED: Message8.M4.M12.M15.M28.M41.E17
                        E17_CONST_1: Message8.M4.M12.M15.M28.M41.E17
                        E17_CONST_2: Message8.M4.M12.M15.M28.M41.E17
                        E17_CONST_3: Message8.M4.M12.M15.M28.M41.E17
                        E17_CONST_4: Message8.M4.M12.M15.M28.M41.E17
                        E17_CONST_5: Message8.M4.M12.M15.M28.M41.E17
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message8.M4.M12.M15.M28.M41.E17
                        def __init__(self, f_0: _Optional[_Union[Message8.M4.M12.M15.M28.M41.E17, str]] = ...) -> None: ...
                    class M43(_message.Message):
                        __slots__ = ("f_0",)
                        class E18(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E18_UNSPECIFIED: _ClassVar[Message8.M4.M12.M15.M28.M43.E18]
                            E18_CONST_1: _ClassVar[Message8.M4.M12.M15.M28.M43.E18]
                            E18_CONST_2: _ClassVar[Message8.M4.M12.M15.M28.M43.E18]
                            E18_CONST_3: _ClassVar[Message8.M4.M12.M15.M28.M43.E18]
                            E18_CONST_4: _ClassVar[Message8.M4.M12.M15.M28.M43.E18]
                            E18_CONST_5: _ClassVar[Message8.M4.M12.M15.M28.M43.E18]
                        E18_UNSPECIFIED: Message8.M4.M12.M15.M28.M43.E18
                        E18_CONST_1: Message8.M4.M12.M15.M28.M43.E18
                        E18_CONST_2: Message8.M4.M12.M15.M28.M43.E18
                        E18_CONST_3: Message8.M4.M12.M15.M28.M43.E18
                        E18_CONST_4: Message8.M4.M12.M15.M28.M43.E18
                        E18_CONST_5: Message8.M4.M12.M15.M28.M43.E18
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message8.M4.M12.M15.M28.M43.E18
                        def __init__(self, f_0: _Optional[_Union[Message8.M4.M12.M15.M28.M43.E18, str]] = ...) -> None: ...
                    class M45(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4")
                        class E19(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E19_UNSPECIFIED: _ClassVar[Message8.M4.M12.M15.M28.M45.E19]
                            E19_CONST_1: _ClassVar[Message8.M4.M12.M15.M28.M45.E19]
                            E19_CONST_2: _ClassVar[Message8.M4.M12.M15.M28.M45.E19]
                            E19_CONST_3: _ClassVar[Message8.M4.M12.M15.M28.M45.E19]
                            E19_CONST_4: _ClassVar[Message8.M4.M12.M15.M28.M45.E19]
                            E19_CONST_5: _ClassVar[Message8.M4.M12.M15.M28.M45.E19]
                        E19_UNSPECIFIED: Message8.M4.M12.M15.M28.M45.E19
                        E19_CONST_1: Message8.M4.M12.M15.M28.M45.E19
                        E19_CONST_2: Message8.M4.M12.M15.M28.M45.E19
                        E19_CONST_3: Message8.M4.M12.M15.M28.M45.E19
                        E19_CONST_4: Message8.M4.M12.M15.M28.M45.E19
                        E19_CONST_5: Message8.M4.M12.M15.M28.M45.E19
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        f_1: int
                        f_2: bool
                        f_3: Message8.M4.M12.M15.M28.M45.E19
                        f_4: int
                        def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[int] = ..., f_2: _Optional[bool] = ..., f_3: _Optional[_Union[Message8.M4.M12.M15.M28.M45.E19, str]] = ..., f_4: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    F_7_FIELD_NUMBER: _ClassVar[int]
                    F_8_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_1: int
                    f_5: _containers.RepeatedCompositeFieldContainer[Message8.M4.M12.M15.M28.M41]
                    f_7: _containers.RepeatedCompositeFieldContainer[Message8.M4.M12.M15.M28.M43]
                    f_8: Message8.M4.M12.M15.M28.M45
                    def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_5: _Optional[_Iterable[_Union[Message8.M4.M12.M15.M28.M41, _Mapping]]] = ..., f_7: _Optional[_Iterable[_Union[Message8.M4.M12.M15.M28.M43, _Mapping]]] = ..., f_8: _Optional[_Union[Message8.M4.M12.M15.M28.M45, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                f_0: float
                f_2: Message8.M4.M12.M15.M28
                def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message8.M4.M12.M15.M28, _Mapping]] = ...) -> None: ...
            class M19(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
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
            F_93_FIELD_NUMBER: _ClassVar[int]
            F_95_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            f_1: int
            f_2: float
            f_3: int
            f_4: _containers.RepeatedScalarFieldContainer[int]
            f_5: float
            f_6: str
            f_7: int
            f_8: int
            f_9: float
            f_10: int
            f_11: int
            f_12: int
            f_13: str
            f_14: Message8.M4.M12.E5
            f_15: _containers.RepeatedScalarFieldContainer[int]
            f_16: int
            f_17: Message8.M4.M12.E6
            f_18: _containers.RepeatedScalarFieldContainer[str]
            f_19: int
            f_20: int
            f_21: str
            f_22: _containers.RepeatedScalarFieldContainer[Message8.M4.M12.E7]
            f_23: int
            f_24: int
            f_25: int
            f_26: float
            f_27: int
            f_28: int
            f_29: _containers.RepeatedScalarFieldContainer[int]
            f_30: int
            f_31: str
            f_32: float
            f_33: float
            f_34: bool
            f_35: int
            f_36: int
            f_37: int
            f_38: float
            f_39: int
            f_40: str
            f_41: int
            f_42: int
            f_43: _containers.RepeatedScalarFieldContainer[str]
            f_44: int
            f_45: Message8.M4.M12.E8
            f_46: Message8.M4.M12.E9
            f_47: float
            f_48: float
            f_49: int
            f_50: Message8.M4.M12.E10
            f_51: int
            f_52: Message8.M4.M12.E11
            f_53: int
            f_54: float
            f_55: _containers.RepeatedScalarFieldContainer[int]
            f_56: bool
            f_57: str
            f_58: int
            f_59: int
            f_60: str
            f_61: int
            f_62: int
            f_63: int
            f_64: _containers.RepeatedScalarFieldContainer[int]
            f_65: bytes
            f_66: float
            f_67: float
            f_68: Message8.M4.M12.E12
            f_69: int
            f_93: Message8.M4.M12.M15
            f_95: Message8.M4.M12.M19
            def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[float] = ..., f_3: _Optional[int] = ..., f_4: _Optional[_Iterable[int]] = ..., f_5: _Optional[float] = ..., f_6: _Optional[str] = ..., f_7: _Optional[int] = ..., f_8: _Optional[int] = ..., f_9: _Optional[float] = ..., f_10: _Optional[int] = ..., f_11: _Optional[int] = ..., f_12: _Optional[int] = ..., f_13: _Optional[str] = ..., f_14: _Optional[_Union[Message8.M4.M12.E5, str]] = ..., f_15: _Optional[_Iterable[int]] = ..., f_16: _Optional[int] = ..., f_17: _Optional[_Union[Message8.M4.M12.E6, str]] = ..., f_18: _Optional[_Iterable[str]] = ..., f_19: _Optional[int] = ..., f_20: _Optional[int] = ..., f_21: _Optional[str] = ..., f_22: _Optional[_Iterable[_Union[Message8.M4.M12.E7, str]]] = ..., f_23: _Optional[int] = ..., f_24: _Optional[int] = ..., f_25: _Optional[int] = ..., f_26: _Optional[float] = ..., f_27: _Optional[int] = ..., f_28: _Optional[int] = ..., f_29: _Optional[_Iterable[int]] = ..., f_30: _Optional[int] = ..., f_31: _Optional[str] = ..., f_32: _Optional[float] = ..., f_33: _Optional[float] = ..., f_34: _Optional[bool] = ..., f_35: _Optional[int] = ..., f_36: _Optional[int] = ..., f_37: _Optional[int] = ..., f_38: _Optional[float] = ..., f_39: _Optional[int] = ..., f_40: _Optional[str] = ..., f_41: _Optional[int] = ..., f_42: _Optional[int] = ..., f_43: _Optional[_Iterable[str]] = ..., f_44: _Optional[int] = ..., f_45: _Optional[_Union[Message8.M4.M12.E8, str]] = ..., f_46: _Optional[_Union[Message8.M4.M12.E9, str]] = ..., f_47: _Optional[float] = ..., f_48: _Optional[float] = ..., f_49: _Optional[int] = ..., f_50: _Optional[_Union[Message8.M4.M12.E10, str]] = ..., f_51: _Optional[int] = ..., f_52: _Optional[_Union[Message8.M4.M12.E11, str]] = ..., f_53: _Optional[int] = ..., f_54: _Optional[float] = ..., f_55: _Optional[_Iterable[int]] = ..., f_56: _Optional[bool] = ..., f_57: _Optional[str] = ..., f_58: _Optional[int] = ..., f_59: _Optional[int] = ..., f_60: _Optional[str] = ..., f_61: _Optional[int] = ..., f_62: _Optional[int] = ..., f_63: _Optional[int] = ..., f_64: _Optional[_Iterable[int]] = ..., f_65: _Optional[bytes] = ..., f_66: _Optional[float] = ..., f_67: _Optional[float] = ..., f_68: _Optional[_Union[Message8.M4.M12.E12, str]] = ..., f_69: _Optional[int] = ..., f_93: _Optional[_Union[Message8.M4.M12.M15, _Mapping]] = ..., f_95: _Optional[_Union[Message8.M4.M12.M19, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_1_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        F_5_FIELD_NUMBER: _ClassVar[int]
        F_9_FIELD_NUMBER: _ClassVar[int]
        F_10_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_1: int
        f_2: int
        f_3: Message8.M4.E3
        f_4: float
        f_5: _containers.RepeatedScalarFieldContainer[str]
        f_9: _containers.RepeatedCompositeFieldContainer[Message8.M4.M7]
        f_10: _containers.RepeatedCompositeFieldContainer[Message8.M4.M12]
        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[_Union[Message8.M4.E3, str]] = ..., f_4: _Optional[float] = ..., f_5: _Optional[_Iterable[str]] = ..., f_9: _Optional[_Iterable[_Union[Message8.M4.M7, _Mapping]]] = ..., f_10: _Optional[_Iterable[_Union[Message8.M4.M12, _Mapping]]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_2_FIELD_NUMBER: _ClassVar[int]
    F_4_FIELD_NUMBER: _ClassVar[int]
    F_5_FIELD_NUMBER: _ClassVar[int]
    F_6_FIELD_NUMBER: _ClassVar[int]
    f_0: Message8.E1
    f_2: Message8.M1
    f_4: Message8.M2
    f_5: Message8.M3
    f_6: _containers.RepeatedCompositeFieldContainer[Message8.M4]
    def __init__(self, f_0: _Optional[_Union[Message8.E1, str]] = ..., f_2: _Optional[_Union[Message8.M1, _Mapping]] = ..., f_4: _Optional[_Union[Message8.M2, _Mapping]] = ..., f_5: _Optional[_Union[Message8.M3, _Mapping]] = ..., f_6: _Optional[_Iterable[_Union[Message8.M4, _Mapping]]] = ...) -> None: ...
