from pydantic import BaseModel

from dnd.models.auth import UserModel


class PawnModel(BaseModel):
    user: UserModel
    name: str
    color: str
