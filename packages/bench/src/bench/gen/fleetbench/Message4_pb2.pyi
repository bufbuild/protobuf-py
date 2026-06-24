from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message4(_message.Message):
    __slots__ = ("f_0", "f_2")
    class M1(_message.Message):
        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_6", "f_7", "f_9")
        class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E1_UNSPECIFIED: _ClassVar[Message4.M1.E1]
            E1_CONST_1: _ClassVar[Message4.M1.E1]
            E1_CONST_2: _ClassVar[Message4.M1.E1]
            E1_CONST_3: _ClassVar[Message4.M1.E1]
            E1_CONST_4: _ClassVar[Message4.M1.E1]
            E1_CONST_5: _ClassVar[Message4.M1.E1]
        E1_UNSPECIFIED: Message4.M1.E1
        E1_CONST_1: Message4.M1.E1
        E1_CONST_2: Message4.M1.E1
        E1_CONST_3: Message4.M1.E1
        E1_CONST_4: Message4.M1.E1
        E1_CONST_5: Message4.M1.E1
        class M2(_message.Message):
            __slots__ = ("f_0", "f_3", "f_4")
            class M5(_message.Message):
                __slots__ = ("f_0", "f_3", "f_4")
                class M20(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: bytes
                    def __init__(self, f_0: _Optional[bytes] = ...) -> None: ...
                class M24(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_4")
                    class M35(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: _containers.RepeatedScalarFieldContainer[str]
                        def __init__(self, f_0: _Optional[_Iterable[str]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_1: int
                    f_4: Message4.M1.M2.M5.M24.M35
                    def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_4: _Optional[_Union[Message4.M1.M2.M5.M24.M35, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                f_0: bytes
                f_3: Message4.M1.M2.M5.M20
                f_4: Message4.M1.M2.M5.M24
                def __init__(self, f_0: _Optional[bytes] = ..., f_3: _Optional[_Union[Message4.M1.M2.M5.M20, _Mapping]] = ..., f_4: _Optional[_Union[Message4.M1.M2.M5.M24, _Mapping]] = ...) -> None: ...
            class M12(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_5")
                class E14(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E14_UNSPECIFIED: _ClassVar[Message4.M1.M2.M12.E14]
                    E14_CONST_1: _ClassVar[Message4.M1.M2.M12.E14]
                    E14_CONST_2: _ClassVar[Message4.M1.M2.M12.E14]
                    E14_CONST_3: _ClassVar[Message4.M1.M2.M12.E14]
                    E14_CONST_4: _ClassVar[Message4.M1.M2.M12.E14]
                    E14_CONST_5: _ClassVar[Message4.M1.M2.M12.E14]
                E14_UNSPECIFIED: Message4.M1.M2.M12.E14
                E14_CONST_1: Message4.M1.M2.M12.E14
                E14_CONST_2: Message4.M1.M2.M12.E14
                E14_CONST_3: Message4.M1.M2.M12.E14
                E14_CONST_4: Message4.M1.M2.M12.E14
                E14_CONST_5: Message4.M1.M2.M12.E14
                class M18(_message.Message):
                    __slots__ = ("f_0", "f_3")
                    class M28(_message.Message):
                        __slots__ = ("f_0",)
                        class E18(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E18_UNSPECIFIED: _ClassVar[Message4.M1.M2.M12.M18.M28.E18]
                            E18_CONST_1: _ClassVar[Message4.M1.M2.M12.M18.M28.E18]
                            E18_CONST_2: _ClassVar[Message4.M1.M2.M12.M18.M28.E18]
                            E18_CONST_3: _ClassVar[Message4.M1.M2.M12.M18.M28.E18]
                            E18_CONST_4: _ClassVar[Message4.M1.M2.M12.M18.M28.E18]
                            E18_CONST_5: _ClassVar[Message4.M1.M2.M12.M18.M28.E18]
                        E18_UNSPECIFIED: Message4.M1.M2.M12.M18.M28.E18
                        E18_CONST_1: Message4.M1.M2.M12.M18.M28.E18
                        E18_CONST_2: Message4.M1.M2.M12.M18.M28.E18
                        E18_CONST_3: Message4.M1.M2.M12.M18.M28.E18
                        E18_CONST_4: Message4.M1.M2.M12.M18.M28.E18
                        E18_CONST_5: Message4.M1.M2.M12.M18.M28.E18
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message4.M1.M2.M12.M18.M28.E18
                        def __init__(self, f_0: _Optional[_Union[Message4.M1.M2.M12.M18.M28.E18, str]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_3: Message4.M1.M2.M12.M18.M28
                    def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message4.M1.M2.M12.M18.M28, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_1_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_1: float
                f_2: Message4.M1.M2.M12.E14
                f_5: Message4.M1.M2.M12.M18
                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[float] = ..., f_2: _Optional[_Union[Message4.M1.M2.M12.E14, str]] = ..., f_5: _Optional[_Union[Message4.M1.M2.M12.M18, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_4_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_3: _containers.RepeatedCompositeFieldContainer[Message4.M1.M2.M5]
            f_4: _containers.RepeatedCompositeFieldContainer[Message4.M1.M2.M12]
            def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.M2.M5, _Mapping]]] = ..., f_4: _Optional[_Iterable[_Union[Message4.M1.M2.M12, _Mapping]]] = ...) -> None: ...
        class M3(_message.Message):
            __slots__ = ("f_0", "f_5")
            class M7(_message.Message):
                __slots__ = ("f_0", "f_2", "f_4", "f_5")
                class M17(_message.Message):
                    __slots__ = ("f_0",)
                    class E16(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E16_UNSPECIFIED: _ClassVar[Message4.M1.M3.M7.M17.E16]
                        E16_CONST_1: _ClassVar[Message4.M1.M3.M7.M17.E16]
                        E16_CONST_2: _ClassVar[Message4.M1.M3.M7.M17.E16]
                        E16_CONST_3: _ClassVar[Message4.M1.M3.M7.M17.E16]
                        E16_CONST_4: _ClassVar[Message4.M1.M3.M7.M17.E16]
                        E16_CONST_5: _ClassVar[Message4.M1.M3.M7.M17.E16]
                    E16_UNSPECIFIED: Message4.M1.M3.M7.M17.E16
                    E16_CONST_1: Message4.M1.M3.M7.M17.E16
                    E16_CONST_2: Message4.M1.M3.M7.M17.E16
                    E16_CONST_3: Message4.M1.M3.M7.M17.E16
                    E16_CONST_4: Message4.M1.M3.M7.M17.E16
                    E16_CONST_5: Message4.M1.M3.M7.M17.E16
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message4.M1.M3.M7.M17.E16
                    def __init__(self, f_0: _Optional[_Union[Message4.M1.M3.M7.M17.E16, str]] = ...) -> None: ...
                class M19(_message.Message):
                    __slots__ = ("f_0", "f_2", "f_3")
                    class M32(_message.Message):
                        __slots__ = ("f_0", "f_2", "f_4")
                        class E20(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E20_UNSPECIFIED: _ClassVar[Message4.M1.M3.M7.M19.M32.E20]
                            E20_CONST_1: _ClassVar[Message4.M1.M3.M7.M19.M32.E20]
                            E20_CONST_2: _ClassVar[Message4.M1.M3.M7.M19.M32.E20]
                            E20_CONST_3: _ClassVar[Message4.M1.M3.M7.M19.M32.E20]
                            E20_CONST_4: _ClassVar[Message4.M1.M3.M7.M19.M32.E20]
                            E20_CONST_5: _ClassVar[Message4.M1.M3.M7.M19.M32.E20]
                        E20_UNSPECIFIED: Message4.M1.M3.M7.M19.M32.E20
                        E20_CONST_1: Message4.M1.M3.M7.M19.M32.E20
                        E20_CONST_2: Message4.M1.M3.M7.M19.M32.E20
                        E20_CONST_3: Message4.M1.M3.M7.M19.M32.E20
                        E20_CONST_4: Message4.M1.M3.M7.M19.M32.E20
                        E20_CONST_5: Message4.M1.M3.M7.M19.M32.E20
                        class M38(_message.Message):
                            __slots__ = ("f_0",)
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                        class M40(_message.Message):
                            __slots__ = ("f_0", "f_2")
                            class M44(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_8")
                                class M45(_message.Message):
                                    __slots__ = ("f_0", "f_3")
                                    class M51(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: bool
                                    f_3: Message4.M1.M3.M7.M19.M32.M40.M44.M45.M51
                                    def __init__(self, f_0: _Optional[bool] = ..., f_3: _Optional[_Union[Message4.M1.M3.M7.M19.M32.M40.M44.M45.M51, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                F_4_FIELD_NUMBER: _ClassVar[int]
                                F_5_FIELD_NUMBER: _ClassVar[int]
                                F_8_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                f_1: float
                                f_2: str
                                f_3: float
                                f_4: str
                                f_5: str
                                f_8: Message4.M1.M3.M7.M19.M32.M40.M44.M45
                                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[float] = ..., f_2: _Optional[str] = ..., f_3: _Optional[float] = ..., f_4: _Optional[str] = ..., f_5: _Optional[str] = ..., f_8: _Optional[_Union[Message4.M1.M3.M7.M19.M32.M40.M44.M45, _Mapping]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: _containers.RepeatedScalarFieldContainer[bytes]
                            f_2: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M19.M32.M40.M44]
                            def __init__(self, f_0: _Optional[_Iterable[bytes]] = ..., f_2: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M19.M32.M40.M44, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message4.M1.M3.M7.M19.M32.E20
                        f_2: Message4.M1.M3.M7.M19.M32.M38
                        f_4: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M19.M32.M40]
                        def __init__(self, f_0: _Optional[_Union[Message4.M1.M3.M7.M19.M32.E20, str]] = ..., f_2: _Optional[_Union[Message4.M1.M3.M7.M19.M32.M38, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M19.M32.M40, _Mapping]]] = ...) -> None: ...
                    class M34(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M37(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4")
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            f_0: str
                            f_1: str
                            f_2: int
                            f_3: float
                            f_4: _containers.RepeatedScalarFieldContainer[int]
                            def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[str] = ..., f_2: _Optional[int] = ..., f_3: _Optional[float] = ..., f_4: _Optional[_Iterable[int]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        f_2: Message4.M1.M3.M7.M19.M34.M37
                        def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message4.M1.M3.M7.M19.M34.M37, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_2: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M19.M32]
                    f_3: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M19.M34]
                    def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M19.M32, _Mapping]]] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M19.M34, _Mapping]]] = ...) -> None: ...
                class M22(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M36(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6")
                        class E21(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E21_UNSPECIFIED: _ClassVar[Message4.M1.M3.M7.M22.M36.E21]
                            E21_CONST_1: _ClassVar[Message4.M1.M3.M7.M22.M36.E21]
                            E21_CONST_2: _ClassVar[Message4.M1.M3.M7.M22.M36.E21]
                            E21_CONST_3: _ClassVar[Message4.M1.M3.M7.M22.M36.E21]
                            E21_CONST_4: _ClassVar[Message4.M1.M3.M7.M22.M36.E21]
                            E21_CONST_5: _ClassVar[Message4.M1.M3.M7.M22.M36.E21]
                        E21_UNSPECIFIED: Message4.M1.M3.M7.M22.M36.E21
                        E21_CONST_1: Message4.M1.M3.M7.M22.M36.E21
                        E21_CONST_2: Message4.M1.M3.M7.M22.M36.E21
                        E21_CONST_3: Message4.M1.M3.M7.M22.M36.E21
                        E21_CONST_4: Message4.M1.M3.M7.M22.M36.E21
                        E21_CONST_5: Message4.M1.M3.M7.M22.M36.E21
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        F_6_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        f_1: _containers.RepeatedScalarFieldContainer[int]
                        f_2: int
                        f_3: float
                        f_4: Message4.M1.M3.M7.M22.M36.E21
                        f_5: float
                        f_6: int
                        def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[_Iterable[int]] = ..., f_2: _Optional[int] = ..., f_3: _Optional[float] = ..., f_4: _Optional[_Union[Message4.M1.M3.M7.M22.M36.E21, str]] = ..., f_5: _Optional[float] = ..., f_6: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_2: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M22.M36]
                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M22.M36, _Mapping]]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_2: Message4.M1.M3.M7.M17
                f_4: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M19]
                f_5: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7.M22]
                def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message4.M1.M3.M7.M17, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M19, _Mapping]]] = ..., f_5: _Optional[_Iterable[_Union[Message4.M1.M3.M7.M22, _Mapping]]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_5_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_5: _containers.RepeatedCompositeFieldContainer[Message4.M1.M3.M7]
            def __init__(self, f_0: _Optional[int] = ..., f_5: _Optional[_Iterable[_Union[Message4.M1.M3.M7, _Mapping]]] = ...) -> None: ...
        class M4(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_31", "f_32", "f_33", "f_34", "f_35", "f_36", "f_37", "f_38", "f_39", "f_40", "f_41", "f_42", "f_43", "f_44", "f_45", "f_46", "f_47", "f_48", "f_49", "f_50", "f_51", "f_52", "f_53", "f_54", "f_55", "f_56", "f_57", "f_58", "f_59", "f_60", "f_61", "f_62", "f_63", "f_64", "f_65", "f_66", "f_67", "f_68", "f_69", "f_70", "f_71", "f_72", "f_73", "f_74", "f_75", "f_76", "f_77", "f_78", "f_79", "f_80", "f_81", "f_82", "f_83", "f_84", "f_85", "f_86", "f_87", "f_88", "f_89", "f_90", "f_91", "f_92", "f_93", "f_94", "f_95", "f_96", "f_131", "f_133", "f_134", "f_135", "f_136", "f_138")
            class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E2_UNSPECIFIED: _ClassVar[Message4.M1.M4.E2]
                E2_CONST_1: _ClassVar[Message4.M1.M4.E2]
                E2_CONST_2: _ClassVar[Message4.M1.M4.E2]
                E2_CONST_3: _ClassVar[Message4.M1.M4.E2]
                E2_CONST_4: _ClassVar[Message4.M1.M4.E2]
                E2_CONST_5: _ClassVar[Message4.M1.M4.E2]
            E2_UNSPECIFIED: Message4.M1.M4.E2
            E2_CONST_1: Message4.M1.M4.E2
            E2_CONST_2: Message4.M1.M4.E2
            E2_CONST_3: Message4.M1.M4.E2
            E2_CONST_4: Message4.M1.M4.E2
            E2_CONST_5: Message4.M1.M4.E2
            class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E3_UNSPECIFIED: _ClassVar[Message4.M1.M4.E3]
                E3_CONST_1: _ClassVar[Message4.M1.M4.E3]
                E3_CONST_2: _ClassVar[Message4.M1.M4.E3]
                E3_CONST_3: _ClassVar[Message4.M1.M4.E3]
                E3_CONST_4: _ClassVar[Message4.M1.M4.E3]
                E3_CONST_5: _ClassVar[Message4.M1.M4.E3]
            E3_UNSPECIFIED: Message4.M1.M4.E3
            E3_CONST_1: Message4.M1.M4.E3
            E3_CONST_2: Message4.M1.M4.E3
            E3_CONST_3: Message4.M1.M4.E3
            E3_CONST_4: Message4.M1.M4.E3
            E3_CONST_5: Message4.M1.M4.E3
            class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E4_UNSPECIFIED: _ClassVar[Message4.M1.M4.E4]
                E4_CONST_1: _ClassVar[Message4.M1.M4.E4]
                E4_CONST_2: _ClassVar[Message4.M1.M4.E4]
                E4_CONST_3: _ClassVar[Message4.M1.M4.E4]
                E4_CONST_4: _ClassVar[Message4.M1.M4.E4]
                E4_CONST_5: _ClassVar[Message4.M1.M4.E4]
            E4_UNSPECIFIED: Message4.M1.M4.E4
            E4_CONST_1: Message4.M1.M4.E4
            E4_CONST_2: Message4.M1.M4.E4
            E4_CONST_3: Message4.M1.M4.E4
            E4_CONST_4: Message4.M1.M4.E4
            E4_CONST_5: Message4.M1.M4.E4
            class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E5_UNSPECIFIED: _ClassVar[Message4.M1.M4.E5]
                E5_CONST_1: _ClassVar[Message4.M1.M4.E5]
                E5_CONST_2: _ClassVar[Message4.M1.M4.E5]
                E5_CONST_3: _ClassVar[Message4.M1.M4.E5]
                E5_CONST_4: _ClassVar[Message4.M1.M4.E5]
                E5_CONST_5: _ClassVar[Message4.M1.M4.E5]
            E5_UNSPECIFIED: Message4.M1.M4.E5
            E5_CONST_1: Message4.M1.M4.E5
            E5_CONST_2: Message4.M1.M4.E5
            E5_CONST_3: Message4.M1.M4.E5
            E5_CONST_4: Message4.M1.M4.E5
            E5_CONST_5: Message4.M1.M4.E5
            class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E6_UNSPECIFIED: _ClassVar[Message4.M1.M4.E6]
                E6_CONST_1: _ClassVar[Message4.M1.M4.E6]
                E6_CONST_2: _ClassVar[Message4.M1.M4.E6]
                E6_CONST_3: _ClassVar[Message4.M1.M4.E6]
                E6_CONST_4: _ClassVar[Message4.M1.M4.E6]
                E6_CONST_5: _ClassVar[Message4.M1.M4.E6]
            E6_UNSPECIFIED: Message4.M1.M4.E6
            E6_CONST_1: Message4.M1.M4.E6
            E6_CONST_2: Message4.M1.M4.E6
            E6_CONST_3: Message4.M1.M4.E6
            E6_CONST_4: Message4.M1.M4.E6
            E6_CONST_5: Message4.M1.M4.E6
            class E7(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E7_UNSPECIFIED: _ClassVar[Message4.M1.M4.E7]
                E7_CONST_1: _ClassVar[Message4.M1.M4.E7]
                E7_CONST_2: _ClassVar[Message4.M1.M4.E7]
                E7_CONST_3: _ClassVar[Message4.M1.M4.E7]
                E7_CONST_4: _ClassVar[Message4.M1.M4.E7]
                E7_CONST_5: _ClassVar[Message4.M1.M4.E7]
            E7_UNSPECIFIED: Message4.M1.M4.E7
            E7_CONST_1: Message4.M1.M4.E7
            E7_CONST_2: Message4.M1.M4.E7
            E7_CONST_3: Message4.M1.M4.E7
            E7_CONST_4: Message4.M1.M4.E7
            E7_CONST_5: Message4.M1.M4.E7
            class E8(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E8_UNSPECIFIED: _ClassVar[Message4.M1.M4.E8]
                E8_CONST_1: _ClassVar[Message4.M1.M4.E8]
                E8_CONST_2: _ClassVar[Message4.M1.M4.E8]
                E8_CONST_3: _ClassVar[Message4.M1.M4.E8]
                E8_CONST_4: _ClassVar[Message4.M1.M4.E8]
                E8_CONST_5: _ClassVar[Message4.M1.M4.E8]
            E8_UNSPECIFIED: Message4.M1.M4.E8
            E8_CONST_1: Message4.M1.M4.E8
            E8_CONST_2: Message4.M1.M4.E8
            E8_CONST_3: Message4.M1.M4.E8
            E8_CONST_4: Message4.M1.M4.E8
            E8_CONST_5: Message4.M1.M4.E8
            class E9(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E9_UNSPECIFIED: _ClassVar[Message4.M1.M4.E9]
                E9_CONST_1: _ClassVar[Message4.M1.M4.E9]
                E9_CONST_2: _ClassVar[Message4.M1.M4.E9]
                E9_CONST_3: _ClassVar[Message4.M1.M4.E9]
                E9_CONST_4: _ClassVar[Message4.M1.M4.E9]
                E9_CONST_5: _ClassVar[Message4.M1.M4.E9]
            E9_UNSPECIFIED: Message4.M1.M4.E9
            E9_CONST_1: Message4.M1.M4.E9
            E9_CONST_2: Message4.M1.M4.E9
            E9_CONST_3: Message4.M1.M4.E9
            E9_CONST_4: Message4.M1.M4.E9
            E9_CONST_5: Message4.M1.M4.E9
            class E10(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E10_UNSPECIFIED: _ClassVar[Message4.M1.M4.E10]
                E10_CONST_1: _ClassVar[Message4.M1.M4.E10]
                E10_CONST_2: _ClassVar[Message4.M1.M4.E10]
                E10_CONST_3: _ClassVar[Message4.M1.M4.E10]
                E10_CONST_4: _ClassVar[Message4.M1.M4.E10]
                E10_CONST_5: _ClassVar[Message4.M1.M4.E10]
            E10_UNSPECIFIED: Message4.M1.M4.E10
            E10_CONST_1: Message4.M1.M4.E10
            E10_CONST_2: Message4.M1.M4.E10
            E10_CONST_3: Message4.M1.M4.E10
            E10_CONST_4: Message4.M1.M4.E10
            E10_CONST_5: Message4.M1.M4.E10
            class E11(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E11_UNSPECIFIED: _ClassVar[Message4.M1.M4.E11]
                E11_CONST_1: _ClassVar[Message4.M1.M4.E11]
                E11_CONST_2: _ClassVar[Message4.M1.M4.E11]
                E11_CONST_3: _ClassVar[Message4.M1.M4.E11]
                E11_CONST_4: _ClassVar[Message4.M1.M4.E11]
                E11_CONST_5: _ClassVar[Message4.M1.M4.E11]
            E11_UNSPECIFIED: Message4.M1.M4.E11
            E11_CONST_1: Message4.M1.M4.E11
            E11_CONST_2: Message4.M1.M4.E11
            E11_CONST_3: Message4.M1.M4.E11
            E11_CONST_4: Message4.M1.M4.E11
            E11_CONST_5: Message4.M1.M4.E11
            class E12(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E12_UNSPECIFIED: _ClassVar[Message4.M1.M4.E12]
                E12_CONST_1: _ClassVar[Message4.M1.M4.E12]
                E12_CONST_2: _ClassVar[Message4.M1.M4.E12]
                E12_CONST_3: _ClassVar[Message4.M1.M4.E12]
                E12_CONST_4: _ClassVar[Message4.M1.M4.E12]
                E12_CONST_5: _ClassVar[Message4.M1.M4.E12]
            E12_UNSPECIFIED: Message4.M1.M4.E12
            E12_CONST_1: Message4.M1.M4.E12
            E12_CONST_2: Message4.M1.M4.E12
            E12_CONST_3: Message4.M1.M4.E12
            E12_CONST_4: Message4.M1.M4.E12
            E12_CONST_5: Message4.M1.M4.E12
            class E13(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E13_UNSPECIFIED: _ClassVar[Message4.M1.M4.E13]
                E13_CONST_1: _ClassVar[Message4.M1.M4.E13]
                E13_CONST_2: _ClassVar[Message4.M1.M4.E13]
                E13_CONST_3: _ClassVar[Message4.M1.M4.E13]
                E13_CONST_4: _ClassVar[Message4.M1.M4.E13]
                E13_CONST_5: _ClassVar[Message4.M1.M4.E13]
            E13_UNSPECIFIED: Message4.M1.M4.E13
            E13_CONST_1: Message4.M1.M4.E13
            E13_CONST_2: Message4.M1.M4.E13
            E13_CONST_3: Message4.M1.M4.E13
            E13_CONST_4: Message4.M1.M4.E13
            E13_CONST_5: Message4.M1.M4.E13
            class M6(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
            class M8(_message.Message):
                __slots__ = ("f_0", "f_3", "f_4")
                class M14(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M29(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: bool
                    f_2: Message4.M1.M4.M8.M14.M29
                    def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Union[Message4.M1.M4.M8.M14.M29, _Mapping]] = ...) -> None: ...
                class M25(_message.Message):
                    __slots__ = ("f_0", "f_3")
                    class E17(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E17_UNSPECIFIED: _ClassVar[Message4.M1.M4.M8.M25.E17]
                        E17_CONST_1: _ClassVar[Message4.M1.M4.M8.M25.E17]
                        E17_CONST_2: _ClassVar[Message4.M1.M4.M8.M25.E17]
                        E17_CONST_3: _ClassVar[Message4.M1.M4.M8.M25.E17]
                        E17_CONST_4: _ClassVar[Message4.M1.M4.M8.M25.E17]
                        E17_CONST_5: _ClassVar[Message4.M1.M4.M8.M25.E17]
                    E17_UNSPECIFIED: Message4.M1.M4.M8.M25.E17
                    E17_CONST_1: Message4.M1.M4.M8.M25.E17
                    E17_CONST_2: Message4.M1.M4.M8.M25.E17
                    E17_CONST_3: Message4.M1.M4.M8.M25.E17
                    E17_CONST_4: Message4.M1.M4.M8.M25.E17
                    E17_CONST_5: Message4.M1.M4.M8.M25.E17
                    class M33(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message4.M1.M4.M8.M25.E17
                    f_3: Message4.M1.M4.M8.M25.M33
                    def __init__(self, f_0: _Optional[_Union[Message4.M1.M4.M8.M25.E17, str]] = ..., f_3: _Optional[_Union[Message4.M1.M4.M8.M25.M33, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_3: Message4.M1.M4.M8.M14
                f_4: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M8.M25]
                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message4.M1.M4.M8.M14, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message4.M1.M4.M8.M25, _Mapping]]] = ...) -> None: ...
            class M9(_message.Message):
                __slots__ = ("f_0", "f_2", "f_3")
                class M16(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_3", "f_4")
                    class M26(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_4")
                        class M39(_message.Message):
                            __slots__ = ("f_0",)
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: str
                            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        f_1: bool
                        f_2: str
                        f_4: Message4.M1.M4.M9.M16.M26.M39
                        def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[bool] = ..., f_2: _Optional[str] = ..., f_4: _Optional[_Union[Message4.M1.M4.M9.M16.M26.M39, _Mapping]] = ...) -> None: ...
                    class M31(_message.Message):
                        __slots__ = ("f_0", "f_2", "f_3")
                        class M41(_message.Message):
                            __slots__ = ("f_0",)
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                        class M42(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_39")
                            class E22(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E22_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E22]
                                E22_CONST_1: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E22]
                                E22_CONST_2: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E22]
                                E22_CONST_3: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E22]
                                E22_CONST_4: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E22]
                                E22_CONST_5: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E22]
                            E22_UNSPECIFIED: Message4.M1.M4.M9.M16.M31.M42.E22
                            E22_CONST_1: Message4.M1.M4.M9.M16.M31.M42.E22
                            E22_CONST_2: Message4.M1.M4.M9.M16.M31.M42.E22
                            E22_CONST_3: Message4.M1.M4.M9.M16.M31.M42.E22
                            E22_CONST_4: Message4.M1.M4.M9.M16.M31.M42.E22
                            E22_CONST_5: Message4.M1.M4.M9.M16.M31.M42.E22
                            class E23(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E23_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E23]
                                E23_CONST_1: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E23]
                                E23_CONST_2: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E23]
                                E23_CONST_3: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E23]
                                E23_CONST_4: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E23]
                                E23_CONST_5: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E23]
                            E23_UNSPECIFIED: Message4.M1.M4.M9.M16.M31.M42.E23
                            E23_CONST_1: Message4.M1.M4.M9.M16.M31.M42.E23
                            E23_CONST_2: Message4.M1.M4.M9.M16.M31.M42.E23
                            E23_CONST_3: Message4.M1.M4.M9.M16.M31.M42.E23
                            E23_CONST_4: Message4.M1.M4.M9.M16.M31.M42.E23
                            E23_CONST_5: Message4.M1.M4.M9.M16.M31.M42.E23
                            class E24(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E24_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E24]
                                E24_CONST_1: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E24]
                                E24_CONST_2: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E24]
                                E24_CONST_3: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E24]
                                E24_CONST_4: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E24]
                                E24_CONST_5: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.E24]
                            E24_UNSPECIFIED: Message4.M1.M4.M9.M16.M31.M42.E24
                            E24_CONST_1: Message4.M1.M4.M9.M16.M31.M42.E24
                            E24_CONST_2: Message4.M1.M4.M9.M16.M31.M42.E24
                            E24_CONST_3: Message4.M1.M4.M9.M16.M31.M42.E24
                            E24_CONST_4: Message4.M1.M4.M9.M16.M31.M42.E24
                            E24_CONST_5: Message4.M1.M4.M9.M16.M31.M42.E24
                            class M43(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_6", "f_8", "f_9", "f_10")
                                class M46(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: bool
                                    def __init__(self, f_0: _Optional[bool] = ...) -> None: ...
                                class M47(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: bool
                                    def __init__(self, f_0: _Optional[bool] = ...) -> None: ...
                                class M48(_message.Message):
                                    __slots__ = ("f_0", "f_2", "f_3")
                                    class M50(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: bytes
                                        def __init__(self, f_0: _Optional[bytes] = ...) -> None: ...
                                    class M52(_message.Message):
                                        __slots__ = ("f_0", "f_2")
                                        class E25(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                            __slots__ = ()
                                            E25_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25]
                                            E25_CONST_1: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25]
                                            E25_CONST_2: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25]
                                            E25_CONST_3: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25]
                                            E25_CONST_4: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25]
                                            E25_CONST_5: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25]
                                        E25_UNSPECIFIED: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        E25_CONST_1: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        E25_CONST_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        E25_CONST_3: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        E25_CONST_4: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        E25_CONST_5: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        class M53(_message.Message):
                                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_13")
                                            class E26(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                __slots__ = ()
                                                E26_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26]
                                                E26_CONST_1: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26]
                                                E26_CONST_2: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26]
                                                E26_CONST_3: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26]
                                                E26_CONST_4: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26]
                                                E26_CONST_5: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26]
                                            E26_UNSPECIFIED: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            E26_CONST_1: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            E26_CONST_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            E26_CONST_3: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            E26_CONST_4: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            E26_CONST_5: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            class M54(_message.Message):
                                                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_9")
                                                class E27(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                    __slots__ = ()
                                                    E27_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27]
                                                    E27_CONST_1: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27]
                                                    E27_CONST_2: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27]
                                                    E27_CONST_3: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27]
                                                    E27_CONST_4: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27]
                                                    E27_CONST_5: _ClassVar[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27]
                                                E27_UNSPECIFIED: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                E27_CONST_1: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                E27_CONST_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                E27_CONST_3: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                E27_CONST_4: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                E27_CONST_5: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                class M55(_message.Message):
                                                    __slots__ = ("f_0", "f_3")
                                                    class M56(_message.Message):
                                                        __slots__ = ("f_0", "f_1")
                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                        F_1_FIELD_NUMBER: _ClassVar[int]
                                                        f_0: float
                                                        f_1: str
                                                        def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[str] = ...) -> None: ...
                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                                    f_0: str
                                                    f_3: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.M55.M56]
                                                    def __init__(self, f_0: _Optional[str] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.M55.M56, _Mapping]]] = ...) -> None: ...
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                F_1_FIELD_NUMBER: _ClassVar[int]
                                                F_2_FIELD_NUMBER: _ClassVar[int]
                                                F_3_FIELD_NUMBER: _ClassVar[int]
                                                F_4_FIELD_NUMBER: _ClassVar[int]
                                                F_5_FIELD_NUMBER: _ClassVar[int]
                                                F_9_FIELD_NUMBER: _ClassVar[int]
                                                f_0: float
                                                f_1: int
                                                f_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27
                                                f_3: int
                                                f_4: _containers.RepeatedScalarFieldContainer[int]
                                                f_5: _containers.RepeatedScalarFieldContainer[int]
                                                f_9: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.M55
                                                def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.E27, str]] = ..., f_3: _Optional[int] = ..., f_4: _Optional[_Iterable[int]] = ..., f_5: _Optional[_Iterable[int]] = ..., f_9: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54.M55, _Mapping]] = ...) -> None: ...
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            F_1_FIELD_NUMBER: _ClassVar[int]
                                            F_2_FIELD_NUMBER: _ClassVar[int]
                                            F_3_FIELD_NUMBER: _ClassVar[int]
                                            F_4_FIELD_NUMBER: _ClassVar[int]
                                            F_5_FIELD_NUMBER: _ClassVar[int]
                                            F_6_FIELD_NUMBER: _ClassVar[int]
                                            F_7_FIELD_NUMBER: _ClassVar[int]
                                            F_8_FIELD_NUMBER: _ClassVar[int]
                                            F_13_FIELD_NUMBER: _ClassVar[int]
                                            f_0: int
                                            f_1: int
                                            f_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26
                                            f_3: str
                                            f_4: float
                                            f_5: str
                                            f_6: int
                                            f_7: int
                                            f_8: int
                                            f_13: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54
                                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.E26, str]] = ..., f_3: _Optional[str] = ..., f_4: _Optional[float] = ..., f_5: _Optional[str] = ..., f_6: _Optional[int] = ..., f_7: _Optional[int] = ..., f_8: _Optional[int] = ..., f_13: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53.M54, _Mapping]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        f_0: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25
                                        f_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53
                                        def __init__(self, f_0: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.E25, str]] = ..., f_2: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52.M53, _Mapping]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_3_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    f_2: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M50
                                    f_3: Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52
                                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M50, _Mapping]] = ..., f_3: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48.M52, _Mapping]] = ...) -> None: ...
                                class M49(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_2")
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    f_1: int
                                    f_2: str
                                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[str] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                F_6_FIELD_NUMBER: _ClassVar[int]
                                F_8_FIELD_NUMBER: _ClassVar[int]
                                F_9_FIELD_NUMBER: _ClassVar[int]
                                F_10_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                f_1: float
                                f_2: str
                                f_3: str
                                f_6: Message4.M1.M4.M9.M16.M31.M42.M43.M46
                                f_8: Message4.M1.M4.M9.M16.M31.M42.M43.M47
                                f_9: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M16.M31.M42.M43.M48]
                                f_10: Message4.M1.M4.M9.M16.M31.M42.M43.M49
                                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[float] = ..., f_2: _Optional[str] = ..., f_3: _Optional[str] = ..., f_6: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M46, _Mapping]] = ..., f_8: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M47, _Mapping]] = ..., f_9: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M48, _Mapping]]] = ..., f_10: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.M43.M49, _Mapping]] = ...) -> None: ...
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
                            F_39_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_1: int
                            f_2: Message4.M1.M4.M9.M16.M31.M42.E22
                            f_3: int
                            f_4: str
                            f_5: int
                            f_6: float
                            f_7: int
                            f_8: bool
                            f_9: int
                            f_10: int
                            f_11: str
                            f_12: int
                            f_13: Message4.M1.M4.M9.M16.M31.M42.E23
                            f_14: int
                            f_15: int
                            f_16: float
                            f_17: int
                            f_18: float
                            f_19: _containers.RepeatedScalarFieldContainer[float]
                            f_20: _containers.RepeatedScalarFieldContainer[int]
                            f_21: int
                            f_22: Message4.M1.M4.M9.M16.M31.M42.E24
                            f_23: str
                            f_24: float
                            f_25: str
                            f_26: int
                            f_27: str
                            f_28: str
                            f_39: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M16.M31.M42.M43]
                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.E22, str]] = ..., f_3: _Optional[int] = ..., f_4: _Optional[str] = ..., f_5: _Optional[int] = ..., f_6: _Optional[float] = ..., f_7: _Optional[int] = ..., f_8: _Optional[bool] = ..., f_9: _Optional[int] = ..., f_10: _Optional[int] = ..., f_11: _Optional[str] = ..., f_12: _Optional[int] = ..., f_13: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.E23, str]] = ..., f_14: _Optional[int] = ..., f_15: _Optional[int] = ..., f_16: _Optional[float] = ..., f_17: _Optional[int] = ..., f_18: _Optional[float] = ..., f_19: _Optional[_Iterable[float]] = ..., f_20: _Optional[_Iterable[int]] = ..., f_21: _Optional[int] = ..., f_22: _Optional[_Union[Message4.M1.M4.M9.M16.M31.M42.E24, str]] = ..., f_23: _Optional[str] = ..., f_24: _Optional[float] = ..., f_25: _Optional[str] = ..., f_26: _Optional[int] = ..., f_27: _Optional[str] = ..., f_28: _Optional[str] = ..., f_39: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M16.M31.M42.M43, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        f_0: _containers.RepeatedScalarFieldContainer[int]
                        f_2: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M16.M31.M41]
                        f_3: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M16.M31.M42]
                        def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_2: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M16.M31.M41, _Mapping]]] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M16.M31.M42, _Mapping]]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_1: int
                    f_3: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M16.M26]
                    f_4: Message4.M1.M4.M9.M16.M31
                    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M16.M26, _Mapping]]] = ..., f_4: _Optional[_Union[Message4.M1.M4.M9.M16.M31, _Mapping]] = ...) -> None: ...
                class M21(_message.Message):
                    __slots__ = ("f_0", "f_2", "f_3")
                    class M27(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                    class M30(_message.Message):
                        __slots__ = ("f_0",)
                        class E19(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E19_UNSPECIFIED: _ClassVar[Message4.M1.M4.M9.M21.M30.E19]
                            E19_CONST_1: _ClassVar[Message4.M1.M4.M9.M21.M30.E19]
                            E19_CONST_2: _ClassVar[Message4.M1.M4.M9.M21.M30.E19]
                            E19_CONST_3: _ClassVar[Message4.M1.M4.M9.M21.M30.E19]
                            E19_CONST_4: _ClassVar[Message4.M1.M4.M9.M21.M30.E19]
                            E19_CONST_5: _ClassVar[Message4.M1.M4.M9.M21.M30.E19]
                        E19_UNSPECIFIED: Message4.M1.M4.M9.M21.M30.E19
                        E19_CONST_1: Message4.M1.M4.M9.M21.M30.E19
                        E19_CONST_2: Message4.M1.M4.M9.M21.M30.E19
                        E19_CONST_3: Message4.M1.M4.M9.M21.M30.E19
                        E19_CONST_4: Message4.M1.M4.M9.M21.M30.E19
                        E19_CONST_5: Message4.M1.M4.M9.M21.M30.E19
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message4.M1.M4.M9.M21.M30.E19
                        def __init__(self, f_0: _Optional[_Union[Message4.M1.M4.M9.M21.M30.E19, str]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_2: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M21.M27]
                    f_3: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M9.M21.M30]
                    def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M21.M27, _Mapping]]] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.M4.M9.M21.M30, _Mapping]]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_2: Message4.M1.M4.M9.M16
                f_3: Message4.M1.M4.M9.M21
                def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message4.M1.M4.M9.M16, _Mapping]] = ..., f_3: _Optional[_Union[Message4.M1.M4.M9.M21, _Mapping]] = ...) -> None: ...
            class M10(_message.Message):
                __slots__ = ("f_0", "f_2")
                class M15(_message.Message):
                    __slots__ = ("f_0",)
                    class E15(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E15_UNSPECIFIED: _ClassVar[Message4.M1.M4.M10.M15.E15]
                        E15_CONST_1: _ClassVar[Message4.M1.M4.M10.M15.E15]
                        E15_CONST_2: _ClassVar[Message4.M1.M4.M10.M15.E15]
                        E15_CONST_3: _ClassVar[Message4.M1.M4.M10.M15.E15]
                        E15_CONST_4: _ClassVar[Message4.M1.M4.M10.M15.E15]
                        E15_CONST_5: _ClassVar[Message4.M1.M4.M10.M15.E15]
                    E15_UNSPECIFIED: Message4.M1.M4.M10.M15.E15
                    E15_CONST_1: Message4.M1.M4.M10.M15.E15
                    E15_CONST_2: Message4.M1.M4.M10.M15.E15
                    E15_CONST_3: Message4.M1.M4.M10.M15.E15
                    E15_CONST_4: Message4.M1.M4.M10.M15.E15
                    E15_CONST_5: Message4.M1.M4.M10.M15.E15
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message4.M1.M4.M10.M15.E15
                    def __init__(self, f_0: _Optional[_Union[Message4.M1.M4.M10.M15.E15, str]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                f_0: _containers.RepeatedScalarFieldContainer[str]
                f_2: Message4.M1.M4.M10.M15
                def __init__(self, f_0: _Optional[_Iterable[str]] = ..., f_2: _Optional[_Union[Message4.M1.M4.M10.M15, _Mapping]] = ...) -> None: ...
            class M11(_message.Message):
                __slots__ = ("f_0", "f_2")
                class M23(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                f_0: float
                f_2: Message4.M1.M4.M11.M23
                def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message4.M1.M4.M11.M23, _Mapping]] = ...) -> None: ...
            class M13(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: bool
                def __init__(self, f_0: _Optional[bool] = ...) -> None: ...
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
            F_74_FIELD_NUMBER: _ClassVar[int]
            F_75_FIELD_NUMBER: _ClassVar[int]
            F_76_FIELD_NUMBER: _ClassVar[int]
            F_77_FIELD_NUMBER: _ClassVar[int]
            F_78_FIELD_NUMBER: _ClassVar[int]
            F_79_FIELD_NUMBER: _ClassVar[int]
            F_80_FIELD_NUMBER: _ClassVar[int]
            F_81_FIELD_NUMBER: _ClassVar[int]
            F_82_FIELD_NUMBER: _ClassVar[int]
            F_83_FIELD_NUMBER: _ClassVar[int]
            F_84_FIELD_NUMBER: _ClassVar[int]
            F_85_FIELD_NUMBER: _ClassVar[int]
            F_86_FIELD_NUMBER: _ClassVar[int]
            F_87_FIELD_NUMBER: _ClassVar[int]
            F_88_FIELD_NUMBER: _ClassVar[int]
            F_89_FIELD_NUMBER: _ClassVar[int]
            F_90_FIELD_NUMBER: _ClassVar[int]
            F_91_FIELD_NUMBER: _ClassVar[int]
            F_92_FIELD_NUMBER: _ClassVar[int]
            F_93_FIELD_NUMBER: _ClassVar[int]
            F_94_FIELD_NUMBER: _ClassVar[int]
            F_95_FIELD_NUMBER: _ClassVar[int]
            F_96_FIELD_NUMBER: _ClassVar[int]
            F_131_FIELD_NUMBER: _ClassVar[int]
            F_133_FIELD_NUMBER: _ClassVar[int]
            F_134_FIELD_NUMBER: _ClassVar[int]
            F_135_FIELD_NUMBER: _ClassVar[int]
            F_136_FIELD_NUMBER: _ClassVar[int]
            F_138_FIELD_NUMBER: _ClassVar[int]
            f_0: float
            f_1: float
            f_2: str
            f_3: Message4.M1.M4.E2
            f_4: int
            f_5: _containers.RepeatedScalarFieldContainer[int]
            f_6: int
            f_7: int
            f_8: str
            f_9: Message4.M1.M4.E3
            f_10: bytes
            f_11: str
            f_12: int
            f_13: _containers.RepeatedScalarFieldContainer[int]
            f_14: bool
            f_15: int
            f_16: Message4.M1.M4.E4
            f_17: bool
            f_18: str
            f_19: bool
            f_20: Message4.M1.M4.E5
            f_21: float
            f_22: int
            f_23: int
            f_24: Message4.M1.M4.E6
            f_25: float
            f_26: bool
            f_27: float
            f_28: str
            f_29: float
            f_30: int
            f_31: float
            f_32: Message4.M1.M4.E7
            f_33: int
            f_34: Message4.M1.M4.E8
            f_35: str
            f_36: int
            f_37: str
            f_38: int
            f_39: str
            f_40: int
            f_41: str
            f_42: int
            f_43: bytes
            f_44: str
            f_45: int
            f_46: bool
            f_47: str
            f_48: str
            f_49: _containers.RepeatedScalarFieldContainer[str]
            f_50: str
            f_51: _containers.RepeatedScalarFieldContainer[float]
            f_52: int
            f_53: int
            f_54: int
            f_55: float
            f_56: int
            f_57: str
            f_58: int
            f_59: float
            f_60: int
            f_61: float
            f_62: Message4.M1.M4.E9
            f_63: Message4.M1.M4.E10
            f_64: int
            f_65: bool
            f_66: str
            f_67: Message4.M1.M4.E11
            f_68: str
            f_69: bool
            f_70: _containers.RepeatedScalarFieldContainer[bytes]
            f_71: int
            f_72: _containers.RepeatedScalarFieldContainer[int]
            f_73: Message4.M1.M4.E12
            f_74: int
            f_75: str
            f_76: int
            f_77: int
            f_78: str
            f_79: float
            f_80: _containers.RepeatedScalarFieldContainer[int]
            f_81: str
            f_82: str
            f_83: Message4.M1.M4.E13
            f_84: float
            f_85: int
            f_86: float
            f_87: str
            f_88: _containers.RepeatedScalarFieldContainer[int]
            f_89: int
            f_90: int
            f_91: int
            f_92: float
            f_93: str
            f_94: int
            f_95: int
            f_96: int
            f_131: Message4.M1.M4.M6
            f_133: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4.M8]
            f_134: Message4.M1.M4.M9
            f_135: Message4.M1.M4.M10
            f_136: Message4.M1.M4.M11
            f_138: Message4.M1.M4.M13
            def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[float] = ..., f_2: _Optional[str] = ..., f_3: _Optional[_Union[Message4.M1.M4.E2, str]] = ..., f_4: _Optional[int] = ..., f_5: _Optional[_Iterable[int]] = ..., f_6: _Optional[int] = ..., f_7: _Optional[int] = ..., f_8: _Optional[str] = ..., f_9: _Optional[_Union[Message4.M1.M4.E3, str]] = ..., f_10: _Optional[bytes] = ..., f_11: _Optional[str] = ..., f_12: _Optional[int] = ..., f_13: _Optional[_Iterable[int]] = ..., f_14: _Optional[bool] = ..., f_15: _Optional[int] = ..., f_16: _Optional[_Union[Message4.M1.M4.E4, str]] = ..., f_17: _Optional[bool] = ..., f_18: _Optional[str] = ..., f_19: _Optional[bool] = ..., f_20: _Optional[_Union[Message4.M1.M4.E5, str]] = ..., f_21: _Optional[float] = ..., f_22: _Optional[int] = ..., f_23: _Optional[int] = ..., f_24: _Optional[_Union[Message4.M1.M4.E6, str]] = ..., f_25: _Optional[float] = ..., f_26: _Optional[bool] = ..., f_27: _Optional[float] = ..., f_28: _Optional[str] = ..., f_29: _Optional[float] = ..., f_30: _Optional[int] = ..., f_31: _Optional[float] = ..., f_32: _Optional[_Union[Message4.M1.M4.E7, str]] = ..., f_33: _Optional[int] = ..., f_34: _Optional[_Union[Message4.M1.M4.E8, str]] = ..., f_35: _Optional[str] = ..., f_36: _Optional[int] = ..., f_37: _Optional[str] = ..., f_38: _Optional[int] = ..., f_39: _Optional[str] = ..., f_40: _Optional[int] = ..., f_41: _Optional[str] = ..., f_42: _Optional[int] = ..., f_43: _Optional[bytes] = ..., f_44: _Optional[str] = ..., f_45: _Optional[int] = ..., f_46: _Optional[bool] = ..., f_47: _Optional[str] = ..., f_48: _Optional[str] = ..., f_49: _Optional[_Iterable[str]] = ..., f_50: _Optional[str] = ..., f_51: _Optional[_Iterable[float]] = ..., f_52: _Optional[int] = ..., f_53: _Optional[int] = ..., f_54: _Optional[int] = ..., f_55: _Optional[float] = ..., f_56: _Optional[int] = ..., f_57: _Optional[str] = ..., f_58: _Optional[int] = ..., f_59: _Optional[float] = ..., f_60: _Optional[int] = ..., f_61: _Optional[float] = ..., f_62: _Optional[_Union[Message4.M1.M4.E9, str]] = ..., f_63: _Optional[_Union[Message4.M1.M4.E10, str]] = ..., f_64: _Optional[int] = ..., f_65: _Optional[bool] = ..., f_66: _Optional[str] = ..., f_67: _Optional[_Union[Message4.M1.M4.E11, str]] = ..., f_68: _Optional[str] = ..., f_69: _Optional[bool] = ..., f_70: _Optional[_Iterable[bytes]] = ..., f_71: _Optional[int] = ..., f_72: _Optional[_Iterable[int]] = ..., f_73: _Optional[_Union[Message4.M1.M4.E12, str]] = ..., f_74: _Optional[int] = ..., f_75: _Optional[str] = ..., f_76: _Optional[int] = ..., f_77: _Optional[int] = ..., f_78: _Optional[str] = ..., f_79: _Optional[float] = ..., f_80: _Optional[_Iterable[int]] = ..., f_81: _Optional[str] = ..., f_82: _Optional[str] = ..., f_83: _Optional[_Union[Message4.M1.M4.E13, str]] = ..., f_84: _Optional[float] = ..., f_85: _Optional[int] = ..., f_86: _Optional[float] = ..., f_87: _Optional[str] = ..., f_88: _Optional[_Iterable[int]] = ..., f_89: _Optional[int] = ..., f_90: _Optional[int] = ..., f_91: _Optional[int] = ..., f_92: _Optional[float] = ..., f_93: _Optional[str] = ..., f_94: _Optional[int] = ..., f_95: _Optional[int] = ..., f_96: _Optional[int] = ..., f_131: _Optional[_Union[Message4.M1.M4.M6, _Mapping]] = ..., f_133: _Optional[_Iterable[_Union[Message4.M1.M4.M8, _Mapping]]] = ..., f_134: _Optional[_Union[Message4.M1.M4.M9, _Mapping]] = ..., f_135: _Optional[_Union[Message4.M1.M4.M10, _Mapping]] = ..., f_136: _Optional[_Union[Message4.M1.M4.M11, _Mapping]] = ..., f_138: _Optional[_Union[Message4.M1.M4.M13, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_1_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_6_FIELD_NUMBER: _ClassVar[int]
        F_7_FIELD_NUMBER: _ClassVar[int]
        F_9_FIELD_NUMBER: _ClassVar[int]
        f_0: _containers.RepeatedScalarFieldContainer[int]
        f_1: int
        f_2: _containers.RepeatedScalarFieldContainer[int]
        f_3: _containers.RepeatedScalarFieldContainer[Message4.M1.E1]
        f_6: Message4.M1.M2
        f_7: Message4.M1.M3
        f_9: _containers.RepeatedCompositeFieldContainer[Message4.M1.M4]
        def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Iterable[int]] = ..., f_3: _Optional[_Iterable[_Union[Message4.M1.E1, str]]] = ..., f_6: _Optional[_Union[Message4.M1.M2, _Mapping]] = ..., f_7: _Optional[_Union[Message4.M1.M3, _Mapping]] = ..., f_9: _Optional[_Iterable[_Union[Message4.M1.M4, _Mapping]]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_2_FIELD_NUMBER: _ClassVar[int]
    f_0: _containers.RepeatedScalarFieldContainer[str]
    f_2: _containers.RepeatedCompositeFieldContainer[Message4.M1]
    def __init__(self, f_0: _Optional[_Iterable[str]] = ..., f_2: _Optional[_Iterable[_Union[Message4.M1, _Mapping]]] = ...) -> None: ...
