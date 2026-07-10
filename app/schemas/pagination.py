from pydantic import BaseModel, Field


class PaginatedResponse(BaseModel):
    page: int = Field(description="Número de página actual")
    page_size: int = Field(description="Cantidad de elementos por página")
    total: int = Field(description="Número total de registros disponibles")
    items: list = Field(description="Lista de registros en la página actual")
