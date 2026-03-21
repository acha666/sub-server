from __future__ import annotations

import base64
import json

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.utils.validators import normalize_uuid


class VmessRenderer(ShareLinkRenderer):
    protocol = "vmess"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.uuid:
            raise ValueError(f"server {server.id} missing auth.uuid for vmess")

        remark = server.name if not include_key_in_name or not key else f"{server.name} [{key}]"
        transport = server.transport
        tls = server.tls

        obj = {
            "v": "2",
            "ps": remark,
            "add": server.endpoint.host,
            "port": str(server.endpoint.port),
            "id": normalize_uuid(server.auth.uuid),
            "aid": str(server.auth.alter_id or 0),
            "scy": server.options.get("scy", "auto"),
            "net": transport.type if transport and transport.type else "tcp",
            "type": transport.header_type if transport and transport.header_type else "none",
            "host": transport.host if transport and transport.host else "",
            "path": transport.path if transport and transport.path else "",
            "tls": tls.mode if tls and tls.mode else "",
            "sni": tls.sni if tls and tls.sni else "",
            "alpn": ",".join(tls.alpn) if tls and tls.alpn else "",
            "fp": tls.fp if tls and tls.fp else "",
        }
        raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        encoded = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        return f"vmess://{encoded}"

