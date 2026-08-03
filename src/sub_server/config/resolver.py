from __future__ import annotations

from collections.abc import Iterable

from sub_server.core.exceptions import ConfigError, SubscriptionKeyNotFoundError
from sub_server.models.keyrule import AnonymousServer, KeyRule
from sub_server.models.server import ServerConfig
from sub_server.services.override import apply_server_patch
from sub_server.services.selector import select_servers_for_key
from sub_server.services.templates import validate_template


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
        self.anonymous_servers: dict[str, list[ServerConfig]] = {}
        self._validate_references()

    def _materialize_anonymous(
        self,
        key_name: str,
        index: int,
        definition: AnonymousServer,
    ) -> ServerConfig:
        server_id = f"{key_name}@{index + 1}"
        if definition.extends:
            base = self.server_map.get(definition.extends)
            if base is None:
                raise ConfigError(
                    f"key '{key_name}' anonymous server references unknown "
                    f"server id '{definition.extends}'"
                )
            return apply_server_patch(base, definition.patch(), server_id=server_id)

        data = definition.patch()
        data["id"] = server_id
        return ServerConfig.model_validate(data)

    def _validate_references(self) -> None:
        if len(self.server_map) != len(self.servers):
            raise ConfigError("duplicate server ids found")
        for server in self.servers:
            try:
                validate_template(server.name)
            except Exception as exc:
                raise ConfigError(f"server '{server.id}' has an invalid name template") from exc

        for key_name, key_rule in self.keys.items():
            try:
                validate_template(key_rule.output.remark_nodes)
            except Exception as exc:
                raise ConfigError(f"key '{key_name}' has invalid remark node templates") from exc

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
                try:
                    server = apply_server_patch(
                        self.server_map[server_id], key_rule.overrides[server_id]
                    )
                    validate_template(server.name)
                except Exception as exc:
                    raise ConfigError(
                        f"key '{key_name}' has an invalid override for server '{server_id}'"
                    ) from exc

            anonymous_servers = []
            for index, definition in enumerate(key_rule.servers):
                try:
                    server = self._materialize_anonymous(key_name, index, definition)
                    validate_template(server.name)
                    anonymous_servers.append(server)
                except ConfigError:
                    raise
                except Exception as exc:
                    raise ConfigError(
                        f"key '{key_name}' has an invalid anonymous server at position {index + 1}"
                    ) from exc
            self.anonymous_servers[key_name] = anonymous_servers

    def resolve_key(self, key: str) -> ResolvedSubscription:
        key_rule = self.keys.get(key)
        if key_rule is None or not key_rule.enabled:
            raise SubscriptionKeyNotFoundError(key)

        selected = select_servers_for_key(self.servers, key_rule.select)
        final_servers = []
        for server in selected:
            override = key_rule.overrides.get(server.id)
            if override:
                final_servers.append(apply_server_patch(server, override))
            else:
                final_servers.append(server)
        final_servers.extend(server for server in self.anonymous_servers[key] if server.enabled)
        return ResolvedSubscription(key=key, key_rule=key_rule, servers=final_servers)
