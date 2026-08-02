import logging

from fastapi.testclient import TestClient

import sub_server.main as main
from sub_server.core.exceptions import ConfigError


def test_access_log_uses_route_template_and_root_hides_config_path(caplog) -> None:
    with TestClient(main.app) as client, caplog.at_level(logging.INFO, logger="sub-backend"):
        response = client.get("/demo-private?raw=1")
        root = client.get("/")

    assert response.status_code == 200
    assert "demo-private" not in caplog.text
    assert 'path="/{key}"' in caplog.text
    assert "config_dir" not in root.json()


def test_config_errors_are_generic_and_health_reports_unavailable(monkeypatch) -> None:
    def invalid_resolver():
        raise ConfigError("SECRET_CONFIG_DETAIL")

    with TestClient(main.app) as client:
        monkeypatch.setattr(main.app.state, "config_resolver", invalid_resolver)
        health = client.get("/healthz")
        subscription = client.get("/anything")

    assert health.status_code == 503
    assert health.json() == {"ok": False}
    assert subscription.status_code == 500
    assert subscription.json() == {"detail": "invalid server configuration"}
    assert "SECRET_CONFIG_DETAIL" not in subscription.text


def test_run_applies_proxy_settings_and_disables_uvicorn_access_log(monkeypatch) -> None:
    captured = {}

    def fake_run(app, **kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(main.uvicorn, "run", fake_run)
    main.run()

    assert captured["proxy_headers"] is True
    assert captured["access_log"] is False
    assert captured["forwarded_allow_ips"] != "*"
    assert "172.16.0.0/12" in captured["forwarded_allow_ips"]
