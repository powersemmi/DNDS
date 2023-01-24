from typing import Self

from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ColorType

from dnd.database.models.base import BaseSchema


class Pawn(BaseSchema):
    __tablename__ = "pawns"
    user_id: int = Column(
        BigInteger,
        ForeignKey("users.id"),
    )
    gameset_meta_id: int = Column(
        BigInteger,
        ForeignKey("gamesets_meta.id"),
    )

    user = relationship("User", uselist=False)
    meta = relationship("PawnMeta", backref="pawn", uselist=False)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_meta_id: int,
        meta: str,
        user: int,
    ) -> Self:
        return await cls._create(
            gameset_meta_id=gameset_meta_id,
            meta=meta,
            user=user,
            session=session,
        )


class PawnMeta(BaseSchema):
    __tablename__ = "pawns_meta"
    pawn_id = Column(BigInteger, ForeignKey("pawns.id"))
    name: str = Column(String(256))
    color: hex = Column(ColorType)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        pawn_id: int,
        name: str,
        color: hex,
    ) -> Self:
        return await cls._create(
            id=pawn_id,
            name=name,
            color=color,
            session=session,
        )
