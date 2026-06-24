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
from __future__ import annotations

from math import copysign

from .gen.messages_pb import ImplicitFields


def test_negative_zero() -> None:
    positive = ImplicitFields(float_field=0.0)
    negative = ImplicitFields(float_field=-0.0)

    assert positive.to_binary() != negative.to_binary()

    assert (
        copysign(1, ImplicitFields.from_binary(positive.to_binary()).float_field) == 1
    )
    assert (
        copysign(1, ImplicitFields.from_binary(negative.to_binary()).float_field) == -1
    )
