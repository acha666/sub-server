from __future__ import annotations

from copy import deepcopy
from typing import Any

from sub_server.models.server import ServerConfig
from sub_server.utils.deepmerge import deep_merge
from sub_server.utils.validators import inject_vless_route


def _apply_vless_helper(patch: dict[str, Any]) -> dict[str, Any]:
    patch_copy = deepcopy(patch)
    routing = patch_copy.get("routing")
    auth = patch_copy.get("auth")
    if isinstance(routing, dict) and routing.get("vless_route") is not None:
        route = routing["vless_route"]
        if not isinstance(auth, dict):
            auth = {}
            patch_copy["auth"] = auth
        uuid_value = auth.get("uuid")
        auth["_vless_route_helper"] = route
        if uuid_value is not None:
            auth["uuid"] = inject_vless_route(uuid_value, route)
    return patch_copy


def apply_server_patch(server: ServerConfig, patch: dict[str, Any]) -> ServerConfig:
    base = server.model_dump(by_alias=True, exclude_none=True)
    merged = deep_merge(base, _apply_vless_helper(patch))

    route = merged.get("routing", {}).get("vless_route")
    uuid_value = merged.get("auth", {}).get("uuid")
    if route is not None and uuid_value:
        merged["auth"]["uuid"] = inject_vless_route(uuid_value, route)
        merged["auth"].pop("_vless_route_helper", None)

    return ServerConfig.model_validate(merged)

