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

# Generated from fleetbench access_message12.cc by _fleetbench.py. DO NOT EDIT.
#
# Derived from github.com/google/fleetbench
# Copyright 2025 The Fleetbench Authors
# SPDX-License-Identifier: Apache-2.0
# ruff: noqa: F841
# pyright: reportUnusedExpression=false
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bench.gen.fleetbench.Message12_pb2 import Message12


class Message12Access:
    if TYPE_CHECKING:
        # Provided by the Access subclass, which wires the
        # backend's classes; never assigned on the mixin itself.
        Message12: type[Message12]
        Message12_M1_M2: type[Message12.M1.M2]
        Message12_M1_M2_M3_M9: type[Message12.M1.M2.M3.M9]
        Message12_M1_M2_M4_M7_M14_M20_M22_M25: type[
            Message12.M1.M2.M4.M7.M14.M20.M22.M25
        ]
        Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29: type[
            Message12.M1.M2.M4.M7.M14.M20.M22.M25.M27.M29
        ]
        Message12_M1_M2_M4_M7_M16: type[Message12.M1.M2.M4.M7.M16]
        Message12_M1_M2_M6: type[Message12.M1.M2.M6]

    def message12_set_1(self, message: Message12, s: str, b: bytes) -> None:
        Message12 = self.Message12
        Message12_M1_M2 = self.Message12_M1_M2
        Message12_M1_M2_M4_M7_M14_M20_M22_M25 = (
            self.Message12_M1_M2_M4_M7_M14_M20_M22_M25
        )
        Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29 = (
            self.Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29
        )
        Message12_M1_M2_M4_M7_M16 = self.Message12_M1_M2_M4_M7_M16
        Message12_M1_M2_M6 = self.Message12_M1_M2_M6
        message.f_0 = Message12.E1_CONST_3
        v0 = message.f_2
        v1 = v0.f_2
        v1.f_6 = 0x57
        v2_0 = v1.f_13.add()
        v2_0.f_5 = 0x422B45C33F53
        v2_0.f_11 = 0x5E
        v2_0.f_4.append(Message12_M1_M2_M6.E4_CONST_2)
        v1.f_3 = Message12_M1_M2.E2_CONST_4
        v1.f_5.append(s[0:19])
        v1.f_5.append(s[0:47])
        v1.f_5.append(s[0:13])
        v1.f_5.append(s[0:4])
        v3_0 = v1.f_11.add()
        v4_0 = v3_0.f_2.add()
        v5_0 = v4_0.f_4.add()
        v6 = v5_0.f_2
        v7_0 = v6.f_2.add()
        v7_0.f_0 = 0.256808
        v5_0.f_0 = 0x21
        v8 = v4_0.f_6
        v8.f_6 = Message12_M1_M2_M4_M7_M16.E7_CONST_2
        v8.f_12 = 0.782744
        v8.f_13 = Message12_M1_M2_M4_M7_M16.E8_CONST_4
        v8.f_8 = 0x6F
        v8.f_2 = 0x1A3E0B2
        v8.f_0 = 0xE0BAEB4
        v8.f_3 = 0x79
        v8.f_23 = 0x9F1F68D
        v8.f_17 = 0x7FC81AB6D29B4AC4
        v4_0.f_0 = b[0:34]
        v9 = v4_0.f_3
        v10 = v9.f_2
        v10.f_0 = 0.681656
        v11_0 = v10.f_3.add()
        v3_1 = v1.f_11.add()
        v3_1.f_0 = 0.533492
        v12_0 = v3_1.f_2.add()
        v13 = v12_0.f_6
        v13.f_23 = 0x6B
        v13.f_18 = 0x391903C8B
        v13.f_24.append(0x747A6)
        v13.f_24.append(0x54770)
        v13.f_24.append(0x14)
        v13.f_24.append(0x11861D)
        v13.f_21 = 0.912619
        v13.f_19 = 0.282900
        v13.f_12 = 0.855926
        v13.f_7 = 0xABF6808195A4E6
        v13.f_4 = 0x57
        v13.f_16 = Message12_M1_M2_M4_M7_M16.E10_CONST_3
        v12_0.f_0 = b[0:30]
        v14 = v12_0.f_3
        v15 = v14.f_2
        v16_0 = v15.f_3.add()
        v17 = v16_0.f_3
        v17.f_0 = Message12_M1_M2_M4_M7_M14_M20_M22_M25.E11_CONST_1
        v18 = v17.f_2
        v19_0 = v18.f_2.add()
        v19_0.f_0 = Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29.E12_CONST_4
        v20_0 = v19_0.f_2.add()
        v20_0.f_0 = 0.175452
        v20_1 = v19_0.f_2.add()
        v20_1.f_0 = 0.363899
        v16_0.f_0 = False
        v21_0 = v12_0.f_4.add()
        v22 = v21_0.f_2
        v22.f_0 = 0x49
        v21_1 = v12_0.f_4.add()
        v23 = v21_1.f_2
        v24_0 = v23.f_2.add()
        v25 = v1.f_12
        v25.SetInParent()
        v26_0 = v1.f_10.add()
        v27_0 = v26_0.f_3.add()
        v28_0 = v27_0.f_4.add()
        v29 = v28_0.f_5
        v29.f_8 = 0x3D5F8FBB05A6CB77
        v29.f_4 = 0x1C8B42
        v29.f_0 = s[0:17]
        v29.f_3 = 0x20
        v29.f_5 = 0.585469
        v27_1 = v26_0.f_3.add()
        v30_0 = v27_1.f_4.add()
        v31 = v30_0.f_5
        v31.f_7 = 0xCEC
        v31.f_10 = 0x41
        v31.f_5 = 0.459415
        v31.f_9 = 0x16
        v30_0.f_0 = s[0:10]
        v32 = v30_0.f_4
        v32.SetInParent()
        v30_1 = v27_1.f_4.add()
        v33 = v30_1.f_5
        v33.f_9 = 0x28
        v33.f_5 = 0.117205
        v33.f_1 = 0x5F
        v33.f_7 = 0x43
        v33.f_4 = 0x2C
        v33.f_11 = 0x39AEF5C2
        v34_0 = v26_0.f_5.add()
        v35 = v26_0.f_4
        v36 = v35.f_3
        v37 = v36.f_3
        v38_0 = v37.f_2.add()
        v38_0.f_0 = 0x71324C8313E1CA
        v39 = v38_0.f_3
        v39.f_1 = False
        v38_1 = v37.f_2.add()
        v40 = v38_1.f_3
        v41_0 = v40.f_4.add()
        v0.f_0 = b[0:6]

    def message12_set_2(self, message: Message12, s: str, b: bytes) -> None:
        Message12_M1_M2 = self.Message12_M1_M2
        Message12_M1_M2_M3_M9 = self.Message12_M1_M2_M3_M9
        Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29 = (
            self.Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29
        )
        Message12_M1_M2_M4_M7_M16 = self.Message12_M1_M2_M4_M7_M16
        Message12_M1_M2_M6 = self.Message12_M1_M2_M6
        v0 = message.f_2
        v1 = v0.f_2
        v1.f_4 = 0x2C60
        v1.f_3 = Message12_M1_M2.E2_CONST_2
        v2_0 = v1.f_10.add()
        v3 = v2_0.f_4
        v3.f_0 = Message12_M1_M2_M3_M9.E5_CONST_1
        v4 = v3.f_3
        v5 = v4.f_3
        v6_0 = v5.f_2.add()
        v7 = v6_0.f_3
        v7.f_2 = 0.850811
        v7.f_0 = 0x14
        v8_0 = v2_0.f_3.add()
        v8_0.f_0 = 0.363148
        v9_0 = v8_0.f_4.add()
        v10 = v9_0.f_5
        v10.f_7 = 0xCF0
        v10.f_8 = 0x3090927530AD181E
        v10.f_0 = s[0:5]
        v10.f_9 = 0x10
        v9_0.f_0 = s[0:11]
        v11_0 = v1.f_13.add()
        v11_0.f_5 = 0x1BDA
        v11_0.f_1 = 0x3599C3B80
        v12 = v11_0.f_17
        v12.SetInParent()
        v11_0.f_4.append(Message12_M1_M2_M6.E4_CONST_1)
        v11_0.f_3 = 0.794525
        v1.f_6 = 0xB057A6D
        v13_0 = v1.f_11.add()
        v14_0 = v13_0.f_2.add()
        v15 = v14_0.f_3
        v16 = v15.f_2
        v17_0 = v16.f_3.add()
        v18 = v14_0.f_6
        v18.f_13 = Message12_M1_M2_M4_M7_M16.E8_CONST_3
        v18.f_2 = 0x4F
        v18.f_8 = 0x6D
        v18.f_21 = 0.565025
        v18.f_16 = Message12_M1_M2_M4_M7_M16.E10_CONST_1
        v18.f_15 = Message12_M1_M2_M4_M7_M16.E9_CONST_5
        v18.f_6 = Message12_M1_M2_M4_M7_M16.E7_CONST_4
        v19_0 = v14_0.f_4.add()
        v20 = v19_0.f_2
        v21_0 = v20.f_2.add()
        v14_1 = v13_0.f_2.add()
        v22 = v14_1.f_3
        v23 = v22.f_2
        v24_0 = v23.f_3.add()
        v24_0.f_0 = True
        v25 = v24_0.f_3
        v26 = v25.f_2
        v27_0 = v26.f_2.add()
        v28_0 = v27_0.f_2.add()
        v28_1 = v27_0.f_2.add()
        v27_0.f_0 = Message12_M1_M2_M4_M7_M14_M20_M22_M25_M27_M29.E12_CONST_4
        v27_1 = v26.f_2.add()
        v29_0 = v27_1.f_2.add()
        v24_0.f_1 = s[0:2]
        v30 = v14_1.f_6
        v30.f_16 = Message12_M1_M2_M4_M7_M16.E10_CONST_3
        v30.f_11 = False
        v30.f_0 = 0x5
        v30.f_8 = 0x60
        v30.f_22 = True
        v30.f_7 = 0x3D
        v30.f_9 = b[0:41]
        v30.f_23 = 0x137DB9
        v30.f_19 = 0.308959
        v30.f_10 = True
        v30.f_12 = 0.345252

    def message12_set_3(self, message: Message12, s: str, b: bytes) -> None:
        Message12_M1_M2 = self.Message12_M1_M2
        Message12_M1_M2_M4_M7_M16 = self.Message12_M1_M2_M4_M7_M16
        Message12_M1_M2_M6 = self.Message12_M1_M2_M6
        v0 = message.f_2
        v1 = v0.f_2
        v1.f_3 = Message12_M1_M2.E2_CONST_5
        v2_0 = v1.f_11.add()
        v3_0 = v2_0.f_2.add()
        v4_0 = v3_0.f_4.add()
        v5 = v4_0.f_2
        v5.f_0 = 0xDBEB4
        v6 = v3_0.f_3
        v7 = v6.f_2
        v7.SetInParent()
        v8 = v3_0.f_6
        v8.f_5 = 0xCA80A
        v8.f_4 = 0x4C80E915A4C7B6
        v8.f_11 = False
        v8.f_19 = 0.081712
        v8.f_9 = b[0:69]
        v8.f_6 = Message12_M1_M2_M4_M7_M16.E7_CONST_2
        v8.f_13 = Message12_M1_M2_M4_M7_M16.E8_CONST_2
        v8.f_17 = 0x477E86EADB9A2F67
        v8.f_23 = 0xEFB
        v8.f_10 = True
        v1.f_4 = 0x47
        v9_0 = v1.f_13.add()
        v9_0.f_10 = 0.118165
        v9_0.f_8 = 0.256039
        v9_0.f_5 = 0x45
        v9_0.f_7 = s[0:30]
        v9_0.f_9 = 0x27A88D450
        v9_0.f_2 = Message12_M1_M2_M6.E3_CONST_4
        v9_0.f_1 = 0xF6F89C787CA647
        v10_0 = v1.f_10.add()
        v11 = v10_0.f_4
        v12 = v11.f_3
        v13 = v12.f_3
        v14_0 = v13.f_2.add()
        v14_0.f_0 = 0x7B0CB5A7C6B05
        v15 = v14_0.f_3
        v16_0 = v15.f_4.add()
        v16_0.f_0 = 0.615942
        v16_1 = v15.f_4.add()
        v15.f_2 = 0.940002
        v15.f_0 = 0xA6BFC4178DDC7A
        v17_0 = v10_0.f_3.add()
        v18_0 = v17_0.f_4.add()
        v19 = v18_0.f_5
        v19.f_2 = 0x4EF177B6F
        v19.f_4 = 0x23A043031F68
        v19.f_11 = 0x1EBD456A
        v19.f_1 = 0x36
        v20_0 = v10_0.f_5.add()
        v20_0.f_0 = 0x11CA3BAC
        v10_1 = v1.f_10.add()
        v21_0 = v10_1.f_3.add()
        v22_0 = v21_0.f_4.add()
        v22_0.f_0 = s[0:6]
        v23 = v22_0.f_5
        v23.f_11 = 0x2E435EA2
        v23.f_10 = 0x79
        v23.f_3 = 0x2E0F8B063E5B4B
        v23.f_1 = 0x9E00BC3
        v23.f_5 = 0.040424
        v22_1 = v21_0.f_4.add()
        v24 = v22_1.f_5
        v24.f_7 = 0x3F5367E7CCD02
        v24.f_4 = 0x3D
        v24.f_1 = 0x39
        v24.f_0 = s[0:32]
        v24.f_2 = 0x13
        v24.f_8 = 0x7BA7F351F305A6A9
        v24.f_5 = 0.135590
        v22_1.f_0 = s[0:6]
        v25_0 = v10_1.f_5.add()
        v25_1 = v10_1.f_5.add()
        v25_1.f_1.extend(
            [
                0x66F87,
                0x64517EA,
                0xDD932A6,
                0xA277364,
                0x104FDB,
                0x21,
                0x58D00B8,
                0xA4DBA91,
                0x352B050,
                0x1B3544E,
                0x1A84A3,
                0xAE7F499,
                0x3768F08,
                0x87830,
                0x188635,
                0x6474F1C,
                0x6B333E3,
                0x43667A9,
                0x42F7,
                0xFA66EA1,
                0x28E26C7,
                0x5E,
                0x57,
                0xC30514F,
                0xFAAC627,
                0x19EE,
                0xCCF635A,
                0x22,
                0xBD0EE18,
                0xD435432,
                0x5F1D959,
                0x667CC91,
                0x107181D,
                0x3DDB0A1,
                0x9434CD3,
                0x859812,
                0x1F2C7D,
                0x4DA75C5,
                0x2758,
                0x1F8F2F0,
                0xDBE22FD,
                0x4B6213E,
                0xE265CE1,
                0x785CB0D,
                0x9237E8C,
                0x28B8B09,
                0x20BEE69,
                0xE86FB,
                0xEAB57,
                0x9A93C,
                0x446F089,
                0xDB83129,
                0xF3692CA,
                0x1354,
                0xF38897D,
                0x7FDD06A,
                0xD8FC71E,
                0x76,
                0x5A1A0A2,
                0xA27E8AF,
                0x1C,
                0x28134FC,
                0x36,
                0xB8C148,
                0x2B144,
                0xA42CBAC,
                0xD614220,
                0xEC70B3F,
                0x39291,
                0x1C4556,
                0x2E,
                0x9C61C04,
                0x10550B,
                0x4E680,
                0x127078,
                0x18DD80,
                0xE04BCF6,
                0xB898B8A,
                0x18E79C,
                0x19D1DD,
                0x7ED99E,
                0xFC63035,
                0xDD5798B,
            ]
        )
        v26 = v10_1.f_4
        v27 = v26.f_3
        v28 = v27.f_3
        v29_0 = v28.f_2.add()
        v0.f_0 = b[0:4]

    def message12_set_4(self, message: Message12, s: str, b: bytes) -> None:
        Message12 = self.Message12
        Message12_M1_M2_M3_M9 = self.Message12_M1_M2_M3_M9
        Message12_M1_M2_M4_M7_M16 = self.Message12_M1_M2_M4_M7_M16
        v0 = message.f_2
        v1 = v0.f_2
        v1.f_0 = 0x67
        v2_0 = v1.f_11.add()
        v3_0 = v2_0.f_2.add()
        v4_0 = v3_0.f_4.add()
        v5 = v4_0.f_2
        v5.SetInParent()
        v6 = v3_0.f_6
        v6.f_15 = Message12_M1_M2_M4_M7_M16.E9_CONST_5
        v6.f_3 = 0x40B0576
        v6.f_1 = Message12_M1_M2_M4_M7_M16.E6_CONST_4
        v6.f_8 = 0x24B88EE
        v6.f_14.extend(
            [
                0xC4F34,
                0x69,
                0xEE3102C,
                0xB6BAA50,
                0x3D62EAA,
                0xCF6C6E0,
                0x19CC2D,
                0x10C2263,
                0x7C2B27E,
                0xA15030C,
                0x1D5527,
                0xB474EAF,
                0x58,
                0x60F9DA0,
                0x7D,
                0x1A6BA6,
                0x6F,
                0x6B7875F,
                0x53,
                0x9D5AE19,
                0xC051738,
                0x52128A1,
                0xB,
                0x19F282D,
                0xCB6844A,
                0x8A5F40B,
                0x1E,
                0xAA19917,
                0xBA9D5B5,
                0x120AB72,
                0x717F427,
                0x253C,
                0x599F9,
                0x48,
                0x6ABAD5F,
                0x65D5B9B,
                0x99D08DE,
                0xA66C754,
                0x13,
                0xE085C2C,
                0xA2A88FF,
                0xCB92EBC,
                0x77E4711,
                0x46,
                0x30,
                0x97D74FC,
                0x3C93,
                0x73F131D,
                0xCDFA111,
                0x17,
            ]
        )
        v6.f_4 = 0x27
        v6.f_11 = True
        v6.f_6 = Message12_M1_M2_M4_M7_M16.E7_CONST_5
        v6.f_24.append(0x1567)
        v6.f_24.append(0x51C2A8A)
        v6.f_12 = 0.563049
        v6.f_9 = b[0:111]
        v7 = v3_0.f_3
        v8 = v7.f_2
        v8.f_0 = 0.495130
        v9_0 = v8.f_3.add()
        v10 = v9_0.f_3
        v11 = v10.f_2
        v11.f_0.append(0x14AB)
        v11.f_0.append(0x16)
        v12_0 = v1.f_13.add()
        v12_0.f_9 = 0x1FC88E
        v12_0.f_0 = 0x63
        v13 = v12_0.f_17
        v13.f_0.append(0x83891EA)
        v13.f_0.append(0x125254)
        v13.f_0.append(0x592E3CF)
        v13.f_0.append(0x7E)
        v12_0.f_11 = 0x2725
        v12_0.f_5 = 0x3BA6
        v14_0 = v1.f_10.add()
        v15 = v14_0.f_4
        v15.f_0 = Message12_M1_M2_M3_M9.E5_CONST_5
        v16 = v15.f_3
        v17 = v16.f_3
        v17.f_0 = 0x52
        v14_0.f_0 = 0x5C37291E5
        v18_0 = v14_0.f_5.add()
        v18_0.f_1.extend([0x18, 0xF145A8A, 0x12EA94, 0x36, 0x4B7FB01, 0x38])
        v18_1 = v14_0.f_5.add()
        v18_1.f_0 = 0x14065AE6
        v19_0 = v14_0.f_3.add()
        v20_0 = v19_0.f_4.add()
        v21 = v20_0.f_5
        v21.f_6 = True
        v21.f_9 = 0x56
        v21.f_10 = 0x30
        v21.f_3 = 0x35A238A
        v21.f_8 = 0x2237BC7C7692AC27
        v21.f_1 = 0x4C
        v20_0.f_0 = s[0:11]
        v20_1 = v19_0.f_4.add()
        v22 = v20_1.f_5
        v22.f_6 = False
        v22.f_2 = 0x2F
        v22.f_9 = 0x23
        v22.f_3 = 0x79DE66678
        v22.f_0 = s[0:12]
        v19_0.f_0 = 0.406222
        message.f_0 = Message12.E1_CONST_2

    def message12_get_1(self, message: Message12) -> None:
        v0 = message.f_2
        v1 = v0.f_2
        v1.f_4
        for v2 in v1.f_10:
            v2.f_0
            for v3 in v2.f_5:
                for i in range(len(v3.f_1)):
                    v3.f_1[i]
                v3.f_0
            v4 = v2.f_4
            v4.f_0
            v5 = v4.f_3
            v6 = v5.f_3
            v6.f_0
            for v7 in v6.f_2:
                v7.f_0
                v8 = v7.f_3
                v8.f_1
                v8.f_0
                v8.f_2
                for v9 in v8.f_4:
                    v9.f_0
            v5.f_0
            for v10 in v2.f_3:
                v10.f_0
                for v11 in v10.f_4:
                    v12 = v11.f_4
                    v12.f_0
                    v11.f_0
                    v13 = v11.f_5
                    v13.f_8
                    v13.f_2
                    v13.f_4
                    v13.f_11
                    v13.f_10
                    v13.f_9
                    v13.f_0
                    v13.f_5
                    v13.f_3
                    v13.f_1
                    v13.f_7
                    v13.f_6
        v14 = v1.f_12
        v14.f_0
        v1.f_0
        v1.f_3
        v1.f_6
        v1.f_2
        v1.f_1
        for v15 in v1.f_13:
            v15.f_1
            v15.f_0
            for i in range(len(v15.f_4)):
                v15.f_4[i]
            v16 = v15.f_17
            for i in range(len(v16.f_0)):
                v16.f_0[i]
            v16.f_1
            v15.f_6
            v15.f_2
            v15.f_3
            v15.f_5
            v15.f_7
            v15.f_8
            v15.f_10
            v15.f_9
            v15.f_11
        for v17 in v1.f_11:
            for v18 in v17.f_2:
                v18.f_0
                for v19 in v18.f_4:
                    v19.f_0
                    v20 = v19.f_2
                    v20.f_0
                    for v21 in v20.f_2:
                        v21.f_0
                v22 = v18.f_6
                for i in range(len(v22.f_14)):
                    v22.f_14[i]
                v22.f_13
                v22.f_9
                v22.f_12
                v22.f_2
                v22.f_7
                v22.f_21
                v22.f_17
                v22.f_6
                v22.f_11
                v22.f_15
                for i in range(len(v22.f_24)):
                    v22.f_24[i]
                v22.f_23
                v22.f_20
                v22.f_5
                v22.f_19
                v22.f_18
                v22.f_8
                v22.f_0
                v22.f_1
                v22.f_10
                v22.f_22
                v22.f_4
                v22.f_16
                v22.f_3
                v23 = v18.f_3
                v24 = v23.f_2
                v24.f_0
                for v25 in v24.f_3:
                    v25.f_1
                    v26 = v25.f_3
                    v26.f_0
                    v27 = v26.f_2
                    for i in range(len(v27.f_0)):
                        v27.f_0[i]
                    for v28 in v27.f_2:
                        v28.f_0
                        for v29 in v28.f_2:
                            v29.f_0
                    v25.f_0
                v23.f_0
            v17.f_0
        for i in range(len(v1.f_5)):
            v1.f_5[i]
        v0.f_0
        message.f_0

    def message12_get_2(self, message: Message12) -> None:
        v0 = message.f_2
        v0.f_0
        v1 = v0.f_2
        v1.f_1
        for i in range(len(v1.f_5)):
            v1.f_5[i]
        v1.f_4
        v2 = v1.f_12
        v2.f_0
        v1.f_6
        for v3 in v1.f_13:
            v3.f_9
            v3.f_5
            v3.f_2
            for i in range(len(v3.f_4)):
                v3.f_4[i]
            v3.f_1
            v3.f_6
            v4 = v3.f_17
            for i in range(len(v4.f_0)):
                v4.f_0[i]
            v4.f_1
            v3.f_3
            v3.f_10
            v3.f_0
            v3.f_7
            v3.f_8
            v3.f_11
        v1.f_3
        v1.f_2
        for v5 in v1.f_10:
            for v6 in v5.f_3:
                v6.f_0
                for v7 in v6.f_4:
                    v8 = v7.f_4
                    v8.f_0
                    v7.f_0
                    v9 = v7.f_5
                    v9.f_1
                    v9.f_0
                    v9.f_3
                    v9.f_11
                    v9.f_5
                    v9.f_6
                    v9.f_9
                    v9.f_7
                    v9.f_2
                    v9.f_8
                    v9.f_10
                    v9.f_4
            v10 = v5.f_4
            v11 = v10.f_3
            v11.f_0
            v12 = v11.f_3
            for v13 in v12.f_2:
                v13.f_0
                v14 = v13.f_3
                v14.f_2
                for v15 in v14.f_4:
                    v15.f_0
                v14.f_1
                v14.f_0
            v12.f_0
            v10.f_0
            v5.f_0
            for v16 in v5.f_5:
                v16.f_0
                for i in range(len(v16.f_1)):
                    v16.f_1[i]
        for v17 in v1.f_11:
            v17.f_0
            for v18 in v17.f_2:
                for v19 in v18.f_4:
                    v20 = v19.f_2
                    for v21 in v20.f_2:
                        v21.f_0
                    v20.f_0
                    v19.f_0
                v22 = v18.f_3
                v22.f_0
                v23 = v22.f_2
                for v24 in v23.f_3:
                    v24.f_0
                    v25 = v24.f_3
                    v26 = v25.f_2
                    for i in range(len(v26.f_0)):
                        v26.f_0[i]
                    for v27 in v26.f_2:
                        v27.f_0
                        for v28 in v27.f_2:
                            v28.f_0
                    v25.f_0
                    v24.f_1
                v23.f_0
                v29 = v18.f_6
                v29.f_18
                v29.f_20
                v29.f_4
                v29.f_17
                for i in range(len(v29.f_14)):
                    v29.f_14[i]
                v29.f_3
                v29.f_7
                v29.f_23
                v29.f_12
                v29.f_10
                v29.f_9
                v29.f_16
                v29.f_6
                v29.f_0
                v29.f_2
                v29.f_1
                v29.f_22
                v29.f_19
                v29.f_15
                v29.f_8
                v29.f_5
                v29.f_11
                v29.f_21
                v29.f_13
                for i in range(len(v29.f_24)):
                    v29.f_24[i]
                v18.f_0
        v1.f_0
        message.f_0

    def message12_get_3(self, message: Message12) -> None:
        message.f_0
        v0 = message.f_2
        v1 = v0.f_2
        for v2 in v1.f_11:
            v2.f_0
            for v3 in v2.f_2:
                v4 = v3.f_3
                v4.f_0
                v5 = v4.f_2
                for v6 in v5.f_3:
                    v7 = v6.f_3
                    v7.f_0
                    v8 = v7.f_2
                    for v9 in v8.f_2:
                        for v10 in v9.f_2:
                            v10.f_0
                        v9.f_0
                    for i in range(len(v8.f_0)):
                        v8.f_0[i]
                    v6.f_0
                    v6.f_1
                v5.f_0
                v11 = v3.f_6
                v11.f_20
                v11.f_4
                for i in range(len(v11.f_24)):
                    v11.f_24[i]
                v11.f_6
                v11.f_1
                v11.f_8
                v11.f_7
                v11.f_19
                v11.f_3
                v11.f_9
                v11.f_10
                v11.f_0
                v11.f_5
                v11.f_12
                for i in range(len(v11.f_14)):
                    v11.f_14[i]
                v11.f_22
                v11.f_13
                v11.f_16
                v11.f_11
                v11.f_2
                v11.f_23
                v11.f_17
                v11.f_18
                v11.f_21
                v11.f_15
                for v12 in v3.f_4:
                    v13 = v12.f_2
                    for v14 in v13.f_2:
                        v14.f_0
                    v13.f_0
                    v12.f_0
                v3.f_0
        v1.f_0
        v15 = v1.f_12
        v15.f_0
        v1.f_2
        v1.f_4
        v1.f_3
        v1.f_6
        for i in range(len(v1.f_5)):
            v1.f_5[i]
        for v16 in v1.f_13:
            v16.f_7
            v16.f_0
            v16.f_2
            for i in range(len(v16.f_4)):
                v16.f_4[i]
            v16.f_3
            v16.f_5
            v17 = v16.f_17
            for i in range(len(v17.f_0)):
                v17.f_0[i]
            v17.f_1
            v16.f_9
            v16.f_11
            v16.f_10
            v16.f_1
            v16.f_6
            v16.f_8
        v1.f_1
        for v18 in v1.f_10:
            for v19 in v18.f_3:
                for v20 in v19.f_4:
                    v20.f_0
                    v21 = v20.f_5
                    v21.f_10
                    v21.f_2
                    v21.f_11
                    v21.f_6
                    v21.f_0
                    v21.f_7
                    v21.f_5
                    v21.f_4
                    v21.f_3
                    v21.f_1
                    v21.f_8
                    v21.f_9
                    v22 = v20.f_4
                    v22.f_0
                v19.f_0
            v23 = v18.f_4
            v24 = v23.f_3
            v24.f_0
            v25 = v24.f_3
            v25.f_0
            for v26 in v25.f_2:
                v26.f_0
                v27 = v26.f_3
                v27.f_2
                v27.f_1
                v27.f_0
                for v28 in v27.f_4:
                    v28.f_0
            v23.f_0
            v18.f_0
            for v29 in v18.f_5:
                v29.f_0
                for i in range(len(v29.f_1)):
                    v29.f_1[i]
        v0.f_0

    def message12_get_4(self, message: Message12) -> None:
        message.f_0
        v0 = message.f_2
        v0.f_0
        v1 = v0.f_2
        v1.f_2
        for v2 in v1.f_11:
            v2.f_0
            for v3 in v2.f_2:
                v4 = v3.f_3
                v5 = v4.f_2
                v5.f_0
                for v6 in v5.f_3:
                    v6.f_1
                    v7 = v6.f_3
                    v7.f_0
                    v8 = v7.f_2
                    for v9 in v8.f_2:
                        v9.f_0
                        for v10 in v9.f_2:
                            v10.f_0
                    for i in range(len(v8.f_0)):
                        v8.f_0[i]
                    v6.f_0
                v4.f_0
                v3.f_0
                for v11 in v3.f_4:
                    v12 = v11.f_2
                    v12.f_0
                    for v13 in v12.f_2:
                        v13.f_0
                    v11.f_0
                v14 = v3.f_6
                v14.f_23
                v14.f_13
                v14.f_19
                v14.f_2
                v14.f_1
                for i in range(len(v14.f_14)):
                    v14.f_14[i]
                v14.f_20
                v14.f_5
                v14.f_17
                v14.f_21
                v14.f_22
                v14.f_7
                v14.f_11
                v14.f_18
                v14.f_3
                v14.f_9
                v14.f_16
                v14.f_15
                for i in range(len(v14.f_24)):
                    v14.f_24[i]
                v14.f_0
                v14.f_6
                v14.f_8
                v14.f_10
                v14.f_12
                v14.f_4
        v1.f_4
        v1.f_6
        for i in range(len(v1.f_5)):
            v1.f_5[i]
        for v15 in v1.f_10:
            v15.f_0
            v16 = v15.f_4
            v16.f_0
            v17 = v16.f_3
            v17.f_0
            v18 = v17.f_3
            for v19 in v18.f_2:
                v20 = v19.f_3
                v20.f_2
                for v21 in v20.f_4:
                    v21.f_0
                v20.f_0
                v20.f_1
                v19.f_0
            v18.f_0
            for v22 in v15.f_3:
                for v23 in v22.f_4:
                    v24 = v23.f_4
                    v24.f_0
                    v23.f_0
                    v25 = v23.f_5
                    v25.f_2
                    v25.f_3
                    v25.f_8
                    v25.f_5
                    v25.f_7
                    v25.f_10
                    v25.f_1
                    v25.f_11
                    v25.f_6
                    v25.f_4
                    v25.f_0
                    v25.f_9
                v22.f_0
            for v26 in v15.f_5:
                for i in range(len(v26.f_1)):
                    v26.f_1[i]
                v26.f_0
        for v27 in v1.f_13:
            v27.f_5
            v27.f_6
            v27.f_2
            v27.f_7
            v27.f_0
            for i in range(len(v27.f_4)):
                v27.f_4[i]
            v28 = v27.f_17
            v28.f_1
            for i in range(len(v28.f_0)):
                v28.f_0[i]
            v27.f_10
            v27.f_9
            v27.f_3
            v27.f_1
            v27.f_11
            v27.f_8
        v29 = v1.f_12
        v29.f_0
        v1.f_3
        v1.f_1
        v1.f_0
