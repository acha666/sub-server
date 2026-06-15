from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.renderers.vless import VlessRenderer
from sub_server.services.override import apply_server_patch

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_vless_renderer_injects_route() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    server = apply_server_patch(server, {"routing": {"vless_route": 1}})
    line = VlessRenderer().render(server)
    assert "-0001-" in line
    assert line.startswith("vless://")


def test_vless_renderer_uses_custom_encryption() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    server = apply_server_patch(
        server,
        {
            "options": {
                "encryption": (
                    "mlkem768x25519plus.native.0rtt."
                    "TEST_ONLY_PLACEHOLDER_PUBLIC_KEY"
                )
            }
        },
    )

    line = VlessRenderer().render(server)

    assert "encryption=mlkem768x25519plus.native.0rtt." in line
    assert "TEST_ONLY_PLACEHOLDER_PUBLIC_KEY" in line
    assert "encryption=none" not in line
