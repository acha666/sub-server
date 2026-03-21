from __future__ import annotations

import base64
from urllib.parse import quote, urlencode


def encode_fragment(value: str) -> str:
    return quote(value, safe="")


def urlencode_items(items: list[tuple[str, str]]) -> str:
    return urlencode(items)


def b64encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def b64encode_urlsafe_no_padding(value: str) -> str:
    encoded = base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii")
    return encoded.rstrip("=")

