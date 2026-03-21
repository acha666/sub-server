from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class AppSettings:
    title: str = "sub-server"
    config_dir: Path = Path("/config")
    cache_control: str = "no-store"
    trust_proxy_headers: bool = True


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def resolve_default_config_dir() -> Path:
    explicit = os.getenv("SUB_SERVER_CONFIG_DIR")
    if explicit:
        return Path(explicit)

    container_dir = Path("/config")
    if (container_dir / "servers.yaml").exists() and (container_dir / "keys.yaml").exists():
        return container_dir

    return project_root() / "config" / "examples"


def load_settings_file(config_dir: Path) -> dict:
    """Load settings from settings.yaml if it exists."""
    settings_file = config_dir / "settings.yaml"
    if not settings_file.exists():
        return {}

    try:
        with open(settings_file, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data or {}
    except Exception as e:
        raise ValueError(f"Failed to load settings.yaml: {e}") from e


def get_settings() -> AppSettings:
    config_dir = resolve_default_config_dir()
    settings_data = load_settings_file(config_dir)

    return AppSettings(
        title=settings_data.get("title", "sub-server"),
        config_dir=config_dir,
        cache_control=settings_data.get("cache_control", "no-store"),
        trust_proxy_headers=settings_data.get("trust_proxy_headers", True),
    )


