from __future__ import annotations

from typing import Any

from sub_server.core.exceptions import ConfigError
from sub_server.models.server import ServerConfig, ServerDefinition
from sub_server.utils.deepmerge import deep_merge


def apply_server_patch(
    server: ServerConfig,
    patch: dict[str, Any],
    *,
    server_id: str | None = None,
) -> ServerConfig:
    base = server.model_dump(by_alias=True, exclude_none=True)
    merged = deep_merge(base, patch)
    merged["id"] = server_id or server.id
    return ServerConfig.model_validate(merged)


def resolve_server_definitions(
    definitions: list[ServerDefinition],
) -> list[ServerConfig]:
    definition_map: dict[str, ServerDefinition] = {}
    for definition in definitions:
        if definition.id in definition_map:
            raise ConfigError(f"duplicate server id '{definition.id}'")
        definition_map[definition.id] = definition

    resolved: dict[str, ServerConfig] = {}
    resolving: list[str] = []

    def resolve(server_id: str) -> ServerConfig:
        if server_id in resolved:
            return resolved[server_id]
        definition = definition_map.get(server_id)
        if definition is None:
            raise ConfigError(f"unknown server id '{server_id}'")
        if server_id in resolving:
            cycle = " -> ".join([*resolving, server_id])
            raise ConfigError(f"server inheritance cycle: {cycle}")

        resolving.append(server_id)
        try:
            if definition.extends:
                server = apply_server_patch(
                    resolve(definition.extends),
                    definition.patch(),
                    server_id=definition.id,
                )
            else:
                data = definition.model_dump(by_alias=True, exclude_unset=True)
                data.pop("extends", None)
                server = ServerConfig.model_validate(data)
        except ConfigError:
            raise
        except Exception as exc:
            raise ConfigError(f"invalid server '{server_id}': {exc}") from exc
        finally:
            resolving.pop()
        resolved[server_id] = server
        return server

    return [resolve(definition.id) for definition in definitions]
