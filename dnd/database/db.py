from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from dnd.settings import settings

engine = create_async_engine(
    settings.DB_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=True,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with async_session() as session:  # type: AsyncSession
        yield session
