from pathlib import Path

from sub_server.config.loader import ConfigLoader

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_load_example_files() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    servers = loader.load_servers()
    keys = loader.load_keys()

    assert len(servers.servers) == 5
    routed = next(server for server in servers.servers if server.id == "hk-vless-route-14")
    assert routed.endpoint.host == "hk1.example.com"
    assert routed.routing
    assert routed.routing.vless_route == 14
    assert "demo-public" in keys.keys
