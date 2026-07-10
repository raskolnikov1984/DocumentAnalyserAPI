import pytest
from sqlalchemy import text

from app.adapters.persistence.database import Base, create_engine, create_session_factory
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.core.domain.models import CbamRecord


@pytest.fixture
async def session():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = create_session_factory(engine)
    async with session_factory() as s:
        yield s
    await engine.dispose()


@pytest.fixture
def repository(session):
    return SqlAlchemyRecordRepository(session)


@pytest.fixture
def sample_record():
    return CbamRecord(
        eori_number="DE123456789012345",
        declarant_legal_name="Test Corp",
        declarant_address="Test Address 1",
        contact_person="John Doe, john@test.com",
        competent_authority="DEHSt",
        cbam_account_number="CBAM-DE-2026-00142",
        data_owner="Sam Smith",
        taric_code="7207111400",
        cn_code="72071114",
        goods_description="Semi-finished iron",
        sector_category="Iron and Steel",
        product_type="Complex",
        import_volume=1250.0,
        date_of_importation="05.05.2026",
        country_of_origin="China",
        customs_declaration_ref="DE/2026/MRN-123",
        supplier_name="Supplier X",
        notes_comments="",
    )


@pytest.mark.asyncio
async def test_save_record(repository, sample_record):
    saved = await repository.save(sample_record)
    assert saved.eori_number == "DE123456789012345"
    assert saved.cn_code == "72071114"


@pytest.mark.asyncio
async def test_count_empty(repository):
    assert await repository.count() == 0


@pytest.mark.asyncio
async def test_count_after_insert(repository, sample_record):
    await repository.save(sample_record)
    assert await repository.count() == 1


@pytest.mark.asyncio
async def test_find_all_pagination(repository, sample_record):
    record2 = CbamRecord(
        eori_number="DE987654321098765",
        declarant_legal_name="Other Corp",
        declarant_address="Other Address",
        contact_person="Jane Doe",
        competent_authority="DEHSt",
        cbam_account_number="CBAM-DE-2026-00143",
        data_owner="Sam Smith",
        taric_code="",
        cn_code="72071114",
        goods_description="Other goods",
        sector_category="Iron and Steel",
        product_type="Simple",
        import_volume=500.0,
        date_of_importation="06.06.2026",
        country_of_origin="India",
        customs_declaration_ref="",
        supplier_name="Supplier Y",
        notes_comments="",
    )
    await repository.save(sample_record)
    await repository.save(record2)

    records, total = await repository.find_all(page=1, page_size=1)
    assert len(records) == 1
    assert total == 2
    assert records[0].eori_number == "DE123456789012345"

    records, total = await repository.find_all(page=2, page_size=1)
    assert len(records) == 1
    assert total == 2
    assert records[0].eori_number == "DE987654321098765"


@pytest.mark.asyncio
async def test_find_all_returns_domain_models(repository, sample_record):
    await repository.save(sample_record)
    records, _ = await repository.find_all()
    assert isinstance(records[0], CbamRecord)
