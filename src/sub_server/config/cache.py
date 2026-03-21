from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.models.keyrule import KeysFile
from sub_server.models.server import ServersFile


@dataclass
class LoadedConfig:
    servers: ServersFile
    keys: KeysFile


class ConfigStore:
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.loader = ConfigLoader(config_dir)
        self._cached: LoadedConfig | None = None
        self._mtimes: tuple[float, float] | None = None

    def _current_mtimes(self) -> tuple[float, float]:
        servers_mtime = (self.config_dir / "servers.yaml").stat().st_mtime
        keys_mtime = (self.config_dir / "keys.yaml").stat().st_mtime
        return servers_mtime, keys_mtime

    def get(self) -> LoadedConfig:
        mtimes = self._current_mtimes()
        if self._cached is None or self._mtimes != mtimes:
            self._cached = LoadedConfig(
                servers=self.loader.load_servers(),
                keys=self.loader.load_keys(),
            )
            self._mtimes = mtimes
        return self._cached

