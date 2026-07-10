from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_engine(database_url: str):
    return create_async_engine(database_url, echo=False)


def create_session_factory(engine):
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


async def get_async_session(
    engine,
) -> AsyncGenerator[AsyncSession, None]:
    session_factory = create_session_factory(engine)
    async with session_factory() as session:
        yield session
