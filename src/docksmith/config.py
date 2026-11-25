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

    # LLM gateway (Day 8). Keys default to empty so tests and CI never need them.
    gemini_api_key: str = ""
    groq_api_key: str = ""
    llm_primary_model: str = "gemini-3.8-flash"
    llm_fallback_model: str = "openai/gpt-oss-20b"
    # Both providers speak the OpenAI API, so any compatible server works (Ollama, a test fake).
    llm_primary_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai"
    llm_fallback_base_url: str = "https://api.groq.com/openai/v1"
    llm_timeout_seconds: float = 30.0
    usd_inr: float = 95.0  # rupees per US dollar, for cost estimates
    prompts_dir: Path = Path("prompts")

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
