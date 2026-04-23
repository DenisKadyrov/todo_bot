import importlib
import sys


def test_database_uri_is_built_from_postgres_settings(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("POSTGRES_SERVER", "localhost")
    monkeypatch.setenv("POSTGRES_USER", "admin")
    monkeypatch.setenv("POSTGRES_PASSWORD", "Passw0rd")
    monkeypatch.setenv("POSTGRES_DB", "tasks")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.delenv("SQLALCHEMY_DATABASE_URI", raising=False)

    sys.modules.pop("config", None)
    config = importlib.import_module("config")

    settings = config.Settings(_env_file=None)

    assert str(settings.SQLALCHEMY_DATABASE_URI) == (
        "postgresql+asyncpg://admin:Passw0rd@localhost:5433/tasks"
    )


def test_explicit_database_uri_has_priority(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("POSTGRES_SERVER", "localhost")
    monkeypatch.setenv("POSTGRES_USER", "admin")
    monkeypatch.setenv("POSTGRES_PASSWORD", "Passw0rd")
    monkeypatch.setenv("POSTGRES_DB", "tasks")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.setenv(
        "SQLALCHEMY_DATABASE_URI",
        "postgresql+asyncpg://custom:secret@db:5432/custom_db",
    )

    sys.modules.pop("config", None)
    config = importlib.import_module("config")

    settings = config.Settings(_env_file=None)

    assert str(settings.SQLALCHEMY_DATABASE_URI) == (
        "postgresql+asyncpg://custom:secret@db:5432/custom_db"
    )
