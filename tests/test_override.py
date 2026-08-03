from pathlib import Path

import pytest

from sub_server.config.loader import ConfigLoader
from sub_server.core.exceptions import ConfigError
from sub_server.models.server import ServerDefinition
from sub_server.services.override import apply_server_patch, resolve_server_definitions

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "config" / "examples"


def test_apply_vless_route_patch() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    patched = apply_server_patch(server, {"routing": {"vless_route": 14}})
    assert patched.auth.uuid == server.auth.uuid
    assert patched.routing
    assert patched.routing.vless_route == 14


def test_override_can_clear_optional_routing() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]
    patched = apply_server_patch(server, {"routing": None})
    assert patched.routing is None


def test_override_cannot_change_server_identity() -> None:
    loader = ConfigLoader(CONFIG_DIR)
    server = loader.load_servers().servers[0]

    patched = apply_server_patch(server, {"id": "different"})

    assert patched.id == server.id


def test_server_definitions_support_forward_references() -> None:
    definitions = [
        ServerDefinition.model_validate(
            {
                "id": "child",
                "extends": "parent",
                "name": "Child",
            }
        ),
        ServerDefinition.model_validate(
            {
                "id": "parent",
                "enabled": True,
                "protocol": "trojan",
                "name": "Parent",
                "endpoint": {"host": "example.com", "port": 443},
                "auth": {"password": "secret"},
            }
        ),
    ]

    child, parent = resolve_server_definitions(definitions)

    assert child.endpoint == parent.endpoint
    assert child.name == "Child"


def test_server_inheritance_cycles_are_rejected() -> None:
    definitions = [
        ServerDefinition.model_validate({"id": "a", "extends": "b"}),
        ServerDefinition.model_validate({"id": "b", "extends": "a"}),
    ]

    with pytest.raises(ConfigError, match="inheritance cycle"):
        resolve_server_definitions(definitions)
