# Development Container Configuration

This directory contains the Dev Container configuration for the sub-server project.

## Overview

- **Python Version**: 3.13
- **Base Image**: `mcr.microsoft.com/devcontainers/python:3.13`
- **Package Manager**: pip
- **Build Tool**: hatchling

## Features

The development container includes:

### System Features
- Git and Git LFS support
- GitHub CLI for repository management
- Docker-in-Docker for containerization

### VS Code Extensions
- Python language support (ms-python.python)
- Pylance type checking (ms-python.vscode-pylance)
- Debugpy for debugging (ms-python.debugpy)
- Ruff for linting and formatting (charliermarsh.ruff)
- Makefile tools support (ms-vscode.makefile-tools)
- GitHub Actions support (github.vscode-github-actions)

## Setup

The container automatically:

1. Installs the project in editable mode: `pip install -e '.[dev]'`
2. Sets up Python linting with Ruff
3. Configures VSCode for Python development
4. Mounts SSH and Git config from the host (read-only)

## Usage

### Using VS Code Dev Containers

1. Open the workspace in VS Code
2. When prompted, reopen in Dev Container or use Command Palette: "Dev Containers: Reopen in Container"
3. Wait for setup to complete (environment ready message will appear)

### Development Commands

Use `make` commands:

```bash
make help          # Show all available commands
make dev-install   # Install development dependencies
make lint          # Run linter checks
make lint-fix      # Fix auto-fixable lint issues
make test          # Run tests
make check         # Run lint + tests
make run           # Run development server (with auto-reload)
make clean         # Clean cache and build artifacts
```

## Customization

### Adding System Dependencies

Edit `.devcontainer/Dockerfile` and uncomment the `apt-get install` section:

```dockerfile
RUN apt-get update && apt-get install -y \
    package-name && \
    rm -rf /var/lib/apt/lists/*
```

Then rebuild the container.

### Adding Python Packages

For development-only packages, add them to `pyproject.toml` under `[project.optional-dependencies] dev`.
For production packages, add them to `[project] dependencies`.

### Port Forwarding

Port 8000 is automatically forwarded for the development server.

## Troubleshooting

### Container rebuild fails
```bash
# Rebuild from scratch
dev-container rebuild --no-cache
```

### Python packages not found
```bash
# Reinstall development dependencies
pip install -e ".[dev]"
```

### VSCode extensions not loading
- Wait for the Dev Container to fully initialize
- Check the Dev Container's terminal for errors
- Reload VS Code window

## References

- [Dev Containers Documentation](https://containers.dev/)
- [VS Code Dev Containers](https://code.visualstudio.com/docs/remote/containers)
