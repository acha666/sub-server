from __future__ import annotations

import base64
import ipaddress
from urllib.parse import quote, urlencode


def encode_fragment(value: str) -> str:
    return quote(value, safe="")


def encode_userinfo(value: str) -> str:
    return quote(value, safe="")


def normalize_host(value: str) -> str:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return value.encode("idna").decode("ascii")
    return str(address)


def format_uri_host(value: str) -> str:
    host = normalize_host(value)
    return f"[{host}]" if ":" in host else host


def urlencode_items(items: list[tuple[str, str]]) -> str:
    return urlencode(items, quote_via=quote, safe="")


def b64encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


def b64encode_urlsafe_no_padding(value: str) -> str:
    encoded = base64.urlsafe_b64encode(value.encode("utf-8")).decode("ascii")
    return encoded.rstrip("=")
