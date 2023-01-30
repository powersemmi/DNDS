import logging

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from dnd.settings import settings

engine = create_async_engine(
    settings.DB_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

logger = logging.getLogger(__name__)


async def get_db() -> AsyncSession:
    async with async_session() as session:  # type: AsyncSession
        yield session
