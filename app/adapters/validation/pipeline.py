from app.adapters.validation.validators.base import BaseValidator
from app.core.domain.ports.record_validator import RecordValidator


class ValidationPipeline(RecordValidator):
    def __init__(self, validators: list[BaseValidator]):
        self._validators = validators

    async def validate(self, row: dict, row_num: int) -> list[dict]:
        errors = []
        for validator in self._validators:
            errors.extend(await validator.validate(row, row_num))
        return errors
