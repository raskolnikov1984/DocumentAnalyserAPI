from pydantic import BaseModel


class RecordResponse(BaseModel):
    eori_number: str
    declarant_legal_name: str
    declarant_address: str
    contact_person: str
    competent_authority: str
    cbam_account_number: str
    data_owner: str
    taric_code: str
    cn_code: str
    goods_description: str
    sector_category: str
    product_type: str
    import_volume: float
    date_of_importation: str
    country_of_origin: str
    customs_declaration_ref: str
    supplier_name: str
    notes_comments: str
