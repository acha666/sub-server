from __future__ import annotations

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.utils.url import b64encode_urlsafe_no_padding, encode_fragment, urlencode_items


class ShadowsocksRenderer(ShareLinkRenderer):
    protocol = "shadowsocks"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.method or not server.auth.password:
            raise ValueError(f"server {server.id} missing auth.method/password for shadowsocks")

        userinfo = b64encode_urlsafe_no_padding(f"{server.auth.method}:{server.auth.password}")
        params: list[tuple[str, str]] = []
        plugin = server.options.get("plugin")
        if plugin:
            params.append(("plugin", str(plugin)))

        remark = server.name if not include_key_in_name or not key else f"{server.name} [{key}]"
        query = urlencode_items(params)
        fragment = encode_fragment(remark)
        suffix = f"?{query}" if query else ""
        return (
            f"ss://{userinfo}@{server.endpoint.host}:{server.endpoint.port}"
            f"{suffix}#{fragment}"
        )

