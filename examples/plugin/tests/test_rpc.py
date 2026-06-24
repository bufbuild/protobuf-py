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

from gen.user.v1.user_pb import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserRequest,
    GetUserResponse,
    User,
)
from gen.user.v1.user_rpc import UserService


class InMemoryUserService(UserService):
    """A concrete implementation of the generated UserService protocol."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def get_user(self, request: GetUserRequest) -> GetUserResponse:
        user = self._users.get(request.user_id)
        return GetUserResponse(user=user)

    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        if request.user is not None:
            self._users[request.user.user_id] = request.user
        return CreateUserResponse(user=request.user)


def test_user_service() -> None:
    assert InMemoryUserService()
