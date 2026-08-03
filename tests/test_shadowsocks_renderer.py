from pathlib import Path
from urllib.parse import urlsplit

from sub_server.config.loader import ConfigLoader
from sub_server.models.server import ServerConfig
from sub_server.renderers.shadowsocks import ShadowsocksRenderer

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_shadowsocks_renderer() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = next(server for server in loader.load_servers().servers if server.id == "us-ss-01")
    line = ShadowsocksRenderer().render(server)
    assert line.startswith("ss://")
    assert "plugin=" in line


def test_shadowsocks_renderer_brackets_ipv6() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "ss-ipv6",
            "enabled": True,
            "protocol": "shadowsocks",
            "name": "SS IPv6",
            "endpoint": {"host": "2001:db8::1", "port": 8388},
            "auth": {"method": "aes-256-gcm", "password": "secret"},
        }
    )

    parsed = urlsplit(ShadowsocksRenderer().render(server))
    assert parsed.hostname == "2001:db8::1"


def test_shadowsocks_2022_uses_plain_sip002_userinfo() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "ss-2022",
            "enabled": True,
            "protocol": "shadowsocks",
            "name": "SS 2022",
            "endpoint": {"host": "example.com", "port": 8388},
            "auth": {
                "method": "2022-blake3-aes-128-gcm",
                "password": "key:with/specials",
            },
        }
    )

    line = ShadowsocksRenderer().render(server)
    assert line.startswith("ss://2022-blake3-aes-128-gcm:key%3Awith%2Fspecials@")
