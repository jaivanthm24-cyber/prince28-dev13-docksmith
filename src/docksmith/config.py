"""All settings come from environment variables (or a local .env file)."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from docksmith.db.url import to_asyncpg_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "docksmith"
    # No default on purpose: if APP_ENV is missing, the app refuses to start.
    app_env: Literal["local", "ci", "production"]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    data_file: Path = Path("data/sample_records.json")
    database_url: str = "postgresql+asyncpg://localhost:5432/docksmith"
    git_sha: str = "development"

    @field_validator("database_url", mode="before")
    @classmethod
    def _normalize_db_url(cls, v: str) -> str:
        return to_asyncpg_url(v)

    @field_validator("git_sha", mode="before")
    @classmethod
    def _resolve_git_sha(cls, v: str | None) -> str:
        if not v or v == "development":
            render_commit = os.getenv("RENDER_GIT_COMMIT")
            if render_commit:
                return render_commit
        return v or "development"


@lru_cache
def get_settings() -> Settings:
    """Build the settings once and reuse them."""
    return Settings()
