from __future__ import annotations

from copy import deepcopy
from typing import Any

JsonMap = dict[str, Any]


def deep_merge(base: JsonMap, patch: JsonMap) -> JsonMap:
    result = deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result

