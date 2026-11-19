import pytest

from sub_server.config.xray import server_from_outbound
from sub_server.models.server import ServerConfig, ServerDefinition
from sub_server.renderers.registry import RendererRegistry
from sub_server.services.override import apply_server_patch, resolve_server_definitions

REALITY = {
    "fingerprint": "chrome",
    "serverName": "www.example.com",
    "publicKey": "PUBLIC",
    "shortId": "0a1b",
}
VLESS = {
    "protocol": "vless",
    "settings": {
        "address": "entry.example.com",
        "port": 443,
        "id": "11111111-2222-0000-3333-444444444444",
        "encryption": "none",
        "flow": "xtls-rprx-vision",
    },
    "streamSettings": {
        "network": "xhttp",
        "security": "reality",
        "realitySettings": {**REALITY, "spiderX": "/spider", "mldsa65Verify": "VERIFY"},
        "xhttpSettings": {"path": "/path", "mode": "auto"},
    },
}
HYSTERIA = {
    "protocol": "hysteria",
    "settings": {"version": 2, "address": "hy.example.com", "port": 443},
    "streamSettings": {
        "network": "hysteria",
        "security": "tls",
        "tlsSettings": {
            "serverName": "hy.example.com",
            "alpn": ["h3"],
            "pinnedPeerCertSha256": "AB12",
        },
        "hysteriaSettings": {"version": 2, "auth": "PASSWORD"},
        "finalmask": {"udp": [{"type": "salamander", "settings": {"password": "OBFS"}}]},
    },
}


def test_vless_outbound_gives_every_link_field() -> None:
    assert server_from_outbound(VLESS) == {
        "protocol": "vless",
        "endpoint": {"host": "entry.example.com", "port": 443},
        "auth": {"uuid": "11111111-2222-0000-3333-444444444444"},
        "tls": {
            "mode": "reality",
            "sni": "www.example.com",
            "fp": "chrome",
            "reality": {"public_key": "PUBLIC", "short_id": "0a1b", "spider_x": "/spider"},
        },
        "transport": {"type": "xhttp", "path": "/path", "mode": "auto"},
        "options": {"encryption": "none", "flow": "xtls-rprx-vision", "pqv": "VERIFY"},
    }


def test_raw_outbound_without_stream_settings_is_tcp() -> None:
    relay = {
        "protocol": "vless",
        "settings": {"address": "relay.example.com", "port": 15861, "encryption": "PRIVATE"},
    }

    assert server_from_outbound(relay) == {
        "protocol": "vless",
        "endpoint": {"host": "relay.example.com", "port": 15861},
        "transport": {"type": "tcp"},
        "options": {"encryption": "PRIVATE"},
    }


def test_hysteria_outbound_becomes_hysteria2() -> None:
    assert server_from_outbound(HYSTERIA) == {
        "protocol": "hysteria2",
        "endpoint": {"host": "hy.example.com", "port": 443},
        "auth": {"password": "PASSWORD"},
        "tls": {"sni": "hy.example.com", "alpn": ["h3"]},
        "options": {"pinSHA256": "AB12", "obfs": "salamander", "obfs-password": "OBFS"},
    }


def test_a_server_is_its_outbound_with_the_written_fields_on_top() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "entry",
            "enabled": True,
            "name": "Entry",
            "outbound": VLESS,
            "transport": {"headerType": "none"},
            "routing": {"vless_route": 14},
        }
    )

    assert server.protocol == "vless"
    assert server.transport is not None
    assert (server.transport.type, server.transport.header_type) == ("xhttp", "none")
    assert "outbound" not in server.model_dump()
    line = RendererRegistry().get("vless").render(server)
    assert line.startswith("vless://11111111-2222-000e-3333-444444444444@entry.example.com:443?")
    assert "type=xhttp" in line and "pbk=PUBLIC" in line and "pqv=VERIFY" in line


def test_definitions_and_patches_read_outbounds() -> None:
    servers = resolve_server_definitions(
        [
            ServerDefinition.model_validate(
                {"id": "hy", "enabled": True, "name": "Hy", "outbound": HYSTERIA}
            ),
            ServerDefinition.model_validate({"id": "hy-user", "extends": "hy", "name": "User"}),
        ]
    )

    assert [server.protocol for server in servers] == ["hysteria2", "hysteria2"]
    assert servers[1].auth.password == "PASSWORD"
    # A patch may replace the server by another outbound and still set single fields.
    patched = apply_server_patch(servers[0], {"outbound": VLESS, "name": "Now VLESS"})
    assert (patched.protocol, patched.endpoint.host, patched.name) == (
        "vless",
        "entry.example.com",
        "Now VLESS",
    )


@pytest.mark.parametrize(
    "outbound",
    [
        "not-an-object",
        {"protocol": "wireguard", "settings": {"address": "a.example.com", "port": 1}},
        {"protocol": "vless", "settings": {"port": 443}},
    ],
)
def test_unusable_outbounds_are_rejected(outbound) -> None:
    with pytest.raises(ValueError):
        server_from_outbound(outbound)
