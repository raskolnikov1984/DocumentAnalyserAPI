import re

from app.adapters.validation.validators.base import BaseValidator

EORI_PATTERN = re.compile(r"^[A-Z]{2}[A-Z0-9]{1,15}$")


class EoriValidator(BaseValidator):
    async def validate(self, row: dict, row_num: int) -> list[dict]:
        value = row.get("eori_number")
        if not value:
            return []
        if not EORI_PATTERN.match(str(value)):
            return [
                {
                    "row": row_num,
                    "field": "eori_number",
                    "value": value,
                    "message": "EORI Number debe ser 2 letras de pais + hasta 15 caracteres alfanumericos",
                }
            ]
        return []
