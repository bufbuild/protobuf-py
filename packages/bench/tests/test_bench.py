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

import base64
import json
import uuid
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypeAlias,
    TypeVar,
    cast,
)

import pytest
from protobuf.wkt import FileDescriptorSet, timestamp_pb
from protobuf.wkt import descriptor_pb as google_descriptor_pb

from bench.gen.buffa import bench_messages_pb, benchmark_message1_proto3_pb
from bench.gen.home import home_pb
from bench.gen.hyperpb import descriptor_pb, test_pb
from bench.gen.rsb import options_pb as rsb_options_pb
from bench.gen.rsb.log import log_pb
from bench.gen.rsb.mesh import mesh_pb
from bench.gen.rsb.minecraft import minecraft_pb
from bench.gen.rsb.mk48 import mk48_pb
from bench.gen.suite_pb import Suite

if TYPE_CHECKING:
    from google.protobuf.message import Message as GoogleProtobufMessage
    from protobuf import Message, Registry
    from pytest_benchmark.fixture import BenchmarkFixture

    from bench.gen.buffa.bench_messages_pb import LogRecord
    from bench.gen.buffa.bench_messages_pb2 import LogRecord as LogRecordGoogle
    from bench.gen.home import home_pb2
    from bench.gen.home.home_pb import GetUserHomeRequest
    from bench.gen.home.home_pb2 import GetUserHomeRequest as GetUserHomeRequestGoogle

suite = Suite.from_binary((Path(__file__).parent / "suite.binpb").read_bytes())

# We thread the case name as the _id parameter so pytest-benchmark can group on it.
all_external_cases = [
    pytest.param(case.name, case.typename, case.payload, id=case.name)
    for case in suite.cases
]
nested_message_external_cases = [
    pytest.param(case.name, case.typename, case.payload, id=case.name)
    for case in suite.cases
    if case.typename == "bench.LogRecord"
]


Impl: TypeAlias = Literal[
    "bufbuild-python", "bufbuild-rust", "google-python", "google-upb"
]


@pytest.fixture(autouse=True, scope="module")
def _setup_backend(setup_bufbuild: None, setup_google: None) -> None:
    """Activate the implementation backend for every test in this module."""


@pytest.fixture(scope="module")
def registry(setup_bufbuild) -> Registry:
    # Round trip through descriptor bytes to get fresh Message classes that reflect
    # native vs python setup
    fds = FileDescriptorSet(
        file=[
            google_descriptor_pb.desc().proto,
            timestamp_pb.desc().proto,
            rsb_options_pb.desc().proto,
            bench_messages_pb.desc().proto,
            benchmark_message1_proto3_pb.desc().proto,
            descriptor_pb.desc().proto,
            test_pb.desc().proto,
            log_pb.desc().proto,
            mesh_pb.desc().proto,
            minecraft_pb.desc().proto,
            mk48_pb.desc().proto,
            home_pb.desc().proto,
        ]
    )
    return fds.to_registry()


def _get_google_protobuf_message_instance(
    typename: str, impl: Impl
) -> GoogleProtobufMessage:
    import google.protobuf.symbol_database

    import bench.gen.buffa.bench_messages_pb2  # noqa: F401
    import bench.gen.buffa.benchmark_message1_proto3_pb2  # noqa: F401
    import bench.gen.home.home_pb2  # noqa: F401
    import bench.gen.hyperpb.descriptor_pb2  # noqa: F401
    import bench.gen.hyperpb.test_pb2  # noqa: F401
    import bench.gen.rsb.options_pb2  # noqa: F401 # isort: skip
    import bench.gen.rsb.log.log_pb2  # noqa: F401
    import bench.gen.rsb.mesh.mesh_pb2  # noqa: F401
    import bench.gen.rsb.minecraft.minecraft_pb2  # noqa: F401
    import bench.gen.rsb.mk48.mk48_pb2  # noqa: F401

    message = google.protobuf.symbol_database.Default().GetSymbol(typename)()
    # qualname not set correctly on classes so just string match
    match impl:
        case "google-python":
            assert "google.protobuf.descriptor.Descriptor" in str(
                message.DESCRIPTOR.__class__
            )
        case "google-upb":
            assert "google._upb._message.Descriptor" in str(
                message.DESCRIPTOR.__class__
            )
        case _:
            msg = f"unknown impl {impl}"
            raise ValueError(msg)
    return message


class TestBench:
    @pytest.mark.parametrize(("_id", "typename", "payload"), all_external_cases)
    def test_serialize(
        self,
        _id: str,
        typename: str,
        payload: bytes,
        impl: Impl,
        registry: Registry,
        benchmark: BenchmarkFixture,
    ) -> None:
        match impl:
            case "bufbuild-python" | "bufbuild-rust":
                message_desc = registry.message(typename)
                assert message_desc is not None, (
                    f"Message {typename} not found in registry"
                )
                message = message_desc.type().from_binary(payload)
                benchmark(message.to_binary)
            case "google-python" | "google-upb":
                message = _get_google_protobuf_message_instance(typename, impl)
                message.ParseFromString(payload)
                benchmark(message.SerializeToString)

    @pytest.mark.parametrize(("_id", "typename", "payload"), all_external_cases)
    def test_parse(
        self,
        _id: str,
        typename: str,
        payload: bytes,
        impl: Impl,
        registry: Registry,
        benchmark: BenchmarkFixture,
    ) -> None:
        match impl:
            case "bufbuild-python" | "bufbuild-rust":
                message_desc = registry.message(typename)
                assert message_desc is not None, (
                    f"Message {typename} not found in registry"
                )
                message_class = message_desc.type
                benchmark(message_class.from_binary, payload)
            case "google-python" | "google-upb":
                message = _get_google_protobuf_message_instance(typename, impl)
                benchmark(message.ParseFromString, payload)

    @pytest.mark.parametrize(("_id", "typename", "payload"), all_external_cases)
    def test_deepcopy(
        self,
        _id: str,
        typename: str,
        payload: bytes,
        impl: Impl,
        registry: Registry,
        benchmark: BenchmarkFixture,
    ) -> None:
        match impl:
            case "bufbuild-python" | "bufbuild-rust":
                message_desc = registry.message(typename)
                assert message_desc is not None, (
                    f"Message {typename} not found in registry"
                )
                message = message_desc.type().from_binary(payload)
                benchmark(deepcopy, message)
            case "google-python" | "google-upb":
                message = _get_google_protobuf_message_instance(typename, impl)
                message.ParseFromString(payload)
                benchmark(deepcopy, message)

    class TestAttrAccess:
        _scalar_cases = [
            pytest.param(
                "implicit_int",
                "hyperpb.test.Scalars",
                "a1",
                1234,
                id="implicit_int",
            ),
            pytest.param(
                "implicit_double",
                "hyperpb.test.Scalars",
                "a12",
                1234.5678,
                id="implicit_double",
            ),
            pytest.param(
                "implicit_string",
                "hyperpb.test.Scalars",
                "a14",
                "a" * 32,
                id="implicit_string",
            ),
            pytest.param(
                "explicit_int",
                "hyperpb.test.Scalars",
                "b1",
                1234,
                id="explicit_int",
            ),
            pytest.param(
                "explicit_double",
                "hyperpb.test.Scalars",
                "b12",
                1234.5678,
                id="explicit_double",
            ),
            pytest.param(
                "explicit_string",
                "hyperpb.test.Scalars",
                "b14",
                "a" * 32,
                id="explicit_string",
            ),
        ]

        @pytest.mark.parametrize(
            ("_id", "typename", "attr_name", "attr_value"),
            _scalar_cases,
        )
        def test_scalar_setattr(
            self,
            _id: str,
            typename: str,
            attr_name: str,
            attr_value: Any,
            impl: Impl,
            registry: Registry,
            benchmark: BenchmarkFixture,
        ):
            match impl:
                case "bufbuild-python" | "bufbuild-rust":
                    message_desc = registry.message(typename)
                    assert message_desc is not None, (
                        f"Message {typename} not found in registry"
                    )
                    message = message_desc.type()
                    benchmark(setattr, message, attr_name, attr_value)
                case "google-python" | "google-upb":
                    message = _get_google_protobuf_message_instance(typename, impl)
                    benchmark(setattr, message, attr_name, attr_value)

        @pytest.mark.parametrize(
            ("_id", "typename", "attr_name", "attr_value"),
            _scalar_cases,
        )
        def test_scalar_getattr(
            self,
            _id: str,
            typename: str,
            attr_name: str,
            attr_value: Any,
            impl: Impl,
            registry: Registry,
            benchmark: BenchmarkFixture,
        ):
            match impl:
                case "bufbuild-python" | "bufbuild-rust":
                    message_desc = registry.message(typename)
                    assert message_desc is not None, (
                        f"Message {typename} not found in registry"
                    )
                    message = message_desc.type()
                    setattr(message, attr_name, attr_value)
                    benchmark(getattr, message, attr_name)
                case "google-python" | "google-upb":
                    message = _get_google_protobuf_message_instance(typename, impl)
                    setattr(message, attr_name, attr_value)
                    benchmark(getattr, message, attr_name)

        # We use pedantic mode because we cannot share a upb message instance among many iterations
        # since upb intentionally leaves old memory unallocated until the message itself is freed.
        # As a normal benchmark, the same message would be assigned to in many iterations, eventually
        # running out of memory.
        #
        # The numbers should be read with that in mind.
        #
        # https://github.com/protocolbuffers/protobuf/issues/10294
        @pytest.mark.parametrize(
            ("_id", "typename", "payload"), nested_message_external_cases
        )
        def test_nested_message_setattr(
            self,
            _id: str,
            typename: str,
            payload: bytes,
            impl: Impl,
            registry: Registry,
            benchmark: BenchmarkFixture,
        ):
            match impl:
                case "bufbuild-python" | "bufbuild-rust":
                    message_desc = registry.message(typename)
                    assert message_desc is not None, (
                        f"Message {typename} not found in registry"
                    )
                    message = cast(
                        "LogRecord", message_desc.type().from_binary(payload)
                    )
                    source = message.source

                    def construct_args_bufbuild():
                        return (message_desc.type(), "source", source), {}

                    benchmark.pedantic(
                        setattr,
                        rounds=200000,
                        iterations=1,
                        setup=construct_args_bufbuild,
                    )
                case "google-python" | "google-upb":
                    message = cast(
                        "LogRecordGoogle",
                        _get_google_protobuf_message_instance(typename, impl),
                    )
                    message.ParseFromString(payload)
                    source = message.source
                    from google.protobuf.message import Message as GoogleMessage

                    def construct_args_google():
                        message = cast(
                            "LogRecordGoogle",
                            _get_google_protobuf_message_instance(typename, impl),
                        )
                        return (
                            message.source,
                            source,
                        ), {}

                    benchmark.pedantic(
                        GoogleMessage.CopyFrom,
                        rounds=200000,
                        iterations=1,
                        setup=construct_args_google,
                    )

        @pytest.mark.parametrize(
            ("_id", "typename", "payload"), nested_message_external_cases
        )
        def test_nested_message_getattr(
            self,
            _id: str,
            typename: str,
            payload: bytes,
            impl: Impl,
            registry: Registry,
            benchmark: BenchmarkFixture,
        ):
            match impl:
                case "bufbuild-python" | "bufbuild-rust":
                    message_desc = registry.message(typename)
                    assert message_desc is not None, (
                        f"Message {typename} not found in registry"
                    )
                    message = cast(
                        "LogRecord", message_desc.type().from_binary(payload)
                    )
                    benchmark(getattr, message, "source")
                case "google-python" | "google-upb":
                    message = cast(
                        "LogRecordGoogle",
                        _get_google_protobuf_message_instance(typename, impl),
                    )
                    message.ParseFromString(payload)
                    benchmark(getattr, message, "source")


# The home page BFF simulates a social-network "home" endpoint that fans out to
# three backend services (profile, timeline, notifications) and merges their
# responses into one. The canned backend payloads below are what those services would
# return over the wire.
_HOME_USER_ID = "3c1cef76394d4d6993773bf07af8ca2c"
_TIMELINE_LIMIT = 20
_NOTIFICATION_COUNT = 10
_HOME_BASE_TIME = datetime(2024, 6, 18, 9, 20, tzinfo=timezone.utc)

# A fixed namespace so the item and notification UUIDs are deterministic 128-bit
# values derived from their index, matching the format of the user IDs above.
_HOME_ID_NAMESPACE = uuid.UUID("6f9619ff8b86d011b42d00cf4fc964ff")


def _home_uuid(name: str) -> str:
    return uuid.uuid5(_HOME_ID_NAMESPACE, name).hex


# A handful of other accounts that show up in the timeline and notifications.
_HOME_OTHER_USER_IDS = [
    "a1b2c3d4e5f64718293a4b5c6d7e8f90",
    "f0e1d2c3b4a5968778695a4b3c2d1e0f",
    "1234567890abcdef1234567890abcdef",
    "fedcba0987654321fedcba0987654321",
]

# Real Reddit post bodies for the timeline from the webis/tldr-17 dataset.
_TIMELINE_CONTENTS: list[str] = json.loads(
    base64.b64decode((Path(__file__).parent / "home_timeline.json.b64").read_bytes())
)

# A few canned notifications
_NOTIFICATION_CONTENTS: dict[home_pb.Notification.Type, str] = {
    home_pb.Notification.Type.FOLLOW: "started following you",
    home_pb.Notification.Type.LIKE: "liked your post",
    home_pb.Notification.Type.COMMENT: (
        "commented: this is such a good point, I had never thought about it "
        "quite that way before. Do you have any reading you would recommend "
        "for someone trying to go deeper on the subject?"
    ),
    home_pb.Notification.Type.MESSAGE: (
        "sent you a message: hey! It has been way too long since we caught up. "
        "Are you around for a coffee sometime next week? I am pretty flexible "
        "most afternoons and would love to hear what you have been working on."
    ),
}
_NOTIFICATION_TYPE_CYCLE: list[home_pb.Notification.Type] = [
    home_pb.Notification.Type.FOLLOW,
    home_pb.Notification.Type.LIKE,
    home_pb.Notification.Type.COMMENT,
    home_pb.Notification.Type.MESSAGE,
]


def _build_profile_response() -> home_pb.GetUserProfileResponse:
    return home_pb.GetUserProfileResponse(
        profile=home_pb.Profile(
            user_id=_HOME_USER_ID,
            name="Ada Lovelace",
            email="ada.lovelace@example.com",
            profile_picture_url=f"https://cdn.example.com/u/{_HOME_USER_ID}/avatar.jpg",
            bio=(
                "Mathematician, writer, and arguably the first computer "
                "programmer. I spend my days thinking about analytical engines and "
                "my nights thinking about what they might one day become. Building "
                "things at the intersection of math and machines. Opinions are "
                "entirely my own and definitely not those of my employer."
            ),
        )
    )


def _build_timeline_response() -> home_pb.GetTimelineResponse:
    assert len(_TIMELINE_CONTENTS) >= _TIMELINE_LIMIT, (
        f"home_timeline.json.b64 has {len(_TIMELINE_CONTENTS)} posts, "
        f"need at least {_TIMELINE_LIMIT}"
    )
    items: list[home_pb.TimelineItem] = []
    for i, content in enumerate(_TIMELINE_CONTENTS[:_TIMELINE_LIMIT]):
        # Every fourth item is a reshare of someone else's post.
        is_share: bool = i % 4 == 3
        author: str = _HOME_OTHER_USER_IDS[i % len(_HOME_OTHER_USER_IDS)]
        items.append(
            home_pb.TimelineItem(
                item_id=_home_uuid(f"timeline-{i}"),
                type=home_pb.TimelineItem.Type.SHARE
                if is_share
                else home_pb.TimelineItem.Type.POST,
                user_id=author if is_share else _HOME_USER_ID,
                content=content,
                timestamp=timestamp_pb.Timestamp.from_datetime(
                    _HOME_BASE_TIME - timedelta(hours=i)
                ),
            )
        )
    return home_pb.GetTimelineResponse(items=items)


def _build_notifications_response() -> home_pb.GetNotificationsResponse:
    notifications: list[home_pb.Notification] = []
    for i in range(_NOTIFICATION_COUNT):
        notification_type = _NOTIFICATION_TYPE_CYCLE[i % len(_NOTIFICATION_TYPE_CYCLE)]
        notifications.append(
            home_pb.Notification(
                notification_id=_home_uuid(f"notification-{i}"),
                type=notification_type,
                from_user_id=_HOME_OTHER_USER_IDS[i % len(_HOME_OTHER_USER_IDS)],
                content=_NOTIFICATION_CONTENTS[notification_type],
                timestamp=timestamp_pb.Timestamp.from_datetime(
                    _HOME_BASE_TIME - timedelta(minutes=30 * i)
                ),
            )
        )
    return home_pb.GetNotificationsResponse(notifications=notifications)


class HomeDB:
    def __init__(self) -> None:
        self.profile = _build_profile_response().to_binary()
        self.timeline = _build_timeline_response().to_binary()
        self.notifications = _build_notifications_response().to_binary()


class BufbuildHomeAPI:
    def __init__(self, registry: Registry, db: HomeDB) -> None:
        self._db = db
        self._request_type: type[home_pb.GetUserHomeRequest] = _bufbuild_home_type(
            registry, home_pb.GetUserHomeRequest
        )
        self._response_type: type[home_pb.GetUserHomeResponse] = _bufbuild_home_type(
            registry, home_pb.GetUserHomeResponse
        )
        self._profile_request_type: type[home_pb.GetUserProfileRequest] = (
            _bufbuild_home_type(registry, home_pb.GetUserProfileRequest)
        )
        self._profile_response_type: type[home_pb.GetUserProfileResponse] = (
            _bufbuild_home_type(registry, home_pb.GetUserProfileResponse)
        )
        self._timeline_request_type: type[home_pb.GetTimelineRequest] = (
            _bufbuild_home_type(registry, home_pb.GetTimelineRequest)
        )
        self._timeline_response_type: type[home_pb.GetTimelineResponse] = (
            _bufbuild_home_type(registry, home_pb.GetTimelineResponse)
        )
        self._notifications_request_type: type[home_pb.GetNotificationsRequest] = (
            _bufbuild_home_type(registry, home_pb.GetNotificationsRequest)
        )
        self._notifications_response_type: type[home_pb.GetNotificationsResponse] = (
            _bufbuild_home_type(registry, home_pb.GetNotificationsResponse)
        )

    def get_user_home(self, request_bytes: bytes) -> bytes:
        request = self._request_type.from_binary(request_bytes)
        profile = self.get_user_profile(
            self._profile_request_type(user_id=request.user_id)
        )
        timeline = self.get_timeline(
            self._timeline_request_type(user_id=request.user_id, limit=_TIMELINE_LIMIT)
        )
        notifications = self.get_notifications(
            self._notifications_request_type(user_id=request.user_id)
        )
        response: home_pb.GetUserHomeResponse = self._response_type()
        # A BFF doesn't need to copy backend responses - we assign directly.
        response.profile = profile.profile
        response.timeline = timeline.items
        response.notifications = notifications.notifications
        return response.to_binary()

    def get_user_profile(
        self, request: home_pb.GetUserProfileRequest
    ) -> home_pb.GetUserProfileResponse:
        request.to_binary()  # simulate marshalling the outgoing request
        return self._profile_response_type.from_binary(self._db.profile)

    def get_timeline(
        self, request: home_pb.GetTimelineRequest
    ) -> home_pb.GetTimelineResponse:
        request.to_binary()  # simulate marshalling the outgoing request
        return self._timeline_response_type.from_binary(self._db.timeline)

    def get_notifications(
        self, request: home_pb.GetNotificationsRequest
    ) -> home_pb.GetNotificationsResponse:
        request.to_binary()  # simulate marshalling the outgoing request
        return self._notifications_response_type.from_binary(self._db.notifications)


class GoogleHomeAPI:
    # `home_pb2` is imported fresh per impl (python vs upb), so it is typed as the
    # module rather than statically; the locals below pin down the message types.
    def __init__(self, home_module: ModuleType, db: HomeDB) -> None:
        self._db = db
        self._pb: Any = home_module

    def get_user_home(self, request_bytes: bytes) -> bytes:
        request: home_pb2.GetUserHomeRequest = self._pb.GetUserHomeRequest()
        request.ParseFromString(request_bytes)
        profile = self.get_user_profile(
            self._pb.GetUserProfileRequest(user_id=request.user_id)
        )
        timeline = self.get_timeline(
            self._pb.GetTimelineRequest(user_id=request.user_id, limit=_TIMELINE_LIMIT)
        )
        notifications = self.get_notifications(
            self._pb.GetNotificationsRequest(user_id=request.user_id)
        )
        response: home_pb2.GetUserHomeResponse = self._pb.GetUserHomeResponse()
        # Google requires copying the backend sub-messages into the response.
        response.profile.CopyFrom(profile.profile)
        response.timeline.extend(timeline.items)
        response.notifications.extend(notifications.notifications)
        return response.SerializeToString()

    def get_user_profile(
        self, request: home_pb2.GetUserProfileRequest
    ) -> home_pb2.GetUserProfileResponse:
        request.SerializeToString()  # simulate marshalling the outgoing request
        response: home_pb2.GetUserProfileResponse = self._pb.GetUserProfileResponse()
        response.ParseFromString(self._db.profile)
        return response

    def get_timeline(
        self, request: home_pb2.GetTimelineRequest
    ) -> home_pb2.GetTimelineResponse:
        request.SerializeToString()  # simulate marshalling the outgoing request
        response: home_pb2.GetTimelineResponse = self._pb.GetTimelineResponse()
        response.ParseFromString(self._db.timeline)
        return response

    def get_notifications(
        self, request: home_pb2.GetNotificationsRequest
    ) -> home_pb2.GetNotificationsResponse:
        request.SerializeToString()  # simulate marshalling the outgoing request
        response: home_pb2.GetNotificationsResponse = (
            self._pb.GetNotificationsResponse()
        )
        response.ParseFromString(self._db.notifications)
        return response


_HomeMessageT = TypeVar("_HomeMessageT", bound="Message")


def _bufbuild_home_type(
    registry: Registry, message_type: type[_HomeMessageT]
) -> type[_HomeMessageT]:
    type_name = f"home.{message_type.__name__}"
    message_desc = registry.message(type_name)
    assert message_desc is not None, f"Message {type_name} not found in registry"
    return cast("type[_HomeMessageT]", message_desc.type)


class TestHome:
    @pytest.mark.parametrize("_id", ["full", "serialize", "parse"])
    # Set min time to get around 100 iterations per round
    @pytest.mark.benchmark(min_time=0.001)
    def test_get_user_home(
        self,
        _id: Literal["full", "serialize", "parse"],
        impl: Impl,
        registry: Registry,
        benchmark: BenchmarkFixture,
    ) -> None:
        db = HomeDB()
        typename = "home.GetUserHomeRequest"
        match impl:
            case "bufbuild-python" | "bufbuild-rust":
                request_desc = registry.message(typename)
                assert request_desc is not None, (
                    f"Message {typename} not found in registry"
                )
                response_desc = registry.message("home.GetUserHomeResponse")
                assert response_desc is not None, (
                    "Message home.GetUserHomeResponse not found in registry"
                )
                bufbuild_request = cast("GetUserHomeRequest", request_desc.type())
                bufbuild_request.user_id = _HOME_USER_ID
                request: bytes = bufbuild_request.to_binary()
                bufbuild_api = BufbuildHomeAPI(registry, db)
                match _id:
                    case "full":
                        benchmark(bufbuild_api.get_user_home, request)
                    case "serialize":
                        response_bytes = bufbuild_api.get_user_home(request)
                        bufbuild_response = response_desc.type.from_binary(
                            response_bytes
                        )
                        benchmark(bufbuild_response.to_binary)
                    case "parse":
                        response_bytes = bufbuild_api.get_user_home(request)
                        benchmark(response_desc.type.from_binary, response_bytes)
            case "google-python" | "google-upb":
                google_request = cast(
                    "GetUserHomeRequestGoogle",
                    _get_google_protobuf_message_instance(typename, impl),
                )
                google_request.user_id = _HOME_USER_ID
                request = google_request.SerializeToString()
                import bench.gen.home.home_pb2 as home_module

                google_api = GoogleHomeAPI(home_module, db)
                match _id:
                    case "full":
                        benchmark(google_api.get_user_home, request)
                    case "serialize":
                        response_bytes = google_api.get_user_home(request)
                        google_response = _get_google_protobuf_message_instance(
                            "home.GetUserHomeResponse", impl
                        )
                        google_response.ParseFromString(response_bytes)
                        benchmark(google_response.SerializeToString)
                    case "parse":
                        response_bytes = google_api.get_user_home(request)
                        google_response = _get_google_protobuf_message_instance(
                            "home.GetUserHomeResponse", impl
                        )
                        benchmark(google_response.__class__.FromString, response_bytes)
