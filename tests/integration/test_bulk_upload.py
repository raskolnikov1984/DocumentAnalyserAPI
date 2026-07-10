import pytest
from httpx import ASGITransport, AsyncClient

from app.adapters.persistence.database import Base, create_engine, create_session_factory
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.main import create_app

BULK_PATH = "tests/fixtures/valid_bulk_data.xlsx"


@pytest.fixture
async def app_with_db():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = create_session_factory(engine)

    async def repo_factory():
        async with session_factory() as session:
            yield SqlAlchemyRecordRepository(session)

    app = create_app(repository_factory=repo_factory)
    yield app
    await engine.dispose()


@pytest.mark.asyncio
async def test_bulk_upload_15_valid_1_invalid(app_with_db):
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with open(BULK_PATH, "rb") as f:
            response = await client.post(
                "/api/v1/upload",
                files={"file": ("valid_bulk_data.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            )

    assert response.status_code == 200
    data = response.json()

    assert data["total_rows"] == 16
    assert data["valid_rows"] == 15
    assert data["invalid_rows"] == 1


@pytest.mark.asyncio
async def test_bulk_upload_errors_detail(app_with_db):
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with open(BULK_PATH, "rb") as f:
            response = await client.post(
                "/api/v1/upload",
                files={"file": ("valid_bulk_data.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            )

    data = response.json()
    errors = data["errors"]

    assert len(errors) >= 8

    error_fields = {e["field"] for e in errors}
    assert "declarant_legal_name" in error_fields
    assert "cn_code" in error_fields
    assert "product_type" in error_fields
    assert "import_volume" in error_fields
    assert "country_of_origin" in error_fields
    assert "supplier_name" in error_fields

    for error in errors:
        assert error["row"] == 16


@pytest.mark.asyncio
async def test_bulk_upload_persists_valid_records(app_with_db):
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        with open(BULK_PATH, "rb") as f:
            await client.post(
                "/api/v1/upload",
                files={"file": ("valid_bulk_data.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            )
        response = await client.get("/api/v1/records?page=1&page_size=20")

    data = response.json()
    assert data["total"] == 15
    assert len(data["items"]) == 15
