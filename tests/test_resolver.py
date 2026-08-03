import pytest

from sub_server.config.resolver import ConfigResolver
from sub_server.core.exceptions import ConfigError
from sub_server.models.keyrule import KeyRule
from sub_server.models.server import ServerConfig


def vless_server() -> ServerConfig:
    return ServerConfig.model_validate(
        {
            "id": "shared-node",
            "enabled": True,
            "protocol": "vless",
            "name": "Shared ${key_name}",
            "tags": ["shared"],
            "endpoint": {"host": "example.com", "port": 443},
            "auth": {"uuid": "11111111-2222-0000-3333-444444444444"},
        }
    )


def test_key_can_override_and_repeat_one_server_anonymously() -> None:
    key = KeyRule.model_validate(
        {
            "enabled": True,
            "name": "Combined",
            "select": {"include_ids": ["shared-node"]},
            "overrides": {
                "shared-node": {"auth": {"uuid": "aaaaaaaa-bbbb-0000-cccc-dddddddddddd"}}
            },
            "servers": [
                {
                    "extends": "shared-node",
                    "auth": {"uuid": "eeeeeeee-ffff-0000-aaaa-bbbbbbbbbbbb"},
                    "routing": {"vless_route": 14},
                }
            ],
        }
    )

    resolved = ConfigResolver([vless_server()], {"combined": key}).resolve_key("combined")

    assert len(resolved.servers) == 2
    assert resolved.servers[0].auth.uuid == "aaaaaaaa-bbbb-0000-cccc-dddddddddddd"
    assert resolved.servers[1].auth.uuid == "eeeeeeee-ffff-0000-aaaa-bbbbbbbbbbbb"
    assert resolved.servers[1].routing
    assert resolved.servers[1].routing.vless_route == 14
    assert resolved.servers[1].endpoint == resolved.servers[0].endpoint


def test_key_can_define_a_complete_anonymous_server() -> None:
    key = KeyRule.model_validate(
        {
            "enabled": True,
            "select": {"include_tags": ["not-present"]},
            "servers": [
                {
                    "enabled": True,
                    "protocol": "trojan",
                    "name": "Local",
                    "endpoint": {"host": "example.net", "port": 443},
                    "auth": {"password": "secret"},
                }
            ],
        }
    )

    resolved = ConfigResolver([vless_server()], {"local": key}).resolve_key("local")

    assert len(resolved.servers) == 1
    assert resolved.servers[0].id == "local@1"
    assert resolved.servers[0].endpoint.host == "example.net"


def test_unknown_template_variable_is_rejected_at_config_resolution() -> None:
    key = KeyRule.model_validate(
        {
            "enabled": True,
            "output": {"remark_nodes": "${unknown}"},
        }
    )

    with pytest.raises(ConfigError, match="invalid remark node templates"):
        ConfigResolver([vless_server()], {"broken": key})
