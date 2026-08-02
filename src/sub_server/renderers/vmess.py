from __future__ import annotations

import base64
import json

from sub_server.models.server import ServerConfig
from sub_server.renderers.base import ShareLinkRenderer
from sub_server.renderers.common import display_name
from sub_server.utils.url import normalize_host
from sub_server.utils.validators import normalize_uuid


class VmessRenderer(ShareLinkRenderer):
    protocol = "vmess"

    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        if not server.auth.uuid:
            raise ValueError(f"server {server.id} missing auth.uuid for vmess")

        remark = display_name(server, include_key_in_name, key)
        transport = server.transport
        tls = server.tls
        configured_transport = transport.type if transport and transport.type else "tcp"
        transport_type = "tcp" if configured_transport == "raw" else configured_transport
        if transport_type == "grpc":
            type_value = transport.mode if transport and transport.mode else "gun"
            host = transport.authority if transport and transport.authority else ""
            path = transport.service_name if transport and transport.service_name else ""
        else:
            type_value = (
                transport.mode
                if transport_type == "xhttp" and transport and transport.mode
                else transport.header_type
                if transport and transport.header_type
                else "none"
            )
            host = transport.host if transport and transport.host else ""
            path = transport.path if transport and transport.path else ""
            if transport_type == "kcp" and server.options.get("seed"):
                path = str(server.options["seed"])

        obj = {
            "v": 2,
            "ps": remark,
            "add": normalize_host(server.endpoint.host),
            "port": server.endpoint.port,
            "id": normalize_uuid(server.auth.uuid),
            "aid": server.auth.alter_id or 0,
            "scy": str(server.options.get("scy", "auto")),
            "net": transport_type,
            "type": type_value,
            "host": host,
            "path": path,
            "tls": tls.mode if tls and tls.mode else "",
            "sni": tls.sni if tls and tls.sni else "",
            "alpn": ",".join(tls.alpn) if tls and tls.alpn else "",
            "fp": tls.fp if tls and tls.fp else "",
            "insecure": "1" if tls and tls.insecure else "0",
        }
        raw = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
        encoded = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        return f"vmess://{encoded}"
