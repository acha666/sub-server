from urllib.parse import parse_qs, unquote, urlsplit

import pytest

from sub_server.models.server import ServerConfig
from sub_server.renderers.hysteria2 import Hysteria2Renderer
from sub_server.renderers.registry import RendererRegistry


def server(**changes) -> ServerConfig:
    data = {
        "id": "hy2",
        "enabled": True,
        "protocol": "hysteria2",
        "name": "Hysteria 2",
        "endpoint": {"host": "hy.example.com", "port": 443},
        "auth": {"password": "PA#SS/?@"},
        "tls": {"sni": "hy.example.com", "insecure": False},
        "options": {"pinSHA256": "AB12", "obfs": "salamander", "obfs-password": "OBFS"},
    }
    return ServerConfig.model_validate({**data, **changes})


def test_hysteria2_renderer_writes_the_official_uri() -> None:
    line = RendererRegistry().get("hysteria2").render(server())
    parsed = urlsplit(line)

    assert parsed.scheme == "hysteria2"
    assert unquote(parsed.username or "") == "PA#SS/?@"
    assert (parsed.hostname, parsed.port, parsed.path) == ("hy.example.com", 443, "/")
    assert parse_qs(parsed.query) == {
        "sni": ["hy.example.com"],
        "insecure": ["0"],
        "pinSHA256": ["AB12"],
        "obfs": ["salamander"],
        "obfs-password": ["OBFS"],
    }
    assert unquote(parsed.fragment) == "Hysteria 2"


def test_hysteria2_renderer_brackets_ipv6_and_needs_no_query() -> None:
    line = Hysteria2Renderer().render(
        server(endpoint={"host": "2001:db8::1", "port": 8443}, tls=None, options={})
    )

    assert line.startswith("hysteria2://PA%23SS%2F%3F%40@[2001:db8::1]:8443/#")


def test_hysteria2_requires_a_password() -> None:
    with pytest.raises(ValueError, match="hysteria2 requires auth.password"):
        server(auth={})
