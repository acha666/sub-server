from __future__ import annotations

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.utils.url import encode_fragment, urlencode_items
from sub_server.utils.validators import inject_vless_route, normalize_uuid


class VlessRenderer(ShareLinkRenderer):
    protocol = "vless"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.uuid:
            raise ValueError(f"server {server.id} missing auth.uuid for vless")

        uuid_value = normalize_uuid(server.auth.uuid)
        if server.routing and server.routing.vless_route is not None:
            uuid_value = inject_vless_route(uuid_value, server.routing.vless_route)

        params: list[tuple[str, str]] = [("encryption", "none")]

        tls = server.tls
        transport = server.transport
        options = server.options or {}

        if tls and tls.mode:
            params.append(("security", tls.mode))
        if options.get("flow"):
            params.append(("flow", str(options["flow"])))
        if transport and transport.type:
            params.append(("type", transport.type))
        if tls and tls.sni:
            params.append(("sni", tls.sni))
        if transport and transport.host:
            params.append(("host", transport.host))
        if transport and transport.path:
            params.append(("path", transport.path))
        if tls and tls.alpn:
            params.append(("alpn", ",".join(tls.alpn)))
        if tls and tls.fp:
            params.append(("fp", tls.fp))
        if tls and tls.reality and tls.reality.public_key:
            params.append(("pbk", tls.reality.public_key))
        if tls and tls.reality and tls.reality.short_id:
            params.append(("sid", tls.reality.short_id))
        if tls and tls.reality and tls.reality.spider_x:
            params.append(("spx", tls.reality.spider_x))
        if transport and transport.service_name:
            params.append(("serviceName", transport.service_name))
        if transport and transport.authority:
            params.append(("authority", transport.authority))
        if transport and transport.mode:
            params.append(("mode", transport.mode))
        if transport and transport.header_type:
            params.append(("headerType", transport.header_type))

        for key_name in sorted(options.keys()):
            if key_name in {"flow"}:
                continue
            value = options[key_name]
            if value is None or value == "":
                continue
            params.append((key_name, str(value)))

        remark = server.name if not include_key_in_name or not key else f"{server.name} [{key}]"
        query = urlencode_items(params)
        fragment = encode_fragment(remark)
        return (
            f"vless://{uuid_value}@{server.endpoint.host}:{server.endpoint.port}"
            f"?{query}#{fragment}"
        )

