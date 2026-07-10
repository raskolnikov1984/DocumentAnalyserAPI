from pydantic import BaseModel


class ErrorDetail(BaseModel):
    row: int
    field: str
    value: str | int | float | None = None
    message: str


class UploadResponse(BaseModel):
    total_rows: int
    valid_rows: int
    invalid_rows: int
    errors: list[ErrorDetail] = []
