from typing import TYPE_CHECKING, Self

from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ColorType

from dnd.database.models.base import BaseSchema

if TYPE_CHECKING:
    from dnd.database.models.maps import Map
    from dnd.database.models.users import User


class Pawn(BaseSchema):
    __tablename__ = "pawns"
    user_id = mapped_column(ForeignKey("users.id"))
    map_id = mapped_column(ForeignKey("maps.id"))
    name: Mapped[str]

    map: Mapped["Map"] = relationship(back_populates="pawns")
    user: Mapped["User"] = relationship(back_populates="pawns")
    meta: Mapped["PawnMeta"] = relationship(
        back_populates="pawn", lazy="immediate"
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        map_id: int,
        user_id: int,
    ) -> Self:
        return await cls._create(
            map_id=map_id,
            name=name,
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def get_by_name_and_map_id(
        cls, session: AsyncSession, name: str, map_id: int
    ) -> Self | None:
        return (
            await session.execute(
                select(cls).where((cls.name == name), (cls.map_id == map_id))
            )
        ).scalar_one_or_none()


class PawnMeta(BaseSchema):
    __tablename__ = "pawns_meta"
    pawn_id = mapped_column(ForeignKey("pawns.id"))
    x: Mapped[int]
    y: Mapped[int]

    color = mapped_column(ColorType, nullable=False)

    pawn: Mapped["Pawn"] = relationship(back_populates="meta")

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        pawn_id: int,
        color: hex,
        x: int = 0,
        y: int = 0,
    ) -> Self:
        return await cls._create(
            id=pawn_id,
            x=x,
            y=y,
            color=color,
            session=session,
        )
