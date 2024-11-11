from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from config import settings


engine: AsyncEngine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    echo=True,
)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def session_getter() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
