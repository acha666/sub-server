from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from sub_server.models.common import FlexibleBaseModel
from sub_server.models.enums import ProtocolType


class EndpointConfig(FlexibleBaseModel):
    host: str
    port: int


class RealityConfig(FlexibleBaseModel):
    public_key: str | None = None
    short_id: str | None = None
    spider_x: str | None = None


class TLSConfig(FlexibleBaseModel):
    mode: str | None = None
    sni: str | None = None
    alpn: list[str] | None = None
    fp: str | None = None
    insecure: bool | None = None
    reality: RealityConfig | None = None


class TransportConfig(FlexibleBaseModel):
    type: str | None = None
    host: str | None = None
    path: str | None = None
    service_name: str | None = Field(default=None, alias="serviceName")
    authority: str | None = None
    mode: str | None = None
    header_type: str | None = Field(default=None, alias="headerType")


class AuthConfig(FlexibleBaseModel):
    uuid: str | None = None
    password: str | None = None
    method: str | None = None
    alter_id: int | None = Field(default=None, alias="alterId")


class RoutingConfig(FlexibleBaseModel):
    vless_route: int | str | None = None


class ServerConfig(FlexibleBaseModel):
    id: str
    enabled: bool = True
    protocol: ProtocolType
    name: str
    tags: list[str] = Field(default_factory=list)
    endpoint: EndpointConfig
    auth: AuthConfig
    tls: TLSConfig | None = None
    transport: TransportConfig | None = None
    routing: RoutingConfig | None = None
    options: dict[str, Any] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if "/" in value or not value.strip():
            raise ValueError("server id must be non-empty and may not contain '/'")
        return value


class ServersFile(FlexibleBaseModel):
    servers: list[ServerConfig]

