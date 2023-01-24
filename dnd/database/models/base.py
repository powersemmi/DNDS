from datetime import datetime
from typing import Optional, Self, TypeAlias

from sqlalchemy import TIMESTAMP, BigInteger, Column, Identity, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base: TypeAlias = declarative_base()

metadata = Base.metadata


class BaseSchema(Base):
    __abstract__ = True

    id: int = Column(
        BigInteger, Identity(always=True), primary_key=True, nullable=False
    )
    created_at: datetime = Column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: datetime = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )

    @classmethod
    async def _create(cls, session: AsyncSession, **kwargs) -> Self:
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def get(cls, session: AsyncSession, _id: int) -> Optional[Self]:
        result: Result = await session.get(cls, _id)
        return result.scalar_one_or_none()
