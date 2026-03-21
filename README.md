# sub-server

A small but maintainable FastAPI subscription backend for multi-protocol share links.

## Features

- External YAML configuration, suitable for distributing the container image without embedded secrets
- FastAPI HTTP backend with `/healthz`, `/`, and `/{key}` endpoints
- Current protocol renderers:
  - VLESS
  - VMess
  - Trojan
  - Shadowsocks
- Per-key selection rules:
  - include / exclude by id
  - include / exclude by tag
  - per-server deep patch overrides
- VLESS-specific `routing.vless_route` helper that rewrites UUID bytes 7 and 8 via the third UUID segment
- Base64 or raw subscription output
- Docker, Compose, GitHub Actions CI, docs, and tests included

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn sub_server.main:app --reload
```

By default, the app will try to read config from:

1. `SUB_SERVER_CONFIG_DIR`
2. `/config`
3. `./config/examples`

Open:

- `http://127.0.0.1:8000/healthz`
- `http://127.0.0.1:8000/demo-public`
- `http://127.0.0.1:8000/demo-public?raw=1`

## Container usage

```bash
docker compose up -d --build
```

Prepare your own `./config/servers.yaml` and `./config/keys.yaml` before production use.

## Documentation

See `docs/`.
