"""Gateway settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _project_root() -> Path:
    """Return the Horizon repository root."""
    return Path(__file__).resolve().parents[4]


class GatewaySettings(BaseSettings):
    """Runtime settings for the local ingestion gateway."""

    storage_path: Path = Field(default_factory=lambda: _project_root() / "storage")

    model_config = SettingsConfigDict(
        env_prefix="HORIZON_GATEWAY_",
        arbitrary_types_allowed=True,
    )


@lru_cache
def get_settings() -> GatewaySettings:
    """Return cached gateway settings."""
    return GatewaySettings()

