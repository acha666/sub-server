"""Read a server from an Xray outbound, so one definition serves Xray and the subscriptions."""

from __future__ import annotations

from typing import Any

from sub_server.utils.deepmerge import deep_merge

JsonMap = dict[str, Any]

# Xray outbound protocol to the protocol of the share link.
PROTOCOLS = {
    "vless": "vless",
    "vmess": "vmess",
    "trojan": "trojan",
    "shadowsocks": "shadowsocks",
    "hysteria": "hysteria2",
}
REALITY_FIELDS = {"publicKey": "public_key", "shortId": "short_id", "spiderX": "spider_x"}


def _without_empty(data: JsonMap) -> JsonMap:
    return {name: value for name, value in data.items() if value not in (None, "", [], {})}


def _tls(stream: JsonMap) -> JsonMap:
    security = stream.get("security")
    if security == "reality":
        reality = stream.get("realitySettings") or {}
        return _without_empty(
            {
                "mode": security,
                "sni": reality.get("serverName"),
                "fp": reality.get("fingerprint"),
                "reality": _without_empty(
                    {new: reality.get(old) for old, new in REALITY_FIELDS.items()}
                ),
            }
        )
    if security == "tls":
        tls = stream.get("tlsSettings") or {}
        return _without_empty(
            {
                "mode": security,
                "sni": tls.get("serverName"),
                "fp": tls.get("fingerprint"),
                "alpn": tls.get("alpn"),
                "insecure": tls.get("allowInsecure"),
            }
        )
    return {}


def _transport(stream: JsonMap) -> JsonMap:
    network = stream.get("network") or stream.get("method") or "raw"
    settings = stream.get(f"{network}Settings") or {}
    return _without_empty(
        {
            "type": "tcp" if network == "raw" else network,
            "host": settings.get("host"),
            "path": settings.get("path"),
            "mode": settings.get("mode"),
            "serviceName": settings.get("serviceName"),
            "authority": settings.get("authority"),
        }
    )


def _pin(tls: JsonMap) -> str | None:
    pin = tls.get("pinnedPeerCertSha256")
    if isinstance(pin, list):
        return pin[0] if pin else None
    return pin


def _salamander(stream: JsonMap) -> JsonMap:
    for mask in (stream.get("finalmask") or {}).get("udp") or []:
        if mask.get("type") == "salamander":
            password = (mask.get("settings") or {}).get("password")
            return {"obfs": "salamander", "obfs-password": password}
    return {}


def server_from_outbound(outbound: Any) -> JsonMap:
    """Return the server fields that an Xray outbound describes."""
    if not isinstance(outbound, dict):
        raise ValueError("outbound must be an Xray outbound object")
    protocol = PROTOCOLS.get(outbound.get("protocol"))
    if protocol is None:
        raise ValueError(f"unsupported Xray outbound protocol: {outbound.get('protocol')!r}")
    settings = outbound.get("settings") or {}
    stream = outbound.get("streamSettings") or {}
    if "address" not in settings or "port" not in settings:
        raise ValueError("outbound.settings needs address and port")

    server: JsonMap = {
        "protocol": protocol,
        "endpoint": {"host": settings["address"], "port": settings["port"]},
    }
    tls = _tls(stream)
    if protocol == "hysteria2":
        hysteria = stream.get("hysteriaSettings") or {}
        auth = {"password": hysteria.get("auth")}
        # The certificate is part of the protocol: TLS needs no mode and the pin is a query field.
        tls.pop("mode", None)
        tls.pop("fp", None)
        options = {"pinSHA256": _pin(stream.get("tlsSettings") or {}), **_salamander(stream)}
    else:
        auth = {
            "uuid": settings.get("id"),
            "password": settings.get("password"),
            "method": settings.get("method"),
        }
        options = {"encryption": settings.get("encryption"), "flow": settings.get("flow")}
        if protocol == "vless":
            reality = stream.get("realitySettings") or {}
            options["pqv"] = reality.get("mldsa65Verify")
        server["transport"] = _transport(stream)
    parts = {"auth": _without_empty(auth), "tls": tls, "options": _without_empty(options)}
    server.update(_without_empty(parts))
    return server


def expand_outbound(data: JsonMap) -> JsonMap:
    """Replace `outbound` in a server definition by the fields it describes; written fields win."""
    if "outbound" not in data:
        return data
    written = {name: value for name, value in data.items() if name != "outbound"}
    return deep_merge(server_from_outbound(data["outbound"]), written)
