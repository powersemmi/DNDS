from pydantic import BaseModel

from dnd.models.auth import UserModel


class PawnMetaModel(BaseModel):
    name: str
    color: str

    class Config:
        orm_mode = True


class PawnModel(BaseModel):
    user: UserModel
    meta: PawnMetaModel

    class Config:
        orm_mode = True
