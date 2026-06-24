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

import gc
import pickle
from weakref import WeakValueDictionary

from tests.gen.messages_pb import MixedFields


def test_message_weakref() -> None:
    msg = MixedFields()
    refs = WeakValueDictionary()
    refs["msg"] = msg
    assert len(refs) == 1
    del msg
    gc.collect()
    assert len(refs) == 0


def test_message_pickle() -> None:
    msg = MixedFields(
        explicit_field=123, implicit_field=456, repeated_field=["a", "b", "c"]
    )
    pickled = pickle.dumps(msg)
    unpickled = pickle.loads(pickled)  # noqa: S301
    assert unpickled == msg
