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

import pytest

from protobuf import Oneof
from tests.gen.messages_pb import MixedFieldsWithRequired


@pytest.mark.parametrize(
    ("msg", "expected_repr"),
    [
        (
            MixedFieldsWithRequired(
                explicit_field=42, implicit_field=100, legacy_required_field="test"
            ),
            "MixedFieldsWithRequired(explicit_field=42, implicit_field=100, legacy_required_field='test')",
        ),
        (
            MixedFieldsWithRequired(
                message_field=MixedFieldsWithRequired.Bar(value="nested")
            ),
            "MixedFieldsWithRequired(message_field=MixedFieldsWithRequired.Bar(value='nested'))",
        ),
        (MixedFieldsWithRequired(), "MixedFieldsWithRequired()"),
        (
            MixedFieldsWithRequired(
                repeated_field=["a", "b", "c"], map_field={"key": 1}
            ),
            "MixedFieldsWithRequired(repeated_field=['a', 'b', 'c'], map_field={'key': 1})",
        ),
        (
            MixedFieldsWithRequired(oneof_group=Oneof("oneof_field", "test_value")),
            "MixedFieldsWithRequired(oneof_group=Oneof(field='oneof_field', value='test_value'))",
        ),
        (
            MixedFieldsWithRequired(explicit_field=False),
            "MixedFieldsWithRequired(explicit_field=False)",
        ),
        (MixedFieldsWithRequired(implicit_field=0), "MixedFieldsWithRequired()"),
    ],
)
def test_repr(msg: MixedFieldsWithRequired, expected_repr: str) -> None:
    assert repr(msg) == expected_repr
