import tempfile
from pathlib import Path

import openpyxl
import pytest
from httpx import ASGITransport, AsyncClient

from app.adapters.persistence.database import Base, create_engine
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.main import create_app


@pytest.fixture
def sample_xlsx():
    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Template"
    ws.append(
        [
            "EORI Number",
            "Declarant Legal Name",
            "Declarant Address",
            "Contact Person",
            "Competent Authority",
            "CBAM Account Number",
            "Data Owner",
            "TARIC Code",
            "CN Code",
            "Goods Description",
            "Sector Category",
            "Product Type",
            "Import Volume",
            "Date of importation",
            "Country of Origin",
            "Customs Declaration Ref",
            "Supplier Name",
            "Notes / Comments",
        ]
    )
    ws.append(
        [
            "DE123456789012345",
            "ArcelorMittal SA",
            "Addr 1",
            "John Doe, john@test.com",
            "DEHSt",
            "CBAM-DE-2026-00142",
            "Sam Smith",
            "7207111400",
            "72071114",
            "Semi-finished iron",
            "Iron and Steel",
            "Complex Goods",
            1250,
            "05.05.2026",
            "China",
            "DE/2026/MRN-123",
            "Supplier X",
            "",
        ]
    )
    ws.append(
        [
            "DE987654321098765",
            "",
            "",
            "",
            "DEHSt",
            "CBAM-DE-2026-00143",
            "",
            "",
            "",
            "",
            "Iron and Steel",
            "Simple Goods",
            500,
            "06.06.2026",
            "India",
            "",
            "Supplier Y",
            "",
        ]
    )
    wb.save(tmp.name)
    wb.close()
    yield tmp.name
    Path(tmp.name).unlink(missing_ok=True)


@pytest.fixture
async def app_with_db():
    engine = create_engine("sqlite+aiosqlite://")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    from app.adapters.excel.openpyxl_parser import OpenpyxlParser
    from app.adapters.validation.pipeline import ValidationPipeline
    from app.adapters.validation.validators.required import (
        RequiredValidator,
    )

    parser = OpenpyxlParser()
    validators = [
        RequiredValidator(
            fields=["declarant_legal_name", "contact_person"]
        ),
    ]
    validator = ValidationPipeline(validators)

    async def get_repo():
        from app.adapters.persistence.database import (
            create_session_factory,
        )

        session_factory = create_session_factory(engine)
        async with session_factory() as session:
            yield SqlAlchemyRecordRepository(session)

    app = create_app(
        parser=parser,
        validator=validator,
        repository_factory=get_repo,
    )
    yield app
    await engine.dispose()


@pytest.mark.asyncio
async def test_upload_endpoint_returns_200(app_with_db, sample_xlsx):
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        with open(sample_xlsx, "rb") as f:
            response = await client.post(
                "/api/v1/upload",
                files={
                    "file": (
                        "test.xlsx",
                        f,
                        (
                            "application/vnd.openxmlformats-"
                            "officedocument.spreadsheetml.sheet"
                        ),
                    )
                },
            )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_upload_endpoint_counts(app_with_db, sample_xlsx):
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        with open(sample_xlsx, "rb") as f:
            response = await client.post(
                "/api/v1/upload",
                files={
                    "file": (
                        "test.xlsx",
                        f,
                        (
                            "application/vnd.openxmlformats-"
                            "officedocument.spreadsheetml.sheet"
                        ),
                    )
                },
            )
    data = response.json()
    assert data["total_rows"] == 2
    assert data["valid_rows"] == 1
    assert data["invalid_rows"] == 1


@pytest.mark.asyncio
async def test_upload_endpoint_rejects_non_xlsx(app_with_db):
    transport = ASGITransport(app=app_with_db)
    async with AsyncClient(
        transport=transport, base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/upload",
            files={"file": ("test.txt", b"not an xlsx", "text/plain")},
        )
    assert response.status_code == 400
