from pathlib import Path

from sub_server.config.loader import ConfigLoader

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_load_example_files() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    servers = loader.load_servers()
    keys = loader.load_keys()

    assert len(servers.servers) == 4
    assert "demo-public" in keys.keys
