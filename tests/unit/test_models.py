from dataclasses import fields
from app.core.domain.models import CbamRecord


def test_cbam_record_fields():
    expected_fields = {
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
    actual_fields = {f.name for f in fields(CbamRecord)}
    assert actual_fields == expected_fields


def test_cbam_record_creation():
    record = CbamRecord(
        eori_number="DE123456789012345",
        declarant_legal_name="ArcelorMittal SA",
        declarant_address="24-26 Boulevard d'Avranches, Luxembourg",
        contact_person="John Doe, john.doe@company.com",
        competent_authority="DEHSt",
        cbam_account_number="CBAM-DE-2026-00142",
        data_owner="Sam Smith, sam.smith@company.com",
        taric_code="7207111400",
        cn_code="72071114",
        goods_description="Semi-finished iron or non-alloy steel",
        sector_category="Iron and Steel",
        product_type="Complex",
        import_volume=1250.0,
        date_of_importation="05.05.2026",
        country_of_origin="China",
        customs_declaration_ref="DE/2026/MRN-ABC-123456",
        supplier_name="Supplier Ch1",
        notes_comments="MRV plan is under preparation",
    )
    assert record.eori_number == "DE123456789012345"
    assert record.import_volume == 1250.0
    assert record.cn_code == "72071114"


def test_cbam_record_is_dataclass():
    assert hasattr(CbamRecord, "__dataclass_fields__")
