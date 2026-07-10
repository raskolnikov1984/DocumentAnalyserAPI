from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.adapters.api.routes.upload import create_upload_router
from app.adapters.persistence.database import Base, create_engine, create_session_factory
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.core.config import Settings


def create_app(
    settings: Settings | None = None,
    parser=None,
    validator=None,
    repository_factory=None,
) -> FastAPI:
    if settings is None:
        settings = Settings()

    engine = create_engine(settings.database_url)

    if repository_factory is None:

        async def default_repo_factory() -> AsyncGenerator[SqlAlchemyRecordRepository, None]:
            session_factory = create_session_factory(engine)
            async with session_factory() as session:
                yield SqlAlchemyRecordRepository(session)

        repository_factory = default_repo_factory

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    upload_router = create_upload_router(
        repository_factory=repository_factory,
        parser=parser,
        validator=validator,
    )

    app.include_router(upload_router, prefix=settings.api_v1_prefix)

    @app.get("/")
    async def root():
        return {"message": f"{settings.app_name} is running!"}

    return app


app = create_app()
