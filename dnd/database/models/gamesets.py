from typing import Self

from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from dnd.database.models.base import BaseSchema


class GameSet(BaseSchema):
    __tablename__ = "gamesets"
    id: int = Column(BigInteger, primary_key=True, nullable=False)
    name: str = Column(String(255), nullable=False)
    short_url: str = Column(
        String(255), unique=True, nullable=False, index=True
    )
    user_id: int = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    user = relationship("User", uselist=False)
    meta: "GameSetMeta" = relationship(
        "GameSetMeta", backref="gameset", uselist=False, lazy="joined"
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        short_url: str,
        owner_id: int,
        gameset_id: int | None = None,
        meta: type["GameSetMeta"] | None = None,
    ) -> Self:
        return await cls._create(
            id=gameset_id,
            user_id=owner_id,
            name=name,
            short_url=short_url,
            meta=meta,
            session=session,
        )

    @classmethod
    async def get_next_id(cls, session: AsyncSession) -> int:
        res = await session.execute("SELECT nextval('gamesets_id_seq');")
        return res.fetchone()[0]


class GameSetMeta(BaseSchema):
    __tablename__ = "gamesets_meta"

    gameset_id: int = Column(BigInteger, ForeignKey("gamesets.id"))
    pawns: list = relationship("Pawn", backref="gameset_meta", uselist=True)
    maps: list = relationship("Map", backref="gameset_meta", uselist=True)
    pawns_position: list[type["GameSetPawnPosition"] | None] = relationship(
        "GameSetPawnPosition", backref="gameset_meta", uselist=True
    )

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_id: GameSet.id,
        pawns: list | None = None,
        maps: list | None = None,
        pawns_position: list["GameSetPawnPosition"] | None = None,
    ) -> Self:
        return await cls._create(
            gameset_id=gameset_id,
            pawns=pawns if pawns else [],
            maps=maps if maps else [],
            pawns_position=pawns_position if pawns_position else [],
            session=session,
        )


class GameSetPawnPosition(BaseSchema):
    __tablename__ = "gameset_pawns_position"
    gameset_meta_id = Column(BigInteger, ForeignKey("gamesets_meta.id"))
    pawn_id: int = Column(BigInteger, ForeignKey("pawns.id"))
    x: int
    y: int

    pawn = relationship("Pawn", uselist=False)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_meta_id: GameSetMeta.id,
        x: int,
        y: int,
        map_id: int,
        pawn_id: int,
    ) -> Self:
        return await cls._create(
            gameset_meta_id=gameset_meta_id,
            x=x,
            y=y,
            map_id=map_id,
            pawn_id=pawn_id,
            session=session,
        )
