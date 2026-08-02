from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from sub_server.config.loader import ConfigLoader
from sub_server.models.server import ServerConfig
from sub_server.renderers.trojan import TrojanRenderer

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_trojan_renderer() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[2]
    line = TrojanRenderer().render(server)
    assert line.startswith("trojan://")
    assert "security=tls" in line
    assert "sni=sg.example.com" in line


def test_trojan_renderer_encodes_password_ipv6_and_grpc() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "trojan-ipv6",
            "enabled": True,
            "protocol": "trojan",
            "name": "Trojan IPv6",
            "endpoint": {"host": "2001:db8::1", "port": 443},
            "auth": {"password": "pa#ss/?@"},
            "tls": {"mode": "tls", "insecure": False},
            "transport": {
                "type": "grpc",
                "serviceName": "proxy service",
                "authority": "grpc.example.com",
                "mode": "gun",
            },
        }
    )

    parsed = urlsplit(TrojanRenderer().render(server))
    query = parse_qs(parsed.query)

    assert parsed.hostname == "2001:db8::1"
    assert unquote(parsed.username or "") == "pa#ss/?@"
    assert parsed.fragment == "Trojan%20IPv6"
    assert query["security"] == ["tls"]
    assert query["serviceName"] == ["proxy service"]
    assert "serviceName=proxy%20service" in parsed.query
    assert query["authority"] == ["grpc.example.com"]
    assert query["insecure"] == ["0"]
