from typing import Self

from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from dnd.database.models.base import BaseSchema


class Map(BaseSchema):
    __tablename__ = "maps"
    user_id: int = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    gameset_meta_id: int = Column(
        BigInteger, ForeignKey("gamesets_meta.id"), nullable=False
    )
    meta = relationship("MapMeta", backref="map", uselist=False)

    @classmethod
    async def create(
        cls, session: AsyncSession, gameset_meta_id: int, meta: "MapMeta"
    ) -> Self:
        return await cls._create(
            gameset_meta_id=gameset_meta_id, meta=meta, session=session
        )


class MapMeta(BaseSchema):
    __tablename__ = "maps_meta"
    map_id = Column(
        BigInteger,
        ForeignKey("maps.id"),
    )
    name: str = Column(String(256), nullable=False)
    len_x: int = Column(Integer, nullable=False)
    len_y: int = Column(Integer, nullable=False)
    image: bytes | None = Column(BYTEA)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        map_id: int,
        name: str,
        len_x: int,
        len_y: int,
        image: bytes,
    ) -> Self:
        return await cls._create(
            map_id=map_id,
            name=name,
            len_x=len_x,
            len_y=len_y,
            image=image,
            session=session,
        )
