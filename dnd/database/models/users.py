from typing import TYPE_CHECKING, Optional, Self

from sqlalchemy import ForeignKey, select
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dnd.database.models.base import Base, BaseSchema
from dnd.utils.crypto import Hasher

if TYPE_CHECKING:
    from dnd.database.models.gamesets import GameSet
    from dnd.database.models.maps import Map
    from dnd.database.models.pawns import Pawn

hasher = Hasher()


class UserInGameset(Base):
    __tablename__ = "users_in_gamesets"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    gameset_id = mapped_column(ForeignKey("gamesets.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="in_games")
    gameset: Mapped["GameSet"] = relationship(back_populates="users_in_game")

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        user_id: int,
        gameset_id: int,
    ) -> Self:
        return await cls._create(
            session=session,
            user_id=user_id,
            gameset_id=gameset_id,
        )


class User(BaseSchema):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True, index=True)
    full_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True, index=True)

    _hashed_password = mapped_column("hashed_password", BYTEA, nullable=False)

    gamesets: Mapped[list["GameSet"]] = relationship(
        back_populates="owner", lazy="immediate"
    )
    maps: Mapped[list["Map"]] = relationship(
        back_populates="user", lazy="immediate"
    )
    pawns: Mapped[list["Pawn"]] = relationship(
        back_populates="user", lazy="immediate"
    )
    in_games: Mapped[list["UserInGameset"]] = relationship(
        back_populates="user", lazy="immediate"
    )

    @hybrid_property
    def password(self) -> bytes:
        return self._hashed_password

    @password.setter
    def password(self, password: str) -> None:
        self._hashed_password = hasher.get_password_hash(password).encode()

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        username: str,
        email: str,
        password: str,
        full_name: str | None = None,
    ) -> Self:
        return await cls._create(
            session=session,
            username=username,
            full_name=full_name,
            password=password,
            email=email,
            in_games=[],
        )

    @classmethod
    async def get_by_username(
        cls,
        session: AsyncSession,
        username: str,
    ) -> Self | None:
        query = select(cls).where(cls.username == username)
        result: Result = await session.execute(query)
        return result.scalar_one_or_none()
