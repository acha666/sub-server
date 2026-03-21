from __future__ import annotations

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.utils.url import encode_fragment, urlencode_items


class TrojanRenderer(ShareLinkRenderer):
    protocol = "trojan"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.password:
            raise ValueError(f"server {server.id} missing auth.password for trojan")

        params: list[tuple[str, str]] = []
        tls = server.tls
        transport = server.transport
        options = server.options or {}

        if tls and tls.sni:
            params.append(("sni", tls.sni))
        if tls and tls.alpn:
            params.append(("alpn", ",".join(tls.alpn)))
        if tls and tls.fp:
            params.append(("fp", tls.fp))
        if transport and transport.type:
            params.append(("type", transport.type))
        if transport and transport.host:
            params.append(("host", transport.host))
        if transport and transport.path:
            params.append(("path", transport.path))
        for key_name in sorted(options.keys()):
            value = options[key_name]
            if value is None or value == "":
                continue
            params.append((key_name, str(value)))

        remark = server.name if not include_key_in_name or not key else f"{server.name} [{key}]"
        query = urlencode_items(params)
        fragment = encode_fragment(remark)
        suffix = f"?{query}" if query else ""
        return (
            f"trojan://{server.auth.password}@{server.endpoint.host}:{server.endpoint.port}"
            f"{suffix}#{fragment}"
        )

