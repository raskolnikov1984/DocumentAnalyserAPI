import re

from app.adapters.validation.validators.base import BaseValidator

CONTACT_METHOD = re.compile(r"[^@]+@[^@]+\.[^@]+|\+\d[\d\s\-\(\)]+|\d{3,}[\d\s\-\(\)]+")


class ContactPersonValidator(BaseValidator):
    async def validate(self, row: dict, row_num: int) -> list[dict]:
        value = row.get("contact_person")
        if not value:
            return []
        if not CONTACT_METHOD.search(str(value)):
            return [
                {
                    "row": row_num,
                    "field": "contact_person",
                    "value": value,
                    "message": "Contact Person debe incluir nombre y al menos un metodo de contacto (email o telefono)",
                }
            ]
        return []
