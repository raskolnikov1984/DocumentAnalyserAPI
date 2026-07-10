import pytest

from app.adapters.validation.pipeline import ValidationPipeline
from app.adapters.validation.validators.required import RequiredValidator
from app.adapters.validation.validators.length import LengthValidator
from app.adapters.validation.validators.numeric import PositiveNumericValidator
from app.adapters.validation.validators.email import EmailValidator
from app.adapters.validation.validators.allowed_values import AllowedValuesValidator


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
    "product_type": "Complex",
    "import_volume": 1250.0,
    "date_of_importation": "05.05.2026",
    "country_of_origin": "China",
    "customs_declaration_ref": "DE/2026/MRN-123",
    "supplier_name": "Supplier X",
    "notes_comments": "",
}


@pytest.mark.asyncio
async def test_required_validator_empty_field():
    validator = RequiredValidator(fields=["contact_person"])
    row = dict(SAMPLE_ROW, contact_person="")
    errors = await validator.validate(row, 1)
    assert len(errors) == 1
    assert errors[0]["field"] == "contact_person"
    assert errors[0]["row"] == 1


@pytest.mark.asyncio
async def test_required_validator_ok():
    validator = RequiredValidator(fields=["contact_person"])
    errors = await validator.validate(SAMPLE_ROW, 1)
    assert errors == []


@pytest.mark.asyncio
async def test_length_validator_min():
    validator = LengthValidator(fields={"cn_code": (8, 8)})
    row = dict(SAMPLE_ROW, cn_code="7207111")
    errors = await validator.validate(row, 1)
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_length_validator_max():
    validator = LengthValidator(fields={"cn_code": (8, 8)})
    row = dict(SAMPLE_ROW, cn_code="720711144")
    errors = await validator.validate(row, 1)
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_length_validator_ok():
    validator = LengthValidator(fields={"cn_code": (8, 8)})
    errors = await validator.validate(SAMPLE_ROW, 1)
    assert errors == []


@pytest.mark.asyncio
async def test_positive_numeric_validator_zero():
    validator = PositiveNumericValidator(fields=["import_volume"])
    row = dict(SAMPLE_ROW, import_volume=0)
    errors = await validator.validate(row, 1)
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_positive_numeric_validator_negative():
    validator = PositiveNumericValidator(fields=["import_volume"])
    row = dict(SAMPLE_ROW, import_volume=-10)
    errors = await validator.validate(row, 1)
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_positive_numeric_validator_ok():
    validator = PositiveNumericValidator(fields=["import_volume"])
    errors = await validator.validate(SAMPLE_ROW, 1)
    assert errors == []


@pytest.mark.asyncio
async def test_pipeline_runs_all_validators():
    validators = [
        RequiredValidator(fields=["contact_person", "supplier_name"]),
        PositiveNumericValidator(fields=["import_volume"]),
    ]
    pipeline = ValidationPipeline(validators)

    row = dict(SAMPLE_ROW, contact_person="", supplier_name="", import_volume=-5)
    errors = await pipeline.validate(row, 1)
    assert len(errors) == 3


@pytest.mark.asyncio
async def test_pipeline_no_errors():
    validators = [
        RequiredValidator(fields=["contact_person"]),
        PositiveNumericValidator(fields=["import_volume"]),
    ]
    pipeline = ValidationPipeline(validators)
    errors = await pipeline.validate(SAMPLE_ROW, 1)
    assert errors == []


@pytest.mark.asyncio
async def test_email_validator_invalid():
    validator = EmailValidator(fields=["contact_person"])
    row = dict(SAMPLE_ROW, contact_person="not-an-email")
    errors = await validator.validate(row, 1)
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_email_validator_ok():
    validator = EmailValidator(fields=["contact_person"])
    errors = await validator.validate(SAMPLE_ROW, 1)
    assert errors == []


@pytest.mark.asyncio
async def test_allowed_values_validator_invalid():
    validator = AllowedValuesValidator(
        fields={"product_type": {"Simple", "Complex"}}
    )
    row = dict(SAMPLE_ROW, product_type="InvalidType")
    errors = await validator.validate(row, 1)
    assert len(errors) == 1


@pytest.mark.asyncio
async def test_allowed_values_validator_ok():
    validator = AllowedValuesValidator(
        fields={"product_type": {"Simple", "Complex"}}
    )
    errors = await validator.validate(SAMPLE_ROW, 1)
    assert errors == []
