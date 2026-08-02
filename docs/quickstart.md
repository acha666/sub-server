# Quick start

## Local run

```bash
pip install -e ".[dev]"
sub-server
```

## Config resolution order

1. `SUB_SERVER_CONFIG_DIR`
2. `/config`
3. `config/examples`

## Test endpoints

- `/healthz`
- `/demo-public`
- `/demo-public?raw=1`
