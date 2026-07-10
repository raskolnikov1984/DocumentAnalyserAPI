import pytest
from httpx import ASGITransport, AsyncClient

from app.adapters.persistence.database import (
    Base,
    create_engine,
    create_session_factory,
)
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.core.domain.models import CbamRecord
from app.main import create_app


@pytest.fixture
async def app_with_data():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = create_session_factory(engine)
    async with session_factory() as session:
        repo = SqlAlchemyRecordRepository(session)
        await repo.save(
            CbamRecord(
                eori_number="DE123456789012345",
                declarant_legal_name="Test Corp",
                declarant_address="Addr 1",
                contact_person="John",
                competent_authority="DEHSt",
                cbam_account_number="CBAM-DE-2026-00142",
                data_owner="Sam",
                taric_code="7207111400",
                cn_code="72071114",
                goods_description="Iron",
                sector_category="Iron and Steel",
                product_type="Complex",
                import_volume=1250.0,
                date_of_importation="05.05.2026",
                country_of_origin="China",
                customs_declaration_ref="DE/2026/MRN-123",
                supplier_name="Supplier X",
                notes_comments="",
            )
        )
        await repo.save(
            CbamRecord(
                eori_number="DE987654321098765",
                declarant_legal_name="Other Corp",
                declarant_address="Addr 2",
                contact_person="Jane",
                competent_authority="DEHSt",
                cbam_account_number="CBAM-DE-2026-00143",
                data_owner="Tom",
                taric_code="",
                cn_code="72071115",
                goods_description="Steel",
                sector_category="Iron and Steel",
                product_type="Simple",
                import_volume=500.0,
                date_of_importation="06.06.2026",
                country_of_origin="India",
                customs_declaration_ref="",
                supplier_name="Supplier Y",
                notes_comments="",
            )
        )
        await session.commit()

    async def repo_factory():
        async with session_factory() as s:
            yield SqlAlchemyRecordRepository(s)

    app = create_app(repository_factory=repo_factory)
    yield app
    await engine.dispose()


@pytest.mark.asyncio
async def test_records_endpoint_returns_200(app_with_data):
    transport = ASGITransport(app=app_with_data)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/records")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_records_endpoint_pagination(app_with_data):
    transport = ASGITransport(app=app_with_data)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/records?page=1&page_size=1")
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 2
    assert len(data["items"]) == 1


@pytest.mark.asyncio
async def test_records_endpoint_item_structure(app_with_data):
    transport = ASGITransport(app=app_with_data)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/records")
    data = response.json()
    item = data["items"][0]
    assert "eori_number" in item
    assert "cn_code" in item
    assert "import_volume" in item
