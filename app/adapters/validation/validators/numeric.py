from app.adapters.validation.validators.base import BaseValidator


class PositiveNumericValidator(BaseValidator):
    def __init__(self, fields: list[str]):
        self._fields = fields

    async def validate(self, row: dict, row_num: int) -> list[dict]:
        errors = []
        for field in self._fields:
            value = row.get(field)
            if value is None:
                continue
            try:
                num = float(value)
                if num <= 0:
                    errors.append(
                        {
                            "row": row_num,
                            "field": field,
                            "value": value,
                            "message": (
                                f"El campo '{field}' "
                                "debe ser un numero positivo"
                            ),
                        }
                    )
            except ValueError, TypeError:
                errors.append(
                    {
                        "row": row_num,
                        "field": field,
                        "value": value,
                        "message": (
                            f"El campo '{field}' debe ser un numero valido"
                        ),
                    }
                )
        return errors
