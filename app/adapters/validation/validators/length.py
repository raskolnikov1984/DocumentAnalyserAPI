from app.adapters.validation.validators.base import BaseValidator


class LengthValidator(BaseValidator):
    def __init__(self, fields: dict[str, tuple[int, int]]):
        self._fields = fields

    async def validate(self, row: dict, row_num: int) -> list[dict]:
        errors = []
        for field, (min_len, max_len) in self._fields.items():
            value = row.get(field)
            if value is None:
                continue
            str_value = str(value)
            if len(str_value) < min_len:
                errors.append(
                    {
                        "row": row_num,
                        "field": field,
                        "value": value,
                        "message": f"El campo '{field}' debe tener al menos {min_len} caracteres",
                    }
                )
            elif len(str_value) > max_len:
                errors.append(
                    {
                        "row": row_num,
                        "field": field,
                        "value": value,
                        "message": f"El campo '{field}' debe tener maximo {max_len} caracteres",
                    }
                )
        return errors
