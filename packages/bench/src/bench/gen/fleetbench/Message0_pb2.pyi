from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message0(_message.Message):
    __slots__ = ("f_0", "f_4")
    class M1(_message.Message):
        __slots__ = ("f_0", "f_2", "f_3")
        class M2(_message.Message):
            __slots__ = ("f_0", "f_2")
            class M4(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_2: Message0.M1.M2.M4
            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message0.M1.M2.M4, _Mapping]] = ...) -> None: ...
        class M3(_message.Message):
            __slots__ = ("f_0", "f_2")
            class M5(_message.Message):
                __slots__ = ("f_0", "f_3", "f_4")
                class M6(_message.Message):
                    __slots__ = ("f_0", "f_3", "f_4")
                    class M8(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M12(_message.Message):
                            __slots__ = ("f_0",)
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        f_2: _containers.RepeatedCompositeFieldContainer[Message0.M1.M3.M5.M6.M8.M12]
                        def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Iterable[_Union[Message0.M1.M3.M5.M6.M8.M12, _Mapping]]] = ...) -> None: ...
                    class M10(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: float
                        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_3: Message0.M1.M3.M5.M6.M8
                    f_4: _containers.RepeatedCompositeFieldContainer[Message0.M1.M3.M5.M6.M10]
                    def __init__(self, f_0: _Optional[str] = ..., f_3: _Optional[_Union[Message0.M1.M3.M5.M6.M8, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message0.M1.M3.M5.M6.M10, _Mapping]]] = ...) -> None: ...
                class M7(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_4")
                    class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E1_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.E1]
                        E1_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.E1]
                        E1_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.E1]
                        E1_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.E1]
                        E1_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.E1]
                        E1_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.E1]
                    E1_UNSPECIFIED: Message0.M1.M3.M5.M7.E1
                    E1_CONST_1: Message0.M1.M3.M5.M7.E1
                    E1_CONST_2: Message0.M1.M3.M5.M7.E1
                    E1_CONST_3: Message0.M1.M3.M5.M7.E1
                    E1_CONST_4: Message0.M1.M3.M5.M7.E1
                    E1_CONST_5: Message0.M1.M3.M5.M7.E1
                    class M9(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M11(_message.Message):
                            __slots__ = ("f_0", "f_2")
                            class M13(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24", "f_25", "f_26", "f_27", "f_28", "f_29", "f_30", "f_40")
                                class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E2_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
                                    E2_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
                                    E2_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
                                    E2_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
                                    E2_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
                                    E2_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
                                E2_UNSPECIFIED: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                E2_CONST_1: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                E2_CONST_2: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                E2_CONST_3: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                E2_CONST_4: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                E2_CONST_5: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E3_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
                                    E3_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
                                    E3_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
                                    E3_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
                                    E3_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
                                    E3_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
                                E3_UNSPECIFIED: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                E3_CONST_1: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                E3_CONST_2: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                E3_CONST_3: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                E3_CONST_4: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                E3_CONST_5: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E4_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
                                    E4_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
                                    E4_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
                                    E4_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
                                    E4_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
                                    E4_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
                                E4_UNSPECIFIED: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                E4_CONST_1: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                E4_CONST_2: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                E4_CONST_3: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                E4_CONST_4: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                E4_CONST_5: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E5_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
                                    E5_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
                                    E5_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
                                    E5_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
                                    E5_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
                                    E5_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
                                E5_UNSPECIFIED: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                E5_CONST_1: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                E5_CONST_2: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                E5_CONST_3: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                E5_CONST_4: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                E5_CONST_5: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E6_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
                                    E6_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
                                    E6_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
                                    E6_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
                                    E6_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
                                    E6_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
                                E6_UNSPECIFIED: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                E6_CONST_1: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                E6_CONST_2: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                E6_CONST_3: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                E6_CONST_4: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                E6_CONST_5: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                class E7(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E7_UNSPECIFIED: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E7]
                                    E7_CONST_1: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E7]
                                    E7_CONST_2: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E7]
                                    E7_CONST_3: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E7]
                                    E7_CONST_4: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E7]
                                    E7_CONST_5: _ClassVar[Message0.M1.M3.M5.M7.M9.M11.M13.E7]
                                E7_UNSPECIFIED: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                E7_CONST_1: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                E7_CONST_2: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                E7_CONST_3: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                E7_CONST_4: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                E7_CONST_5: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                class M14(_message.Message):
                                    __slots__ = ("f_0", "f_2")
                                    class M15(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: _containers.RepeatedScalarFieldContainer[int]
                                    f_2: Message0.M1.M3.M5.M7.M9.M11.M13.M14.M15
                                    def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_2: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.M14.M15, _Mapping]] = ...) -> None: ...
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
                                F_40_FIELD_NUMBER: _ClassVar[int]
                                f_0: Message0.M1.M3.M5.M7.M9.M11.M13.E2
                                f_1: float
                                f_2: str
                                f_3: int
                                f_4: Message0.M1.M3.M5.M7.M9.M11.M13.E3
                                f_5: int
                                f_6: str
                                f_7: Message0.M1.M3.M5.M7.M9.M11.M13.E4
                                f_8: int
                                f_9: int
                                f_10: int
                                f_11: _containers.RepeatedScalarFieldContainer[int]
                                f_12: bool
                                f_13: int
                                f_14: bool
                                f_15: int
                                f_16: float
                                f_17: int
                                f_18: bool
                                f_19: int
                                f_20: str
                                f_21: Message0.M1.M3.M5.M7.M9.M11.M13.E5
                                f_22: int
                                f_23: int
                                f_24: int
                                f_25: Message0.M1.M3.M5.M7.M9.M11.M13.E6
                                f_26: int
                                f_27: Message0.M1.M3.M5.M7.M9.M11.M13.E7
                                f_28: str
                                f_29: int
                                f_30: str
                                f_40: Message0.M1.M3.M5.M7.M9.M11.M13.M14
                                def __init__(self, f_0: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.E2, str]] = ..., f_1: _Optional[float] = ..., f_2: _Optional[str] = ..., f_3: _Optional[int] = ..., f_4: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.E3, str]] = ..., f_5: _Optional[int] = ..., f_6: _Optional[str] = ..., f_7: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.E4, str]] = ..., f_8: _Optional[int] = ..., f_9: _Optional[int] = ..., f_10: _Optional[int] = ..., f_11: _Optional[_Iterable[int]] = ..., f_12: _Optional[bool] = ..., f_13: _Optional[int] = ..., f_14: _Optional[bool] = ..., f_15: _Optional[int] = ..., f_16: _Optional[float] = ..., f_17: _Optional[int] = ..., f_18: _Optional[bool] = ..., f_19: _Optional[int] = ..., f_20: _Optional[str] = ..., f_21: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.E5, str]] = ..., f_22: _Optional[int] = ..., f_23: _Optional[int] = ..., f_24: _Optional[int] = ..., f_25: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.E6, str]] = ..., f_26: _Optional[int] = ..., f_27: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.E7, str]] = ..., f_28: _Optional[str] = ..., f_29: _Optional[int] = ..., f_30: _Optional[str] = ..., f_40: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13.M14, _Mapping]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_2: Message0.M1.M3.M5.M7.M9.M11.M13
                            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11.M13, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_2: Message0.M1.M3.M5.M7.M9.M11
                        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message0.M1.M3.M5.M7.M9.M11, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message0.M1.M3.M5.M7.E1
                    f_1: int
                    f_4: Message0.M1.M3.M5.M7.M9
                    def __init__(self, f_0: _Optional[_Union[Message0.M1.M3.M5.M7.E1, str]] = ..., f_1: _Optional[int] = ..., f_4: _Optional[_Union[Message0.M1.M3.M5.M7.M9, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_3: Message0.M1.M3.M5.M6
                f_4: Message0.M1.M3.M5.M7
                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message0.M1.M3.M5.M6, _Mapping]] = ..., f_4: _Optional[_Union[Message0.M1.M3.M5.M7, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            f_2: Message0.M1.M3.M5
            def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message0.M1.M3.M5, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_2: Message0.M1.M2
        f_3: Message0.M1.M3
        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message0.M1.M2, _Mapping]] = ..., f_3: _Optional[_Union[Message0.M1.M3, _Mapping]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_4_FIELD_NUMBER: _ClassVar[int]
    f_0: int
    f_4: _containers.RepeatedCompositeFieldContainer[Message0.M1]
    def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Iterable[_Union[Message0.M1, _Mapping]]] = ...) -> None: ...
