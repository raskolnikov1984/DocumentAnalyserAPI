import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

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
    router = APIRouter()

    if parser is None:
        parser = OpenpyxlParser()

    if validator is None:
        validator = create_default_validator()

    @router.post("/upload")
    async def upload_file(
        file: UploadFile = File(...),
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
