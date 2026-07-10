from pydantic import BaseModel, Field


class RecordResponse(BaseModel):
    eori_number: str = Field(description="Número EORI del declarante (formato: XX...)")
    declarant_legal_name: str = Field(description="Razón social del declarante")
    declarant_address: str = Field(description="Dirección del declarante")
    contact_person: str = Field(description="Persona de contacto (nombre, email/teléfono)")
    competent_authority: str = Field(description="Autoridad competente (ej: DEHSt)")
    cbam_account_number: str = Field(description="Número de cuenta CBAM")
    data_owner: str = Field(description="Propietario de los datos (nombre, email)")
    taric_code: str = Field(description="Código TARIC (código de 10 dígitos)")
    cn_code: str = Field(description="Código CN (código de 8 dígitos)")
    goods_description: str = Field(description="Descripción de las mercancías")
    sector_category: str = Field(description="Categoría del sector")
    product_type: str = Field(
        description='Tipo de producto: "Simple Goods" o "Complex Goods"'
    )
    import_volume: float = Field(description="Volumen de importación (valor positivo)")
    date_of_importation: str = Field(description="Fecha de importación (formato DD.MM.YYYY)")
    country_of_origin: str = Field(description="País de origen")
    customs_declaration_ref: str = Field(description="Referencia de la declaración aduanera")
    supplier_name: str = Field(description="Nombre del proveedor")
    notes_comments: str = Field(description="Notas o comentarios adicionales")
