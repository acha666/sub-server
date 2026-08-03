from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "config" / "examples"


def walk(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def test_public_examples_only_use_synthetic_connection_details() -> None:
    documents = [
        yaml.safe_load((EXAMPLES / filename).read_text(encoding="utf-8"))
        for filename in ("servers.yaml", "keys.yaml")
    ]

    for document in documents:
        for key, value in walk(document):
            if key in {"host", "sni"} and isinstance(value, str) and "." in value:
                assert value.endswith(".example.com")
            elif key == "uuid":
                compact = value.replace("-", "")
                assert len(set(compact)) <= 5
            elif key in {"password", "public_key"}:
                assert value == value.upper()
