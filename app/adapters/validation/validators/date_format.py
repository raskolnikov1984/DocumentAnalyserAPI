import re

from app.adapters.validation.validators.base import BaseValidator

DATE_PATTERN = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")


class DateFormatValidator(BaseValidator):
    async def validate(self, row: dict, row_num: int) -> list[dict]:
        value = row.get("date_of_importation")
        if not value:
            return []
        if not DATE_PATTERN.match(str(value)):
            return [
                {
                    "row": row_num,
                    "field": "date_of_importation",
                    "value": value,
                    "message": "Date of importation debe tener formato DD.MM.YYYY",
                }
            ]
        return []
