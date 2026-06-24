# Copyright (c) 2025-2026 Buf Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generated from fleetbench access_message0.cc by _fleetbench.py. DO NOT EDIT.
#
# Derived from github.com/google/fleetbench
# Copyright 2025 The Fleetbench Authors
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: F841
# pyright: reportUnusedExpression=false
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bench.gen.fleetbench.Message0_pb import Message0


class Message0Access:
    if TYPE_CHECKING:
        # Provided by the Access subclass, which wires the
        # backend's classes; never assigned on the mixin itself.
        Message0_M1: type[Message0.M1]
        Message0_M1_M2: type[Message0.M1.M2]
        Message0_M1_M2_M4: type[Message0.M1.M2.M4]
        Message0_M1_M3: type[Message0.M1.M3]
        Message0_M1_M3_M5: type[Message0.M1.M3.M5]
        Message0_M1_M3_M5_M6: type[Message0.M1.M3.M5.M6]
        Message0_M1_M3_M5_M6_M10: type[Message0.M1.M3.M5.M6.M10]
        Message0_M1_M3_M5_M6_M8: type[Message0.M1.M3.M5.M6.M8]
        Message0_M1_M3_M5_M7: type[Message0.M1.M3.M5.M7]
        Message0_M1_M3_M5_M7_M9: type[Message0.M1.M3.M5.M7.M9]
        Message0_M1_M3_M5_M7_M9_M11: type[Message0.M1.M3.M5.M7.M9.M11]
        Message0_M1_M3_M5_M7_M9_M11_M13: type[Message0.M1.M3.M5.M7.M9.M11.M13]
        Message0_M1_M3_M5_M7_M9_M11_M13_E2: type[Message0.M1.M3.M5.M7.M9.M11.M13.E2]
        Message0_M1_M3_M5_M7_M9_M11_M13_E3: type[Message0.M1.M3.M5.M7.M9.M11.M13.E3]
        Message0_M1_M3_M5_M7_M9_M11_M13_E4: type[Message0.M1.M3.M5.M7.M9.M11.M13.E4]
        Message0_M1_M3_M5_M7_M9_M11_M13_E5: type[Message0.M1.M3.M5.M7.M9.M11.M13.E5]
        Message0_M1_M3_M5_M7_M9_M11_M13_E6: type[Message0.M1.M3.M5.M7.M9.M11.M13.E6]
        Message0_M1_M3_M5_M7_M9_M11_M13_M14: type[Message0.M1.M3.M5.M7.M9.M11.M13.M14]
        Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15: type[
            Message0.M1.M3.M5.M7.M9.M11.M13.M14.M15
        ]

    def message0_set_1(self, message: Message0, s: str, b: bytes) -> None:
        Message0_M1 = self.Message0_M1
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M10 = self.Message0_M1_M3_M5_M6_M10
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_E2 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E2
        Message0_M1_M3_M5_M7_M9_M11_M13_E5 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E5
        Message0_M1_M3_M5_M7_M9_M11_M13_E6 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E6
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        v0_0 = Message0_M1()
        message.f_4.append(v0_0)
        v1 = Message0_M1_M3()
        v0_0.f_3 = v1
        v2 = Message0_M1_M3_M5()
        v1.f_2 = v2
        v3 = Message0_M1_M3_M5_M6()
        v2.f_3 = v3
        v3.f_0 = s[0:3]
        v4_0 = Message0_M1_M3_M5_M6_M10()
        v3.f_4.append(v4_0)
        v5 = Message0_M1_M3_M5_M7()
        v2.f_4 = v5
        v6 = Message0_M1_M3_M5_M7_M9()
        v5.f_4 = v6
        v7 = Message0_M1_M3_M5_M7_M9_M11()
        v6.f_2 = v7
        v7.f_0 = 0xC912D02A9B0E7
        v8 = Message0_M1_M3_M5_M7_M9_M11_M13()
        v7.f_2 = v8
        v8.f_13 = 0xFAAE625
        v8.f_29 = 0x13004708B7B5C
        v8.f_3 = 0xCB8C41A
        v8.f_18 = False
        v8.f_0 = Message0_M1_M3_M5_M7_M9_M11_M13_E2.CONST_1
        v8.f_25 = Message0_M1_M3_M5_M7_M9_M11_M13_E6.CONST_5
        v8.f_14 = True
        v8.f_22 = 0x3C35071100C4799
        v8.f_21 = Message0_M1_M3_M5_M7_M9_M11_M13_E5.CONST_1
        v8.f_12 = False
        v8.f_15 = 0x46
        v9 = Message0_M1_M3_M5_M7_M9_M11_M13_M14()
        v8.f_40 = v9
        v9.f_0.append(0xA)
        v9.f_0.append(0x68A788)
        v8.f_16 = 0.404625
        v8.f_8 = 0x64
        v8.f_19 = 0x2D95C
        v10 = Message0_M1_M2()
        v0_0.f_2 = v10

    def message0_set_2(self, message: Message0, s: str, b: bytes) -> None:
        Message0_M1 = self.Message0_M1
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_E4 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E4
        Message0_M1_M3_M5_M7_M9_M11_M13_E6 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E6
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15 = (
            self.Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15
        )
        v0_0 = Message0_M1()
        message.f_4.append(v0_0)
        v1 = Message0_M1_M2()
        v0_0.f_2 = v1
        v1.f_0 = 0x1E58
        v2 = Message0_M1_M3()
        v0_0.f_3 = v2
        v3 = Message0_M1_M3_M5()
        v2.f_2 = v3
        v4 = Message0_M1_M3_M5_M6()
        v3.f_3 = v4
        v5 = Message0_M1_M3_M5_M6_M8()
        v4.f_3 = v5
        v5.f_0 = False
        v6 = Message0_M1_M3_M5_M7()
        v3.f_4 = v6
        v6.f_1 = 0x28FB
        v7 = Message0_M1_M3_M5_M7_M9()
        v6.f_4 = v7
        v8 = Message0_M1_M3_M5_M7_M9_M11()
        v7.f_2 = v8
        v9 = Message0_M1_M3_M5_M7_M9_M11_M13()
        v8.f_2 = v9
        v9.f_29 = 0x2F
        v9.f_25 = Message0_M1_M3_M5_M7_M9_M11_M13_E6.CONST_1
        v9.f_23 = 0x7B2B9D68B0A1E3
        v10 = Message0_M1_M3_M5_M7_M9_M11_M13_M14()
        v9.f_40 = v10
        v10.f_0.append(0xC65EF23)
        v11 = Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15()
        v10.f_2 = v11
        v9.f_19 = 0x867D0C5C95243A
        v9.f_14 = False
        v9.f_8 = 0x29
        v9.f_6 = s[0:7]
        v9.f_7 = Message0_M1_M3_M5_M7_M9_M11_M13_E4.CONST_5

    def message0_set_3(self, message: Message0, s: str, b: bytes) -> None:
        Message0_M1 = self.Message0_M1
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M10 = self.Message0_M1_M3_M5_M6_M10
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_E2 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E2
        Message0_M1_M3_M5_M7_M9_M11_M13_E3 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E3
        Message0_M1_M3_M5_M7_M9_M11_M13_E4 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E4
        Message0_M1_M3_M5_M7_M9_M11_M13_E5 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E5
        Message0_M1_M3_M5_M7_M9_M11_M13_E6 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E6
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        v0_0 = Message0_M1()
        message.f_4.append(v0_0)
        v1 = Message0_M1_M3()
        v0_0.f_3 = v1
        v1.f_0 = s[0:8]
        v2 = Message0_M1_M3_M5()
        v1.f_2 = v2
        v3 = Message0_M1_M3_M5_M7()
        v2.f_4 = v3
        v3.f_1 = 0xF590F16
        v4 = Message0_M1_M3_M5_M7_M9()
        v3.f_4 = v4
        v5 = Message0_M1_M3_M5_M7_M9_M11()
        v4.f_2 = v5
        v6 = Message0_M1_M3_M5_M7_M9_M11_M13()
        v5.f_2 = v6
        v6.f_18 = False
        v6.f_29 = 0xD5B45B9FA4C9F
        v7 = Message0_M1_M3_M5_M7_M9_M11_M13_M14()
        v6.f_40 = v7
        v6.f_30 = s[0:13]
        v6.f_9 = 0x69
        v6.f_4 = Message0_M1_M3_M5_M7_M9_M11_M13_E3.CONST_4
        v6.f_7 = Message0_M1_M3_M5_M7_M9_M11_M13_E4.CONST_2
        v6.f_15 = 0x76
        v6.f_21 = Message0_M1_M3_M5_M7_M9_M11_M13_E5.CONST_4
        v6.f_16 = 0.982743
        v6.f_0 = Message0_M1_M3_M5_M7_M9_M11_M13_E2.CONST_3
        v6.f_14 = True
        v6.f_6 = s[0:19]
        v6.f_25 = Message0_M1_M3_M5_M7_M9_M11_M13_E6.CONST_4
        v6.f_19 = 0x12
        v8 = Message0_M1_M3_M5_M6()
        v2.f_3 = v8
        v9 = Message0_M1_M3_M5_M6_M8()
        v8.f_3 = v9
        v8.f_0 = s[0:26]
        v10_0 = Message0_M1_M3_M5_M6_M10()
        v8.f_4.append(v10_0)
        v10_0.f_0 = 0.270165
        v2.f_0 = 0x43

    def message0_set_4(self, message: Message0, s: str, b: bytes) -> None:
        Message0_M1 = self.Message0_M1
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M2_M4 = self.Message0_M1_M2_M4
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_E5 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E5
        Message0_M1_M3_M5_M7_M9_M11_M13_E6 = self.Message0_M1_M3_M5_M7_M9_M11_M13_E6
        v0_0 = Message0_M1()
        message.f_4.append(v0_0)
        v1 = Message0_M1_M3()
        v0_0.f_3 = v1
        v2 = Message0_M1_M3_M5()
        v1.f_2 = v2
        v3 = Message0_M1_M3_M5_M6()
        v2.f_3 = v3
        v4 = Message0_M1_M3_M5_M6_M8()
        v3.f_3 = v4
        v4.f_0 = True
        v5 = Message0_M1_M3_M5_M7()
        v2.f_4 = v5
        v6 = Message0_M1_M3_M5_M7_M9()
        v5.f_4 = v6
        v7 = Message0_M1_M3_M5_M7_M9_M11()
        v6.f_2 = v7
        v8 = Message0_M1_M3_M5_M7_M9_M11_M13()
        v7.f_2 = v8
        v8.f_17 = 0x5F
        v8.f_13 = 0x4
        v8.f_18 = False
        v8.f_15 = 0x91950B308
        v8.f_16 = 0.096742
        v8.f_25 = Message0_M1_M3_M5_M7_M9_M11_M13_E6.CONST_2
        v8.f_12 = True
        v8.f_20 = s[0:2]
        v8.f_30 = s[0:5]
        v8.f_21 = Message0_M1_M3_M5_M7_M9_M11_M13_E5.CONST_5
        v2.f_0 = 0x1C
        v1.f_0 = s[0:1]
        v9 = Message0_M1_M2()
        v0_0.f_2 = v9
        v10 = Message0_M1_M2_M4()
        v9.f_2 = v10

    def message0_get_1(self, message: Message0) -> None:
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M2_M4 = self.Message0_M1_M2_M4
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15 = (
            self.Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15
        )
        for v0 in message.f_4:
            v1 = v0.f_2 or Message0_M1_M2()
            v1.f_0
            v2 = v1.f_2 or Message0_M1_M2_M4()
            v2.f_0
            v3 = v0.f_3 or Message0_M1_M3()
            v3.f_0
            v4 = v3.f_2 or Message0_M1_M3_M5()
            v5 = v4.f_4 or Message0_M1_M3_M5_M7()
            v5.f_1
            v5.f_0
            v6 = v5.f_4 or Message0_M1_M3_M5_M7_M9()
            v7 = v6.f_2 or Message0_M1_M3_M5_M7_M9_M11()
            v7.f_0
            v8 = v7.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13()
            v8.f_10
            v8.f_14
            v8.f_24
            v8.f_7
            v8.f_17
            v8.f_3
            v8.f_16
            v8.f_15
            v8.f_8
            v8.f_13
            v8.f_25
            v8.f_29
            v8.f_6
            v8.f_23
            v8.f_0
            v8.f_30
            v8.f_4
            v8.f_27
            v8.f_12
            v8.f_28
            v8.f_1
            v8.f_19
            v8.f_22
            v8.f_2
            for i in range(len(v8.f_11)):
                v8.f_11[i]
            v8.f_20
            v8.f_21
            v9 = v8.f_40 or Message0_M1_M3_M5_M7_M9_M11_M13_M14()
            v10 = v9.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15()
            v10.f_0
            for i in range(len(v9.f_0)):
                v9.f_0[i]
            v8.f_9
            v8.f_18
            v8.f_26
            v8.f_5
            v6.f_0
            v11 = v4.f_3 or Message0_M1_M3_M5_M6()
            for v12 in v11.f_4:
                v12.f_0
            v11.f_0
            v13 = v11.f_3 or Message0_M1_M3_M5_M6_M8()
            v13.f_0
            for v14 in v13.f_2:
                v14.f_0
            v4.f_0
            v0.f_0
        message.f_0

    def message0_get_2(self, message: Message0) -> None:
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M2_M4 = self.Message0_M1_M2_M4
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15 = (
            self.Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15
        )
        message.f_0
        for v0 in message.f_4:
            v0.f_0
            v1 = v0.f_2 or Message0_M1_M2()
            v1.f_0
            v2 = v1.f_2 or Message0_M1_M2_M4()
            v2.f_0
            v3 = v0.f_3 or Message0_M1_M3()
            v3.f_0
            v4 = v3.f_2 or Message0_M1_M3_M5()
            v4.f_0
            v5 = v4.f_3 or Message0_M1_M3_M5_M6()
            for v6 in v5.f_4:
                v6.f_0
            v5.f_0
            v7 = v5.f_3 or Message0_M1_M3_M5_M6_M8()
            for v8 in v7.f_2:
                v8.f_0
            v7.f_0
            v9 = v4.f_4 or Message0_M1_M3_M5_M7()
            v10 = v9.f_4 or Message0_M1_M3_M5_M7_M9()
            v10.f_0
            v11 = v10.f_2 or Message0_M1_M3_M5_M7_M9_M11()
            v11.f_0
            v12 = v11.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13()
            v12.f_27
            v12.f_29
            v12.f_17
            v12.f_25
            v12.f_4
            v12.f_13
            v12.f_2
            v13 = v12.f_40 or Message0_M1_M3_M5_M7_M9_M11_M13_M14()
            for i in range(len(v13.f_0)):
                v13.f_0[i]
            v14 = v13.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15()
            v14.f_0
            v12.f_12
            v12.f_7
            v12.f_16
            v12.f_22
            v12.f_14
            for i in range(len(v12.f_11)):
                v12.f_11[i]
            v12.f_26
            v12.f_0
            v12.f_18
            v12.f_30
            v12.f_9
            v12.f_6
            v12.f_23
            v12.f_1
            v12.f_5
            v12.f_20
            v12.f_21
            v12.f_15
            v12.f_28
            v12.f_24
            v12.f_8
            v12.f_19
            v12.f_10
            v12.f_3
            v9.f_1
            v9.f_0

    def message0_get_3(self, message: Message0) -> None:
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M2_M4 = self.Message0_M1_M2_M4
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15 = (
            self.Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15
        )
        for v0 in message.f_4:
            v1 = v0.f_3 or Message0_M1_M3()
            v1.f_0
            v2 = v1.f_2 or Message0_M1_M3_M5()
            v3 = v2.f_4 or Message0_M1_M3_M5_M7()
            v3.f_0
            v3.f_1
            v4 = v3.f_4 or Message0_M1_M3_M5_M7_M9()
            v4.f_0
            v5 = v4.f_2 or Message0_M1_M3_M5_M7_M9_M11()
            v5.f_0
            v6 = v5.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13()
            v6.f_24
            v6.f_28
            v6.f_17
            v6.f_2
            v6.f_14
            v6.f_30
            v6.f_10
            v6.f_8
            v6.f_21
            v6.f_15
            v7 = v6.f_40 or Message0_M1_M3_M5_M7_M9_M11_M13_M14()
            v8 = v7.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15()
            v8.f_0
            for i in range(len(v7.f_0)):
                v7.f_0[i]
            v6.f_13
            v6.f_0
            v6.f_5
            v6.f_7
            v6.f_3
            v6.f_20
            v6.f_22
            v6.f_18
            v6.f_25
            v6.f_1
            v6.f_9
            v6.f_19
            v6.f_27
            v6.f_16
            v6.f_29
            v6.f_12
            v6.f_4
            v6.f_23
            v6.f_26
            for i in range(len(v6.f_11)):
                v6.f_11[i]
            v6.f_6
            v9 = v2.f_3 or Message0_M1_M3_M5_M6()
            for v10 in v9.f_4:
                v10.f_0
            v9.f_0
            v11 = v9.f_3 or Message0_M1_M3_M5_M6_M8()
            v11.f_0
            for v12 in v11.f_2:
                v12.f_0
            v2.f_0
            v13 = v0.f_2 or Message0_M1_M2()
            v14 = v13.f_2 or Message0_M1_M2_M4()
            v14.f_0
            v13.f_0
            v0.f_0
        message.f_0

    def message0_get_4(self, message: Message0) -> None:
        Message0_M1_M2 = self.Message0_M1_M2
        Message0_M1_M2_M4 = self.Message0_M1_M2_M4
        Message0_M1_M3 = self.Message0_M1_M3
        Message0_M1_M3_M5 = self.Message0_M1_M3_M5
        Message0_M1_M3_M5_M6 = self.Message0_M1_M3_M5_M6
        Message0_M1_M3_M5_M6_M8 = self.Message0_M1_M3_M5_M6_M8
        Message0_M1_M3_M5_M7 = self.Message0_M1_M3_M5_M7
        Message0_M1_M3_M5_M7_M9 = self.Message0_M1_M3_M5_M7_M9
        Message0_M1_M3_M5_M7_M9_M11 = self.Message0_M1_M3_M5_M7_M9_M11
        Message0_M1_M3_M5_M7_M9_M11_M13 = self.Message0_M1_M3_M5_M7_M9_M11_M13
        Message0_M1_M3_M5_M7_M9_M11_M13_M14 = self.Message0_M1_M3_M5_M7_M9_M11_M13_M14
        Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15 = (
            self.Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15
        )
        for v0 in message.f_4:
            v1 = v0.f_3 or Message0_M1_M3()
            v2 = v1.f_2 or Message0_M1_M3_M5()
            v3 = v2.f_3 or Message0_M1_M3_M5_M6()
            v3.f_0
            for v4 in v3.f_4:
                v4.f_0
            v5 = v3.f_3 or Message0_M1_M3_M5_M6_M8()
            v5.f_0
            for v6 in v5.f_2:
                v6.f_0
            v2.f_0
            v7 = v2.f_4 or Message0_M1_M3_M5_M7()
            v7.f_1
            v7.f_0
            v8 = v7.f_4 or Message0_M1_M3_M5_M7_M9()
            v9 = v8.f_2 or Message0_M1_M3_M5_M7_M9_M11()
            v9.f_0
            v10 = v9.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13()
            v10.f_5
            v10.f_27
            v10.f_0
            v10.f_12
            v10.f_23
            v10.f_9
            v10.f_28
            v10.f_4
            v10.f_10
            for i in range(len(v10.f_11)):
                v10.f_11[i]
            v10.f_14
            v10.f_1
            v10.f_24
            v11 = v10.f_40 or Message0_M1_M3_M5_M7_M9_M11_M13_M14()
            for i in range(len(v11.f_0)):
                v11.f_0[i]
            v12 = v11.f_2 or Message0_M1_M3_M5_M7_M9_M11_M13_M14_M15()
            v12.f_0
            v10.f_2
            v10.f_18
            v10.f_16
            v10.f_20
            v10.f_8
            v10.f_15
            v10.f_17
            v10.f_25
            v10.f_22
            v10.f_6
            v10.f_29
            v10.f_7
            v10.f_13
            v10.f_21
            v10.f_19
            v10.f_3
            v10.f_30
            v10.f_26
            v8.f_0
            v1.f_0
            v13 = v0.f_2 or Message0_M1_M2()
            v13.f_0
            v14 = v13.f_2 or Message0_M1_M2_M4()
            v14.f_0
            v0.f_0
        message.f_0
