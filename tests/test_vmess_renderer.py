import base64
from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.renderers.vmess import VmessRenderer

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_vmess_renderer() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[1]
    line = VmessRenderer().render(server)
    assert line.startswith("vmess://")
    payload = line.removeprefix("vmess://")
    decoded = base64.b64decode(payload).decode("utf-8")
    assert '"net":"ws"' in decoded
