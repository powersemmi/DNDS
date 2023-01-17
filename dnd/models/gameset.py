from pydantic import BaseModel

from dnd.models.auth import UserModel
from dnd.models.map import MapModel
from dnd.models.pawn import PawnModel


class GameSetPlayerPositionModel(BaseModel):
    x: int
    y: int
    map_id: int
    pawn_id: int


class GameSetMetaModel(BaseModel):
    current_map_id: int
    pawns: list[PawnModel]
    maps: list[MapModel]
    pawns_position: dict[int, GameSetPlayerPositionModel]


class GameSetModel(BaseModel):
    owner: UserModel
    name: str
    meta: GameSetMetaModel
