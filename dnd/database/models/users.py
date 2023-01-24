from typing import Self

from sqlalchemy import Column, String, select
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property

from dnd.database.models.base import BaseSchema
from dnd.utils.crypto import Hasher

hasher = Hasher()


class User(BaseSchema):
    __tablename__ = "users"

    username: str = Column(
        String(256), nullable=False, unique=True, index=True
    )
    full_name: str | None = Column(String(256))
    email: str = Column(String(320), nullable=False, unique=True)

    _hashed_password: bytes = Column("hashed_password", BYTEA, nullable=False)

    @hybrid_property
    def password(self) -> bytes:
        return self._hashed_password

    @password.setter
    def password(self, password: str):
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
