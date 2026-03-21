from __future__ import annotations

import uuid as uuidlib


def normalize_uuid(value: str) -> str:
    return str(uuidlib.UUID(value))


def parse_vless_route(value: int | str) -> int:
    if isinstance(value, int):
        route = value
    elif isinstance(value, str):
        text = value.strip().lower()
        if not text:
            raise ValueError("empty vless_route")
        if text.startswith("0x"):
            route = int(text, 16)
        elif len(text) == 4 and all(c in "0123456789abcdef" for c in text):
            route = int(text, 16)
        else:
            route = int(text, 10)
    else:
        raise ValueError("unsupported vless_route type")

    if not 0 <= route <= 65535:
        raise ValueError("vless_route must be in range [0, 65535]")
    return route


def inject_vless_route(uuid_str: str, route: int | str) -> str:
    parts = normalize_uuid(uuid_str).split("-")
    parts[2] = f"{parse_vless_route(route):04x}"
    return "-".join(parts)

