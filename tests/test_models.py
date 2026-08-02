import pytest
from pydantic import ValidationError

from sub_server.models.keyrule import KeyRule, KeysFile
from sub_server.models.server import ServerConfig


def test_enabled_is_required_for_keys_and_servers() -> None:
    with pytest.raises(ValidationError):
        KeyRule.model_validate({"enable": False})

    with pytest.raises(ValidationError):
        ServerConfig.model_validate(
            {
                "id": "server",
                "protocol": "trojan",
                "name": "Server",
                "endpoint": {"host": "example.com", "port": 443},
                "auth": {"password": "secret"},
            }
        )


@pytest.mark.parametrize("key", ["healthz", "DOCS", "redoc", "openapi.json", ".", "..", " key"])
def test_reserved_or_ambiguous_keys_are_rejected(key: str) -> None:
    with pytest.raises(ValidationError):
        KeysFile.model_validate({"keys": {key: {"enabled": True}}})


def test_protocol_credentials_and_endpoint_port_are_validated() -> None:
    with pytest.raises(ValidationError):
        ServerConfig.model_validate(
            {
                "id": "server",
                "enabled": True,
                "protocol": "vless",
                "name": "Server",
                "endpoint": {"host": "example.com", "port": 0},
                "auth": {},
            }
        )


def test_vless_route_is_normalized_during_config_validation() -> None:
    server = ServerConfig.model_validate(
        {
            "id": "server",
            "enabled": True,
            "protocol": "vless",
            "name": "Server",
            "endpoint": {"host": "example.com", "port": 443},
            "auth": {"uuid": "11111111-2222-3333-4444-555555555555"},
            "routing": {"vless_route": "000e"},
        }
    )
    assert server.routing
    assert server.routing.vless_route == 14


def test_vmess_rejects_reality_not_supported_by_legacy_json() -> None:
    with pytest.raises(ValidationError, match="does not support reality"):
        ServerConfig.model_validate(
            {
                "id": "server",
                "enabled": True,
                "protocol": "vmess",
                "name": "Server",
                "endpoint": {"host": "example.com", "port": 443},
                "auth": {"uuid": "11111111-2222-3333-4444-555555555555"},
                "tls": {
                    "mode": "reality",
                    "fp": "chrome",
                    "reality": {"public_key": "test"},
                },
            }
        )
