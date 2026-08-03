from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator, model_validator

from sub_server.models.common import FlexibleBaseModel
from sub_server.models.enums import OutputFormat

RESERVED_KEY_NAMES = frozenset({"healthz", "docs", "redoc", "openapi.json"})


class KeyOutputConfig(FlexibleBaseModel):
    format: OutputFormat = OutputFormat.BASE64
    include_key_in_name: bool = False
    remark_nodes: str = ""


class KeySelectConfig(FlexibleBaseModel):
    include_ids: list[str] = Field(default_factory=list)
    include_tags: list[str] = Field(default_factory=list)
    exclude_ids: list[str] = Field(default_factory=list)
    exclude_tags: list[str] = Field(default_factory=list)


class AnonymousServer(FlexibleBaseModel):
    extends: str | None = None

    @field_validator("extends")
    @classmethod
    def validate_extends(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("anonymous server extends must be a non-empty server id")
        return value

    @model_validator(mode="after")
    def reject_id(self) -> AnonymousServer:
        if self.model_extra and "id" in self.model_extra:
            raise ValueError("key-local servers are anonymous and may not define id")
        return self

    def patch(self) -> dict[str, Any]:
        data = self.model_dump(by_alias=True, exclude_unset=True)
        data.pop("extends", None)
        return data


class KeyRule(FlexibleBaseModel):
    enabled: bool
    name: str | None = None
    output: KeyOutputConfig = Field(default_factory=KeyOutputConfig)
    select: KeySelectConfig = Field(default_factory=KeySelectConfig)
    overrides: dict[str, dict[str, Any]] = Field(default_factory=dict)
    servers: list[AnonymousServer] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("key name must be non-empty when provided")
        return value


class KeysFile(FlexibleBaseModel):
    keys: dict[str, KeyRule]

    @field_validator("keys")
    @classmethod
    def validate_keys(cls, value: dict[str, KeyRule]) -> dict[str, KeyRule]:
        for key in value:
            normalized = key.strip()
            if (
                "/" in key
                or not normalized
                or key != normalized
                or normalized in {".", ".."}
                or normalized.casefold() in RESERVED_KEY_NAMES
            ):
                raise ValueError(
                    "key names must be non-empty, may not contain '/', "
                    "and may not use reserved paths"
                )
        return value
