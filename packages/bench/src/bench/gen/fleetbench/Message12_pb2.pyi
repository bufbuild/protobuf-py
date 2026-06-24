from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message12(_message.Message):
    __slots__ = ("f_0", "f_2")
    class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        E1_UNSPECIFIED: _ClassVar[Message12.E1]
        E1_CONST_1: _ClassVar[Message12.E1]
        E1_CONST_2: _ClassVar[Message12.E1]
        E1_CONST_3: _ClassVar[Message12.E1]
        E1_CONST_4: _ClassVar[Message12.E1]
        E1_CONST_5: _ClassVar[Message12.E1]
    E1_UNSPECIFIED: Message12.E1
    E1_CONST_1: Message12.E1
    E1_CONST_2: Message12.E1
    E1_CONST_3: Message12.E1
    E1_CONST_4: Message12.E1
    E1_CONST_5: Message12.E1
    class M1(_message.Message):
        __slots__ = ("f_0", "f_2")
        class M2(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_10", "f_11", "f_12", "f_13")
            class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E2_UNSPECIFIED: _ClassVar[Message12.M1.M2.E2]
                E2_CONST_1: _ClassVar[Message12.M1.M2.E2]
                E2_CONST_2: _ClassVar[Message12.M1.M2.E2]
                E2_CONST_3: _ClassVar[Message12.M1.M2.E2]
                E2_CONST_4: _ClassVar[Message12.M1.M2.E2]
                E2_CONST_5: _ClassVar[Message12.M1.M2.E2]
            E2_UNSPECIFIED: Message12.M1.M2.E2
            E2_CONST_1: Message12.M1.M2.E2
            E2_CONST_2: Message12.M1.M2.E2
            E2_CONST_3: Message12.M1.M2.E2
            E2_CONST_4: Message12.M1.M2.E2
            E2_CONST_5: Message12.M1.M2.E2
            class M3(_message.Message):
                __slots__ = ("f_0", "f_3", "f_4", "f_5")
                class M8(_message.Message):
                    __slots__ = ("f_0", "f_4")
                    class M12(_message.Message):
                        __slots__ = ("f_0", "f_4", "f_5")
                        class M17(_message.Message):
                            __slots__ = ("f_0",)
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: float
                            def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                        class M21(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11")
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
                            f_0: str
                            f_1: int
                            f_2: int
                            f_3: int
                            f_4: int
                            f_5: float
                            f_6: bool
                            f_7: int
                            f_8: int
                            f_9: int
                            f_10: int
                            f_11: int
                            def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[float] = ..., f_6: _Optional[bool] = ..., f_7: _Optional[int] = ..., f_8: _Optional[int] = ..., f_9: _Optional[int] = ..., f_10: _Optional[int] = ..., f_11: _Optional[int] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        f_4: Message12.M1.M2.M3.M8.M12.M17
                        f_5: Message12.M1.M2.M3.M8.M12.M21
                        def __init__(self, f_0: _Optional[str] = ..., f_4: _Optional[_Union[Message12.M1.M2.M3.M8.M12.M17, _Mapping]] = ..., f_5: _Optional[_Union[Message12.M1.M2.M3.M8.M12.M21, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_4: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M3.M8.M12]
                    def __init__(self, f_0: _Optional[float] = ..., f_4: _Optional[_Iterable[_Union[Message12.M1.M2.M3.M8.M12, _Mapping]]] = ...) -> None: ...
                class M9(_message.Message):
                    __slots__ = ("f_0", "f_3")
                    class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E5_UNSPECIFIED: _ClassVar[Message12.M1.M2.M3.M9.E5]
                        E5_CONST_1: _ClassVar[Message12.M1.M2.M3.M9.E5]
                        E5_CONST_2: _ClassVar[Message12.M1.M2.M3.M9.E5]
                        E5_CONST_3: _ClassVar[Message12.M1.M2.M3.M9.E5]
                        E5_CONST_4: _ClassVar[Message12.M1.M2.M3.M9.E5]
                        E5_CONST_5: _ClassVar[Message12.M1.M2.M3.M9.E5]
                    E5_UNSPECIFIED: Message12.M1.M2.M3.M9.E5
                    E5_CONST_1: Message12.M1.M2.M3.M9.E5
                    E5_CONST_2: Message12.M1.M2.M3.M9.E5
                    E5_CONST_3: Message12.M1.M2.M3.M9.E5
                    E5_CONST_4: Message12.M1.M2.M3.M9.E5
                    E5_CONST_5: Message12.M1.M2.M3.M9.E5
                    class M13(_message.Message):
                        __slots__ = ("f_0", "f_3")
                        class M19(_message.Message):
                            __slots__ = ("f_0", "f_2")
                            class M23(_message.Message):
                                __slots__ = ("f_0", "f_3")
                                class M26(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_2", "f_4")
                                    class M28(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: float
                                        def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_4_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    f_1: bool
                                    f_2: float
                                    f_4: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M3.M9.M13.M19.M23.M26.M28]
                                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[bool] = ..., f_2: _Optional[float] = ..., f_4: _Optional[_Iterable[_Union[Message12.M1.M2.M3.M9.M13.M19.M23.M26.M28, _Mapping]]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                f_3: Message12.M1.M2.M3.M9.M13.M19.M23.M26
                                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message12.M1.M2.M3.M9.M13.M19.M23.M26, _Mapping]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_2: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M3.M9.M13.M19.M23]
                            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message12.M1.M2.M3.M9.M13.M19.M23, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        f_3: Message12.M1.M2.M3.M9.M13.M19
                        def __init__(self, f_0: _Optional[bool] = ..., f_3: _Optional[_Union[Message12.M1.M2.M3.M9.M13.M19, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message12.M1.M2.M3.M9.E5
                    f_3: Message12.M1.M2.M3.M9.M13
                    def __init__(self, f_0: _Optional[_Union[Message12.M1.M2.M3.M9.E5, str]] = ..., f_3: _Optional[_Union[Message12.M1.M2.M3.M9.M13, _Mapping]] = ...) -> None: ...
                class M10(_message.Message):
                    __slots__ = ("f_0", "f_1")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: _containers.RepeatedScalarFieldContainer[int]
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[_Iterable[int]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_3: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M3.M8]
                f_4: Message12.M1.M2.M3.M9
                f_5: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M3.M10]
                def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message12.M1.M2.M3.M8, _Mapping]]] = ..., f_4: _Optional[_Union[Message12.M1.M2.M3.M9, _Mapping]] = ..., f_5: _Optional[_Iterable[_Union[Message12.M1.M2.M3.M10, _Mapping]]] = ...) -> None: ...
            class M4(_message.Message):
                __slots__ = ("f_0", "f_2")
                class M7(_message.Message):
                    __slots__ = ("f_0", "f_3", "f_4", "f_6")
                    class M14(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M20(_message.Message):
                            __slots__ = ("f_0", "f_3")
                            class M22(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_3")
                                class M25(_message.Message):
                                    __slots__ = ("f_0", "f_2")
                                    class E11(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E11_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11]
                                        E11_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11]
                                        E11_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11]
                                        E11_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11]
                                        E11_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11]
                                        E11_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11]
                                    E11_UNSPECIFIED: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    E11_CONST_1: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    E11_CONST_2: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    E11_CONST_3: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    E11_CONST_4: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    E11_CONST_5: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    class M27(_message.Message):
                                        __slots__ = ("f_0", "f_2")
                                        class M29(_message.Message):
                                            __slots__ = ("f_0", "f_2")
                                            class E12(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                __slots__ = ()
                                                E12_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12]
                                                E12_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12]
                                                E12_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12]
                                                E12_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12]
                                                E12_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12]
                                                E12_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12]
                                            E12_UNSPECIFIED: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            E12_CONST_1: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            E12_CONST_2: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            E12_CONST_3: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            E12_CONST_4: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            E12_CONST_5: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            class M30(_message.Message):
                                                __slots__ = ("f_0",)
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                f_0: float
                                                def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            F_2_FIELD_NUMBER: _ClassVar[int]
                                            f_0: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12
                                            f_2: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.M30]
                                            def __init__(self, f_0: _Optional[_Union[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.E12, str]] = ..., f_2: _Optional[_Iterable[_Union[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29.M30, _Mapping]]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        f_0: _containers.RepeatedScalarFieldContainer[int]
                                        f_2: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29]
                                        def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_2: _Optional[_Iterable[_Union[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29, _Mapping]]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11
                                    f_2: Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27
                                    def __init__(self, f_0: _Optional[_Union[Message12.M1.M2.M4.M7.M14.M20.M22.M25.E11, str]] = ..., f_2: _Optional[_Union[Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                f_0: bool
                                f_1: str
                                f_3: Message12.M1.M2.M4.M7.M14.M20.M22.M25
                                def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[str] = ..., f_3: _Optional[_Union[Message12.M1.M2.M4.M7.M14.M20.M22.M25, _Mapping]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            f_0: float
                            f_3: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4.M7.M14.M20.M22]
                            def __init__(self, f_0: _Optional[float] = ..., f_3: _Optional[_Iterable[_Union[Message12.M1.M2.M4.M7.M14.M20.M22, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        f_2: Message12.M1.M2.M4.M7.M14.M20
                        def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message12.M1.M2.M4.M7.M14.M20, _Mapping]] = ...) -> None: ...
                    class M15(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M18(_message.Message):
                            __slots__ = ("f_0", "f_2")
                            class M24(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: float
                                def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_2: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4.M7.M15.M18.M24]
                            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message12.M1.M2.M4.M7.M15.M18.M24, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_2: Message12.M1.M2.M4.M7.M15.M18
                        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message12.M1.M2.M4.M7.M15.M18, _Mapping]] = ...) -> None: ...
                    class M16(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_12", "f_13", "f_14", "f_15", "f_16", "f_17", "f_18", "f_19", "f_20", "f_21", "f_22", "f_23", "f_24")
                        class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E6_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M16.E6]
                            E6_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M16.E6]
                            E6_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M16.E6]
                            E6_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M16.E6]
                            E6_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M16.E6]
                            E6_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M16.E6]
                        E6_UNSPECIFIED: Message12.M1.M2.M4.M7.M16.E6
                        E6_CONST_1: Message12.M1.M2.M4.M7.M16.E6
                        E6_CONST_2: Message12.M1.M2.M4.M7.M16.E6
                        E6_CONST_3: Message12.M1.M2.M4.M7.M16.E6
                        E6_CONST_4: Message12.M1.M2.M4.M7.M16.E6
                        E6_CONST_5: Message12.M1.M2.M4.M7.M16.E6
                        class E7(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E7_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M16.E7]
                            E7_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M16.E7]
                            E7_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M16.E7]
                            E7_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M16.E7]
                            E7_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M16.E7]
                            E7_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M16.E7]
                        E7_UNSPECIFIED: Message12.M1.M2.M4.M7.M16.E7
                        E7_CONST_1: Message12.M1.M2.M4.M7.M16.E7
                        E7_CONST_2: Message12.M1.M2.M4.M7.M16.E7
                        E7_CONST_3: Message12.M1.M2.M4.M7.M16.E7
                        E7_CONST_4: Message12.M1.M2.M4.M7.M16.E7
                        E7_CONST_5: Message12.M1.M2.M4.M7.M16.E7
                        class E8(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E8_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M16.E8]
                            E8_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M16.E8]
                            E8_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M16.E8]
                            E8_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M16.E8]
                            E8_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M16.E8]
                            E8_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M16.E8]
                        E8_UNSPECIFIED: Message12.M1.M2.M4.M7.M16.E8
                        E8_CONST_1: Message12.M1.M2.M4.M7.M16.E8
                        E8_CONST_2: Message12.M1.M2.M4.M7.M16.E8
                        E8_CONST_3: Message12.M1.M2.M4.M7.M16.E8
                        E8_CONST_4: Message12.M1.M2.M4.M7.M16.E8
                        E8_CONST_5: Message12.M1.M2.M4.M7.M16.E8
                        class E9(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E9_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M16.E9]
                            E9_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M16.E9]
                            E9_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M16.E9]
                            E9_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M16.E9]
                            E9_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M16.E9]
                            E9_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M16.E9]
                        E9_UNSPECIFIED: Message12.M1.M2.M4.M7.M16.E9
                        E9_CONST_1: Message12.M1.M2.M4.M7.M16.E9
                        E9_CONST_2: Message12.M1.M2.M4.M7.M16.E9
                        E9_CONST_3: Message12.M1.M2.M4.M7.M16.E9
                        E9_CONST_4: Message12.M1.M2.M4.M7.M16.E9
                        E9_CONST_5: Message12.M1.M2.M4.M7.M16.E9
                        class E10(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E10_UNSPECIFIED: _ClassVar[Message12.M1.M2.M4.M7.M16.E10]
                            E10_CONST_1: _ClassVar[Message12.M1.M2.M4.M7.M16.E10]
                            E10_CONST_2: _ClassVar[Message12.M1.M2.M4.M7.M16.E10]
                            E10_CONST_3: _ClassVar[Message12.M1.M2.M4.M7.M16.E10]
                            E10_CONST_4: _ClassVar[Message12.M1.M2.M4.M7.M16.E10]
                            E10_CONST_5: _ClassVar[Message12.M1.M2.M4.M7.M16.E10]
                        E10_UNSPECIFIED: Message12.M1.M2.M4.M7.M16.E10
                        E10_CONST_1: Message12.M1.M2.M4.M7.M16.E10
                        E10_CONST_2: Message12.M1.M2.M4.M7.M16.E10
                        E10_CONST_3: Message12.M1.M2.M4.M7.M16.E10
                        E10_CONST_4: Message12.M1.M2.M4.M7.M16.E10
                        E10_CONST_5: Message12.M1.M2.M4.M7.M16.E10
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
                        f_0: int
                        f_1: Message12.M1.M2.M4.M7.M16.E6
                        f_2: int
                        f_3: int
                        f_4: int
                        f_5: int
                        f_6: Message12.M1.M2.M4.M7.M16.E7
                        f_7: int
                        f_8: int
                        f_9: bytes
                        f_10: bool
                        f_11: bool
                        f_12: float
                        f_13: Message12.M1.M2.M4.M7.M16.E8
                        f_14: _containers.RepeatedScalarFieldContainer[int]
                        f_15: Message12.M1.M2.M4.M7.M16.E9
                        f_16: Message12.M1.M2.M4.M7.M16.E10
                        f_17: int
                        f_18: int
                        f_19: float
                        f_20: int
                        f_21: float
                        f_22: bool
                        f_23: int
                        f_24: _containers.RepeatedScalarFieldContainer[int]
                        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[_Union[Message12.M1.M2.M4.M7.M16.E6, str]] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[_Union[Message12.M1.M2.M4.M7.M16.E7, str]] = ..., f_7: _Optional[int] = ..., f_8: _Optional[int] = ..., f_9: _Optional[bytes] = ..., f_10: _Optional[bool] = ..., f_11: _Optional[bool] = ..., f_12: _Optional[float] = ..., f_13: _Optional[_Union[Message12.M1.M2.M4.M7.M16.E8, str]] = ..., f_14: _Optional[_Iterable[int]] = ..., f_15: _Optional[_Union[Message12.M1.M2.M4.M7.M16.E9, str]] = ..., f_16: _Optional[_Union[Message12.M1.M2.M4.M7.M16.E10, str]] = ..., f_17: _Optional[int] = ..., f_18: _Optional[int] = ..., f_19: _Optional[float] = ..., f_20: _Optional[int] = ..., f_21: _Optional[float] = ..., f_22: _Optional[bool] = ..., f_23: _Optional[int] = ..., f_24: _Optional[_Iterable[int]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    f_0: bytes
                    f_3: Message12.M1.M2.M4.M7.M14
                    f_4: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4.M7.M15]
                    f_6: Message12.M1.M2.M4.M7.M16
                    def __init__(self, f_0: _Optional[bytes] = ..., f_3: _Optional[_Union[Message12.M1.M2.M4.M7.M14, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message12.M1.M2.M4.M7.M15, _Mapping]]] = ..., f_6: _Optional[_Union[Message12.M1.M2.M4.M7.M16, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                f_0: float
                f_2: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4.M7]
                def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Iterable[_Union[Message12.M1.M2.M4.M7, _Mapping]]] = ...) -> None: ...
            class M5(_message.Message):
                __slots__ = ("f_0",)
                F_0_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
            class M6(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_11", "f_17")
                class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E3_UNSPECIFIED: _ClassVar[Message12.M1.M2.M6.E3]
                    E3_CONST_1: _ClassVar[Message12.M1.M2.M6.E3]
                    E3_CONST_2: _ClassVar[Message12.M1.M2.M6.E3]
                    E3_CONST_3: _ClassVar[Message12.M1.M2.M6.E3]
                    E3_CONST_4: _ClassVar[Message12.M1.M2.M6.E3]
                    E3_CONST_5: _ClassVar[Message12.M1.M2.M6.E3]
                E3_UNSPECIFIED: Message12.M1.M2.M6.E3
                E3_CONST_1: Message12.M1.M2.M6.E3
                E3_CONST_2: Message12.M1.M2.M6.E3
                E3_CONST_3: Message12.M1.M2.M6.E3
                E3_CONST_4: Message12.M1.M2.M6.E3
                E3_CONST_5: Message12.M1.M2.M6.E3
                class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E4_UNSPECIFIED: _ClassVar[Message12.M1.M2.M6.E4]
                    E4_CONST_1: _ClassVar[Message12.M1.M2.M6.E4]
                    E4_CONST_2: _ClassVar[Message12.M1.M2.M6.E4]
                    E4_CONST_3: _ClassVar[Message12.M1.M2.M6.E4]
                    E4_CONST_4: _ClassVar[Message12.M1.M2.M6.E4]
                    E4_CONST_5: _ClassVar[Message12.M1.M2.M6.E4]
                E4_UNSPECIFIED: Message12.M1.M2.M6.E4
                E4_CONST_1: Message12.M1.M2.M6.E4
                E4_CONST_2: Message12.M1.M2.M6.E4
                E4_CONST_3: Message12.M1.M2.M6.E4
                E4_CONST_4: Message12.M1.M2.M6.E4
                E4_CONST_5: Message12.M1.M2.M6.E4
                class M11(_message.Message):
                    __slots__ = ("f_0", "f_1")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    f_0: _containers.RepeatedScalarFieldContainer[int]
                    f_1: int
                    def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_1: _Optional[int] = ...) -> None: ...
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
                F_17_FIELD_NUMBER: _ClassVar[int]
                f_0: int
                f_1: int
                f_2: Message12.M1.M2.M6.E3
                f_3: float
                f_4: _containers.RepeatedScalarFieldContainer[Message12.M1.M2.M6.E4]
                f_5: int
                f_6: float
                f_7: str
                f_8: float
                f_9: int
                f_10: float
                f_11: int
                f_17: Message12.M1.M2.M6.M11
                def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message12.M1.M2.M6.E3, str]] = ..., f_3: _Optional[float] = ..., f_4: _Optional[_Iterable[_Union[Message12.M1.M2.M6.E4, str]]] = ..., f_5: _Optional[int] = ..., f_6: _Optional[float] = ..., f_7: _Optional[str] = ..., f_8: _Optional[float] = ..., f_9: _Optional[int] = ..., f_10: _Optional[float] = ..., f_11: _Optional[int] = ..., f_17: _Optional[_Union[Message12.M1.M2.M6.M11, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_1_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            F_4_FIELD_NUMBER: _ClassVar[int]
            F_5_FIELD_NUMBER: _ClassVar[int]
            F_6_FIELD_NUMBER: _ClassVar[int]
            F_10_FIELD_NUMBER: _ClassVar[int]
            F_11_FIELD_NUMBER: _ClassVar[int]
            F_12_FIELD_NUMBER: _ClassVar[int]
            F_13_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_1: str
            f_2: int
            f_3: Message12.M1.M2.E2
            f_4: int
            f_5: _containers.RepeatedScalarFieldContainer[str]
            f_6: int
            f_10: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M3]
            f_11: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M4]
            f_12: Message12.M1.M2.M5
            f_13: _containers.RepeatedCompositeFieldContainer[Message12.M1.M2.M6]
            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[str] = ..., f_2: _Optional[int] = ..., f_3: _Optional[_Union[Message12.M1.M2.E2, str]] = ..., f_4: _Optional[int] = ..., f_5: _Optional[_Iterable[str]] = ..., f_6: _Optional[int] = ..., f_10: _Optional[_Iterable[_Union[Message12.M1.M2.M3, _Mapping]]] = ..., f_11: _Optional[_Iterable[_Union[Message12.M1.M2.M4, _Mapping]]] = ..., f_12: _Optional[_Union[Message12.M1.M2.M5, _Mapping]] = ..., f_13: _Optional[_Iterable[_Union[Message12.M1.M2.M6, _Mapping]]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        f_0: bytes
        f_2: Message12.M1.M2
        def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Union[Message12.M1.M2, _Mapping]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_2_FIELD_NUMBER: _ClassVar[int]
    f_0: Message12.E1
    f_2: Message12.M1
    def __init__(self, f_0: _Optional[_Union[Message12.E1, str]] = ..., f_2: _Optional[_Union[Message12.M1, _Mapping]] = ...) -> None: ...
