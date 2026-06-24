import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUserProfileRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class Profile(_message.Message):
    __slots__ = ("user_id", "name", "email", "profile_picture_url", "bio")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_URL_FIELD_NUMBER: _ClassVar[int]
    BIO_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    name: str
    email: str
    profile_picture_url: str
    bio: str
    def __init__(self, user_id: _Optional[str] = ..., name: _Optional[str] = ..., email: _Optional[str] = ..., profile_picture_url: _Optional[str] = ..., bio: _Optional[str] = ...) -> None: ...

class GetUserProfileResponse(_message.Message):
    __slots__ = ("profile",)
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    profile: Profile
    def __init__(self, profile: _Optional[_Union[Profile, _Mapping]] = ...) -> None: ...

class GetTimelineRequest(_message.Message):
    __slots__ = ("user_id", "limit", "offset")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    limit: int
    offset: int
    def __init__(self, user_id: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class TimelineItem(_message.Message):
    __slots__ = ("item_id", "type", "user_id", "content", "timestamp")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNSPECIFIED: _ClassVar[TimelineItem.Type]
        TYPE_POST: _ClassVar[TimelineItem.Type]
        TYPE_SHARE: _ClassVar[TimelineItem.Type]
    TYPE_UNSPECIFIED: TimelineItem.Type
    TYPE_POST: TimelineItem.Type
    TYPE_SHARE: TimelineItem.Type
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    item_id: str
    type: TimelineItem.Type
    user_id: str
    content: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, item_id: _Optional[str] = ..., type: _Optional[_Union[TimelineItem.Type, str]] = ..., user_id: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetTimelineResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[TimelineItem]
    def __init__(self, items: _Optional[_Iterable[_Union[TimelineItem, _Mapping]]] = ...) -> None: ...

class GetNotificationsRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class Notification(_message.Message):
    __slots__ = ("notification_id", "type", "from_user_id", "content", "timestamp")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNSPECIFIED: _ClassVar[Notification.Type]
        TYPE_FOLLOW: _ClassVar[Notification.Type]
        TYPE_LIKE: _ClassVar[Notification.Type]
        TYPE_COMMENT: _ClassVar[Notification.Type]
        TYPE_MESSAGE: _ClassVar[Notification.Type]
    TYPE_UNSPECIFIED: Notification.Type
    TYPE_FOLLOW: Notification.Type
    TYPE_LIKE: Notification.Type
    TYPE_COMMENT: Notification.Type
    TYPE_MESSAGE: Notification.Type
    NOTIFICATION_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FROM_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    notification_id: str
    type: Notification.Type
    from_user_id: str
    content: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, notification_id: _Optional[str] = ..., type: _Optional[_Union[Notification.Type, str]] = ..., from_user_id: _Optional[str] = ..., content: _Optional[str] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetNotificationsResponse(_message.Message):
    __slots__ = ("notifications",)
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    notifications: _containers.RepeatedCompositeFieldContainer[Notification]
    def __init__(self, notifications: _Optional[_Iterable[_Union[Notification, _Mapping]]] = ...) -> None: ...

class GetUserHomeRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetUserHomeResponse(_message.Message):
    __slots__ = ("profile", "timeline", "notifications")
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    TIMELINE_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_FIELD_NUMBER: _ClassVar[int]
    profile: Profile
    timeline: _containers.RepeatedCompositeFieldContainer[TimelineItem]
    notifications: _containers.RepeatedCompositeFieldContainer[Notification]
    def __init__(self, profile: _Optional[_Union[Profile, _Mapping]] = ..., timeline: _Optional[_Iterable[_Union[TimelineItem, _Mapping]]] = ..., notifications: _Optional[_Iterable[_Union[Notification, _Mapping]]] = ...) -> None: ...
