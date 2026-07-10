import pytest
from sqlalchemy import text

from app.adapters.persistence.database import Base, create_engine
from app.adapters.persistence.models import CbamRecordModel


@pytest.mark.asyncio
async def test_create_tables():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        tables = await conn.run_sync(
            lambda sync_conn: sync_conn.execute(
                text("SELECT name FROM sqlite_master WHERE type='table'")
            ).fetchall()
        )
        table_names = {row[0] for row in tables}
        assert "cbam_records" in table_names
    await engine.dispose()


@pytest.mark.asyncio
async def test_insert_and_read_record():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with engine.connect() as conn:
        result = await conn.execute(
            text("""
                INSERT INTO cbam_records (
                    eori_number, declarant_legal_name, declarant_address,
                    contact_person, competent_authority, cbam_account_number,
                    data_owner, taric_code, cn_code, goods_description,
                    sector_category, product_type, import_volume,
                    date_of_importation, country_of_origin,
                    customs_declaration_ref, supplier_name, notes_comments
                ) VALUES (
                    :eori, :name, :addr, :contact, :authority, :account,
                    :owner, :taric, :cn, :desc, :sector, :type, :vol,
                    :date, :country, :customs, :supplier, :notes
                )
            """),
            {
                "eori": "DE123456789012345",
                "name": "Test Corp",
                "addr": "Test Address",
                "contact": "John Doe",
                "authority": "DEHSt",
                "account": "CBAM-DE-2026-00142",
                "owner": "Sam Smith",
                "taric": "7207111400",
                "cn": "72071114",
                "desc": "Test goods",
                "sector": "Iron and Steel",
                "type": "Complex",
                "vol": 1250.0,
                "date": "05.05.2026",
                "country": "China",
                "customs": "DE/2026/MRN-123",
                "supplier": "Supplier X",
                "notes": "",
            },
        )
        assert result.rowcount == 1

        rows = await conn.execute(text("SELECT * FROM cbam_records"))
        record = rows.one()
        assert record.eori_number == "DE123456789012345"
        assert record.cn_code == "72071114"
        assert float(record.import_volume) == 1250.0

    await engine.dispose()
