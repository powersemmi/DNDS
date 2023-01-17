from pydantic import BaseModel


class MapMetaModel(BaseModel):
    px: int = 0
    py: int = 0
    image: bytes or None


class MapModel(BaseModel):
    id: int
    meta: MapMetaModel
