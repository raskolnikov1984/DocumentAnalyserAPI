from dataclasses import dataclass, field

from loguru import logger

from app.core.domain.models import CbamRecord
from app.core.domain.ports.excel_parser import ExcelParser
from app.core.domain.ports.record_repository import RecordRepository
from app.core.domain.ports.record_validator import RecordValidator


@dataclass
class UploadResult:
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    errors: list[dict] = field(default_factory=list)


class UploadService:
    def __init__(
        self,
        parser: ExcelParser,
        validator: RecordValidator,
        repository: RecordRepository,
    ):
        self._parser = parser
        self._validator = validator
        self._repository = repository

    async def upload(self, file_path: str) -> UploadResult:
        logger.info("Parsing file: {path}", path=file_path)
        rows = await self._parser.parse(file_path)
        result = UploadResult(total_rows=len(rows))
        logger.info("Parsed {count} rows from file", count=len(rows))

        for i, row in enumerate(rows):
            row_num = i + 1
            errors = await self._validator.validate(row, row_num)
            if errors:
                result.invalid_rows += 1
                result.errors.extend(errors)
                logger.debug(
                    "Row {row_num} invalid: {errors}",
                    row_num=row_num,
                    errors=errors,
                )
            else:
                record = CbamRecord(**row)
                await self._repository.save(record)
                result.valid_rows += 1

        logger.info(
            "Upload complete: {valid} valid, {invalid} invalid out of {total}",
            valid=result.valid_rows,
            invalid=result.invalid_rows,
            total=result.total_rows,
        )
        return result
