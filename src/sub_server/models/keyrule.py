from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from sub_server.models.common import FlexibleBaseModel
from sub_server.models.enums import OutputFormat


class KeyOutputConfig(FlexibleBaseModel):
    format: OutputFormat = OutputFormat.BASE64
    include_key_in_name: bool = False


class KeySelectConfig(FlexibleBaseModel):
    include_ids: list[str] = Field(default_factory=list)
    include_tags: list[str] = Field(default_factory=list)
    exclude_ids: list[str] = Field(default_factory=list)
    exclude_tags: list[str] = Field(default_factory=list)


class ServerOverride(FlexibleBaseModel):
    patch: dict[str, Any] = Field(default_factory=dict)


class KeyRule(FlexibleBaseModel):
    enabled: bool = True
    output: KeyOutputConfig = Field(default_factory=KeyOutputConfig)
    select: KeySelectConfig = Field(default_factory=KeySelectConfig)
    overrides: dict[str, ServerOverride] = Field(default_factory=dict)


class KeysFile(FlexibleBaseModel):
    keys: dict[str, KeyRule]

    @field_validator("keys")
    @classmethod
    def validate_keys(cls, value: dict[str, KeyRule]) -> dict[str, KeyRule]:
        for key in value:
            if "/" in key or not key.strip():
                raise ValueError("key names must be non-empty and may not contain '/'")
        return value

