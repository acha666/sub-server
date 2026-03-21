from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.services.override import apply_server_patch

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_apply_vless_route_patch() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    patched = apply_server_patch(server, {"routing": {"vless_route": 14}})
    assert patched.auth.uuid.split("-")[2] == "000e"
