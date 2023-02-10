from typing import TYPE_CHECKING, Self

from sqlalchemy import ForeignKey, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import ColorType

from dnd.database.schemas.base import BaseSchema

if TYPE_CHECKING:
    from dnd.database.schemas.game_sets import GameSet
    from dnd.database.schemas.users import User


class Pawn(BaseSchema):
    __tablename__ = "pawns"
    user_id = mapped_column(ForeignKey("users.id"))
    game_set_id = mapped_column(ForeignKey("game_sets.id"))
    name: Mapped[str]

    game_set: Mapped["GameSet"] = relationship(back_populates="pawns")
    user: Mapped["User"] = relationship(back_populates="pawns")
    meta: Mapped["PawnMeta"] = relationship(
        back_populates="pawn", lazy="immediate"
    )

    __table_args__ = (
        UniqueConstraint("game_set_id", "name", name="_game_set_id_pawn_uc"),
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        game_set_id: int,
        user_id: int,
    ) -> Self:
        return await cls._create(
            game_set_id=game_set_id,
            name=name,
            user_id=user_id,
            session=session,
        )

    @classmethod
    async def get_by_name_and_game_set_id(
        cls, session: AsyncSession, name: str, game_set_id: int
    ) -> Self | None:
        return (
            await session.execute(
                select(cls).where(
                    (cls.name == name), (cls.game_set_id == game_set_id)
                )
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
