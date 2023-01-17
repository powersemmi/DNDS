from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from dnd.database.models.base import BaseSchema
from dnd.database.models.maps import Map
from dnd.database.models.pawns import Pawn
from dnd.database.models.users import User


class GameSet(BaseSchema):
    __tablename__ = "gameset"
    owner_id: int = Column(
        BigInteger,
        ForeignKey(User.id),
        nullable=False,
        unique=False,
        index=True,
    )
    name: str = Column(String, nullable=False, unique=True, index=True)
    meta: "GameSetMeta" = relationship(
        "GameSetMeta", backref="gamesets_meta", uselist=False
    )
    owner: User = relationship(User, uselist=False)

    @classmethod
    async def create(cls, session: AsyncSession, name: str, meta, owner: User):
        return await cls._create(
            name=name, meta=meta, owner=owner, session=session
        )


class GameSetPawnPosition(BaseSchema):
    __tablename__ = "gameset_pawns_position"
    x: int
    y: int
    map_id: int
    pawn_id: int

    @classmethod
    async def create(
        cls, session: AsyncSession, x: int, y: int, map_id: int, pawn_id: int
    ):
        return await cls._create(
            x=x, y=y, map_id=map_id, pawn_id=pawn_id, session=session
        )


class GameSetMeta(BaseSchema):
    __tablename__ = "gamesets_meta"

    id = Column(
        BigInteger,
        ForeignKey(GameSet.id),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
    )
    current_map_id: int = Column(
        BigInteger, ForeignKey(Map.id), nullable=False
    )
    pawn: list[Pawn] = relationship(Pawn, backref="pawns", uselist=True)
    maps: list[Map] = relationship(Map, backref="maps", uselist=True)
    pawns_position: list[GameSetPawnPosition] = relationship(
        GameSetPawnPosition, uselist=True
    )
    current_map = relationship(Map, uselist=False)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        gameset_id: int,
        pawn: list[Pawn],
        maps: list[Map],
        pawns_position: list[GameSetPawnPosition],
        current_map: Map,
    ):
        return await cls._create(
            id=gameset_id,
            pawn=pawn,
            maps=maps,
            pawns_position=pawns_position,
            current_map=current_map,
            session=session,
        )
