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

# Generated from fleetbench access_message6.cc by _fleetbench.py. DO NOT EDIT.
#
# Derived from github.com/google/fleetbench
# Copyright 2025 The Fleetbench Authors
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: F841
# pyright: reportUnusedExpression=false
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bench.gen.fleetbench.Message6_pb import Message6


class Message6Access:
    if TYPE_CHECKING:
        # Provided by the Access subclass, which wires the
        # backend's classes; never assigned on the mixin itself.
        Message6_M1: type[Message6.M1]
        Message6_M1_M2: type[Message6.M1.M2]
        Message6_M1_M3: type[Message6.M1.M3]
        Message6_M1_M3_M4: type[Message6.M1.M3.M4]
        Message6_M1_M3_M4_E1: type[Message6.M1.M3.M4.E1]
        Message6_M1_M3_M4_M6: type[Message6.M1.M3.M4.M6]
        Message6_M1_M3_M5: type[Message6.M1.M3.M5]
        Message6_M1_M3_M5_M7: type[Message6.M1.M3.M5.M7]
        Message6_M1_M3_M5_M7_E2: type[Message6.M1.M3.M5.M7.E2]
        Message6_M1_M3_M5_M7_E3: type[Message6.M1.M3.M5.M7.E3]
        Message6_M1_M3_M5_M7_M8: type[Message6.M1.M3.M5.M7.M8]
        Message6_M1_M3_M5_M7_M8_M10: type[Message6.M1.M3.M5.M7.M8.M10]
        Message6_M1_M3_M5_M7_M8_M10_E5: type[Message6.M1.M3.M5.M7.M8.M10.E5]
        Message6_M1_M3_M5_M7_M8_M10_M11: type[Message6.M1.M3.M5.M7.M8.M10.M11]
        Message6_M1_M3_M5_M7_M8_M10_M11_M12: type[Message6.M1.M3.M5.M7.M8.M10.M11.M12]
        Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6: type[
            Message6.M1.M3.M5.M7.M8.M10.M11.M12.E6
        ]
        Message6_M1_M3_M5_M7_M8_M10_M11_M12_M13: type[
            Message6.M1.M3.M5.M7.M8.M10.M11.M12.M13
        ]
        Message6_M1_M3_M5_M7_M8_M9: type[Message6.M1.M3.M5.M7.M8.M9]
        Message6_M1_M3_M5_M7_M8_M9_E4: type[Message6.M1.M3.M5.M7.M8.M9.E4]

    def message6_set_1(self, message: Message6, s: str, b: bytes) -> None:
        Message6_M1 = self.Message6_M1
        Message6_M1_M2 = self.Message6_M1_M2
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7 = self.Message6_M1_M3_M5_M7
        Message6_M1_M3_M5_M7_E2 = self.Message6_M1_M3_M5_M7_E2
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10 = self.Message6_M1_M3_M5_M7_M8_M10
        Message6_M1_M3_M5_M7_M8_M10_E5 = self.Message6_M1_M3_M5_M7_M8_M10_E5
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        Message6_M1_M3_M5_M7_M8_M10_M11_M12 = self.Message6_M1_M3_M5_M7_M8_M10_M11_M12
        Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6 = (
            self.Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6
        )
        message.f_1 = 0.905219
        message.f_0 = s[0:6]
        message.f_2 = 0x164A3B177F480
        v0_0 = Message6_M1()
        message.f_5.append(v0_0)
        v0_0.f_1 = s[0:15]
        v1 = Message6_M1_M3()
        v0_0.f_11 = v1
        v1.f_0.append(s[0:18])
        v2 = Message6_M1_M3_M5()
        v1.f_3 = v2
        v3_0 = Message6_M1_M3_M5_M7()
        v2.f_3.append(v3_0)
        v3_0.f_5 = 0x7E74883
        v3_0.f_6 = Message6_M1_M3_M5_M7_E2.CONST_1
        v4 = Message6_M1_M3_M5_M7_M8()
        v3_0.f_12 = v4
        v4.f_0 = 0x1A864C
        v5_0 = Message6_M1_M3_M5_M7_M8_M10()
        v4.f_10.append(v5_0)
        v6 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v5_0.f_2 = v6
        v6.f_1 = 0xD0818531BB837D
        v6.f_0 = 0.017473
        v5_1 = Message6_M1_M3_M5_M7_M8_M10()
        v4.f_10.append(v5_1)
        v5_1.f_0 = Message6_M1_M3_M5_M7_M8_M10_E5.CONST_2
        v7 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v5_1.f_2 = v7
        v3_1 = Message6_M1_M3_M5_M7()
        v2.f_3.append(v3_1)
        v3_1.f_0 = s[0:20]
        v3_1.f_1 = 0x4E978
        v8 = Message6_M1_M3_M5_M7_M8()
        v3_1.f_12 = v8
        v8.f_2 = b[0:17]
        v8.f_0 = 0x941CEFA55F2B77
        v9_0 = Message6_M1_M3_M5_M7_M8_M10()
        v8.f_10.append(v9_0)
        v10 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v9_0.f_2 = v10
        v11_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12()
        v10.f_3.append(v11_0)
        v11_0.f_1 = Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6.CONST_2
        v10.f_0 = 0.208412
        v8.f_4 = s[0:3]
        v3_1.f_6 = Message6_M1_M3_M5_M7_E2.CONST_5
        v3_1.f_4 = 0x50E
        v12 = Message6_M1_M2()
        v0_0.f_8 = v12
        v12.f_0 = s[0:1]
        v0_0.f_0 = 0x3B62

    def message6_set_2(self, message: Message6, s: str, b: bytes) -> None:
        Message6_M1 = self.Message6_M1
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7 = self.Message6_M1_M3_M5_M7
        Message6_M1_M3_M5_M7_E2 = self.Message6_M1_M3_M5_M7_E2
        Message6_M1_M3_M5_M7_E3 = self.Message6_M1_M3_M5_M7_E3
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10 = self.Message6_M1_M3_M5_M7_M8_M10
        Message6_M1_M3_M5_M7_M8_M10_E5 = self.Message6_M1_M3_M5_M7_M8_M10_E5
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        Message6_M1_M3_M5_M7_M8_M10_M11_M12 = self.Message6_M1_M3_M5_M7_M8_M10_M11_M12
        Message6_M1_M3_M5_M7_M8_M9 = self.Message6_M1_M3_M5_M7_M8_M9
        Message6_M1_M3_M5_M7_M8_M9_E4 = self.Message6_M1_M3_M5_M7_M8_M9_E4
        message.f_0 = s[0:6]
        v0_0 = Message6_M1()
        message.f_5.append(v0_0)
        v0_0.f_0 = 0x8E3D9DFD5846D0
        v0_0.f_3 = 0x5B
        v0_0.f_2 = 0x1E
        v1 = Message6_M1_M3()
        v0_0.f_11 = v1
        v2 = Message6_M1_M3_M5()
        v1.f_3 = v2
        v3_0 = Message6_M1_M3_M5_M7()
        v2.f_3.append(v3_0)
        v4 = Message6_M1_M3_M5_M7_M8()
        v3_0.f_12 = v4
        v4.f_3 = 0xCF40BA99599921
        v4.f_1 = 0x6AE7594B027780
        v5_0 = Message6_M1_M3_M5_M7_M8_M10()
        v4.f_10.append(v5_0)
        v5_0.f_0 = Message6_M1_M3_M5_M7_M8_M10_E5.CONST_4
        v6 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v5_0.f_2 = v6
        v6.f_0 = 0.643093
        v7_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12()
        v6.f_3.append(v7_0)
        v7_0.f_0 = s[0:7]
        v4.f_0 = 0x56
        v3_0.f_0 = s[0:6]
        v3_0.f_6 = Message6_M1_M3_M5_M7_E2.CONST_1
        v3_0.f_7 = 0.380619
        v3_0.f_8 = Message6_M1_M3_M5_M7_E3.CONST_1
        v3_0.f_4 = 0x396A
        v3_1 = Message6_M1_M3_M5_M7()
        v2.f_3.append(v3_1)
        v3_1.f_0 = s[0:23]
        v8 = Message6_M1_M3_M5_M7_M8()
        v3_1.f_12 = v8
        v8.f_3 = 0x72
        v9_0 = Message6_M1_M3_M5_M7_M8_M9()
        v8.f_9.append(v9_0)
        v9_0.f_0 = Message6_M1_M3_M5_M7_M8_M9_E4.CONST_2
        v10_0 = Message6_M1_M3_M5_M7_M8_M10()
        v8.f_10.append(v10_0)
        v11 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v10_0.f_2 = v11
        v12_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12()
        v11.f_3.append(v12_0)
        v12_0.f_0 = s[0:5]
        v8.f_2 = b[0:341]
        v3_1.f_5 = 0xE9E1CAB
        v3_1.f_7 = 0.754160
        v3_1.f_8 = Message6_M1_M3_M5_M7_E3.CONST_4
        message.f_2 = 0x11E72F3E0C6FF

    def message6_set_3(self, message: Message6, s: str, b: bytes) -> None:
        Message6_M1 = self.Message6_M1
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7 = self.Message6_M1_M3_M5_M7
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10 = self.Message6_M1_M3_M5_M7_M8_M10
        Message6_M1_M3_M5_M7_M8_M10_E5 = self.Message6_M1_M3_M5_M7_M8_M10_E5
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        Message6_M1_M3_M5_M7_M8_M10_M11_M12 = self.Message6_M1_M3_M5_M7_M8_M10_M11_M12
        Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6 = (
            self.Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6
        )
        Message6_M1_M3_M5_M7_M8_M10_M11_M12_M13 = (
            self.Message6_M1_M3_M5_M7_M8_M10_M11_M12_M13
        )
        Message6_M1_M3_M5_M7_M8_M9 = self.Message6_M1_M3_M5_M7_M8_M9
        Message6_M1_M3_M5_M7_M8_M9_E4 = self.Message6_M1_M3_M5_M7_M8_M9_E4
        v0_0 = Message6_M1()
        message.f_5.append(v0_0)
        v0_0.f_2 = 0x13BD0F5
        v1 = Message6_M1_M3()
        v0_0.f_11 = v1
        v2 = Message6_M1_M3_M5()
        v1.f_3 = v2
        v2.f_0 = 0.254072
        v3_0 = Message6_M1_M3_M5_M7()
        v2.f_3.append(v3_0)
        v3_0.f_1 = 0x30
        v3_0.f_7 = 0.157737
        v4 = Message6_M1_M3_M5_M7_M8()
        v3_0.f_12 = v4
        v5_0 = Message6_M1_M3_M5_M7_M8_M10()
        v4.f_10.append(v5_0)
        v6 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v5_0.f_2 = v6
        v6.f_1 = 0x269D95A6A03099
        v7_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12()
        v6.f_3.append(v7_0)
        v7_0.f_1 = Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6.CONST_2
        v8_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12_M13()
        v7_0.f_4.append(v8_0)
        v8_0.f_0 = 0x26
        v7_0.f_0 = s[0:58]
        v5_0.f_0 = Message6_M1_M3_M5_M7_M8_M10_E5.CONST_4
        v5_1 = Message6_M1_M3_M5_M7_M8_M10()
        v4.f_10.append(v5_1)
        v9 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v5_1.f_2 = v9
        v9.f_0 = 0.995871
        v10_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12()
        v9.f_3.append(v10_0)
        v10_0.f_1 = Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6.CONST_1
        v10_0.f_0 = s[0:6]
        v11_0 = Message6_M1_M3_M5_M7_M8_M9()
        v4.f_9.append(v11_0)
        v11_0.f_0 = Message6_M1_M3_M5_M7_M8_M9_E4.CONST_1
        v0_0.f_0 = 0xE26CD9B39BC724
        v0_0.f_3 = 0x2D

    def message6_set_4(self, message: Message6, s: str, b: bytes) -> None:
        Message6_M1 = self.Message6_M1
        Message6_M1_M2 = self.Message6_M1_M2
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M4 = self.Message6_M1_M3_M4
        Message6_M1_M3_M4_E1 = self.Message6_M1_M3_M4_E1
        Message6_M1_M3_M4_M6 = self.Message6_M1_M3_M4_M6
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7 = self.Message6_M1_M3_M5_M7
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10 = self.Message6_M1_M3_M5_M7_M8_M10
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        Message6_M1_M3_M5_M7_M8_M10_M11_M12 = self.Message6_M1_M3_M5_M7_M8_M10_M11_M12
        Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6 = (
            self.Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6
        )
        v0_0 = Message6_M1()
        message.f_5.append(v0_0)
        v1 = Message6_M1_M2()
        v0_0.f_8 = v1
        v2 = Message6_M1_M3()
        v0_0.f_11 = v2
        v2.f_0.append(s[0:5])
        v2.f_0.append(s[0:4])
        v2.f_0.append(s[0:8])
        v2.f_0.append(s[0:37])
        v3 = Message6_M1_M3_M5()
        v2.f_3 = v3
        v3.f_0 = 0.326377
        v4_0 = Message6_M1_M3_M5_M7()
        v3.f_3.append(v4_0)
        v4_0.f_0 = s[0:4]
        v5 = Message6_M1_M3_M5_M7_M8()
        v4_0.f_12 = v5
        v6_0 = Message6_M1_M3_M5_M7_M8_M10()
        v5.f_10.append(v6_0)
        v7 = Message6_M1_M3_M5_M7_M8_M10_M11()
        v6_0.f_2 = v7
        v8_0 = Message6_M1_M3_M5_M7_M8_M10_M11_M12()
        v7.f_3.append(v8_0)
        v8_0.f_1 = Message6_M1_M3_M5_M7_M8_M10_M11_M12_E6.CONST_4
        v5.f_3 = 0xE22B4205105D0
        v5.f_2 = b[0:112]
        v5.f_0 = 0x2158
        v4_0.f_7 = 0.197611
        v4_0.f_4 = 0x1450
        v4_0.f_2 = b[0:259]
        v4_0.f_3 = 0xC923452CC1F538
        v9 = Message6_M1_M3_M4()
        v2.f_2 = v9
        v9.f_0 = Message6_M1_M3_M4_E1.CONST_5
        v10 = Message6_M1_M3_M4_M6()
        v9.f_2 = v10
        v0_0.f_2 = 0x3D

    def message6_get_1(self, message: Message6) -> None:
        Message6_M1_M2 = self.Message6_M1_M2
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M4 = self.Message6_M1_M3_M4
        Message6_M1_M3_M4_M6 = self.Message6_M1_M3_M4_M6
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        message.f_1
        for v0 in message.f_5:
            v0.f_1
            v0.f_2
            v0.f_0
            v1 = v0.f_8 or Message6_M1_M2()
            v1.f_0
            v0.f_3
            v2 = v0.f_11 or Message6_M1_M3()
            for i in range(len(v2.f_0)):
                v2.f_0[i]
            v3 = v2.f_3 or Message6_M1_M3_M5()
            v3.f_0
            for v4 in v3.f_3:
                v5 = v4.f_12 or Message6_M1_M3_M5_M7_M8()
                v5.f_1
                for v6 in v5.f_10:
                    v7 = v6.f_2 or Message6_M1_M3_M5_M7_M8_M10_M11()
                    for v8 in v7.f_3:
                        for v9 in v8.f_4:
                            v9.f_0
                        v8.f_1
                        v8.f_0
                    v7.f_1
                    v7.f_0
                    v6.f_0
                v5.f_3
                v5.f_0
                v5.f_2
                v5.f_4
                for v10 in v5.f_9:
                    v10.f_0
                v4.f_6
                v4.f_5
                v4.f_0
                v4.f_7
                v4.f_2
                v4.f_4
                v4.f_3
                v4.f_1
                v4.f_8
            v11 = v2.f_2 or Message6_M1_M3_M4()
            v11.f_0
            v12 = v11.f_2 or Message6_M1_M3_M4_M6()
            v12.f_0
            v0.f_4
        message.f_0
        message.f_2

    def message6_get_2(self, message: Message6) -> None:
        Message6_M1_M2 = self.Message6_M1_M2
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M4 = self.Message6_M1_M3_M4
        Message6_M1_M3_M4_M6 = self.Message6_M1_M3_M4_M6
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        for v0 in message.f_5:
            v0.f_3
            v0.f_1
            v1 = v0.f_8 or Message6_M1_M2()
            v1.f_0
            v0.f_0
            v0.f_2
            v2 = v0.f_11 or Message6_M1_M3()
            v3 = v2.f_2 or Message6_M1_M3_M4()
            v4 = v3.f_2 or Message6_M1_M3_M4_M6()
            v4.f_0
            v3.f_0
            v5 = v2.f_3 or Message6_M1_M3_M5()
            for v6 in v5.f_3:
                v6.f_2
                v6.f_0
                v6.f_6
                v6.f_3
                v7 = v6.f_12 or Message6_M1_M3_M5_M7_M8()
                v7.f_0
                v7.f_2
                v7.f_3
                for v8 in v7.f_9:
                    v8.f_0
                v7.f_4
                for v9 in v7.f_10:
                    v10 = v9.f_2 or Message6_M1_M3_M5_M7_M8_M10_M11()
                    v10.f_0
                    for v11 in v10.f_3:
                        v11.f_1
                        for v12 in v11.f_4:
                            v12.f_0
                        v11.f_0
                    v10.f_1
                    v9.f_0
                v7.f_1
                v6.f_7
                v6.f_1
                v6.f_5
                v6.f_8
                v6.f_4
            v5.f_0
            for i in range(len(v2.f_0)):
                v2.f_0[i]
            v0.f_4
        message.f_2
        message.f_1
        message.f_0

    def message6_get_3(self, message: Message6) -> None:
        Message6_M1_M2 = self.Message6_M1_M2
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M4 = self.Message6_M1_M3_M4
        Message6_M1_M3_M4_M6 = self.Message6_M1_M3_M4_M6
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        message.f_2
        message.f_1
        message.f_0
        for v0 in message.f_5:
            v0.f_1
            v1 = v0.f_8 or Message6_M1_M2()
            v1.f_0
            v0.f_2
            v2 = v0.f_11 or Message6_M1_M3()
            v3 = v2.f_2 or Message6_M1_M3_M4()
            v4 = v3.f_2 or Message6_M1_M3_M4_M6()
            v4.f_0
            v3.f_0
            v5 = v2.f_3 or Message6_M1_M3_M5()
            for v6 in v5.f_3:
                v6.f_0
                v7 = v6.f_12 or Message6_M1_M3_M5_M7_M8()
                v7.f_0
                v7.f_1
                v7.f_4
                v7.f_2
                v7.f_3
                for v8 in v7.f_9:
                    v8.f_0
                for v9 in v7.f_10:
                    v10 = v9.f_2 or Message6_M1_M3_M5_M7_M8_M10_M11()
                    for v11 in v10.f_3:
                        for v12 in v11.f_4:
                            v12.f_0
                        v11.f_1
                        v11.f_0
                    v10.f_1
                    v10.f_0
                    v9.f_0
                v6.f_2
                v6.f_4
                v6.f_8
                v6.f_6
                v6.f_5
                v6.f_7
                v6.f_3
                v6.f_1
            v5.f_0
            for i in range(len(v2.f_0)):
                v2.f_0[i]
            v0.f_4
            v0.f_0
            v0.f_3

    def message6_get_4(self, message: Message6) -> None:
        Message6_M1_M2 = self.Message6_M1_M2
        Message6_M1_M3 = self.Message6_M1_M3
        Message6_M1_M3_M4 = self.Message6_M1_M3_M4
        Message6_M1_M3_M4_M6 = self.Message6_M1_M3_M4_M6
        Message6_M1_M3_M5 = self.Message6_M1_M3_M5
        Message6_M1_M3_M5_M7_M8 = self.Message6_M1_M3_M5_M7_M8
        Message6_M1_M3_M5_M7_M8_M10_M11 = self.Message6_M1_M3_M5_M7_M8_M10_M11
        for v0 in message.f_5:
            v0.f_2
            v1 = v0.f_11 or Message6_M1_M3()
            for i in range(len(v1.f_0)):
                v1.f_0[i]
            v2 = v1.f_3 or Message6_M1_M3_M5()
            for v3 in v2.f_3:
                v3.f_1
                v3.f_3
                v3.f_2
                v3.f_7
                v3.f_0
                v3.f_5
                v3.f_4
                v4 = v3.f_12 or Message6_M1_M3_M5_M7_M8()
                v4.f_4
                v4.f_3
                v4.f_0
                v4.f_2
                for v5 in v4.f_9:
                    v5.f_0
                v4.f_1
                for v6 in v4.f_10:
                    v6.f_0
                    v7 = v6.f_2 or Message6_M1_M3_M5_M7_M8_M10_M11()
                    v7.f_1
                    v7.f_0
                    for v8 in v7.f_3:
                        v8.f_0
                        for v9 in v8.f_4:
                            v9.f_0
                        v8.f_1
                v3.f_8
                v3.f_6
            v2.f_0
            v10 = v1.f_2 or Message6_M1_M3_M4()
            v11 = v10.f_2 or Message6_M1_M3_M4_M6()
            v11.f_0
            v10.f_0
            v0.f_1
            v0.f_0
            v0.f_3
            v0.f_4
            v12 = v0.f_8 or Message6_M1_M2()
            v12.f_0
        message.f_0
        message.f_2
        message.f_1
