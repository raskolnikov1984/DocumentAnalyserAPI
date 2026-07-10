from app.core.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.app_name == "DocumentAnalyserAPI"
    assert settings.database_url == "sqlite+aiosqlite:///./cbam.db"
    assert settings.api_v1_prefix == "/api/v1"


def test_settings_override(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///test.db")
    monkeypatch.setenv("APP_NAME", "TestApp")
    settings = Settings()
    assert settings.database_url == "sqlite+aiosqlite:///test.db"
    assert settings.app_name == "TestApp"
