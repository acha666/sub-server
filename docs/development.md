# Development

## Local checks

```bash
ruff check .
pytest -q
```

## Design layers

- `models/`: typed config structures
- `config/`: load and resolve external YAML
- `services/`: selection, patching, and subscription assembly
- `renderers/`: per-protocol share link generation
- `api/`: HTTP endpoints only
