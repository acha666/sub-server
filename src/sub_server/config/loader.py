from __future__ import annotations

from pathlib import Path

import yaml

from sub_server.core.exceptions import ConfigError
from sub_server.models.keyrule import KeysFile
from sub_server.models.server import ServerDefinition, ServersFile
from sub_server.services.override import resolve_server_definitions


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
            data = self._read_yaml("servers.yaml")
            raw_servers = data.get("servers")
            if not isinstance(raw_servers, list):
                raise ValueError("servers must be a list")
            definitions = [
                ServerDefinition.model_validate(definition) for definition in raw_servers
            ]
            return ServersFile(servers=resolve_server_definitions(definitions))
        except Exception as exc:  # noqa: BLE001
            raise ConfigError(f"failed to load servers.yaml: {exc}") from exc

    def load_keys(self) -> KeysFile:
        try:
            return KeysFile.model_validate(self._read_yaml("keys.yaml"))
        except Exception as exc:  # noqa: BLE001
            raise ConfigError(f"failed to load keys.yaml: {exc}") from exc
