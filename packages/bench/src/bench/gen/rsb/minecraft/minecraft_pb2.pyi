from ...rsb import options_pb2 as _options_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SURVIVAL: _ClassVar[GameType]
    CREATIVE: _ClassVar[GameType]
    ADVENTURE: _ClassVar[GameType]
    SPECTATOR: _ClassVar[GameType]
SURVIVAL: GameType
CREATIVE: GameType
ADVENTURE: GameType
SPECTATOR: GameType

class Item(_message.Message):
    __slots__ = ("count", "slot", "id")
    COUNT_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    count: int
    slot: int
    id: str
    def __init__(self, count: _Optional[int] = ..., slot: _Optional[int] = ..., id: _Optional[str] = ...) -> None: ...

class Abilities(_message.Message):
    __slots__ = ("walk_speed", "fly_speed", "may_fly", "flying", "invulnerable", "may_build", "instabuild")
    WALK_SPEED_FIELD_NUMBER: _ClassVar[int]
    FLY_SPEED_FIELD_NUMBER: _ClassVar[int]
    MAY_FLY_FIELD_NUMBER: _ClassVar[int]
    FLYING_FIELD_NUMBER: _ClassVar[int]
    INVULNERABLE_FIELD_NUMBER: _ClassVar[int]
    MAY_BUILD_FIELD_NUMBER: _ClassVar[int]
    INSTABUILD_FIELD_NUMBER: _ClassVar[int]
    walk_speed: float
    fly_speed: float
    may_fly: bool
    flying: bool
    invulnerable: bool
    may_build: bool
    instabuild: bool
    def __init__(self, walk_speed: _Optional[float] = ..., fly_speed: _Optional[float] = ..., may_fly: _Optional[bool] = ..., flying: _Optional[bool] = ..., invulnerable: _Optional[bool] = ..., may_build: _Optional[bool] = ..., instabuild: _Optional[bool] = ...) -> None: ...

class Vector3d(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Vector2f(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Uuid(_message.Message):
    __slots__ = ("x0", "x1", "x2", "x3")
    X0_FIELD_NUMBER: _ClassVar[int]
    X1_FIELD_NUMBER: _ClassVar[int]
    X2_FIELD_NUMBER: _ClassVar[int]
    X3_FIELD_NUMBER: _ClassVar[int]
    x0: int
    x1: int
    x2: int
    x3: int
    def __init__(self, x0: _Optional[int] = ..., x1: _Optional[int] = ..., x2: _Optional[int] = ..., x3: _Optional[int] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ("id", "pos", "motion", "rotation", "fall_distance", "fire", "air", "on_ground", "no_gravity", "invulnerable", "portal_cooldown", "uuid", "custom_name", "custom_name_visible", "silent", "glowing")
    ID_FIELD_NUMBER: _ClassVar[int]
    POS_FIELD_NUMBER: _ClassVar[int]
    MOTION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    FALL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    FIRE_FIELD_NUMBER: _ClassVar[int]
    AIR_FIELD_NUMBER: _ClassVar[int]
    ON_GROUND_FIELD_NUMBER: _ClassVar[int]
    NO_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    INVULNERABLE_FIELD_NUMBER: _ClassVar[int]
    PORTAL_COOLDOWN_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_NAME_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    SILENT_FIELD_NUMBER: _ClassVar[int]
    GLOWING_FIELD_NUMBER: _ClassVar[int]
    id: str
    pos: Vector3d
    motion: Vector3d
    rotation: Vector2f
    fall_distance: float
    fire: int
    air: int
    on_ground: bool
    no_gravity: bool
    invulnerable: bool
    portal_cooldown: int
    uuid: Uuid
    custom_name: str
    custom_name_visible: bool
    silent: bool
    glowing: bool
    def __init__(self, id: _Optional[str] = ..., pos: _Optional[_Union[Vector3d, _Mapping]] = ..., motion: _Optional[_Union[Vector3d, _Mapping]] = ..., rotation: _Optional[_Union[Vector2f, _Mapping]] = ..., fall_distance: _Optional[float] = ..., fire: _Optional[int] = ..., air: _Optional[int] = ..., on_ground: _Optional[bool] = ..., no_gravity: _Optional[bool] = ..., invulnerable: _Optional[bool] = ..., portal_cooldown: _Optional[int] = ..., uuid: _Optional[_Union[Uuid, _Mapping]] = ..., custom_name: _Optional[str] = ..., custom_name_visible: _Optional[bool] = ..., silent: _Optional[bool] = ..., glowing: _Optional[bool] = ...) -> None: ...

class RecipeBook(_message.Message):
    __slots__ = ("recipes", "to_be_displayed", "is_filtering_craftable", "is_gui_open", "is_furnace_filtering_craftable", "is_furnace_gui_open", "is_blasting_furnace_filtering_craftable", "is_blasting_furnace_gui_open", "is_smoker_filtering_craftable", "is_smoker_gui_open")
    RECIPES_FIELD_NUMBER: _ClassVar[int]
    TO_BE_DISPLAYED_FIELD_NUMBER: _ClassVar[int]
    IS_FILTERING_CRAFTABLE_FIELD_NUMBER: _ClassVar[int]
    IS_GUI_OPEN_FIELD_NUMBER: _ClassVar[int]
    IS_FURNACE_FILTERING_CRAFTABLE_FIELD_NUMBER: _ClassVar[int]
    IS_FURNACE_GUI_OPEN_FIELD_NUMBER: _ClassVar[int]
    IS_BLASTING_FURNACE_FILTERING_CRAFTABLE_FIELD_NUMBER: _ClassVar[int]
    IS_BLASTING_FURNACE_GUI_OPEN_FIELD_NUMBER: _ClassVar[int]
    IS_SMOKER_FILTERING_CRAFTABLE_FIELD_NUMBER: _ClassVar[int]
    IS_SMOKER_GUI_OPEN_FIELD_NUMBER: _ClassVar[int]
    recipes: _containers.RepeatedScalarFieldContainer[str]
    to_be_displayed: _containers.RepeatedScalarFieldContainer[str]
    is_filtering_craftable: bool
    is_gui_open: bool
    is_furnace_filtering_craftable: bool
    is_furnace_gui_open: bool
    is_blasting_furnace_filtering_craftable: bool
    is_blasting_furnace_gui_open: bool
    is_smoker_filtering_craftable: bool
    is_smoker_gui_open: bool
    def __init__(self, recipes: _Optional[_Iterable[str]] = ..., to_be_displayed: _Optional[_Iterable[str]] = ..., is_filtering_craftable: _Optional[bool] = ..., is_gui_open: _Optional[bool] = ..., is_furnace_filtering_craftable: _Optional[bool] = ..., is_furnace_gui_open: _Optional[bool] = ..., is_blasting_furnace_filtering_craftable: _Optional[bool] = ..., is_blasting_furnace_gui_open: _Optional[bool] = ..., is_smoker_filtering_craftable: _Optional[bool] = ..., is_smoker_gui_open: _Optional[bool] = ...) -> None: ...

class Vehicle(_message.Message):
    __slots__ = ("uuid", "entity")
    UUID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    uuid: Uuid
    entity: Entity
    def __init__(self, uuid: _Optional[_Union[Uuid, _Mapping]] = ..., entity: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...

class Player(_message.Message):
    __slots__ = ("game_type", "previous_game_type", "score", "dimension", "selected_item_slot", "selected_item", "spawn_dimension", "spawn_x", "spawn_y", "spawn_z", "spawn_forced", "sleep_timer", "food_exhaustion_level", "food_saturation_level", "food_tick_timer", "xp_level", "xp_p", "xp_total", "xp_seed", "inventory", "ender_items", "abilities", "entered_nether_position", "root_vehicle", "shoulder_entity_left", "shoulder_entity_right", "seen_credits", "recipe_book")
    GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_GAME_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ITEM_SLOT_FIELD_NUMBER: _ClassVar[int]
    SELECTED_ITEM_FIELD_NUMBER: _ClassVar[int]
    SPAWN_DIMENSION_FIELD_NUMBER: _ClassVar[int]
    SPAWN_X_FIELD_NUMBER: _ClassVar[int]
    SPAWN_Y_FIELD_NUMBER: _ClassVar[int]
    SPAWN_Z_FIELD_NUMBER: _ClassVar[int]
    SPAWN_FORCED_FIELD_NUMBER: _ClassVar[int]
    SLEEP_TIMER_FIELD_NUMBER: _ClassVar[int]
    FOOD_EXHAUSTION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FOOD_SATURATION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    FOOD_TICK_TIMER_FIELD_NUMBER: _ClassVar[int]
    XP_LEVEL_FIELD_NUMBER: _ClassVar[int]
    XP_P_FIELD_NUMBER: _ClassVar[int]
    XP_TOTAL_FIELD_NUMBER: _ClassVar[int]
    XP_SEED_FIELD_NUMBER: _ClassVar[int]
    INVENTORY_FIELD_NUMBER: _ClassVar[int]
    ENDER_ITEMS_FIELD_NUMBER: _ClassVar[int]
    ABILITIES_FIELD_NUMBER: _ClassVar[int]
    ENTERED_NETHER_POSITION_FIELD_NUMBER: _ClassVar[int]
    ROOT_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    SHOULDER_ENTITY_LEFT_FIELD_NUMBER: _ClassVar[int]
    SHOULDER_ENTITY_RIGHT_FIELD_NUMBER: _ClassVar[int]
    SEEN_CREDITS_FIELD_NUMBER: _ClassVar[int]
    RECIPE_BOOK_FIELD_NUMBER: _ClassVar[int]
    game_type: GameType
    previous_game_type: GameType
    score: int
    dimension: str
    selected_item_slot: int
    selected_item: Item
    spawn_dimension: str
    spawn_x: int
    spawn_y: int
    spawn_z: int
    spawn_forced: bool
    sleep_timer: int
    food_exhaustion_level: float
    food_saturation_level: float
    food_tick_timer: int
    xp_level: int
    xp_p: float
    xp_total: int
    xp_seed: int
    inventory: _containers.RepeatedCompositeFieldContainer[Item]
    ender_items: _containers.RepeatedCompositeFieldContainer[Item]
    abilities: Abilities
    entered_nether_position: Vector3d
    root_vehicle: Vehicle
    shoulder_entity_left: Entity
    shoulder_entity_right: Entity
    seen_credits: bool
    recipe_book: RecipeBook
    def __init__(self, game_type: _Optional[_Union[GameType, str]] = ..., previous_game_type: _Optional[_Union[GameType, str]] = ..., score: _Optional[int] = ..., dimension: _Optional[str] = ..., selected_item_slot: _Optional[int] = ..., selected_item: _Optional[_Union[Item, _Mapping]] = ..., spawn_dimension: _Optional[str] = ..., spawn_x: _Optional[int] = ..., spawn_y: _Optional[int] = ..., spawn_z: _Optional[int] = ..., spawn_forced: _Optional[bool] = ..., sleep_timer: _Optional[int] = ..., food_exhaustion_level: _Optional[float] = ..., food_saturation_level: _Optional[float] = ..., food_tick_timer: _Optional[int] = ..., xp_level: _Optional[int] = ..., xp_p: _Optional[float] = ..., xp_total: _Optional[int] = ..., xp_seed: _Optional[int] = ..., inventory: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., ender_items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ..., abilities: _Optional[_Union[Abilities, _Mapping]] = ..., entered_nether_position: _Optional[_Union[Vector3d, _Mapping]] = ..., root_vehicle: _Optional[_Union[Vehicle, _Mapping]] = ..., shoulder_entity_left: _Optional[_Union[Entity, _Mapping]] = ..., shoulder_entity_right: _Optional[_Union[Entity, _Mapping]] = ..., seen_credits: _Optional[bool] = ..., recipe_book: _Optional[_Union[RecipeBook, _Mapping]] = ...) -> None: ...

class Players(_message.Message):
    __slots__ = ("players",)
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    players: _containers.RepeatedCompositeFieldContainer[Player]
    def __init__(self, players: _Optional[_Iterable[_Union[Player, _Mapping]]] = ...) -> None: ...
