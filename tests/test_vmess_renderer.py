import base64
from pathlib import Path

from sub_server.config.loader import ConfigLoader
from sub_server.models.server import ServerConfig
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


def test_vmess_renderer_maps_grpc_fields_and_numeric_values() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "vmess-grpc",
            "enabled": True,
            "protocol": "vmess",
            "name": "VMess gRPC",
            "endpoint": {"host": "example.com", "port": 443},
            "auth": {
                "uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "alterId": 0,
            },
            "transport": {
                "type": "grpc",
                "serviceName": "proxy",
                "authority": "grpc.example.com",
                "mode": "multi",
            },
        }
    )

    payload = VmessRenderer().render(server).removeprefix("vmess://")
    decoded = base64.b64decode(payload).decode("utf-8")

    assert '"port":443' in decoded
    assert '"aid":0' in decoded
    assert '"net":"grpc"' in decoded
    assert '"type":"multi"' in decoded
    assert '"host":"grpc.example.com"' in decoded
    assert '"path":"proxy"' in decoded
