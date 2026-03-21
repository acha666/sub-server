from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.renderers.shadowsocks import ShadowsocksRenderer

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_shadowsocks_renderer() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[3]
    line = ShadowsocksRenderer().render(server)
    assert line.startswith("ss://")
    assert "plugin=" in line
