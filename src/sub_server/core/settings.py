from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from sub_server.core.exceptions import ConfigError

DEFAULT_TRUSTED_PROXY_IPS = (
    "127.0.0.1",
    "::1",
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "169.254.0.0/16",
    "fc00::/7",
    "fe80::/10",
)


@dataclass(frozen=True)
class AppSettings:
    title: str = "sub-server"
    config_dir: Path = Path("/config")
    cache_control: str = "no-store"
    host: str = "0.0.0.0"
    port: int = 8000
    trust_proxy_headers: bool = True
    trusted_proxy_ips: tuple[str, ...] = DEFAULT_TRUSTED_PROXY_IPS

    @property
    def forwarded_allow_ips(self) -> str:
        return ",".join(self.trusted_proxy_ips)


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


def load_settings_file(config_dir: Path) -> dict[str, Any]:
    """Load settings from settings.yaml if it exists."""
    settings_file = config_dir / "settings.yaml"
    if not settings_file.exists():
        return {}

    try:
        with settings_file.open(encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
    except Exception as exc:
        raise ConfigError(f"failed to load settings.yaml: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigError("settings.yaml must contain a mapping")
    return data


def _trusted_proxy_ips(settings_data: dict[str, Any]) -> tuple[str, ...]:
    env_value = os.getenv("SUB_SERVER_TRUSTED_PROXY_IPS")
    value = (
        env_value.split(",")
        if env_value is not None
        else settings_data.get("trusted_proxy_ips", DEFAULT_TRUSTED_PROXY_IPS)
    )
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) for item in value):
        raise ConfigError("trusted_proxy_ips must be a list of IP addresses or networks")
    result = tuple(item.strip() for item in value if item.strip())
    if not result:
        raise ConfigError("trusted_proxy_ips may not be empty")
    try:
        for item in result:
            ipaddress.ip_network(item, strict=False)
    except ValueError as exc:
        raise ConfigError(f"invalid trusted proxy address or network: {item}") from exc
    return result


def _trust_proxy_headers(settings_data: dict[str, Any]) -> bool:
    value: Any = os.getenv(
        "SUB_SERVER_TRUST_PROXY_HEADERS",
        settings_data.get("trust_proxy_headers", True),
    )
    if isinstance(value, str):
        normalized = value.strip().casefold()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    if not isinstance(value, bool):
        raise ConfigError("trust_proxy_headers must be a boolean")
    return value


def _port(settings_data: dict[str, Any]) -> int:
    value = os.getenv("SUB_SERVER_PORT", settings_data.get("port", 8000))
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError("port must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ConfigError("port must be in range [1, 65535]")
    return port


def get_settings() -> AppSettings:
    config_dir = resolve_default_config_dir()
    settings_data = load_settings_file(config_dir)
    host = os.getenv("SUB_SERVER_HOST", str(settings_data.get("host", "0.0.0.0"))).strip()
    if not host:
        raise ConfigError("host may not be empty")

    return AppSettings(
        title=str(settings_data.get("title", "sub-server")),
        config_dir=config_dir,
        cache_control=str(settings_data.get("cache_control", "no-store")),
        host=host,
        port=_port(settings_data),
        trust_proxy_headers=_trust_proxy_headers(settings_data),
        trusted_proxy_ips=_trusted_proxy_ips(settings_data),
    )
