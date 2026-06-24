from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Message6(_message.Message):
    __slots__ = ("f_0", "f_1", "f_2", "f_5")
    class M1(_message.Message):
        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_8", "f_11")
        class M2(_message.Message):
            __slots__ = ("f_0",)
            F_0_FIELD_NUMBER: _ClassVar[int]
            f_0: str
            def __init__(self, f_0: _Optional[str] = ...) -> None: ...
        class M3(_message.Message):
            __slots__ = ("f_0", "f_2", "f_3")
            class M4(_message.Message):
                __slots__ = ("f_0", "f_2")
                class E1(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                    __slots__ = ()
                    E1_UNSPECIFIED: _ClassVar[Message6.M1.M3.M4.E1]
                    E1_CONST_1: _ClassVar[Message6.M1.M3.M4.E1]
                    E1_CONST_2: _ClassVar[Message6.M1.M3.M4.E1]
                    E1_CONST_3: _ClassVar[Message6.M1.M3.M4.E1]
                    E1_CONST_4: _ClassVar[Message6.M1.M3.M4.E1]
                    E1_CONST_5: _ClassVar[Message6.M1.M3.M4.E1]
                E1_UNSPECIFIED: Message6.M1.M3.M4.E1
                E1_CONST_1: Message6.M1.M3.M4.E1
                E1_CONST_2: Message6.M1.M3.M4.E1
                E1_CONST_3: Message6.M1.M3.M4.E1
                E1_CONST_4: Message6.M1.M3.M4.E1
                E1_CONST_5: Message6.M1.M3.M4.E1
                class M6(_message.Message):
                    __slots__ = ("f_0",)
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    f_0: int
                    def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_2_FIELD_NUMBER: _ClassVar[int]
                f_0: Message6.M1.M3.M4.E1
                f_2: Message6.M1.M3.M4.M6
                def __init__(self, f_0: _Optional[_Union[Message6.M1.M3.M4.E1, str]] = ..., f_2: _Optional[_Union[Message6.M1.M3.M4.M6, _Mapping]] = ...) -> None: ...
            class M5(_message.Message):
                __slots__ = ("f_0", "f_3")
                class M7(_message.Message):
                    __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_5", "f_6", "f_7", "f_8", "f_12")
                    class E2(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E2_UNSPECIFIED: _ClassVar[Message6.M1.M3.M5.M7.E2]
                        E2_CONST_1: _ClassVar[Message6.M1.M3.M5.M7.E2]
                        E2_CONST_2: _ClassVar[Message6.M1.M3.M5.M7.E2]
                        E2_CONST_3: _ClassVar[Message6.M1.M3.M5.M7.E2]
                        E2_CONST_4: _ClassVar[Message6.M1.M3.M5.M7.E2]
                        E2_CONST_5: _ClassVar[Message6.M1.M3.M5.M7.E2]
                    E2_UNSPECIFIED: Message6.M1.M3.M5.M7.E2
                    E2_CONST_1: Message6.M1.M3.M5.M7.E2
                    E2_CONST_2: Message6.M1.M3.M5.M7.E2
                    E2_CONST_3: Message6.M1.M3.M5.M7.E2
                    E2_CONST_4: Message6.M1.M3.M5.M7.E2
                    E2_CONST_5: Message6.M1.M3.M5.M7.E2
                    class E3(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                        __slots__ = ()
                        E3_UNSPECIFIED: _ClassVar[Message6.M1.M3.M5.M7.E3]
                        E3_CONST_1: _ClassVar[Message6.M1.M3.M5.M7.E3]
                        E3_CONST_2: _ClassVar[Message6.M1.M3.M5.M7.E3]
                        E3_CONST_3: _ClassVar[Message6.M1.M3.M5.M7.E3]
                        E3_CONST_4: _ClassVar[Message6.M1.M3.M5.M7.E3]
                        E3_CONST_5: _ClassVar[Message6.M1.M3.M5.M7.E3]
                    E3_UNSPECIFIED: Message6.M1.M3.M5.M7.E3
                    E3_CONST_1: Message6.M1.M3.M5.M7.E3
                    E3_CONST_2: Message6.M1.M3.M5.M7.E3
                    E3_CONST_3: Message6.M1.M3.M5.M7.E3
                    E3_CONST_4: Message6.M1.M3.M5.M7.E3
                    E3_CONST_5: Message6.M1.M3.M5.M7.E3
                    class M8(_message.Message):
                        __slots__ = ("f_0", "f_1", "f_2", "f_3", "f_4", "f_9", "f_10")
                        class M9(_message.Message):
                            __slots__ = ("f_0",)
                            class E4(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E4_UNSPECIFIED: _ClassVar[Message6.M1.M3.M5.M7.M8.M9.E4]
                                E4_CONST_1: _ClassVar[Message6.M1.M3.M5.M7.M8.M9.E4]
                                E4_CONST_2: _ClassVar[Message6.M1.M3.M5.M7.M8.M9.E4]
                                E4_CONST_3: _ClassVar[Message6.M1.M3.M5.M7.M8.M9.E4]
                                E4_CONST_4: _ClassVar[Message6.M1.M3.M5.M7.M8.M9.E4]
                                E4_CONST_5: _ClassVar[Message6.M1.M3.M5.M7.M8.M9.E4]
                            E4_UNSPECIFIED: Message6.M1.M3.M5.M7.M8.M9.E4
                            E4_CONST_1: Message6.M1.M3.M5.M7.M8.M9.E4
                            E4_CONST_2: Message6.M1.M3.M5.M7.M8.M9.E4
                            E4_CONST_3: Message6.M1.M3.M5.M7.M8.M9.E4
                            E4_CONST_4: Message6.M1.M3.M5.M7.M8.M9.E4
                            E4_CONST_5: Message6.M1.M3.M5.M7.M8.M9.E4
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            f_0: Message6.M1.M3.M5.M7.M8.M9.E4
                            def __init__(self, f_0: _Optional[_Union[Message6.M1.M3.M5.M7.M8.M9.E4, str]] = ...) -> None: ...
                        class M10(_message.Message):
                            __slots__ = ("f_0", "f_2")
                            class E5(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                __slots__ = ()
                                E5_UNSPECIFIED: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.E5]
                                E5_CONST_1: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.E5]
                                E5_CONST_2: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.E5]
                                E5_CONST_3: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.E5]
                                E5_CONST_4: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.E5]
                                E5_CONST_5: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.E5]
                            E5_UNSPECIFIED: Message6.M1.M3.M5.M7.M8.M10.E5
                            E5_CONST_1: Message6.M1.M3.M5.M7.M8.M10.E5
                            E5_CONST_2: Message6.M1.M3.M5.M7.M8.M10.E5
                            E5_CONST_3: Message6.M1.M3.M5.M7.M8.M10.E5
                            E5_CONST_4: Message6.M1.M3.M5.M7.M8.M10.E5
                            E5_CONST_5: Message6.M1.M3.M5.M7.M8.M10.E5
                            class M11(_message.Message):
                                __slots__ = ("f_0", "f_1", "f_3")
                                class M12(_message.Message):
                                    __slots__ = ("f_0", "f_1", "f_4")
                                    class E6(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                                        __slots__ = ()
                                        E6_UNSPECIFIED: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6]
                                        E6_CONST_1: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6]
                                        E6_CONST_2: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6]
                                        E6_CONST_3: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6]
                                        E6_CONST_4: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6]
                                        E6_CONST_5: _ClassVar[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6]
                                    E6_UNSPECIFIED: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    E6_CONST_1: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    E6_CONST_2: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    E6_CONST_3: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    E6_CONST_4: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    E6_CONST_5: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    class M13(_message.Message):
                                        __slots__ = ("f_0",)
                                        F_0_FIELD_NUMBER: _ClassVar[int]
                                        f_0: int
                                        def __init__(self, f_0: _Optional[int] = ...) -> None: ...
                                    F_0_FIELD_NUMBER: _ClassVar[int]
                                    F_1_FIELD_NUMBER: _ClassVar[int]
                                    F_4_FIELD_NUMBER: _ClassVar[int]
                                    f_0: str
                                    f_1: Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
                                    f_4: _containers.RepeatedCompositeFieldContainer[Message6.M1.M3.M5.M7.M8.M10.M11.M12.M13]
                                    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[_Union[Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6, str]] = ..., f_4: _Optional[_Iterable[_Union[Message6.M1.M3.M5.M7.M8.M10.M11.M12.M13, _Mapping]]] = ...) -> None: ...
                                F_0_FIELD_NUMBER: _ClassVar[int]
                                F_1_FIELD_NUMBER: _ClassVar[int]
                                F_3_FIELD_NUMBER: _ClassVar[int]
                                f_0: float
                                f_1: int
                                f_3: _containers.RepeatedCompositeFieldContainer[Message6.M1.M3.M5.M7.M8.M10.M11.M12]
                                def __init__(self, f_0: _Optional[float] = ..., f_1: _Optional[int] = ..., f_3: _Optional[_Iterable[_Union[Message6.M1.M3.M5.M7.M8.M10.M11.M12, _Mapping]]] = ...) -> None: ...
                            F_0_FIELD_NUMBER: _ClassVar[int]
                            F_2_FIELD_NUMBER: _ClassVar[int]
                            f_0: Message6.M1.M3.M5.M7.M8.M10.E5
                            f_2: Message6.M1.M3.M5.M7.M8.M10.M11
                            def __init__(self, f_0: _Optional[_Union[Message6.M1.M3.M5.M7.M8.M10.E5, str]] = ..., f_2: _Optional[_Union[Message6.M1.M3.M5.M7.M8.M10.M11, _Mapping]] = ...) -> None: ...
                        F_0_FIELD_NUMBER: _ClassVar[int]
                        F_1_FIELD_NUMBER: _ClassVar[int]
                        F_2_FIELD_NUMBER: _ClassVar[int]
                        F_3_FIELD_NUMBER: _ClassVar[int]
                        F_4_FIELD_NUMBER: _ClassVar[int]
                        F_9_FIELD_NUMBER: _ClassVar[int]
                        F_10_FIELD_NUMBER: _ClassVar[int]
                        f_0: int
                        f_1: int
                        f_2: bytes
                        f_3: int
                        f_4: str
                        f_9: _containers.RepeatedCompositeFieldContainer[Message6.M1.M3.M5.M7.M8.M9]
                        f_10: _containers.RepeatedCompositeFieldContainer[Message6.M1.M3.M5.M7.M8.M10]
                        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[int] = ..., f_2: _Optional[bytes] = ..., f_3: _Optional[int] = ..., f_4: _Optional[str] = ..., f_9: _Optional[_Iterable[_Union[Message6.M1.M3.M5.M7.M8.M9, _Mapping]]] = ..., f_10: _Optional[_Iterable[_Union[Message6.M1.M3.M5.M7.M8.M10, _Mapping]]] = ...) -> None: ...
                    F_0_FIELD_NUMBER: _ClassVar[int]
                    F_1_FIELD_NUMBER: _ClassVar[int]
                    F_2_FIELD_NUMBER: _ClassVar[int]
                    F_3_FIELD_NUMBER: _ClassVar[int]
                    F_4_FIELD_NUMBER: _ClassVar[int]
                    F_5_FIELD_NUMBER: _ClassVar[int]
                    F_6_FIELD_NUMBER: _ClassVar[int]
                    F_7_FIELD_NUMBER: _ClassVar[int]
                    F_8_FIELD_NUMBER: _ClassVar[int]
                    F_12_FIELD_NUMBER: _ClassVar[int]
                    f_0: str
                    f_1: int
                    f_2: bytes
                    f_3: int
                    f_4: int
                    f_5: int
                    f_6: Message6.M1.M3.M5.M7.E2
                    f_7: float
                    f_8: Message6.M1.M3.M5.M7.E3
                    f_12: Message6.M1.M3.M5.M7.M8
                    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[int] = ..., f_2: _Optional[bytes] = ..., f_3: _Optional[int] = ..., f_4: _Optional[int] = ..., f_5: _Optional[int] = ..., f_6: _Optional[_Union[Message6.M1.M3.M5.M7.E2, str]] = ..., f_7: _Optional[float] = ..., f_8: _Optional[_Union[Message6.M1.M3.M5.M7.E3, str]] = ..., f_12: _Optional[_Union[Message6.M1.M3.M5.M7.M8, _Mapping]] = ...) -> None: ...
                F_0_FIELD_NUMBER: _ClassVar[int]
                F_3_FIELD_NUMBER: _ClassVar[int]
                f_0: float
                f_3: _containers.RepeatedCompositeFieldContainer[Message6.M1.M3.M5.M7]
                def __init__(self, f_0: _Optional[float] = ..., f_3: _Optional[_Iterable[_Union[Message6.M1.M3.M5.M7, _Mapping]]] = ...) -> None: ...
            F_0_FIELD_NUMBER: _ClassVar[int]
            F_2_FIELD_NUMBER: _ClassVar[int]
            F_3_FIELD_NUMBER: _ClassVar[int]
            f_0: _containers.RepeatedScalarFieldContainer[str]
            f_2: Message6.M1.M3.M4
            f_3: Message6.M1.M3.M5
            def __init__(self, f_0: _Optional[_Iterable[str]] = ..., f_2: _Optional[_Union[Message6.M1.M3.M4, _Mapping]] = ..., f_3: _Optional[_Union[Message6.M1.M3.M5, _Mapping]] = ...) -> None: ...
        F_0_FIELD_NUMBER: _ClassVar[int]
        F_1_FIELD_NUMBER: _ClassVar[int]
        F_2_FIELD_NUMBER: _ClassVar[int]
        F_3_FIELD_NUMBER: _ClassVar[int]
        F_4_FIELD_NUMBER: _ClassVar[int]
        F_8_FIELD_NUMBER: _ClassVar[int]
        F_11_FIELD_NUMBER: _ClassVar[int]
        f_0: int
        f_1: str
        f_2: int
        f_3: int
        f_4: str
        f_8: Message6.M1.M2
        f_11: Message6.M1.M3
        def __init__(self, f_0: _Optional[int] = ..., f_1: _Optional[str] = ..., f_2: _Optional[int] = ..., f_3: _Optional[int] = ..., f_4: _Optional[str] = ..., f_8: _Optional[_Union[Message6.M1.M2, _Mapping]] = ..., f_11: _Optional[_Union[Message6.M1.M3, _Mapping]] = ...) -> None: ...
    F_0_FIELD_NUMBER: _ClassVar[int]
    F_1_FIELD_NUMBER: _ClassVar[int]
    F_2_FIELD_NUMBER: _ClassVar[int]
    F_5_FIELD_NUMBER: _ClassVar[int]
    f_0: str
    f_1: float
    f_2: int
    f_5: _containers.RepeatedCompositeFieldContainer[Message6.M1]
    def __init__(self, f_0: _Optional[str] = ..., f_1: _Optional[float] = ..., f_2: _Optional[int] = ..., f_5: _Optional[_Iterable[_Union[Message6.M1, _Mapping]]] = ...) -> None: ...
