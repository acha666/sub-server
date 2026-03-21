from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.renderers.trojan import TrojanRenderer

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_trojan_renderer() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[2]
    line = TrojanRenderer().render(server)
    assert line.startswith("trojan://")
    assert "sni=sg.example.com" in line
