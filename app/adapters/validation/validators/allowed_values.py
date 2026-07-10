from app.adapters.validation.validators.base import BaseValidator


class AllowedValuesValidator(BaseValidator):
    def __init__(self, fields: dict[str, set[str]]):
        self._fields = fields

    async def validate(self, row: dict, row_num: int) -> list[dict]:
        errors = []
        for field, allowed in self._fields.items():
            value = row.get(field)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                continue
            if value not in allowed:
                errors.append(
                    {
                        "row": row_num,
                        "field": field,
                        "value": value,
                        "message": f"El campo '{field}' tiene un valor no permitido: '{value}'",
                    }
                )
        return errors
