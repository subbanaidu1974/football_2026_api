from __future__ import annotations
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/sportshub",
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

@asynccontextmanager
async def lifespan(app):
    # create tables on startup (swap to Alembic later if you want migrations)
    async with engine.begin() as conn:
        from . import models  # ensure models are imported
        await conn.run_sync(models.Base.metadata.create_all)
    yield
