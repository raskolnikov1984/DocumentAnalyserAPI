import re

from app.adapters.validation.validators.base import BaseValidator

CN_CODE_PATTERN = re.compile(r"^\d{8}$")


class CnCodeValidator(BaseValidator):
    async def validate(self, row: dict, row_num: int) -> list[dict]:
        value = row.get("cn_code")
        if not value:
            return []
        if not CN_CODE_PATTERN.match(str(value)):
            return [
                {
                    "row": row_num,
                    "field": "cn_code",
                    "value": value,
                    "message": "CN Code debe tener exactamente 8 digitos numericos",
                }
            ]
        return []
