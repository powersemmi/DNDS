from typing import TYPE_CHECKING, Optional, Self

from sqlalchemy import ForeignKey, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dnd.database.models.base import BaseSchema

if TYPE_CHECKING:
    from dnd.database.models.gamesets import GameSet
    from dnd.database.models.pawns import Pawn
    from dnd.database.models.users import User


class Map(BaseSchema):
    __tablename__ = "maps"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    gameset_id: Mapped[int] = mapped_column(ForeignKey("gamesets.id"))
    name: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="maps")
    gameset: Mapped["GameSet"] = relationship(back_populates="maps")

    pawns: Mapped[list["Pawn"]] = relationship(
        back_populates="map", lazy="immediate"
    )
    meta: Mapped["MapMeta"] = relationship(
        back_populates="map", lazy="immediate"
    )

    __table_args__ = (
        UniqueConstraint("gameset_id", "name", name="_gameset_map_uc"),
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_id: int,
        user_id: int,
        name: str,
    ) -> Self:
        return await cls._create(
            session=session,
            gameset_id=gameset_id,
            user_id=user_id,
            name=name,
            pawns=[],
        )

    @classmethod
    async def get_by_name_and_gameset_id(
        cls, session: AsyncSession, name: str, gameset_id: int
    ) -> Self | None:
        return (
            await session.execute(
                select(cls).where(
                    (cls.name == name), (cls.gameset_id == gameset_id)
                )
            )
        ).scalar_one_or_none()


class MapMeta(BaseSchema):
    __tablename__ = "maps_meta"
    map_id = mapped_column(ForeignKey("maps.id"))
    len_x: Mapped[int]
    len_y: Mapped[int]
    image_short_url: Mapped[Optional[str]]

    map: Mapped["Map"] = relationship(back_populates="meta")

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        map_id: int,
        len_x: int,
        len_y: int,
        image_short_url: Optional[str] = None,
    ) -> Self:
        return await cls._create(
            map_id=map_id,
            len_x=len_x,
            len_y=len_y,
            image_short_url=image_short_url,
            session=session,
        )
