from ...rsb import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EntityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ARLEIGH_BURKE: _ClassVar[EntityType]
    BISMARCK: _ClassVar[EntityType]
    CLEMENCEAU: _ClassVar[EntityType]
    FLETCHER: _ClassVar[EntityType]
    G5: _ClassVar[EntityType]
    IOWA: _ClassVar[EntityType]
    KOLKATA: _ClassVar[EntityType]
    OSA: _ClassVar[EntityType]
    YASEN: _ClassVar[EntityType]
    ZUBR: _ClassVar[EntityType]
ARLEIGH_BURKE: EntityType
BISMARCK: EntityType
CLEMENCEAU: EntityType
FLETCHER: EntityType
G5: EntityType
IOWA: EntityType
KOLKATA: EntityType
OSA: EntityType
YASEN: EntityType
ZUBR: EntityType

class Vector2f(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Transform(_message.Message):
    __slots__ = ("altitude", "angle", "position", "velocity")
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    altitude: int
    angle: int
    position: Vector2f
    velocity: int
    def __init__(self, altitude: _Optional[int] = ..., angle: _Optional[int] = ..., position: _Optional[_Union[Vector2f, _Mapping]] = ..., velocity: _Optional[int] = ...) -> None: ...

class Guidance(_message.Message):
    __slots__ = ("angle", "submerge", "velocity")
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    SUBMERGE_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    angle: int
    submerge: bool
    velocity: int
    def __init__(self, angle: _Optional[int] = ..., submerge: _Optional[bool] = ..., velocity: _Optional[int] = ...) -> None: ...

class Contact(_message.Message):
    __slots__ = ("damage", "entity_id", "entity_type", "guidance", "player_id", "reloads", "transform", "turret_angles")
    DAMAGE_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    GUIDANCE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    RELOADS_FIELD_NUMBER: _ClassVar[int]
    TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    TURRET_ANGLES_FIELD_NUMBER: _ClassVar[int]
    damage: int
    entity_id: int
    entity_type: EntityType
    guidance: Guidance
    player_id: int
    reloads: _containers.RepeatedScalarFieldContainer[bool]
    transform: Transform
    turret_angles: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, damage: _Optional[int] = ..., entity_id: _Optional[int] = ..., entity_type: _Optional[_Union[EntityType, str]] = ..., guidance: _Optional[_Union[Guidance, _Mapping]] = ..., player_id: _Optional[int] = ..., reloads: _Optional[_Iterable[bool]] = ..., transform: _Optional[_Union[Transform, _Mapping]] = ..., turret_angles: _Optional[_Iterable[int]] = ...) -> None: ...

class ChunkId(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class TerrainUpdate(_message.Message):
    __slots__ = ("chunk_id", "data")
    CHUNK_ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    chunk_id: ChunkId
    data: bytes
    def __init__(self, chunk_id: _Optional[_Union[ChunkId, _Mapping]] = ..., data: _Optional[bytes] = ...) -> None: ...

class Update(_message.Message):
    __slots__ = ("contacts", "score", "world_radius", "terrain_updates")
    CONTACTS_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    WORLD_RADIUS_FIELD_NUMBER: _ClassVar[int]
    TERRAIN_UPDATES_FIELD_NUMBER: _ClassVar[int]
    contacts: _containers.RepeatedCompositeFieldContainer[Contact]
    score: int
    world_radius: float
    terrain_updates: _containers.RepeatedCompositeFieldContainer[TerrainUpdate]
    def __init__(self, contacts: _Optional[_Iterable[_Union[Contact, _Mapping]]] = ..., score: _Optional[int] = ..., world_radius: _Optional[float] = ..., terrain_updates: _Optional[_Iterable[_Union[TerrainUpdate, _Mapping]]] = ...) -> None: ...

class Updates(_message.Message):
    __slots__ = ("updates",)
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[Update]
    def __init__(self, updates: _Optional[_Iterable[_Union[Update, _Mapping]]] = ...) -> None: ...
