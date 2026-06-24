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

# Generated from fleetbench access_message15.cc by _fleetbench.py. DO NOT EDIT.
#
# Derived from github.com/google/fleetbench
# Copyright 2025 The Fleetbench Authors
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: F841
# pyright: reportUnusedExpression=false
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bench.gen.fleetbench.Message15_pb2 import Message15


class Message15Access:
    if TYPE_CHECKING:
        # Provided by the Access subclass, which wires the
        # backend's classes; never assigned on the mixin itself.
        Message15_M1: type[Message15.M1]
        Message15_M1_M2: type[Message15.M1.M2]
        Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14: type[
            Message15.M1.M2.M4.M6.M8.M9.M12.M13.M14
        ]

    def message15_set_1(self, message: Message15, s: str, b: bytes) -> None:
        Message15_M1 = self.Message15_M1
        Message15_M1_M2 = self.Message15_M1_M2
        Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14 = (
            self.Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14
        )
        v0 = message.f_3
        v0.f_9 = 0x3837C59EBFE57F8
        v0.f_10 = 0x3409549E3F18D7
        v0.f_25 = Message15_M1.E3_CONST_3
        v0.f_20 = 0x59
        v0.f_28.append(0xCA6A279)
        v0.f_17 = Message15_M1.E2_CONST_1
        v0.f_12 = 0x18B9AFFDA44A1
        v0.f_21 = 0x59
        v0.f_11 = 0x1B
        v0.f_0 = 0x2F5AB8B2
        v0.f_16 = b[0:18]
        v1_0 = v0.f_48.add()
        v1_0.f_28 = Message15_M1_M2.E8_CONST_2
        v1_0.f_22 = 0x1D21D2C1A3EA7
        v1_0.f_69 = 0xD5D8165
        v1_0.f_12 = 0x4D
        v1_0.f_62 = s[0:7]
        v2 = v1_0.f_103
        v3 = v2.f_4
        v3.f_3 = 0.131037
        v3.f_4 = 0x28
        v3.f_1 = s[0:3]
        v4 = v3.f_7
        v4.f_0 = 0x15
        v5_0 = v4.f_3.add()
        v5_0.f_0 = s[0:63]
        v6 = v5_0.f_3
        v6.f_1.append(0x15)
        v6.f_0 = 0xF12
        v7 = v6.f_4
        v7.f_0 = 0x55
        v8 = v7.f_2
        v8.f_1.append(Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E14_CONST_5)
        v8.f_4 = 0x44FD02D4561FA603
        v8.f_5 = s[0:11]
        v8.f_8 = 0xF1BEA34
        v8.f_2 = 0x54A27CFC30F3ACEF
        v8.f_9 = Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E15_CONST_1
        v9 = v3.f_6
        v10 = v9.f_4
        v10.f_0 = 0xABE4FBD165B7B0
        v2.f_1 = 0x17
        v1_0.f_6 = 0.258971
        v1_0.f_2 = Message15_M1_M2.E5_CONST_5
        v1_0.f_44 = s[0:4]
        v1_0.f_71 = Message15_M1_M2.E11_CONST_3
        v11 = v1_0.f_102
        v11.SetInParent()
        v1_0.f_47 = False
        v1_0.f_9.extend(
            [
                0x982D512,
                0x3B839,
                0x1029D9,
                0x78,
                0x21,
                0xAD4AF82,
                0x1608A4,
                0x247C,
                0xFD362FD,
                0x9B0DDA9,
                0x88B05E4,
                0x90CCC02,
            ]
        )
        v1_0.f_37 = 0x5912F1D4EBE4DB
        v1_0.f_61 = False
        v1_0.f_24 = 0.379154
        v1_0.f_51 = 0x4516590
        v1_0.f_72.append(0x788FC95)
        v1_0.f_14 = 0x1FA22
        v1_0.f_10 = 0x227DB4CF2E87FDA1
        v1_0.f_17 = s[0:93]
        v1_0.f_18 = 0xD5A0741D778597
        v1_0.f_38 = 0.533021
        v1_0.f_48 = 0.996099
        v1_0.f_59 = 0x16F6E94C
        v1_0.f_30 = 0xB2DD023B354C
        v1_0.f_13 = s[0:393]
        v1_0.f_11.append(Message15_M1_M2.E6_CONST_1)
        v1_0.f_63 = 0x5F
        v1_0.f_0 = 0.045761
        v1_0.f_15 = 0x4EC39E9ADC5107C
        v1_1 = v0.f_48.add()
        v1_1.f_57 = s[0:6]
        v12 = v1_1.f_103
        v12.f_1 = 0xFBB320DC58F3
        v13 = v12.f_4
        v13.f_4 = 0xE1A6B85
        v13.f_3 = 0.047877
        v14 = v13.f_6
        v15 = v14.f_4
        v15.f_0 = 0x9E82E2A60244FE
        v14.f_0 = 0x228E
        v14.f_1 = False
        v16 = v13.f_7
        v17_0 = v16.f_3.add()
        v18 = v17_0.f_3
        v19 = v18.f_4
        v20 = v19.f_2
        v20.f_3 = 0x17
        v20.f_7.append(0x8E760B6)
        v20.f_7.append(0xD053FA7)
        v20.f_4 = 0x4C5E7451D3C58128
        v20.f_5 = s[0:27]
        v20.f_9 = Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E15_CONST_5
        v20.f_8 = 0x191F1D8
        v16.f_0 = 0x50
        v1_1.f_30 = 0x12EA0CD0C0C58
        v1_1.f_60 = 0.203106
        v1_1.f_56 = 0.360738
        v1_1.f_13 = s[0:7]
        v1_1.f_48 = 0.263951
        v1_1.f_11.append(Message15_M1_M2.E6_CONST_5)
        v1_1.f_53 = False
        v1_1.f_36 = 0.147140
        v1_1.f_17 = s[0:7]
        v1_1.f_70.append(s[0:4])
        v1_1.f_67 = 0x1F542DF55B895
        v1_1.f_33.append(Message15_M1_M2.E10_CONST_5)
        v1_1.f_23 = 0x59
        v1_1.f_58 = 0x6A
        v1_1.f_51 = 0x3A1E81082B32
        v1_1.f_28 = Message15_M1_M2.E8_CONST_1
        v1_1.f_71 = Message15_M1_M2.E11_CONST_2
        v1_1.f_20 = 0xE
        v1_1.f_14 = 0x7DD3C6021
        v1_1.f_43 = 0x950C33
        v1_1.f_39 = b[0:24]
        v1_1.f_7 = 0x206E40D1337AB94B
        v1_1.f_4 = 0x324123CC
        v1_1.f_41 = 0x30
        v0.f_7 = Message15_M1.E1_CONST_4
        v0.f_23 = b[0:64]
        v0.f_29 = 0xE019AA911586
        v0.f_22 = 0x7A

    def message15_set_2(self, message: Message15, s: str, b: bytes) -> None:
        Message15_M1 = self.Message15_M1
        Message15_M1_M2 = self.Message15_M1_M2
        Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14 = (
            self.Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14
        )
        v0 = message.f_3
        v0.f_4 = s[0:8]
        v0.f_2 = 0.329908
        v0.f_6 = 0xCBF8417
        v0.f_23 = b[0:14147]
        v0.f_33 = Message15_M1.E4_CONST_3
        v0.f_10 = 0x1F275BF7F
        v0.f_1 = 0x9A4A024
        v0.f_32 = 0x20
        v1_0 = v0.f_48.add()
        v1_0.f_2 = Message15_M1_M2.E5_CONST_3
        v1_0.f_40 = True
        v1_0.f_45.append(s[0:64])
        v2 = v1_0.f_103
        v3 = v2.f_4
        v4 = v3.f_7
        v5_0 = v4.f_3.add()
        v5_0.f_0 = s[0:3]
        v6 = v5_0.f_3
        v7 = v6.f_4
        v8 = v7.f_2
        v8.f_2 = 0x641348971F0D2E1C
        v8.f_9 = Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E15_CONST_4
        v8.f_6 = 0xC76ED4F
        v6.f_2 = 0x99312EF
        v5_1 = v4.f_3.add()
        v9 = v5_1.f_3
        v10 = v9.f_4
        v11 = v10.f_2
        v11.f_7.extend(
            [
                0x2A7D074,
                0x75E5D61,
                0x34BFA7B,
                0x1E6CCBB,
                0x7E,
                0xC979DF,
                0x6AD4EC3,
                0x2A,
                0xDCFB25F,
                0x72,
                0x2776789,
                0xED48AB5,
                0x97C779B,
                0x67A52,
                0x933E871,
                0xCB47637,
                0xE5D8C5F,
                0x6883F5E,
                0x171D89,
                0x30E00D9,
                0x4D47FE2,
                0xA881378,
                0x115BD9,
                0x1C67,
                0x19BA6ED,
                0x13E698,
                0x256FCDC,
                0x30753AA,
                0xEF3A741,
                0x6CC557D,
                0xC026ECD,
                0x98056,
                0xEF40E,
                0xA6F18,
                0x4962B5D,
                0xF6BA16F,
                0x56,
                0x33,
                0xF98F9,
                0x9A8DCC4,
                0x130CEC,
                0xB157C37,
                0xA5C2C,
                0xBF5,
                0x68,
            ]
        )
        v11.f_2 = 0x1A6E0CBBD93238A9
        v11.f_1.append(Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E14_CONST_4)
        v11.f_0 = Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E13_CONST_5
        v12 = v3.f_6
        v12.SetInParent()
        v3.f_1 = s[0:14]
        v3.f_3 = 0.081370
        v3.f_0 = 0x2269
        v1_0.f_68 = 0x34B657845
        v1_0.f_55 = s[0:9]
        v1_0.f_20 = 0x14DE
        v1_0.f_53 = False
        v1_0.f_26 = 0x1082
        v1_0.f_10 = 0xAFA2EEFD4703AF5
        v1_0.f_47 = False
        v1_0.f_35 = 0x50
        v1_0.f_3 = s[0:18]
        v1_0.f_27 = 0x1688C369560A0
        v1_0.f_0 = 0.972370
        v1_0.f_4 = 0x8
        v1_0.f_72.append(0x70)
        v1_0.f_72.append(0x82DFC)
        v1_0.f_38 = 0.774744
        v1_0.f_65 = s[0:32]
        v1_0.f_54 = b[0:1]
        v1_0.f_28 = Message15_M1_M2.E8_CONST_4
        v1_0.f_9.extend(
            [
                0xD8EAED2,
                0x19,
                0x62,
                0x7799014,
                0x2C729F0,
                0xAB992A4,
                0xF360314,
                0xE5B4C0C,
                0x3FECE8D,
                0xE9789E0,
                0x3602,
                0x6A8,
                0xB23D584,
                0x1637C4,
                0x33869,
                0xF4BA91,
                0xA6952CE,
                0x15,
                0x2F62337,
                0x7737932,
                0x4F,
                0x468970C,
                0x9,
                0xA3B5AF9,
                0x1873A0,
                0x57,
                0xA2432A0,
                0x7C,
                0x53,
                0xFF06BE6,
                0x1F45B6,
                0x3312,
                0x7CEDEBD,
                0x45B5896,
                0x1C19D2,
                0x7849B68,
                0x300DD,
                0x9C41C,
                0xAE70263,
                0x286C3CD,
                0x982B106,
                0x1D4D74,
                0x3CC4344,
                0x16,
                0x604CF3B,
                0x4BBDAB3,
                0x1997E6,
                0x16DEC2,
                0x1D8516B,
                0x7EFC0C1,
                0x8BFDFBC,
                0xA1F8A59,
                0xD8D71,
                0x4ACF02E,
            ]
        )
        v1_0.f_42 = 0x2CF
        v1_0.f_58 = 0xDCB2BA0A5E2CF8
        v1_0.f_60 = 0.840559
        v1_0.f_57 = s[0:2]
        v1_0.f_14 = 0x8CA68901FE1CE8
        v1_0.f_73 = 0.461768
        v1_0.f_30 = 0x53469AA7EFA00C
        v1_0.f_69 = 0xC893075
        v1_0.f_13 = s[0:13]
        v0.f_17 = Message15_M1.E2_CONST_2
        v0.f_13 = 0.870645
        v0.f_11 = 0x47
        v0.f_8 = 0x7D
        for n in [2, 27, 3, 36, 36]:
            v0.f_30.append(s[0:n])
        v0.f_24 = 0x3AC8
        message.f_0 = 0xE

    def message15_set_3(self, message: Message15, s: str, b: bytes) -> None:
        Message15_M1 = self.Message15_M1
        Message15_M1_M2 = self.Message15_M1_M2
        Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14 = (
            self.Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14
        )
        v0 = message.f_3
        v0.f_32 = 0xAB64FD9
        v1_0 = v0.f_48.add()
        v1_0.f_30 = 0x1F2830631F26E
        v1_0.f_54 = b[0:10]
        v1_0.f_14 = 0x5E39E064F
        v1_0.f_55 = s[0:1]
        v1_0.f_67 = 0x1B65C
        v1_0.f_33.append(Message15_M1_M2.E10_CONST_3)
        v1_0.f_33.append(Message15_M1_M2.E10_CONST_5)
        v1_0.f_74 = 0x12A136729070821C
        v1_0.f_56 = 0.362431
        v1_0.f_47 = False
        v1_0.f_19 = s[0:7]
        v1_0.f_57 = s[0:11]
        v1_0.f_41 = 0x347A
        v1_0.f_60 = 0.853297
        v1_0.f_8 = 0x55ACA54AEB878C97
        v1_0.f_3 = s[0:56]
        v1_0.f_6 = 0.681241
        v1_0.f_5 = 0x80AA13042181EF
        v1_0.f_61 = True
        v1_0.f_29 = s[0:4]
        v1_0.f_44 = s[0:5]
        v1_0.f_37 = 0xA18B0FE
        v1_0.f_38 = 0.484341
        v2 = v1_0.f_103
        v3 = v2.f_4
        v3.f_3 = 0.437082
        v4 = v3.f_6
        v5_0 = v4.f_5.add()
        v4.f_0 = 0x3C
        v6 = v3.f_7
        v6.f_0 = 0x1F
        v7_0 = v6.f_3.add()
        v8 = v7_0.f_3
        v9 = v8.f_4
        v10 = v9.f_2
        v10.f_0 = Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E13_CONST_4
        v10.f_1.append(Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E14_CONST_5)
        v10.f_1.append(Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E14_CONST_3)
        v10.f_2 = 0x4EC051E5E49D615F
        v10.f_3 = 0x29E0404B1B8EB9
        v10.f_7.append(0x5D4DF)
        v9.f_0 = 0x66
        v3.f_0 = 0x5F27C84C6C0BC
        v2.f_1 = 0x215414079
        v1_0.f_16 = Message15_M1_M2.E7_CONST_4
        v1_0.f_62 = s[0:58]
        v1_0.f_58 = 0x63
        v1_0.f_23 = 0x19
        v0.f_3 = 0.267157
        v0.f_21 = 0x114686
        v0.f_33 = Message15_M1.E4_CONST_1
        v0.f_19 = 0x5FBB60D43
        v0.f_8 = 0x1730B9
        v0.f_13 = 0.313499
        v0.f_6 = 0x24D7
        v0.f_0 = 0x76EADB3F
        v0.f_5 = 0x3B
        v0.f_24 = 0xC4DFAAD52C17C3
        v0.f_22 = 0x7B
        v0.f_4 = s[0:12]
        v0.f_27 = s[0:10]
        v0.f_29 = 0x388

    def message15_set_4(self, message: Message15, s: str, b: bytes) -> None:
        Message15_M1 = self.Message15_M1
        Message15_M1_M2 = self.Message15_M1_M2
        Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14 = (
            self.Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14
        )
        v0 = message.f_3
        v0.f_8 = 0x5E
        v0.f_27 = s[0:15]
        v0.f_1 = 0xB655E9C
        v0.f_29 = 0x7CE3833CA3A938
        v0.f_6 = 0x30D090D
        v0.f_24 = 0x3A8EB2B35B49B
        v0.f_19 = 0x28
        v0.f_3 = 0.046031
        v0.f_17 = Message15_M1.E2_CONST_2
        v0.f_22 = 0xD
        v0.f_11 = 0x30
        v0.f_33 = Message15_M1.E4_CONST_4
        v0.f_12 = 0x419A28FF7
        v0.f_34 = 0xD2E31195
        v0.f_32 = 0x4
        v1_0 = v0.f_48.add()
        v1_0.f_25 = 0x61
        v1_0.f_71 = Message15_M1_M2.E11_CONST_1
        v1_0.f_16 = Message15_M1_M2.E7_CONST_1
        v1_0.f_7 = 0x2CBA83B4B701EB5C
        v1_0.f_34.append(s[0:5])
        v1_0.f_5 = 0x1C1D3A9B7E18
        v2 = v1_0.f_103
        v3 = v2.f_4
        v4 = v3.f_6
        v4.SetInParent()
        v5 = v3.f_7
        v6_0 = v5.f_3.add()
        v7 = v6_0.f_3
        v7.f_0 = 0x43
        v7.f_1.append(0x7C)
        v8 = v7.f_4
        v9 = v8.f_2
        v9.f_1.append(Message15_M1_M2_M4_M6_M8_M9_M12_M13_M14.E14_CONST_5)
        v9.f_8 = 0x19
        v8.f_0 = 0x920
        v7.f_2 = 0x21E997F7
        v1_0.f_58 = 0x6098BD0
        v1_0.f_47 = True
        v1_0.f_24 = 0.742325
        v1_0.f_17 = s[0:6]
        v1_0.f_2 = Message15_M1_M2.E5_CONST_5
        v1_0.f_32 = s[0:16]
        v1_0.f_62 = s[0:6]
        v1_0.f_30 = 0x786739C667C2
        v1_0.f_72.append(0x60F5B1BD23B5AA)
        v1_0.f_21 = s[0:5]
        v1_0.f_3 = s[0:3]
        v1_0.f_67 = 0x3B1A
        v1_0.f_27 = 0xAA142C4F738C95
        v1_0.f_65 = s[0:2]
        v1_0.f_54 = b[0:17629]
        v1_0.f_15 = 0x2557375CDC9BDFB9
        v1_0.f_60 = 0.939886
        v10 = v1_0.f_102
        v10.SetInParent()
        v1_0.f_70.append(s[0:18])
        v1_0.f_70.append(s[0:17])
        v1_0.f_70.append(s[0:3])
        v1_0.f_12 = 0x5A7B71
        v1_0.f_41 = 0xEC1F9DC
        v1_0.f_31 = Message15_M1_M2.E9_CONST_3
        v1_0.f_69 = 0x52

    def message15_get_1(self, message: Message15) -> None:
        v0 = message.f_3
        v0.f_1
        v0.f_6
        v0.f_19
        v0.f_18
        v0.f_24
        v0.f_4
        v0.f_0
        v0.f_11
        v0.f_23
        for v1 in v0.f_48:
            v1.f_5
            v1.f_51
            v1.f_27
            v1.f_28
            v1.f_64
            v1.f_58
            v1.f_61
            v1.f_8
            v1.f_50
            v1.f_36
            v1.f_4
            v1.f_16
            for i in range(len(v1.f_46)):
                v1.f_46[i]
            for i in range(len(v1.f_11)):
                v1.f_11[i]
            v1.f_40
            v1.f_42
            v1.f_30
            v1.f_0
            v1.f_31
            v1.f_62
            v1.f_55
            v1.f_66
            v1.f_49
            v1.f_35
            for i in range(len(v1.f_45)):
                v1.f_45[i]
            v1.f_47
            v1.f_67
            for i in range(len(v1.f_72)):
                v1.f_72[i]
            v1.f_44
            v1.f_21
            v1.f_17
            for i in range(len(v1.f_33)):
                v1.f_33[i]
            v1.f_74
            v1.f_63
            v1.f_7
            v1.f_56
            v1.f_69
            v1.f_3
            v1.f_22
            v1.f_39
            for i in range(len(v1.f_9)):
                v1.f_9[i]
            v1.f_25
            v1.f_73
            v1.f_14
            v1.f_41
            v1.f_15
            v1.f_1
            v1.f_60
            v1.f_65
            v1.f_32
            v1.f_43
            v1.f_20
            v1.f_24
            v1.f_53
            v1.f_29
            v1.f_18
            v1.f_38
            v1.f_26
            for i in range(len(v1.f_70)):
                v1.f_70[i]
            v2 = v1.f_103
            v2.f_0
            v3 = v2.f_3
            v3.f_0
            v2.f_1
            v4 = v2.f_4
            v4.f_2
            v5 = v4.f_7
            for v6 in v5.f_3:
                v7 = v6.f_3
                v8 = v7.f_4
                v8.f_0
                v9 = v8.f_2
                v9.f_6
                v9.f_4
                v9.f_0
                v9.f_2
                v9.f_5
                v9.f_3
                for i in range(len(v9.f_7)):
                    v9.f_7[i]
                v9.f_9
                v9.f_8
                for i in range(len(v9.f_1)):
                    v9.f_1[i]
                v7.f_0
                v7.f_2
                for i in range(len(v7.f_1)):
                    v7.f_1[i]
                v6.f_0
            v5.f_0
            v4.f_0
            v4.f_3
            v10 = v4.f_6
            v11 = v10.f_4
            v11.f_0
            v10.f_1
            v10.f_0
            for v12 in v10.f_5:
                for i in range(len(v12.f_0)):
                    v12.f_0[i]
            v4.f_1
            v4.f_4
            v1.f_10
            v1.f_68
            v1.f_52
            v1.f_12
            v1.f_13
            v1.f_23
            v1.f_37
            v1.f_2
            v1.f_54
            v1.f_71
            v13 = v1.f_102
            v13.f_0
            for i in range(len(v1.f_34)):
                v1.f_34[i]
            v1.f_6
            v1.f_57
            v1.f_59
            v1.f_48
            v1.f_19
        v0.f_17
        v0.f_16
        for i in range(len(v0.f_30)):
            v0.f_30[i]
        v0.f_5
        v0.f_33
        v0.f_10
        v0.f_12
        v0.f_25
        v0.f_20
        v0.f_3
        v0.f_7
        v0.f_8
        v0.f_31
        v0.f_21
        for i in range(len(v0.f_28)):
            v0.f_28[i]
        v0.f_32
        v0.f_9
        v0.f_29
        v0.f_2
        v0.f_34
        v0.f_14
        v0.f_22
        v0.f_13
        for i in range(len(v0.f_26)):
            v0.f_26[i]
        v0.f_15
        v0.f_27
        message.f_0

    def message15_get_2(self, message: Message15) -> None:
        message.f_0
        v0 = message.f_3
        v0.f_16
        for v1 in v0.f_48:
            v1.f_43
            v1.f_37
            v1.f_8
            v1.f_51
            for i in range(len(v1.f_9)):
                v1.f_9[i]
            v1.f_65
            v1.f_23
            v1.f_32
            v1.f_55
            v1.f_14
            v1.f_16
            v1.f_30
            v1.f_0
            v1.f_4
            v1.f_41
            v1.f_5
            v1.f_60
            for i in range(len(v1.f_34)):
                v1.f_34[i]
            v1.f_66
            v1.f_48
            v1.f_63
            v1.f_74
            v1.f_24
            v1.f_27
            v1.f_49
            v1.f_42
            v2 = v1.f_103
            v2.f_0
            v3 = v2.f_3
            v3.f_0
            v2.f_1
            v4 = v2.f_4
            v4.f_0
            v4.f_4
            v5 = v4.f_6
            v5.f_0
            v5.f_1
            for v6 in v5.f_5:
                for i in range(len(v6.f_0)):
                    v6.f_0[i]
            v7 = v5.f_4
            v7.f_0
            v4.f_2
            v4.f_1
            v4.f_3
            v8 = v4.f_7
            for v9 in v8.f_3:
                v10 = v9.f_3
                for i in range(len(v10.f_1)):
                    v10.f_1[i]
                v10.f_0
                v10.f_2
                v11 = v10.f_4
                v12 = v11.f_2
                v12.f_9
                v12.f_8
                v12.f_0
                v12.f_6
                v12.f_5
                v12.f_3
                for i in range(len(v12.f_7)):
                    v12.f_7[i]
                for i in range(len(v12.f_1)):
                    v12.f_1[i]
                v12.f_4
                v12.f_2
                v11.f_0
                v9.f_0
            v8.f_0
            v1.f_50
            for i in range(len(v1.f_33)):
                v1.f_33[i]
            v1.f_1
            v1.f_17
            v1.f_13
            v1.f_31
            v1.f_20
            v1.f_47
            v1.f_52
            for i in range(len(v1.f_46)):
                v1.f_46[i]
            v1.f_68
            v1.f_67
            v1.f_69
            v1.f_44
            v1.f_22
            v1.f_7
            for i in range(len(v1.f_70)):
                v1.f_70[i]
            v1.f_38
            v1.f_59
            v1.f_57
            v1.f_2
            for i in range(len(v1.f_11)):
                v1.f_11[i]
            v1.f_19
            v1.f_21
            v1.f_35
            v1.f_39
            v1.f_62
            for i in range(len(v1.f_72)):
                v1.f_72[i]
            v1.f_54
            v1.f_56
            v1.f_36
            v1.f_28
            v1.f_71
            v1.f_64
            v1.f_73
            v1.f_29
            v1.f_40
            v1.f_25
            v1.f_3
            v1.f_53
            v1.f_6
            v1.f_18
            v1.f_15
            v1.f_58
            v1.f_10
            v1.f_61
            v13 = v1.f_102
            v13.f_0
            for i in range(len(v1.f_45)):
                v1.f_45[i]
            v1.f_26
            v1.f_12
        v0.f_18
        v0.f_0
        v0.f_1
        v0.f_11
        v0.f_15
        v0.f_29
        v0.f_6
        v0.f_12
        v0.f_3
        v0.f_23
        v0.f_5
        v0.f_32
        v0.f_25
        v0.f_8
        v0.f_20
        for i in range(len(v0.f_26)):
            v0.f_26[i]
        v0.f_14
        v0.f_33
        v0.f_9
        v0.f_4
        v0.f_19
        v0.f_27
        v0.f_17
        for i in range(len(v0.f_30)):
            v0.f_30[i]
        v0.f_7
        v0.f_34
        v0.f_13
        v0.f_21
        v0.f_22
        v0.f_10
        for i in range(len(v0.f_28)):
            v0.f_28[i]
        v0.f_31
        v0.f_24
        v0.f_2

    def message15_get_3(self, message: Message15) -> None:
        message.f_0
        v0 = message.f_3
        v0.f_34
        v0.f_1
        v0.f_4
        v0.f_15
        v0.f_11
        v0.f_21
        v0.f_24
        v0.f_18
        v0.f_10
        v0.f_32
        v0.f_9
        for i in range(len(v0.f_30)):
            v0.f_30[i]
        v0.f_33
        v0.f_27
        v0.f_19
        v0.f_29
        v0.f_13
        v0.f_31
        v0.f_2
        for i in range(len(v0.f_28)):
            v0.f_28[i]
        v0.f_25
        v0.f_22
        v0.f_8
        v0.f_6
        v0.f_7
        v0.f_5
        v0.f_14
        v0.f_20
        v0.f_23
        v0.f_3
        v0.f_16
        v0.f_12
        for i in range(len(v0.f_26)):
            v0.f_26[i]
        v0.f_17
        v0.f_0
        for v1 in v0.f_48:
            v1.f_65
            v1.f_18
            v1.f_0
            v1.f_37
            v1.f_6
            v1.f_19
            v1.f_73
            v1.f_74
            v1.f_31
            v1.f_29
            v1.f_21
            v1.f_47
            v1.f_48
            v1.f_28
            v1.f_2
            v1.f_55
            v1.f_13
            v1.f_25
            v1.f_30
            for i in range(len(v1.f_9)):
                v1.f_9[i]
            v1.f_5
            v1.f_53
            v1.f_71
            v1.f_69
            v1.f_26
            v1.f_59
            for i in range(len(v1.f_46)):
                v1.f_46[i]
            v1.f_22
            v1.f_12
            v1.f_1
            v1.f_52
            v1.f_43
            v1.f_61
            v1.f_60
            v1.f_20
            v2 = v1.f_102
            v2.f_0
            v1.f_68
            v1.f_36
            for i in range(len(v1.f_11)):
                v1.f_11[i]
            v1.f_66
            for i in range(len(v1.f_33)):
                v1.f_33[i]
            v1.f_40
            v1.f_39
            v1.f_4
            for i in range(len(v1.f_34)):
                v1.f_34[i]
            v1.f_44
            v1.f_23
            for i in range(len(v1.f_45)):
                v1.f_45[i]
            v1.f_51
            v3 = v1.f_103
            v3.f_0
            v3.f_1
            v4 = v3.f_4
            v4.f_1
            v5 = v4.f_7
            v5.f_0
            for v6 in v5.f_3:
                v6.f_0
                v7 = v6.f_3
                v8 = v7.f_4
                v8.f_0
                v9 = v8.f_2
                for i in range(len(v9.f_7)):
                    v9.f_7[i]
                v9.f_3
                v9.f_2
                v9.f_6
                v9.f_5
                v9.f_9
                v9.f_4
                v9.f_8
                v9.f_0
                for i in range(len(v9.f_1)):
                    v9.f_1[i]
                v7.f_2
                for i in range(len(v7.f_1)):
                    v7.f_1[i]
                v7.f_0
            v4.f_2
            v4.f_4
            v4.f_0
            v10 = v4.f_6
            for v11 in v10.f_5:
                for i in range(len(v11.f_0)):
                    v11.f_0[i]
            v10.f_1
            v12 = v10.f_4
            v12.f_0
            v10.f_0
            v4.f_3
            v13 = v3.f_3
            v13.f_0
            v1.f_41
            v1.f_50
            v1.f_8
            v1.f_63
            v1.f_58
            v1.f_67
            v1.f_64
            v1.f_17
            for i in range(len(v1.f_72)):
                v1.f_72[i]
            v1.f_24
            v1.f_54
            v1.f_16
            v1.f_38
            v1.f_35
            v1.f_57
            v1.f_14
            v1.f_7
            v1.f_15
            v1.f_3
            for i in range(len(v1.f_70)):
                v1.f_70[i]
            v1.f_62
            v1.f_42
            v1.f_27
            v1.f_10
            v1.f_49
            v1.f_32
            v1.f_56

    def message15_get_4(self, message: Message15) -> None:
        message.f_0
        v0 = message.f_3
        for v1 in v0.f_48:
            v1.f_6
            v1.f_28
            v1.f_24
            v1.f_17
            v1.f_3
            v1.f_66
            v1.f_56
            v2 = v1.f_102
            v2.f_0
            v1.f_65
            v1.f_29
            v1.f_5
            v1.f_23
            for i in range(len(v1.f_45)):
                v1.f_45[i]
            v1.f_4
            v1.f_68
            v1.f_21
            v1.f_48
            v1.f_64
            v1.f_25
            v1.f_22
            v1.f_36
            v1.f_51
            v1.f_26
            v1.f_12
            v1.f_58
            v1.f_62
            v1.f_40
            for i in range(len(v1.f_34)):
                v1.f_34[i]
            v3 = v1.f_103
            v4 = v3.f_3
            v4.f_0
            v3.f_0
            v5 = v3.f_4
            v5.f_3
            v6 = v5.f_7
            v6.f_0
            for v7 in v6.f_3:
                v7.f_0
                v8 = v7.f_3
                v9 = v8.f_4
                v10 = v9.f_2
                for i in range(len(v10.f_1)):
                    v10.f_1[i]
                v10.f_2
                v10.f_0
                v10.f_8
                v10.f_6
                v10.f_3
                v10.f_9
                for i in range(len(v10.f_7)):
                    v10.f_7[i]
                v10.f_5
                v10.f_4
                v9.f_0
                for i in range(len(v8.f_1)):
                    v8.f_1[i]
                v8.f_0
                v8.f_2
            v5.f_2
            v11 = v5.f_6
            for v12 in v11.f_5:
                for i in range(len(v12.f_0)):
                    v12.f_0[i]
            v11.f_1
            v11.f_0
            v13 = v11.f_4
            v13.f_0
            v5.f_1
            v5.f_0
            v5.f_4
            v3.f_1
            v1.f_8
            v1.f_52
            for i in range(len(v1.f_11)):
                v1.f_11[i]
            v1.f_32
            v1.f_20
            for i in range(len(v1.f_46)):
                v1.f_46[i]
            v1.f_39
            v1.f_18
            for i in range(len(v1.f_70)):
                v1.f_70[i]
            v1.f_74
            v1.f_42
            v1.f_1
            v1.f_16
            v1.f_0
            v1.f_2
            v1.f_50
            v1.f_71
            v1.f_73
            v1.f_43
            v1.f_38
            v1.f_61
            v1.f_19
            v1.f_44
            v1.f_60
            v1.f_35
            v1.f_55
            for i in range(len(v1.f_9)):
                v1.f_9[i]
            v1.f_59
            for i in range(len(v1.f_72)):
                v1.f_72[i]
            v1.f_31
            v1.f_63
            v1.f_49
            v1.f_37
            v1.f_13
            v1.f_15
            v1.f_41
            v1.f_54
            v1.f_53
            v1.f_14
            v1.f_7
            v1.f_27
            for i in range(len(v1.f_33)):
                v1.f_33[i]
            v1.f_67
            v1.f_30
            v1.f_10
            v1.f_69
            v1.f_57
            v1.f_47
        v0.f_7
        v0.f_33
        v0.f_19
        for i in range(len(v0.f_28)):
            v0.f_28[i]
        v0.f_4
        v0.f_21
        for i in range(len(v0.f_30)):
            v0.f_30[i]
        v0.f_3
        v0.f_14
        v0.f_23
        v0.f_27
        for i in range(len(v0.f_26)):
            v0.f_26[i]
        v0.f_31
        v0.f_5
        v0.f_15
        v0.f_18
        v0.f_34
        v0.f_1
        v0.f_2
        v0.f_6
        v0.f_24
        v0.f_11
        v0.f_0
        v0.f_16
        v0.f_22
        v0.f_10
        v0.f_25
        v0.f_29
        v0.f_8
        v0.f_12
        v0.f_20
        v0.f_13
        v0.f_9
        v0.f_32
        v0.f_17
