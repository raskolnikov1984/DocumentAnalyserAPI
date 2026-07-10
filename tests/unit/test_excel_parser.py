import pytest

from app.adapters.excel.openpyxl_parser import OpenpyxlParser


SAMPLE_PATH = "tests/fixtures/sample_data.xlsx"


@pytest.mark.asyncio
async def test_parse_returns_list_of_dicts():
    parser = OpenpyxlParser()
    result = await parser.parse(SAMPLE_PATH)
    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)


@pytest.mark.asyncio
async def test_parse_has_all_expected_keys():
    parser = OpenpyxlParser()
    result = await parser.parse(SAMPLE_PATH)

    expected_keys = {
        "eori_number",
        "declarant_legal_name",
        "declarant_address",
        "contact_person",
        "competent_authority",
        "cbam_account_number",
        "data_owner",
        "taric_code",
        "cn_code",
        "goods_description",
        "sector_category",
        "product_type",
        "import_volume",
        "date_of_importation",
        "country_of_origin",
        "customs_declaration_ref",
        "supplier_name",
        "notes_comments",
    }
    assert set(result[0].keys()) == expected_keys


@pytest.mark.asyncio
async def test_parse_correct_number_of_rows():
    parser = OpenpyxlParser()
    result = await parser.parse(SAMPLE_PATH)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_parse_first_row_values():
    parser = OpenpyxlParser()
    result = await parser.parse(SAMPLE_PATH)
    first = result[0]
    assert first["eori_number"] == "DE123456789012345"
    assert first["declarant_legal_name"] == "ArcelorMittal SA"
    assert first["import_volume"] == 1250
    assert first["cn_code"] == "72071114"
