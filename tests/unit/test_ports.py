from app.core.domain.ports.record_repository import RecordRepository
from app.core.domain.ports.excel_parser import ExcelParser
from app.core.domain.ports.record_validator import RecordValidator


def test_record_repository_is_abstract():
    assert RecordRepository.__abstractmethods__


def test_record_repository_methods():
    methods = RecordRepository.__abstractmethods__
    assert "save" in methods
    assert "find_all" in methods
    assert "count" in methods


def test_excel_parser_is_abstract():
    assert ExcelParser.__abstractmethods__


def test_excel_parser_methods():
    assert "parse" in ExcelParser.__abstractmethods__


def test_record_validator_is_abstract():
    assert RecordValidator.__abstractmethods__


def test_record_validator_methods():
    assert "validate" in RecordValidator.__abstractmethods__
