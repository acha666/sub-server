.PHONY: help install dev-install lint lint-fix format test run check clean

help:
	@echo "sub-server development commands:"
	@echo ""
	@echo "  make install      - Install dependencies"
	@echo "  make dev-install  - Install development dependencies"
	@echo "  make lint         - Run ruff linter"
	@echo "  make lint-fix     - Fix auto-fixable lint issues"
	@echo "  make format       - Format code with ruff"
	@echo "  make test         - Run tests"
	@echo "  make check        - Run all checks (lint + test)"
	@echo "  make run          - Run development server"
	@echo "  make clean        - Clean cache and build artifacts"

install:
	pip install .

dev-install:
	pip install -e ".[dev]"

lint:
	ruff check .

lint-fix:
	ruff check . --fix

format:
	ruff format .

test:
	pytest -q

check: lint test

run:
	uvicorn sub_server.main:app --reload --host 0.0.0.0 --port 8000

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
