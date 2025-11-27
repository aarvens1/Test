from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


def _get_env(name: str, default: Optional[str] = None, required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value  # type: ignore[return-value]


def _get_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y"}


@dataclass
class Settings:
    ninja_base_url: str
    ninja_api_key: str

    fresh_base_url: str
    fresh_api_key: str

    asset_default_location: Optional[str]
    asset_source_tag: Optional[str]

    dry_run: bool


def load_settings() -> Settings:
    return Settings(
        ninja_base_url=_get_env("NINJAONE_BASE_URL", required=True),
        ninja_api_key=_get_env("NINJAONE_API_KEY", required=True),
        fresh_base_url=_get_env("FRESHSERVICE_BASE_URL", required=True),
        fresh_api_key=_get_env("FRESHSERVICE_API_KEY", required=True),
        asset_default_location=_get_env("ASSET_DEFAULT_LOCATION", default=None),
        asset_source_tag=_get_env("ASSET_SOURCE_TAG", default=None),
        dry_run=_get_bool("DRY_RUN", default=False),
    )
