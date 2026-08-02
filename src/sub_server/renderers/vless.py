from __future__ import annotations

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.renderers.common import append_options, common_query_params, display_name
from sub_server.utils.url import encode_fragment, format_uri_host, urlencode_items
from sub_server.utils.validators import inject_vless_route, normalize_uuid


class VlessRenderer(ShareLinkRenderer):
    protocol = "vless"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.uuid:
            raise ValueError(f"server {server.id} missing auth.uuid for vless")

        uuid_value = normalize_uuid(server.auth.uuid)
        if server.routing and server.routing.vless_route is not None:
            uuid_value = inject_vless_route(uuid_value, server.routing.vless_route)

        options = server.options or {}
        encryption = options.get("encryption") or "none"
        params: list[tuple[str, str]] = [("encryption", str(encryption))]

        if options.get("flow"):
            params.append(("flow", str(options["flow"])))
        params.extend(common_query_params(server))
        append_options(params, options, excluded={"encryption", "flow"})
        remark = display_name(server, include_key_in_name, key)
        query = urlencode_items(params)
        fragment = encode_fragment(remark)
        return (
            f"vless://{uuid_value}@{format_uri_host(server.endpoint.host)}:{server.endpoint.port}"
            f"?{query}#{fragment}"
        )
