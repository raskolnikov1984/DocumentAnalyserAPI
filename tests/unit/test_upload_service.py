from unittest.mock import AsyncMock

import pytest

from app.core.services.upload_service import UploadResult, UploadService


@pytest.fixture
def mock_parser():
    parser = AsyncMock()
    parser.parse.return_value = [
        {
            "eori_number": "DE123456789012345",
            "declarant_legal_name": "ArcelorMittal SA",
            "declarant_address": "24-26 Boulevard d'Avranches",
            "contact_person": "John Doe, john@test.com",
            "competent_authority": "DEHSt",
            "cbam_account_number": "CBAM-DE-2026-00142",
            "data_owner": "Sam Smith, sam@test.com",
            "taric_code": "7207111400",
            "cn_code": "72071114",
            "goods_description": "Semi-finished iron",
            "sector_category": "Iron and Steel",
            "product_type": "Complex",
            "import_volume": 1250.0,
            "date_of_importation": "05.05.2026",
            "country_of_origin": "China",
            "customs_declaration_ref": "DE/2026/MRN-ABC-123456",
            "supplier_name": "Supplier Ch1",
            "notes_comments": "",
        },
        {
            "eori_number": "DE987654321098765",
            "declarant_legal_name": "Other Corp",
            "declarant_address": "Main Street 1",
            "contact_person": "",
            "competent_authority": "DEHSt",
            "cbam_account_number": "CBAM-DE-2026-00143",
            "data_owner": "",
            "taric_code": "",
            "cn_code": "72071114",
            "goods_description": "",
            "sector_category": "Iron and Steel",
            "product_type": "Simple",
            "import_volume": 500.0,
            "date_of_importation": "06.06.2026",
            "country_of_origin": "India",
            "customs_declaration_ref": "",
            "supplier_name": "Supplier In1",
            "notes_comments": "",
        },
    ]
    return parser


@pytest.fixture
def mock_validator():
    validator = AsyncMock()
    validator.validate.side_effect = [
        [],
        [
            {
                "row": 2,
                "field": "contact_person",
                "value": "",
                "message": "Campo requerido",
            }
        ],
    ]
    return validator


@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    repo.save.return_value = None
    return repo


@pytest.fixture
def upload_service(mock_parser, mock_validator, mock_repository):
    return UploadService(
        parser=mock_parser,
        validator=mock_validator,
        repository=mock_repository,
    )


@pytest.mark.asyncio
async def test_upload_service_returns_upload_result(upload_service):
    result = await upload_service.upload("dummy.xlsx")
    assert isinstance(result, UploadResult)


@pytest.mark.asyncio
async def test_upload_service_counts_correctly(upload_service):
    result = await upload_service.upload("dummy.xlsx")
    assert result.total_rows == 2
    assert result.valid_rows == 1
    assert result.invalid_rows == 1


@pytest.mark.asyncio
async def test_upload_service_returns_errors(upload_service):
    result = await upload_service.upload("dummy.xlsx")
    assert len(result.errors) == 1
    assert result.errors[0]["row"] == 2
    assert result.errors[0]["field"] == "contact_person"


@pytest.mark.asyncio
async def test_upload_service_calls_parse(upload_service, mock_parser):
    await upload_service.upload("dummy.xlsx")
    mock_parser.parse.assert_awaited_once_with("dummy.xlsx")


@pytest.mark.asyncio
async def test_upload_service_calls_validate(
    upload_service, mock_validator
):
    await upload_service.upload("dummy.xlsx")
    assert mock_validator.validate.await_count == 2


@pytest.mark.asyncio
async def test_upload_service_saves_only_valid(
    upload_service, mock_repository
):
    await upload_service.upload("dummy.xlsx")
    assert mock_repository.save.await_count == 1


@pytest.mark.asyncio
async def test_upload_service_all_invalid(mock_parser, mock_repository):
    validator = AsyncMock()
    validator.validate.return_value = [
        {
            "row": 1,
            "field": "cn_code",
            "value": "abc",
            "message": "Invalido",
        }
    ]
    service = UploadService(
        parser=mock_parser,
        validator=validator,
        repository=mock_repository,
    )
    result = await service.upload("dummy.xlsx")
    assert result.valid_rows == 0
    assert result.invalid_rows == 2
    mock_repository.save.assert_not_called()
