from __future__ import annotations

from collections.abc import Iterable

from sub_server.core.exceptions import ConfigError, SubscriptionKeyNotFoundError
from sub_server.models.keyrule import KeyRule
from sub_server.models.server import ServerConfig
from sub_server.services.override import apply_server_patch
from sub_server.services.selector import select_servers_for_key


class ResolvedSubscription:
    def __init__(self, key: str, key_rule: KeyRule, servers: list[ServerConfig]):
        self.key = key
        self.key_rule = key_rule
        self.servers = servers


class ConfigResolver:
    def __init__(self, servers: Iterable[ServerConfig], keys: dict[str, KeyRule]):
        self.servers = list(servers)
        self.keys = keys
        self.server_map = {server.id: server for server in self.servers}
        self._validate_references()

    def _validate_references(self) -> None:
        if len(self.server_map) != len(self.servers):
            raise ConfigError("duplicate server ids found")
        for key_name, key_rule in self.keys.items():
            for server_id in key_rule.select.include_ids + key_rule.select.exclude_ids:
                if server_id not in self.server_map:
                    raise ConfigError(
                        f"key '{key_name}' references unknown server id '{server_id}'"
                    )
            for server_id in key_rule.overrides:
                if server_id not in self.server_map:
                    raise ConfigError(
                        f"key '{key_name}' override references unknown server id '{server_id}'"
                    )

    def resolve_key(self, key: str) -> ResolvedSubscription:
        key_rule = self.keys.get(key)
        if key_rule is None or not key_rule.enabled:
            raise SubscriptionKeyNotFoundError(key)

        selected = select_servers_for_key(self.servers, key_rule.select)
        final_servers = []
        for server in selected:
            override = key_rule.overrides.get(server.id)
            if override:
                final_servers.append(apply_server_patch(server, override.patch))
            else:
                final_servers.append(server)
        return ResolvedSubscription(key=key, key_rule=key_rule, servers=final_servers)

