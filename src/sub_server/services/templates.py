from __future__ import annotations

from datetime import datetime
from string import Template

TEMPLATE_VARIABLES = frozenset({"date", "time", "datetime", "key", "key_name"})


def template_variables(
    key: str,
    key_name: str | None,
    *,
    now: datetime | None = None,
) -> dict[str, str]:
    current = now or datetime.now().astimezone()
    return {
        "date": current.strftime("%Y-%m-%d"),
        "time": current.strftime("%H:%M"),
        "datetime": current.strftime("%Y-%m-%d %H:%M"),
        "key": key,
        "key_name": key_name or key,
    }


def render_template(value: str, variables: dict[str, str]) -> str:
    return Template(value).substitute(variables)


def validate_template(value: str) -> None:
    render_template(value, {name: name for name in TEMPLATE_VARIABLES})
