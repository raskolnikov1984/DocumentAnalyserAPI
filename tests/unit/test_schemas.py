from app.schemas.upload import ErrorDetail, UploadResponse
from app.schemas.record import RecordResponse
from app.schemas.pagination import PaginatedResponse


def test_error_detail():
    error = ErrorDetail(
        row=5, field="cn_code", value="abc", message="Invalid"
    )
    assert error.row == 5
    assert error.field == "cn_code"
    assert error.value == "abc"
    assert error.message == "Invalid"
    assert error.model_dump() == {
        "row": 5,
        "field": "cn_code",
        "value": "abc",
        "message": "Invalid",
    }


def test_upload_response():
    errors = [
        ErrorDetail(
            row=1, field="email", value="bad", message="Invalid email"
        )
    ]
    resp = UploadResponse(
        total_rows=50, valid_rows=45, invalid_rows=5, errors=errors
    )
    assert resp.total_rows == 50
    assert resp.valid_rows == 45
    assert resp.invalid_rows == 5
    assert len(resp.errors) == 1


def test_record_response():
    record = RecordResponse(
        eori_number="DE123456789012345",
        declarant_legal_name="Test Corp",
        declarant_address="Addr",
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
    assert record.eori_number == "DE123456789012345"
    assert record.import_volume == 1250.0


def test_paginated_response():
    items = [
        RecordResponse(
            eori_number="DE123456789012345",
            declarant_legal_name="Test Corp",
            declarant_address="Addr",
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
    ]
    resp = PaginatedResponse(page=1, page_size=20, total=100, items=items)
    assert resp.page == 1
    assert resp.page_size == 20
    assert resp.total == 100
    assert len(resp.items) == 1
