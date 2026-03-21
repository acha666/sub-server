import base64
from pathlib import Path

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


def test_render_subscription_raw() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    resolver = ConfigResolver(loader.load_servers().servers, loader.load_keys().keys)
    service = SubscriptionService()

    rendered = service.render_subscription(resolver.resolve_key("demo-private"))
    assert rendered.startswith("trojan://")
