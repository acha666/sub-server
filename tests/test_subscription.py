import base64
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

from sub_server.config.loader import ConfigLoader
from sub_server.config.resolver import ConfigResolver
from sub_server.services.subscription import SubscriptionService

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_render_subscription_base64() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    resolver = ConfigResolver(loader.load_servers().servers, loader.load_keys().keys)
    service = SubscriptionService()

    rendered = service.render_subscription(resolver.resolve_key("demo-public"))
    decoded = base64.b64decode(rendered).decode("utf-8")

    assert "vless://" in decoded
    assert "vmess://" in decoded
    assert "ss://" in decoded
    lines = decoded.splitlines()
    assert unquote(urlsplit(lines[0]).fragment) == "Public demo"
    assert unquote(urlsplit(lines[1]).fragment).startswith("Updated ")


def test_remark_nodes_and_server_names_share_template_variables() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    resolver = ConfigResolver(loader.load_servers().servers, loader.load_keys().keys)
    service = SubscriptionService()

    lines = service.render_lines(
        resolver.resolve_key("demo-public"),
        now=datetime(2026, 8, 3, 12, 34, tzinfo=UTC),
    )

    assert lines[0].startswith("vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1")
    assert unquote(urlsplit(lines[0]).fragment) == "Public demo"
    vmess_line = next(line for line in lines if line.startswith("vmess://"))
    payload = vmess_line.removeprefix("vmess://")
    assert "JP VMess Public demo" in base64.b64decode(payload).decode("utf-8")


def test_render_subscription_raw() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    resolver = ConfigResolver(loader.load_servers().servers, loader.load_keys().keys)
    service = SubscriptionService()

    rendered = service.render_subscription(resolver.resolve_key("demo-private"))
    assert rendered.count("trojan://") == 2
