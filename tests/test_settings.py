from pathlib import Path

import pytest

from sub_server.core.exceptions import ConfigError
from sub_server.core.settings import get_settings


def test_settings_environment_overrides(monkeypatch, tmp_path: Path) -> None:
    (tmp_path / "settings.yaml").write_text(
        "trust_proxy_headers: false\ntrusted_proxy_ips: [127.0.0.1]\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("SUB_SERVER_CONFIG_DIR", str(tmp_path))
    monkeypatch.setenv("SUB_SERVER_PORT", "9000")
    monkeypatch.setenv("SUB_SERVER_TRUST_PROXY_HEADERS", "true")
    monkeypatch.setenv("SUB_SERVER_TRUSTED_PROXY_IPS", "10.0.0.0/8,172.16.0.0/12")

    settings = get_settings()

    assert settings.port == 9000
    assert settings.trust_proxy_headers is True
    assert settings.trusted_proxy_ips == ("10.0.0.0/8", "172.16.0.0/12")


def test_invalid_trusted_proxy_network_is_rejected(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SUB_SERVER_CONFIG_DIR", str(tmp_path))
    monkeypatch.setenv("SUB_SERVER_TRUSTED_PROXY_IPS", "not-a-network")

    with pytest.raises(ConfigError, match="invalid trusted proxy"):
        get_settings()
