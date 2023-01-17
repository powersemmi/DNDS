from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ColorType

from dnd.database.models.base import BaseSchema
from dnd.database.models.users import User


class Pawn(BaseSchema):
    __tablename__ = "pawns"
    gameset_meta_id = Column(
        BigInteger,
        ForeignKey("gamesets_meta.id"),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )
    user_id: int = Column(
        BigInteger,
        ForeignKey(User.id),
        nullable=False,
        index=True,
    )

    meta = relationship("PawnMeta", backref="pawns", uselist=False)
    user = relationship(User, uselist=False)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_meta_id: int,
        meta: str,
        user: int,
    ):
        return await cls._create(
            gameset_meta_id=gameset_meta_id,
            meta=meta,
            user=user,
            session=session,
        )


class PawnMeta(BaseSchema):
    __tablename__ = "pawns_meta"
    id = Column(
        BigInteger,
        ForeignKey(Pawn.id),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )
    name: str = Column(String(256), nullable=False, unique=False, index=True)
    color: hex = Column(ColorType)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        pawn_id: int,
        name: str,
        color: hex,
    ):
        return await cls._create(
            id=pawn_id,
            name=name,
            color=color,
            session=session,
        )
