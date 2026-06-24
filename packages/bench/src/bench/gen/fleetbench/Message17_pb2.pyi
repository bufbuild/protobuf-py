from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message17(_message.Message):
    __slots__ = ("f_0", "f_2", "f_3", "f_4")
    class M1(_message.Message):
        __slots__ = ("f_0", "f_3", "f_4")
        class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            E1_UNSPECIFIED: _ClassVar[Message17.M1.E1]
            E1_CONST_1: _ClassVar[Message17.M1.E1]
            E1_CONST_2: _ClassVar[Message17.M1.E1]
            E1_CONST_3: _ClassVar[Message17.M1.E1]
            E1_CONST_4: _ClassVar[Message17.M1.E1]
            E1_CONST_5: _ClassVar[Message17.M1.E1]
        E1_UNSPECIFIED: Message17.M1.E1
        E1_CONST_1: Message17.M1.E1
        E1_CONST_2: Message17.M1.E1
        E1_CONST_3: Message17.M1.E1
        E1_CONST_4: Message17.M1.E1
        E1_CONST_5: Message17.M1.E1
        class M5(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
        class M10(_message.Message):
            __slots__ = ("f_0", "f_2")
            class M14(_message.Message):
                __slots__ = ("f_0", "f_3")
                class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E4_UNSPECIFIED: _ClassVar[Message17.M1.M10.M14.E4]
                    E4_CONST_1: _ClassVar[Message17.M1.M10.M14.E4]
                    E4_CONST_2: _ClassVar[Message17.M1.M10.M14.E4]
                    E4_CONST_3: _ClassVar[Message17.M1.M10.M14.E4]
                    E4_CONST_4: _ClassVar[Message17.M1.M10.M14.E4]
                    E4_CONST_5: _ClassVar[Message17.M1.M10.M14.E4]
                E4_UNSPECIFIED: Message17.M1.M10.M14.E4
                E4_CONST_1: Message17.M1.M10.M14.E4
                E4_CONST_2: Message17.M1.M10.M14.E4
                E4_CONST_3: Message17.M1.M10.M14.E4
                E4_CONST_4: Message17.M1.M10.M14.E4
                E4_CONST_5: Message17.M1.M10.M14.E4
                class M26(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class E7(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E7_UNSPECIFIED: _ClassVar[Message17.M1.M10.M14.M26.E7]
                        E7_CONST_1: _ClassVar[Message17.M1.M10.M14.M26.E7]
                        E7_CONST_2: _ClassVar[Message17.M1.M10.M14.M26.E7]
                        E7_CONST_3: _ClassVar[Message17.M1.M10.M14.M26.E7]
                        E7_CONST_4: _ClassVar[Message17.M1.M10.M14.M26.E7]
                        E7_CONST_5: _ClassVar[Message17.M1.M10.M14.M26.E7]
                    E7_UNSPECIFIED: Message17.M1.M10.M14.M26.E7
                    E7_CONST_1: Message17.M1.M10.M14.M26.E7
                    E7_CONST_2: Message17.M1.M10.M14.M26.E7
                    E7_CONST_3: Message17.M1.M10.M14.M26.E7
                    E7_CONST_4: Message17.M1.M10.M14.M26.E7
                    E7_CONST_5: Message17.M1.M10.M14.M26.E7
                    class M40(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_10", "f_16")
                        class M44(_message.Message):
                            __slots__ = ("f_0", "f_2", "f_4")
                            class M51(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_2")
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_2_FIELD_NUMBER: _ClassVar[int]
                                f_0: str
                                f_1: int
                                f_2: int
                                def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ...) -> None: ...
                            class M54(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            f_0: float
                            f_2: Message17.M1.M10.M14.M26.M40.M44.M51
                            f_4: Message17.M1.M10.M14.M26.M40.M44.M54
                            def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message17.M1.M10.M14.M26.M40.M44.M51, _Mapping]] = ..., f_4: _Optional[_Union[Message17.M1.M10.M14.M26.M40.M44.M54, _Mapping]] = ...) -> None: ...
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
                        F_16_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        f_1: bytes
                        f_2: int
                        f_3: float
                        f_4: int
                        f_5: str
                        f_6: int
                        f_7: str
                        f_8: str
                        f_9: int
                        f_10: str
                        f_16: _containers.RepeatedCompositeFieldContainer[Message17.M1.M10.M14.M26.M40.M44]
                        def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[int] = ..., f_3: _Optional[float] = ..., f_4: _Optional[int] = ..., f_5: _Optional[str] = ..., f_6: _Optional[int] = ..., f_7: _Optional[str] = ..., f_8: _Optional[str] = ..., f_9: _Optional[int] = ..., f_10: _Optional[str] = ..., f_16: _Optional[_Iterable[_Union[Message17.M1.M10.M14.M26.M40.M44, _Mapping]]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: Message17.M1.M10.M14.M26.E7
                    f_2: Message17.M1.M10.M14.M26.M40
                    def __init__(self, f_0: _Optional[_Union[Message17.M1.M10.M14.M26.E7, str]] = ..., f_2: _Optional[_Union[Message17.M1.M10.M14.M26.M40, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                f_0: _containers.RepeatedScalarFieldContainer[Message17.M1.M10.M14.E4]
                f_3: Message17.M1.M10.M14.M26
                def __init__(self, f_0: _Optional[_Iterable[_Union[Message17.M1.M10.M14.E4, str]]] = ..., f_3: _Optional[_Union[Message17.M1.M10.M14.M26, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            f_0: bool
            f_2: _containers.RepeatedCompositeFieldContainer[Message17.M1.M10.M14]
            def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Iterable[_Union[Message17.M1.M10.M14, _Mapping]]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        f_0: Message17.M1.E1
        f_3: Message17.M1.M5
        f_4: Message17.M1.M10
        def __init__(self, f_0: _Optional[_Union[Message17.M1.E1, str]] = ..., f_3: _Optional[_Union[Message17.M1.M5, _Mapping]] = ..., f_4: _Optional[_Union[Message17.M1.M10, _Mapping]] = ...) -> None: ...
    class M2(_message.Message):
        __slots__ = ("f_0", "f_2", "f_3", "f_4")
        class M6(_message.Message):
            __slots__ = ("f_0", "f_2", "f_3")
            class M13(_message.Message):
                __slots__ = ("f_0", "f_3", "f_5")
                class M21(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                class M22(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                f_0: float
                f_3: Message17.M2.M6.M13.M21
                f_5: Message17.M2.M6.M13.M22
                def __init__(self, f_0: _Optional[float] = ..., f_3: _Optional[_Union[Message17.M2.M6.M13.M21, _Mapping]] = ..., f_5: _Optional[_Union[Message17.M2.M6.M13.M22, _Mapping]] = ...) -> None: ...
            class M16(_message.Message):
                __slots__ = ("f_0", "f_2", "f_4", "f_5", "f_6")
                class M24(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_1: int
                    f_2: bool
                    def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_2: _Optional[bool] = ...) -> None: ...
                class M25(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_3")
                    class M39(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_1: str
                    f_3: Message17.M2.M6.M16.M25.M39
                    def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[str] = ..., f_3: _Optional[_Union[Message17.M2.M6.M16.M25.M39, _Mapping]] = ...) -> None: ...
                class M27(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                class M28(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_5_FIELD_NUMBER: _ClassVar[int]
                F_6_FIELD_NUMBER: _ClassVar[int]
                f_0: bool
                f_2: _containers.RepeatedCompositeFieldContainer[Message17.M2.M6.M16.M24]
                f_4: _containers.RepeatedCompositeFieldContainer[Message17.M2.M6.M16.M25]
                f_5: Message17.M2.M6.M16.M27
                f_6: Message17.M2.M6.M16.M28
                def __init__(self, f_0: _Optional[bool] = ..., f_2: _Optional[_Iterable[_Union[Message17.M2.M6.M16.M24, _Mapping]]] = ..., f_4: _Optional[_Iterable[_Union[Message17.M2.M6.M16.M25, _Mapping]]] = ..., f_5: _Optional[_Union[Message17.M2.M6.M16.M27, _Mapping]] = ..., f_6: _Optional[_Union[Message17.M2.M6.M16.M28, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            f_0: _containers.RepeatedScalarFieldContainer[float]
            f_2: Message17.M2.M6.M13
            f_3: _containers.RepeatedCompositeFieldContainer[Message17.M2.M6.M16]
            def __init__(self, f_0: _Optional[_Iterable[float]] = ..., f_2: _Optional[_Union[Message17.M2.M6.M13, _Mapping]] = ..., f_3: _Optional[_Iterable[_Union[Message17.M2.M6.M16, _Mapping]]] = ...) -> None: ...
        class M8(_message.Message):
            __slots__ = ("f_0", "f_1", "f_2")
            class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E3_UNSPECIFIED: _ClassVar[Message17.M2.M8.E3]
                E3_CONST_1: _ClassVar[Message17.M2.M8.E3]
                E3_CONST_2: _ClassVar[Message17.M2.M8.E3]
                E3_CONST_3: _ClassVar[Message17.M2.M8.E3]
                E3_CONST_4: _ClassVar[Message17.M2.M8.E3]
                E3_CONST_5: _ClassVar[Message17.M2.M8.E3]
            E3_UNSPECIFIED: Message17.M2.M8.E3
            E3_CONST_1: Message17.M2.M8.E3
            E3_CONST_2: Message17.M2.M8.E3
            E3_CONST_3: Message17.M2.M8.E3
            E3_CONST_4: Message17.M2.M8.E3
            E3_CONST_5: Message17.M2.M8.E3
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_1_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            f_0: Message17.M2.M8.E3
            f_1: int
            f_2: int
            def __init__(self, f_0: _Optional[_Union[Message17.M2.M8.E3, str]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ...) -> None: ...
        class M11(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            def __init__(self, f_0: _Optional[int] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        f_0: _containers.RepeatedScalarFieldContainer[int]
        f_2: Message17.M2.M6
        f_3: Message17.M2.M8
        f_4: _containers.RepeatedCompositeFieldContainer[Message17.M2.M11]
        def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_2: _Optional[_Union[Message17.M2.M6, _Mapping]] = ..., f_3: _Optional[_Union[Message17.M2.M8, _Mapping]] = ..., f_4: _Optional[_Iterable[_Union[Message17.M2.M11, _Mapping]]] = ...) -> None: ...
    class M3(_message.Message):
        __slots__ = ("f_0", "f_1", "f_2", "f_4", "f_5", "f_6")
        class M4(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
        class M7(_message.Message):
            __slots__ = ("f_0",)
            class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                E2_UNSPECIFIED: _ClassVar[Message17.M3.M7.E2]
                E2_CONST_1: _ClassVar[Message17.M3.M7.E2]
                E2_CONST_2: _ClassVar[Message17.M3.M7.E2]
                E2_CONST_3: _ClassVar[Message17.M3.M7.E2]
                E2_CONST_4: _ClassVar[Message17.M3.M7.E2]
                E2_CONST_5: _ClassVar[Message17.M3.M7.E2]
            E2_UNSPECIFIED: Message17.M3.M7.E2
            E2_CONST_1: Message17.M3.M7.E2
            E2_CONST_2: Message17.M3.M7.E2
            E2_CONST_3: Message17.M3.M7.E2
            E2_CONST_4: Message17.M3.M7.E2
            E2_CONST_5: Message17.M3.M7.E2
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: Message17.M3.M7.E2
            def __init__(self, f_0: _Optional[_Union[Message17.M3.M7.E2, str]] = ...) -> None: ...
        class M9(_message.Message):
            __slots__ = ("f_0", "f_2", "f_3")
            class M12(_message.Message):
                __slots__ = ("f_0", "f_3", "f_4", "f_6", "f_7", "f_8")
                class M18(_message.Message):
                    __slots__ = ("f_0", "f_1")
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_1: str
                    def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[str] = ...) -> None: ...
                class M19(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                class M20(_message.Message):
                    __slots__ = ("f_0", "f_2", "f_3")
                    class M31(_message.Message):
                        __slots__ = ("f_0",)
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        f_0: bool
                        def __init__(self, f_0: _Optional[bool] = ...) -> None: ...
                    class M35(_message.Message):
                        __slots__ = ("f_0", "f_2")
                        class M42(_message.Message):
                            __slots__ = ("f_0", "f_3", "f_4")
                            class M55(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                            class M56(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_3_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_3: Message17.M3.M9.M12.M20.M35.M42.M55
                            f_4: Message17.M3.M9.M12.M20.M35.M42.M56
                            def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Union[Message17.M3.M9.M12.M20.M35.M42.M55, _Mapping]] = ..., f_4: _Optional[_Union[Message17.M3.M9.M12.M20.M35.M42.M56, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_2: Message17.M3.M9.M12.M20.M35.M42
                        def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12.M20.M35.M42, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_2: Message17.M3.M9.M12.M20.M31
                    f_3: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M20.M35]
                    def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12.M20.M31, _Mapping]] = ..., f_3: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M20.M35, _Mapping]]] = ...) -> None: ...
                class M29(_message.Message):
                    __slots__ = ("f_0", "f_4", "f_6")
                    class M33(_message.Message):
                        __slots__ = ("f_0", "f_4")
                        class M48(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2")
                            class E11(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E11_UNSPECIFIED: _ClassVar[Message17.M3.M9.M12.M29.M33.M48.E11]
                                E11_CONST_1: _ClassVar[Message17.M3.M9.M12.M29.M33.M48.E11]
                                E11_CONST_2: _ClassVar[Message17.M3.M9.M12.M29.M33.M48.E11]
                                E11_CONST_3: _ClassVar[Message17.M3.M9.M12.M29.M33.M48.E11]
                                E11_CONST_4: _ClassVar[Message17.M3.M9.M12.M29.M33.M48.E11]
                                E11_CONST_5: _ClassVar[Message17.M3.M9.M12.M29.M33.M48.E11]
                            E11_UNSPECIFIED: Message17.M3.M9.M12.M29.M33.M48.E11
                            E11_CONST_1: Message17.M3.M9.M12.M29.M33.M48.E11
                            E11_CONST_2: Message17.M3.M9.M12.M29.M33.M48.E11
                            E11_CONST_3: Message17.M3.M9.M12.M29.M33.M48.E11
                            E11_CONST_4: Message17.M3.M9.M12.M29.M33.M48.E11
                            E11_CONST_5: Message17.M3.M9.M12.M29.M33.M48.E11
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: Message17.M3.M9.M12.M29.M33.M48.E11
                            f_1: bytes
                            f_2: bytes
                            def __init__(self, f_0: _Optional[_Union[Message17.M3.M9.M12.M29.M33.M48.E11, str]] = ..., f_1: _Optional[bytes] = ..., f_2: _Optional[bytes] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_4: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M29.M33.M48]
                        def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M29.M33.M48, _Mapping]]] = ...) -> None: ...
                    class M37(_message.Message):
                        __slots__ = ("f_0", "f_4")
                        class M41(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2")
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_1: int
                            f_2: _containers.RepeatedScalarFieldContainer[bytes]
                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Iterable[bytes]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_4: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M29.M37.M41]
                        def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M29.M37.M41, _Mapping]]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_4: Message17.M3.M9.M12.M29.M33
                    f_6: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M29.M37]
                    def __init__(self, f_0: _Optional[str] = ..., f_4: _Optional[_Union[Message17.M3.M9.M12.M29.M33, _Mapping]] = ..., f_6: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M29.M37, _Mapping]]] = ...) -> None: ...
                class M30(_message.Message):
                    __slots__ = ("f_0", "f_2")
                    class M38(_message.Message):
                        __slots__ = ("f_0", "f_3")
                        class E9(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E9_UNSPECIFIED: _ClassVar[Message17.M3.M9.M12.M30.M38.E9]
                            E9_CONST_1: _ClassVar[Message17.M3.M9.M12.M30.M38.E9]
                            E9_CONST_2: _ClassVar[Message17.M3.M9.M12.M30.M38.E9]
                            E9_CONST_3: _ClassVar[Message17.M3.M9.M12.M30.M38.E9]
                            E9_CONST_4: _ClassVar[Message17.M3.M9.M12.M30.M38.E9]
                            E9_CONST_5: _ClassVar[Message17.M3.M9.M12.M30.M38.E9]
                        E9_UNSPECIFIED: Message17.M3.M9.M12.M30.M38.E9
                        E9_CONST_1: Message17.M3.M9.M12.M30.M38.E9
                        E9_CONST_2: Message17.M3.M9.M12.M30.M38.E9
                        E9_CONST_3: Message17.M3.M9.M12.M30.M38.E9
                        E9_CONST_4: Message17.M3.M9.M12.M30.M38.E9
                        E9_CONST_5: Message17.M3.M9.M12.M30.M38.E9
                        class M47(_message.Message):
                            __slots__ = ("f_0", "f_2")
                            class M52(_message.Message):
                                __slots__ = ("f_0", "f_3")
                                class M61(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_2", "f_6", "f_8")
                                    class E15(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E15_UNSPECIFIED: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15]
                                        E15_CONST_1: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15]
                                        E15_CONST_2: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15]
                                        E15_CONST_3: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15]
                                        E15_CONST_4: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15]
                                        E15_CONST_5: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15]
                                    E15_UNSPECIFIED: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    E15_CONST_1: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    E15_CONST_2: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    E15_CONST_3: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    E15_CONST_4: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    E15_CONST_5: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    class M62(_message.Message):
                                        __slots__ = ("f_0", "f_1")
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_1_FIELD_NUMBER: _ClassVar[int]
                                        f_0: str
                                        f_1: float
                                        def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[float] = ...) -> None: ...
                                    class M63(_message.Message):
                                        __slots__ = ("f_0", "f_2", "f_3")
                                        class M65(_message.Message):
                                            __slots__ = ("f_0",)
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            f_0: bytes
                                            def __init__(self, f_0: _Optional[bytes] = ...) -> None: ...
                                        class M66(_message.Message):
                                            __slots__ = ("f_0", "f_5")
                                            class M67(_message.Message):
                                                __slots__ = ("f_0", "f_3")
                                                class E16(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                                    __slots__ = ()
                                                    E16_UNSPECIFIED: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16]
                                                    E16_CONST_1: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16]
                                                    E16_CONST_2: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16]
                                                    E16_CONST_3: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16]
                                                    E16_CONST_4: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16]
                                                    E16_CONST_5: _ClassVar[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16]
                                                E16_UNSPECIFIED: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                E16_CONST_1: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                E16_CONST_2: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                E16_CONST_3: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                E16_CONST_4: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                E16_CONST_5: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                class M68(_message.Message):
                                                    __slots__ = ("f_0", "f_2")
                                                    class M69(_message.Message):
                                                        __slots__ = ("f_0", "f_3")
                                                        class M70(_message.Message):
                                                            __slots__ = ("f_0", "f_1", "f_4")
                                                            class M71(_message.Message):
                                                                __slots__ = ("f_0",)
                                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                                f_0: str
                                                                def __init__(self, f_0: _Optional[str] = ...) -> None: ...
                                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                                            F_1_FIELD_NUMBER: _ClassVar[int]
                                                            F_4_FIELD_NUMBER: _ClassVar[int]
                                                            f_0: int
                                                            f_1: str
                                                            f_4: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68.M69.M70.M71
                                                            def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[str] = ..., f_4: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68.M69.M70.M71, _Mapping]] = ...) -> None: ...
                                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                                        F_3_FIELD_NUMBER: _ClassVar[int]
                                                        f_0: int
                                                        f_3: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68.M69.M70]
                                                        def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68.M69.M70, _Mapping]]] = ...) -> None: ...
                                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                                    f_0: int
                                                    f_2: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68.M69
                                                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68.M69, _Mapping]] = ...) -> None: ...
                                                F_0_FIELD_NUMBER: _ClassVar[int]
                                                F_3_FIELD_NUMBER: _ClassVar[int]
                                                f_0: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16
                                                f_3: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68]
                                                def __init__(self, f_0: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.E16, str]] = ..., f_3: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67.M68, _Mapping]]] = ...) -> None: ...
                                            F_0_FIELD_NUMBER: _ClassVar[int]
                                            F_5_FIELD_NUMBER: _ClassVar[int]
                                            f_0: bool
                                            f_5: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67
                                            def __init__(self, f_0: _Optional[bool] = ..., f_5: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66.M67, _Mapping]] = ...) -> None: ...
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        F_2_FIELD_NUMBER: _ClassVar[int]
                                        F_3_FIELD_NUMBER: _ClassVar[int]
                                        f_0: str
                                        f_2: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M65
                                        f_3: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66
                                        def __init__(self, f_0: _Optional[str] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M65, _Mapping]] = ..., f_3: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63.M66, _Mapping]] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    F_6_FIELD_NUMBER: _ClassVar[int]
                                    F_8_FIELD_NUMBER: _ClassVar[int]
                                    f_0: str
                                    f_1: Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15
                                    f_2: int
                                    f_6: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M62
                                    f_8: Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63
                                    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.E15, str]] = ..., f_2: _Optional[int] = ..., f_6: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M62, _Mapping]] = ..., f_8: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61.M63, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                f_0: _containers.RepeatedScalarFieldContainer[int]
                                f_3: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M30.M38.M47.M52.M61]
                                def __init__(self, f_0: _Optional[_Iterable[int]] = ..., f_3: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M30.M38.M47.M52.M61, _Mapping]]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: float
                            f_2: Message17.M3.M9.M12.M30.M38.M47.M52
                            def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47.M52, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        f_0: Message17.M3.M9.M12.M30.M38.E9
                        f_3: Message17.M3.M9.M12.M30.M38.M47
                        def __init__(self, f_0: _Optional[_Union[Message17.M3.M9.M12.M30.M38.E9, str]] = ..., f_3: _Optional[_Union[Message17.M3.M9.M12.M30.M38.M47, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_2: Message17.M3.M9.M12.M30.M38
                    def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12.M30.M38, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                F_4_FIELD_NUMBER: _ClassVar[int]
                F_6_FIELD_NUMBER: _ClassVar[int]
                F_7_FIELD_NUMBER: _ClassVar[int]
                F_8_FIELD_NUMBER: _ClassVar[int]
                f_0: str
                f_3: Message17.M3.M9.M12.M18
                f_4: Message17.M3.M9.M12.M19
                f_6: Message17.M3.M9.M12.M20
                f_7: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M29]
                f_8: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M12.M30]
                def __init__(self, f_0: _Optional[str] = ..., f_3: _Optional[_Union[Message17.M3.M9.M12.M18, _Mapping]] = ..., f_4: _Optional[_Union[Message17.M3.M9.M12.M19, _Mapping]] = ..., f_6: _Optional[_Union[Message17.M3.M9.M12.M20, _Mapping]] = ..., f_7: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M29, _Mapping]]] = ..., f_8: _Optional[_Iterable[_Union[Message17.M3.M9.M12.M30, _Mapping]]] = ...) -> None: ...
            class M15(_message.Message):
                __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_9", "f_14", "f_15")
                class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E5_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.E5]
                    E5_CONST_1: _ClassVar[Message17.M3.M9.M15.E5]
                    E5_CONST_2: _ClassVar[Message17.M3.M9.M15.E5]
                    E5_CONST_3: _ClassVar[Message17.M3.M9.M15.E5]
                    E5_CONST_4: _ClassVar[Message17.M3.M9.M15.E5]
                    E5_CONST_5: _ClassVar[Message17.M3.M9.M15.E5]
                E5_UNSPECIFIED: Message17.M3.M9.M15.E5
                E5_CONST_1: Message17.M3.M9.M15.E5
                E5_CONST_2: Message17.M3.M9.M15.E5
                E5_CONST_3: Message17.M3.M9.M15.E5
                E5_CONST_4: Message17.M3.M9.M15.E5
                E5_CONST_5: Message17.M3.M9.M15.E5
                class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E6_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.E6]
                    E6_CONST_1: _ClassVar[Message17.M3.M9.M15.E6]
                    E6_CONST_2: _ClassVar[Message17.M3.M9.M15.E6]
                    E6_CONST_3: _ClassVar[Message17.M3.M9.M15.E6]
                    E6_CONST_4: _ClassVar[Message17.M3.M9.M15.E6]
                    E6_CONST_5: _ClassVar[Message17.M3.M9.M15.E6]
                E6_UNSPECIFIED: Message17.M3.M9.M15.E6
                E6_CONST_1: Message17.M3.M9.M15.E6
                E6_CONST_2: Message17.M3.M9.M15.E6
                E6_CONST_3: Message17.M3.M9.M15.E6
                E6_CONST_4: Message17.M3.M9.M15.E6
                E6_CONST_5: Message17.M3.M9.M15.E6
                class M17(_message.Message):
                    __slots__ = ("f_0", "f_3")
                    class M36(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_5", "f_6")
                        class M43(_message.Message):
                            __slots__ = ("f_0", "f_1", "f_2")
                            class E10(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E10_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.M17.M36.M43.E10]
                                E10_CONST_1: _ClassVar[Message17.M3.M9.M15.M17.M36.M43.E10]
                                E10_CONST_2: _ClassVar[Message17.M3.M9.M15.M17.M36.M43.E10]
                                E10_CONST_3: _ClassVar[Message17.M3.M9.M15.M17.M36.M43.E10]
                                E10_CONST_4: _ClassVar[Message17.M3.M9.M15.M17.M36.M43.E10]
                                E10_CONST_5: _ClassVar[Message17.M3.M9.M15.M17.M36.M43.E10]
                            E10_UNSPECIFIED: Message17.M3.M9.M15.M17.M36.M43.E10
                            E10_CONST_1: Message17.M3.M9.M15.M17.M36.M43.E10
                            E10_CONST_2: Message17.M3.M9.M15.M17.M36.M43.E10
                            E10_CONST_3: Message17.M3.M9.M15.M17.M36.M43.E10
                            E10_CONST_4: Message17.M3.M9.M15.M17.M36.M43.E10
                            E10_CONST_5: Message17.M3.M9.M15.M17.M36.M43.E10
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_1_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: float
                            f_1: int
                            f_2: Message17.M3.M9.M15.M17.M36.M43.E10
                            def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_2: _Optional[_Union[Message17.M3.M9.M15.M17.M36.M43.E10, str]] = ...) -> None: ...
                        class M45(_message.Message):
                            __slots__ = ("f_0", "f_2", "f_4")
                            class M49(_message.Message):
                                __slots__ = ("f_0",)
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                f_0: int
                                def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                            class M50(_message.Message):
                                __slots__ = ("f_0", "f_3", "f_4", "f_5")
                                class E12(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E12_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.E12]
                                    E12_CONST_1: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.E12]
                                    E12_CONST_2: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.E12]
                                    E12_CONST_3: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.E12]
                                    E12_CONST_4: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.E12]
                                    E12_CONST_5: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.E12]
                                E12_UNSPECIFIED: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                E12_CONST_1: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                E12_CONST_2: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                E12_CONST_3: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                E12_CONST_4: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                E12_CONST_5: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                class M57(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: float
                                    def __init__(self, f_0: _Optional[float] = ...) -> None: ...
                                class M58(_message.Message):
                                    __slots__ = ("f_0",)
                                    class E14(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E14_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14]
                                        E14_CONST_1: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14]
                                        E14_CONST_2: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14]
                                        E14_CONST_3: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14]
                                        E14_CONST_4: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14]
                                        E14_CONST_5: _ClassVar[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14]
                                    E14_UNSPECIFIED: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    E14_CONST_1: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    E14_CONST_2: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    E14_CONST_3: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    E14_CONST_4: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    E14_CONST_5: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14
                                    def __init__(self, f_0: _Optional[_Union[Message17.M3.M9.M15.M17.M36.M45.M50.M58.E14, str]] = ...) -> None: ...
                                class M59(_message.Message):
                                    __slots__ = ("f_0",)
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    f_0: int
                                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                F_4_FIELD_NUMBER: _ClassVar[int]
                                F_5_FIELD_NUMBER: _ClassVar[int]
                                f_0: Message17.M3.M9.M15.M17.M36.M45.M50.E12
                                f_3: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M17.M36.M45.M50.M57]
                                f_4: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M17.M36.M45.M50.M58]
                                f_5: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M17.M36.M45.M50.M59]
                                def __init__(self, f_0: _Optional[_Union[Message17.M3.M9.M15.M17.M36.M45.M50.E12, str]] = ..., f_3: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M17.M36.M45.M50.M57, _Mapping]]] = ..., f_4: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M17.M36.M45.M50.M58, _Mapping]]] = ..., f_5: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M17.M36.M45.M50.M59, _Mapping]]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            F_4_FIELD_NUMBER: _ClassVar[int]
                            f_0: int
                            f_2: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M17.M36.M45.M49]
                            f_4: Message17.M3.M9.M15.M17.M36.M45.M50
                            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M17.M36.M45.M49, _Mapping]]] = ..., f_4: _Optional[_Union[Message17.M3.M9.M15.M17.M36.M45.M50, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_5_FIELD_NUMBER: _ClassVar[int]
                        F_6_FIELD_NUMBER: _ClassVar[int]
                        f_0: str
                        f_1: int
                        f_5: Message17.M3.M9.M15.M17.M36.M43
                        f_6: Message17.M3.M9.M15.M17.M36.M45
                        def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_5: _Optional[_Union[Message17.M3.M9.M15.M17.M36.M43, _Mapping]] = ..., f_6: _Optional[_Union[Message17.M3.M9.M15.M17.M36.M45, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    f_0: float
                    f_3: Message17.M3.M9.M15.M17.M36
                    def __init__(self, f_0: _Optional[float] = ..., f_3: _Optional[_Union[Message17.M3.M9.M15.M17.M36, _Mapping]] = ...) -> None: ...
                class M23(_message.Message):
                    __slots__ = ("f_0", "f_3", "f_6")
                    class M32(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2")
                        class E8(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                            __slots__ = ()
                            E8_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.M23.M32.E8]
                            E8_CONST_1: _ClassVar[Message17.M3.M9.M15.M23.M32.E8]
                            E8_CONST_2: _ClassVar[Message17.M3.M9.M15.M23.M32.E8]
                            E8_CONST_3: _ClassVar[Message17.M3.M9.M15.M23.M32.E8]
                            E8_CONST_4: _ClassVar[Message17.M3.M9.M15.M23.M32.E8]
                            E8_CONST_5: _ClassVar[Message17.M3.M9.M15.M23.M32.E8]
                        E8_UNSPECIFIED: Message17.M3.M9.M15.M23.M32.E8
                        E8_CONST_1: Message17.M3.M9.M15.M23.M32.E8
                        E8_CONST_2: Message17.M3.M9.M15.M23.M32.E8
                        E8_CONST_3: Message17.M3.M9.M15.M23.M32.E8
                        E8_CONST_4: Message17.M3.M9.M15.M23.M32.E8
                        E8_CONST_5: Message17.M3.M9.M15.M23.M32.E8
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        f_0: _containers.RepeatedScalarFieldContainer[Message17.M3.M9.M15.M23.M32.E8]
                        f_1: int
                        f_2: int
                        def __init__(self, f_0: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M23.M32.E8, str]]] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ...) -> None: ...
                    class M34(_message.Message):
                        __slots__ = ("f_0", "f_4")
                        class M46(_message.Message):
                            __slots__ = ("f_0", "f_5")
                            class M53(_message.Message):
                                __slots__ = ("f_0", "f_3")
                                class E13(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                    __slots__ = ()
                                    E13_UNSPECIFIED: _ClassVar[Message17.M3.M9.M15.M23.M34.M46.M53.E13]
                                    E13_CONST_1: _ClassVar[Message17.M3.M9.M15.M23.M34.M46.M53.E13]
                                    E13_CONST_2: _ClassVar[Message17.M3.M9.M15.M23.M34.M46.M53.E13]
                                    E13_CONST_3: _ClassVar[Message17.M3.M9.M15.M23.M34.M46.M53.E13]
                                    E13_CONST_4: _ClassVar[Message17.M3.M9.M15.M23.M34.M46.M53.E13]
                                    E13_CONST_5: _ClassVar[Message17.M3.M9.M15.M23.M34.M46.M53.E13]
                                E13_UNSPECIFIED: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                E13_CONST_1: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                E13_CONST_2: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                E13_CONST_3: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                E13_CONST_4: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                E13_CONST_5: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                class M60(_message.Message):
                                    __slots__ = ("f_0", "f_2")
                                    class M64(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_2_FIELD_NUMBER: _ClassVar[int]
                                    f_0: float
                                    f_2: Message17.M3.M9.M15.M23.M34.M46.M53.M60.M64
                                    def __init__(self, f_0: _Optional[float] = ..., f_2: _Optional[_Union[Message17.M3.M9.M15.M23.M34.M46.M53.M60.M64, _Mapping]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                f_0: Message17.M3.M9.M15.M23.M34.M46.M53.E13
                                f_3: Message17.M3.M9.M15.M23.M34.M46.M53.M60
                                def __init__(self, f_0: _Optional[_Union[Message17.M3.M9.M15.M23.M34.M46.M53.E13, str]] = ..., f_3: _Optional[_Union[Message17.M3.M9.M15.M23.M34.M46.M53.M60, _Mapping]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_5_FIELD_NUMBER: _ClassVar[int]
                            f_0: bytes
                            f_5: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M23.M34.M46.M53]
                            def __init__(self, f_0: _Optional[bytes] = ..., f_5: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M23.M34.M46.M53, _Mapping]]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_4: Message17.M3.M9.M15.M23.M34.M46
                        def __init__(self, f_0: _Optional[int] = ..., f_4: _Optional[_Union[Message17.M3.M9.M15.M23.M34.M46, _Mapping]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    f_3: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M23.M32]
                    f_6: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M23.M34]
                    def __init__(self, f_0: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M23.M32, _Mapping]]] = ..., f_6: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M23.M34, _Mapping]]] = ...) -> None: ...
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
                F_15_FIELD_NUMBER: _ClassVar[int]
                f_0: bool
                f_1: int
                f_2: int
                f_3: int
                f_4: int
                f_5: int
                f_6: Message17.M3.M9.M15.E5
                f_7: bytes
                f_8: int
                f_9: Message17.M3.M9.M15.E6
                f_14: _containers.RepeatedCompositeFieldContainer[Message17.M3.M9.M15.M17]
                f_15: Message17.M3.M9.M15.M23
                def __init__(self, f_0: _Optional[bool] = ..., f_1: _Optional[int] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[_Union[Message17.M3.M9.M15.E5, str]] = ..., f_7: _Optional[bytes] = ..., f_8: _Optional[int] = ..., f_9: _Optional[_Union[Message17.M3.M9.M15.E6, str]] = ..., f_14: _Optional[_Iterable[_Union[Message17.M3.M9.M15.M17, _Mapping]]] = ..., f_15: _Optional[_Union[Message17.M3.M9.M15.M23, _Mapping]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            f_0: int
            f_2: Message17.M3.M9.M12
            f_3: Message17.M3.M9.M15
            def __init__(self, f_0: _Optional[int] = ..., f_2: _Optional[_Union[Message17.M3.M9.M12, _Mapping]] = ..., f_3: _Optional[_Union[Message17.M3.M9.M15, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_1_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        F_5_FIELD_NUMBER: _ClassVar[int]
        F_6_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_1: float
        f_2: str
        f_4: Message17.M3.M4
        f_5: Message17.M3.M7
        f_6: Message17.M3.M9
        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[float] = ..., f_2: _Optional[str] = ..., f_4: _Optional[_Union[Message17.M3.M4, _Mapping]] = ..., f_5: _Optional[_Union[Message17.M3.M7, _Mapping]] = ..., f_6: _Optional[_Union[Message17.M3.M9, _Mapping]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_2_FIELD_NUMBER: _ClassVar[int]
    F_3_FIELD_NUMBER: _ClassVar[int]
    F_4_FIELD_NUMBER: _ClassVar[int]
    f_0: bytes
    f_2: _containers.RepeatedCompositeFieldContainer[Message17.M1]
    f_3: _containers.RepeatedCompositeFieldContainer[Message17.M2]
    f_4: Message17.M3
    def __init__(self, f_0: _Optional[bytes] = ..., f_2: _Optional[_Iterable[_Union[Message17.M1, _Mapping]]] = ..., f_3: _Optional[_Iterable[_Union[Message17.M2, _Mapping]]] = ..., f_4: _Optional[_Union[Message17.M3, _Mapping]] = ...) -> None: ...
