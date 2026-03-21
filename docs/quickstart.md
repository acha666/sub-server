# Quick start

## Local run

```bash
pip install -e ".[dev]"
uvicorn sub_backend.main:app --reload
```

## Config resolution order

1. `SUB_BACKEND_CONFIG_DIR`
2. `/config`
3. `config/examples`

## Test endpoints

- `/healthz`
- `/demo-public`
- `/demo-public?raw=1`
