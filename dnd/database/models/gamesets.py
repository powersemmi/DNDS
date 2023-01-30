from typing import TYPE_CHECKING, Self

from sqlalchemy import ForeignKey, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dnd.database.models.base import BaseSchema

if TYPE_CHECKING:
    from dnd.database.models.maps import Map
    from dnd.database.models.users import User, UserInGameset


class GameSet(BaseSchema):
    __tablename__ = "gamesets"
    name: Mapped[str]
    short_url: Mapped[str] = mapped_column(unique=True, index=True)
    owner_id = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(
        back_populates="gamesets", lazy="immediate"
    )

    maps: Mapped[list["Map"]] = relationship(
        back_populates="gameset", lazy="immediate"
    )
    meta: Mapped["GameSetMeta"] = relationship(
        back_populates="gameset", lazy="immediate"
    )

    users_in_game: Mapped[list["UserInGameset"]] = relationship(
        back_populates="gameset", lazy="immediate"
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        short_url: str,
        owner_id: int,
        gameset_id: int | None = None,
    ):
        return await cls._create(
            id=gameset_id,
            owner_id=owner_id,
            name=name,
            short_url=short_url,
            session=session,
            maps=[],
            users_in_game=[],
        )

    @classmethod
    async def get_by_short_url(
        cls, session: AsyncSession, short_url: str
    ) -> Self | None:
        res = await session.execute(
            select(cls).filter(cls.short_url == short_url)
        )
        return res.scalar_one_or_none()

    @classmethod
    async def get_next_id(cls, session: AsyncSession) -> int:
        res = await session.execute(text("SELECT nextval('gamesets_id_seq');"))
        return res.fetchone()[0]


class GameSetMeta(BaseSchema):
    __tablename__ = "gamesets_meta"

    gameset_id = mapped_column(ForeignKey("gamesets.id"))

    gameset: Mapped["GameSet"] = relationship(back_populates="meta")

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_id: GameSet.id,
    ) -> Self:
        return await cls._create(
            gameset_id=gameset_id,
            session=session,
        )
