from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/"
    ) as client:
        yield client
