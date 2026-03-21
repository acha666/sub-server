from __future__ import annotations

from sub_server.models.keyrule import KeySelectConfig
from sub_server.models.server import ServerConfig


def _matches_include(server: ServerConfig, select: KeySelectConfig) -> bool:
    has_include_ids = bool(select.include_ids)
    has_include_tags = bool(select.include_tags)
    if not has_include_ids and not has_include_tags:
        return True
    if server.id in select.include_ids:
        return True
    if set(server.tags).intersection(select.include_tags):
        return True
    return False


def _matches_exclude(server: ServerConfig, select: KeySelectConfig) -> bool:
    if server.id in select.exclude_ids:
        return True
    if set(server.tags).intersection(select.exclude_tags):
        return True
    return False


def select_servers_for_key(
    servers: list[ServerConfig], select: KeySelectConfig
) -> list[ServerConfig]:
    result = []
    for server in servers:
        if not server.enabled:
            continue
        if not _matches_include(server, select):
            continue
        if _matches_exclude(server, select):
            continue
        result.append(server)
    return result

