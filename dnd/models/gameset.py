from typing import Optional

from pydantic import BaseModel

from dnd.models.auth import UserInfoModel
from dnd.models.map import MapModel
from dnd.models.pawn import PawnModel


class GameSetPlayerPositionModel(BaseModel):
    x: int
    y: int
    pawn: PawnModel

    class Config:
        orm_mode = True


class GameSetMetaModel(BaseModel):
    pawns: list[Optional[PawnModel]]
    maps: list[Optional[MapModel]]
    pawns_position: list[Optional[GameSetPlayerPositionModel]]

    class Config:
        orm_mode = True


class GameSetModel(BaseModel):
    user: UserInfoModel
    name: str
    short_url: str
    meta: GameSetMetaModel

    class Config:
        orm_mode = True
