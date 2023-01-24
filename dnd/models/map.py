from pydantic import BaseModel


class MapMetaModel(BaseModel):
    len_x: int = 0
    len_y: int = 0
    image: bytes | None

    class Config:
        orm_mode = True


class MapModel(BaseModel):
    meta: MapMetaModel

    class Config:
        orm_mode = True
