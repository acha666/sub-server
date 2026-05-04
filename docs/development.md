# Development

## Setup

### Using Dev Container (Recommended)

The project includes a Dev Container configuration for consistent development environments:

1. Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Open the workspace in VS Code
3. Click "Reopen in Container" when prompted (or use Command Palette: "Dev Containers: Reopen in Container")
4. Wait for setup to complete

For detailed Dev Container information, see [.devcontainer/README.md](.devcontainer/README.md).

### Manual Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Development Commands

### Using Make (Recommended)

```bash
make help        # Show all available commands
make dev-install # Install development dependencies
make lint        # Run rinter checks
make lint-fix    # Fix auto-fixable lint issues
make test        # Run tests
make check       # Run all checks (lint and tests)
make run         # Run development server with auto-reload
make clean       # Clean cache and build artifacts
```

### Manual Commands

```bash
# Linting
ruff check .

# Auto-fix lint issues
ruff check . --fix

# Format code
ruff format .

# Testing
pytest -q

# Run development server
uvicorn sub_server.main:app --reload
```

## Design Layers

- `models/`: typed config structures
- `config/`: load and resolve external YAML
- `services/`: selection, patching, and subscription assembly
- `renderers/`: per-protocol share link generation
- `api/`: HTTP endpoints only

