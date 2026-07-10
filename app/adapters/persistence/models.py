from sqlalchemy import Column, Float, Integer, String

from app.adapters.persistence.database import Base


class CbamRecordModel(Base):
    __tablename__ = "cbam_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    eori_number = Column(String(17), nullable=False)
    declarant_legal_name = Column(String, nullable=False)
    declarant_address = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    competent_authority = Column(String, nullable=False)
    cbam_account_number = Column(String, nullable=False)
    data_owner = Column(String, nullable=False)
    taric_code = Column(String(10), nullable=False)
    cn_code = Column(String(8), nullable=False)
    goods_description = Column(String, nullable=False)
    sector_category = Column(String, nullable=False)
    product_type = Column(String, nullable=False)
    import_volume = Column(Float, nullable=False)
    date_of_importation = Column(String, nullable=False)
    country_of_origin = Column(String, nullable=False)
    customs_declaration_ref = Column(String, nullable=False)
    supplier_name = Column(String, nullable=False)
    notes_comments = Column(String, nullable=False)
