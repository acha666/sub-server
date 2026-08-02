from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from sub_server.config.loader import ConfigLoader
from sub_server.models.server import ServerConfig
from sub_server.renderers.vless import VlessRenderer
from sub_server.services.override import apply_server_patch

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_vless_renderer_injects_route() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    server = apply_server_patch(server, {"routing": {"vless_route": 1}})
    line = VlessRenderer().render(server)
    assert "-0001-" in line
    assert line.startswith("vless://")


def test_vless_renderer_uses_custom_encryption() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    server = apply_server_patch(
        server,
        {
            "options": {
                "encryption": (
                    "mlkem768x25519plus.native.0rtt."
                    "TEST_ONLY_PLACEHOLDER_PUBLIC_KEY"
                )
            }
        },
    )

    line = VlessRenderer().render(server)

    assert "encryption=mlkem768x25519plus.native.0rtt." in line
    assert "TEST_ONLY_PLACEHOLDER_PUBLIC_KEY" in line
    assert "encryption=none" not in line


def test_vless_renderer_emits_valid_ipv6_url_without_duplicate_fields() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "vless-ipv6",
            "enabled": True,
            "protocol": "vless",
            "name": "VLESS IPv6",
            "endpoint": {"host": "2001:db8::1", "port": 443},
            "auth": {"uuid": "11111111-2222-3333-4444-555555555555"},
            "tls": {"mode": "tls", "sni": "example.com"},
            "transport": {"type": "ws", "host": "cdn.example.com", "path": "/proxy"},
            "options": {"encryption": "none", "sni": "ignored-duplicate"},
        }
    )

    parsed = urlsplit(VlessRenderer().render(server))
    query = parse_qs(parsed.query)

    assert parsed.hostname == "2001:db8::1"
    assert query["sni"] == ["example.com"]
    assert query["path"] == ["/proxy"]
