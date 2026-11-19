from __future__ import annotations

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.renderers.common import append_options, display_name
from sub_server.utils.url import (
    encode_fragment,
    encode_userinfo,
    format_uri_host,
    urlencode_items,
)


class Hysteria2Renderer(ShareLinkRenderer):
    protocol = "hysteria2"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.password:
            raise ValueError(f"server {server.id} missing auth.password for hysteria2")

        params: list[tuple[str, str]] = []
        if server.tls:
            if server.tls.sni:
                params.append(("sni", server.tls.sni))
            if server.tls.insecure is not None:
                params.append(("insecure", "1" if server.tls.insecure else "0"))
        append_options(params, server.options or {})
        remark = display_name(server, include_key_in_name, key)
        query = urlencode_items(params)
        suffix = f"?{query}" if query else ""
        return (
            f"hysteria2://{encode_userinfo(server.auth.password)}@"
            f"{format_uri_host(server.endpoint.host)}:{server.endpoint.port}/"
            f"{suffix}#{encode_fragment(remark)}"
        )
