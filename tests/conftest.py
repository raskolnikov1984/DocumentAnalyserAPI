from httpx import ASGITransport, AsyncClient
import pytest

from app.main import create_app


@pytest.fixture(scope="function")
async def async_client():
    app = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/"
    ) as client:
        yield client
