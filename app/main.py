import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from loguru import logger

from app.adapters.api.routes.records import create_records_router
from app.adapters.api.routes.upload import create_upload_router
from app.adapters.persistence.database import (
    Base,
    create_engine,
    create_session_factory,
)
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.core.config import Settings
from app.core.logging import configure_logging


def create_app(
    settings: Settings | None = None,
    parser=None,
    validator=None,
    repository_factory=None,
) -> FastAPI:
    if settings is None:
        settings = Settings()

    configure_logging(settings.environment)
    logger.info("Starting {app_name}", app_name=settings.app_name)

    engine = create_engine(settings.database_url)

    if repository_factory is None:

        async def default_repo_factory() -> (
            AsyncGenerator[SqlAlchemyRecordRepository, None]
        ):
            session_factory = create_session_factory(engine)
            async with session_factory() as session:
                yield SqlAlchemyRecordRepository(session)

        repository_factory = default_repo_factory

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables ready")
        yield
        logger.info("Disposing database engine...")
        await engine.dispose()
        logger.info("Database engine disposed")

    app = FastAPI(
        title=settings.app_name,
        description=(
            "API de validación e ingreso de datos CBAM (Carbon Border Adjustment "
            "Mechanism). Recibe archivos .xlsx, valida cada fila contra reglas de "
            "negocio (EORI, CN Code, país ISO, fechas, etc.), persiste registros "
            "válidos y devuelve errores detallados por fila inválida."
        ),
        version="1.0.0",
        contact={
            "name": "OneCluster",
            "email": "alejandro.ayala@onecluster.org",
        },
        license_info={
            "name": "GPL-2.0",
            "url": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
        },
        openapi_tags=[
            {
                "name": "Upload",
                "description": "Subida y validación de archivos CBAM (.xlsx)",
            },
            {
                "name": "Records",
                "description": "Consulta de registros CBAM almacenados",
            },
        ],
        lifespan=lifespan,
    )

    upload_router = create_upload_router(
        repository_factory=repository_factory,
        parser=parser,
        validator=validator,
    )
    records_router = create_records_router(
        repository_factory=repository_factory
    )

    app.include_router(upload_router, prefix=settings.api_v1_prefix)
    app.include_router(records_router, prefix=settings.api_v1_prefix)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = time.time() - start
        logger.info(
            "{method} {path} {status_code} {elapsed:.3f}s",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            elapsed=elapsed,
        )
        return response

    @app.get("/")
    async def root():
        return {"message": f"{settings.app_name} is running!"}

    return app


app = create_app()
