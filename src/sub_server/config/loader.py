from __future__ import annotations

from pathlib import Path

import yaml

from sub_server.core.exceptions import ConfigError
from sub_server.models.keyrule import KeysFile
from sub_server.models.server import ServersFile


class ConfigLoader:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir

    def _read_yaml(self, filename: str) -> dict:
        path = self.config_dir / filename
        if not path.exists():
            raise ConfigError(f"missing config file: {path}")
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ConfigError(f"config file must contain a mapping: {path}")
        return data

    def load_servers(self) -> ServersFile:
        try:
            return ServersFile.model_validate(self._read_yaml("servers.yaml"))
        except Exception as exc:  # noqa: BLE001
            raise ConfigError(f"failed to load servers.yaml: {exc}") from exc

    def load_keys(self) -> KeysFile:
        try:
            return KeysFile.model_validate(self._read_yaml("keys.yaml"))
        except Exception as exc:  # noqa: BLE001
            raise ConfigError(f"failed to load keys.yaml: {exc}") from exc

