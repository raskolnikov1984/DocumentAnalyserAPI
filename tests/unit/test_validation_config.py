import pytest

from app.adapters.validation.config import create_default_validator

SAMPLE_ROW = {
    "eori_number": "DE123456789012345",
    "declarant_legal_name": "ArcelorMittal SA",
    "declarant_address": "24-26 Boulevard d'Avranches",
    "contact_person": "John Doe, john@test.com",
    "competent_authority": "DEHSt",
    "cbam_account_number": "CBAM-DE-2026-00142",
    "data_owner": "Sam Smith",
    "taric_code": "7207111400",
    "cn_code": "72071114",
    "goods_description": "Semi-finished iron",
    "sector_category": "Iron and Steel",
    "product_type": "Complex Goods",
    "import_volume": 1250.0,
    "date_of_importation": "05.05.2026",
    "country_of_origin": "China",
    "customs_declaration_ref": "DE/2026/MRN-123",
    "supplier_name": "Supplier X",
    "notes_comments": "",
}


@pytest.mark.asyncio
async def test_default_validator_passes_valid_row():
    validator = create_default_validator()
    errors = await validator.validate(SAMPLE_ROW, 1)
    assert errors == []


@pytest.mark.asyncio
async def test_default_validator_detects_multiple_errors():
    validator = create_default_validator()
    row = dict(
        SAMPLE_ROW,
        eori_number="BAD",
        cn_code="123",
        import_volume=-5,
        contact_person="NoContact",
        country_of_origin="Atlantis",
        product_type="Invalid",
    )
    errors = await validator.validate(row, 1)
    assert len(errors) >= 5


@pytest.mark.asyncio
async def test_default_validator_required_fields():
    validator = create_default_validator()
    row = {k: "" for k in SAMPLE_ROW}
    errors = await validator.validate(row, 1)
    assert len(errors) >= len([
        "eori_number", "declarant_legal_name", "declarant_address",
        "contact_person", "competent_authority", "cbam_account_number",
        "data_owner", "cn_code", "goods_description", "sector_category",
        "product_type", "import_volume", "date_of_importation",
        "country_of_origin", "supplier_name",
    ])
