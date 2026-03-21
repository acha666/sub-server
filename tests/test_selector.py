from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.services.selector import select_servers_for_key

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_select_public_servers() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    servers = loader.load_servers().servers
    key_rule = loader.load_keys().keys["demo-public"]

    selected = select_servers_for_key(servers, key_rule.select)
    ids = [server.id for server in selected]
    assert ids == ["hk-vless-01", "jp-vmess-01", "us-ss-01"]
