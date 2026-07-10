import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.adapters.excel.openpyxl_parser import OpenpyxlParser
from app.adapters.persistence.repository import SqlAlchemyRecordRepository
from app.adapters.validation.config import create_default_validator
from app.core.services.upload_service import UploadService
from app.schemas.upload import ErrorDetail, UploadResponse


def create_upload_router(
    repository_factory=None,
    parser=None,
    validator=None,
) -> APIRouter:
    router = APIRouter(tags=["Upload"])

    if parser is None:
        parser = OpenpyxlParser()

    if validator is None:
        validator = create_default_validator()

    @router.post(
        "/upload",
        summary="Subir archivo CBAM",
        description=(
            "Recibe un archivo .xlsx con datos CBAM, valida cada fila contra las "
            "reglas de negocio (EORI, CN Code, fechas, país, etc.) y persiste "
            "solo los registros válidos. Devuelve un resumen con el conteo de "
            "filas válidas e inválidas, más los errores detallados."
        ),
        response_model=UploadResponse,
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_400_BAD_REQUEST: {
                "description": "El archivo no es un .xlsx válido",
                "content": {
                    "application/json": {
                        "example": {"detail": "Solo se permiten archivos .xlsx"}
                    }
                },
            },
            status.HTTP_200_OK: {
                "description": (
                    "Archivo procesado correctamente. Retorna conteo de filas "
                    "válidas e inválidas con los errores de validación."
                ),
                "content": {
                    "application/json": {
                        "example": {
                            "total_rows": 10,
                            "valid_rows": 9,
                            "invalid_rows": 1,
                            "errors": [
                                {
                                    "row": 5,
                                    "field": "eori_number",
                                    "value": "INVALID",
                                    "message": "El formato del EORI no es válido",
                                }
                            ],
                        }
                    }
                },
            },
        },
    )
    async def upload_file(
        file: UploadFile = File(..., description="Archivo .xlsx con datos CBAM"),
        repo: SqlAlchemyRecordRepository = (
            Depends(repository_factory) if repository_factory else None
        ),
    ):
        if not file.filename or not file.filename.endswith(".xlsx"):
            raise HTTPException(
                status_code=400, detail="Solo se permiten archivos .xlsx"
            )

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        content = await file.read()
        tmp.write(content)
        tmp.close()

        try:
            service = UploadService(
                parser=parser, validator=validator, repository=repo
            )
            result = await service.upload(tmp.name)

            return UploadResponse(
                total_rows=result.total_rows,
                valid_rows=result.valid_rows,
                invalid_rows=result.invalid_rows,
                errors=[ErrorDetail(**e) for e in result.errors],
            )
        finally:
            Path(tmp.name).unlink(missing_ok=True)

    return router
