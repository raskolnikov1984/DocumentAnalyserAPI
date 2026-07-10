from app.core.exceptions import DomainError, ParseError, ValidationError


def test_domain_error():
    error = DomainError("domain error")
    assert str(error) == "domain error"
    assert isinstance(error, Exception)


def test_parse_error():
    error = ParseError("parse error")
    assert str(error) == "parse error"
    assert isinstance(error, DomainError)


def test_validation_error():
    error = ValidationError(
        "validation error", row=5, field="cn_code", value="abc"
    )
    assert str(error) == "validation error"
    assert error.row == 5
    assert error.field == "cn_code"
    assert error.value == "abc"
    assert isinstance(error, DomainError)


def test_validation_error_defaults():
    error = ValidationError("generic error")
    assert error.row is None
    assert error.field is None
    assert error.value is None
