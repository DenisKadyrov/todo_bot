from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ValidationInfo, field_validator
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None
    

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(
        cls,
        v: str | None,
        info: ValidationInfo,
    ) -> str | PostgresDsn:
        if isinstance(v, str) and v:
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
    )


settings = Settings()
