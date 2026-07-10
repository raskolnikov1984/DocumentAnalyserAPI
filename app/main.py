from fastapi import FastAPI

from app.core.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = Settings()

    app = FastAPI(title=settings.app_name)

    @app.get("/")
    async def root():
        return {"message": f"{settings.app_name} is running!"}

    return app


app = create_app()
