from pydantic import BaseModel, Field, PositiveInt
from pydantic.color import Color


class PawnMetaModel(BaseModel):
    color: Color
    x: int
    y: int

    class Config:
        orm_mode = True


class PawnModel(BaseModel):
    name: str
    meta: PawnMetaModel

    class Config:
        orm_mode = True


class PawnsModel(BaseModel):
    meta: PawnMetaModel

    class Config:
        orm_mode = True


class PawnMetaRequestModel(BaseModel):
    color: Color = Field(example=Color("white"))


class PawnMoveModel(BaseModel):
    x: PositiveInt
    y: PositiveInt
