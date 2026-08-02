from __future__ import annotations

from typing import Any

from sub_server.models.server import ServerConfig


def display_name(server: ServerConfig, include_key: bool, key: str) -> str:
    return f"{server.name} [{key}]" if include_key and key else server.name


def common_query_params(server: ServerConfig) -> list[tuple[str, str]]:
    params: list[tuple[str, str]] = []
    tls = server.tls
    transport = server.transport

    if tls:
        if tls.mode:
            params.append(("security", tls.mode))
        if tls.sni:
            params.append(("sni", tls.sni))
        if tls.alpn:
            params.append(("alpn", ",".join(tls.alpn)))
        if tls.fp:
            params.append(("fp", tls.fp))
        if tls.reality:
            if tls.reality.public_key:
                params.append(("pbk", tls.reality.public_key))
            if tls.reality.short_id:
                params.append(("sid", tls.reality.short_id))
            if tls.reality.spider_x:
                params.append(("spx", tls.reality.spider_x))
        if tls.insecure is not None:
            insecure = "1" if tls.insecure else "0"
            params.extend((("insecure", insecure), ("allowInsecure", insecure)))

    if transport:
        transport_type = "tcp" if transport.type == "raw" else transport.type
        fields = (
            ("type", transport_type),
            ("host", transport.host),
            ("path", transport.path),
            ("serviceName", transport.service_name),
            ("authority", transport.authority),
            ("mode", transport.mode),
            ("headerType", transport.header_type),
        )
        params.extend((name, value) for name, value in fields if value)

    return params


def append_options(
    params: list[tuple[str, str]],
    options: dict[str, Any],
    *,
    excluded: set[str] | None = None,
) -> None:
    reserved = {name for name, _ in params}
    reserved.update(excluded or ())
    for name in sorted(options):
        value = options[name]
        if name in reserved or value is None or value == "":
            continue
        params.append((name, str(value).lower() if isinstance(value, bool) else str(value)))
