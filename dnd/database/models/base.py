from datetime import datetime

from sqlalchemy import BigInteger, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    @classmethod
    async def _create(cls, session: AsyncSession, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        return obj

    @classmethod
    async def get(cls, session: AsyncSession, _id: int):
        result = await session.get(cls, _id)
        return result


class BaseSchema(Base):
    __abstract__ = True

    id = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )


metadata = Base.metadata
