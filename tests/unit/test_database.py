import pytest
from sqlalchemy import text

from app.adapters.persistence.database import create_engine, get_async_session


@pytest.mark.asyncio
async def test_create_engine():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
    await engine.dispose()


@pytest.mark.asyncio
async def test_get_async_session():
    engine = create_engine("sqlite+aiosqlite://")
    async for session in get_async_session(engine):
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    await engine.dispose()
