"""
Centralized, environment-driven configuration.

Never hard-code secrets here. Everything that changes between
dev / staging / production comes from environment variables or a
local .env file (see .env.example).
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Clash"
    environment: str = "development"  # development | production
    debug: bool = False

    # SQLite file lives outside the app package so it isn't touched by deploys.
    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/app.db"

    # # Used to sign session-related values. Generate with:
    # #   python -c "import secrets; print(secrets.token_hex(32))"
    # session_secret: str = "DEVELOPMENT"
    # session_cookie_name: str = "session_id"
    # session_max_age_days: int = 14

    static_url: str = "/static"
    media_dir: str = str(BASE_DIR / "media")


@lru_cache
def get_settings() -> Settings:
    # lru_cache means the .env file is only read once per process.
    return Settings()
