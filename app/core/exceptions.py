class DomainError(Exception):
    pass


class ParseError(DomainError):
    pass


class ValidationError(DomainError):
    def __init__(
        self,
        message: str,
        row: int | None = None,
        field: str | None = None,
        value: str | None = None,
    ):
        self.row = row
        self.field = field
        self.value = value
        super().__init__(message)
