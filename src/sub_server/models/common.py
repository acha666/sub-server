from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class FlexibleBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")


def dump_excluding_none(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(exclude_none=True)

