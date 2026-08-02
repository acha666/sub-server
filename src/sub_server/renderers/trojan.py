from __future__ import annotations

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.renderers.common import append_options, common_query_params, display_name
from sub_server.utils.url import (
    encode_fragment,
    encode_userinfo,
    format_uri_host,
    urlencode_items,
)


class TrojanRenderer(ShareLinkRenderer):
    protocol = "trojan"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.password:
            raise ValueError(f"server {server.id} missing auth.password for trojan")

        params = common_query_params(server)
        options = server.options or {}

        append_options(params, options)
        remark = display_name(server, include_key_in_name, key)
        query = urlencode_items(params)
        fragment = encode_fragment(remark)
        suffix = f"?{query}" if query else ""
        return (
            f"trojan://{encode_userinfo(server.auth.password)}@"
            f"{format_uri_host(server.endpoint.host)}:{server.endpoint.port}"
            f"{suffix}#{fragment}"
        )
