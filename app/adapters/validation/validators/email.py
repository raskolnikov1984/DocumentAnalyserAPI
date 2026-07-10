import re

from app.adapters.validation.validators.base import BaseValidator

EMAIL_PATTERN = re.compile(r"[^@]+@[^@]+\.[^@]+")


class EmailValidator(BaseValidator):
    def __init__(self, fields: list[str]):
        self._fields = fields

    async def validate(self, row: dict, row_num: int) -> list[dict]:
        errors = []
        for field in self._fields:
            value = row.get(field)
            if not value or not isinstance(value, str):
                continue
            if not EMAIL_PATTERN.match(value):
                errors.append(
                    {
                        "row": row_num,
                        "field": field,
                        "value": value,
                        "message": (
                            f"El campo '{field}' "
                            "no tiene un formato de email valido"
                        ),
                    }
                )
        return errors
