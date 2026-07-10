from app.adapters.validation.validators.base import BaseValidator


class RequiredValidator(BaseValidator):
    def __init__(self, fields: list[str]):
        self._fields = fields

    async def validate(self, row: dict, row_num: int) -> list[dict]:
        errors = []
        for field in self._fields:
            value = row.get(field)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                errors.append(
                    {
                        "row": row_num,
                        "field": field,
                        "value": value,
                        "message": f"El campo '{field}' es requerido",
                    }
                )
        return errors
