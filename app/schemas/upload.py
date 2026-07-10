from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    row: int = Field(description="Número de fila donde se encontró el error (0-indexed)")
    field: str = Field(description="Nombre del campo que falló la validación")
    value: str | int | float | None = Field(
        None, description="Valor del campo que causó el error"
    )
    message: str = Field(description="Descripción del error de validación")


class UploadResponse(BaseModel):
    total_rows: int = Field(description="Número total de filas procesadas en el archivo")
    valid_rows: int = Field(description="Número de filas que pasaron todas las validaciones")
    invalid_rows: int = Field(description="Número de filas que fallaron alguna validación")
    errors: list[ErrorDetail] = Field(
        default_factory=list,
        description="Lista de errores detallados por fila inválida",
    )
