from typing import Optional

from pydantic import BaseModel, constr

from dnd.models.map import MapModel
from dnd.models.pawn import PawnModel


class GameSetPlayerPositionModel(BaseModel):
    x: int
    y: int
    pawn: PawnModel

    class Config:
        orm_mode = True


class GameSetMetaModel(BaseModel):
    class Config:
        orm_mode = True


class UserInGame(BaseModel):
    username: constr(min_length=1, max_length=256)
    full_name: constr(min_length=1, max_length=256) | None

    class Config:
        orm_mode = True


class UsersInGame(BaseModel):
    user: UserInGame

    class Config:
        orm_mode = True


class GameSetModel(BaseModel):
    name: str
    short_url: str
    owner: UserInGame
    maps: list[MapModel]
    meta: GameSetMetaModel
    users_in_game: list[UsersInGame]

    class Config:
        orm_mode = True


class GameSetsModel(BaseModel):
    __root__: list[Optional[GameSetModel]]

    class Config:
        orm_mode = True
