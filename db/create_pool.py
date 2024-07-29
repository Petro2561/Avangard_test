from __future__ import annotations

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from db.db import Base


async def create_pool(enable_logging: bool = False) -> async_sessionmaker[AsyncSession]:
    DATABASE_URL = "sqlite+aiosqlite:///sqlite.db"
    engine: AsyncEngine = create_async_engine(url=DATABASE_URL, echo=enable_logging)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, expire_on_commit=False)