from __future__ import annotations

import ipaddress
import uuid as uuidlib
from typing import Any

from pydantic import Field, field_validator, model_validator

from sub_server.models.common import FlexibleBaseModel
from sub_server.models.enums import ProtocolType
from sub_server.utils.validators import parse_vless_route


class EndpointConfig(FlexibleBaseModel):
    host: str
    port: int = Field(ge=1, le=65535)

    @field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        host = value.strip()
        if host.startswith("[") and host.endswith("]"):
            host = host[1:-1]
        if not host or any(char in host for char in "/?#@"):
            raise ValueError("endpoint host must be a non-empty hostname or IP address")
        if ":" in host:
            try:
                ipaddress.IPv6Address(host)
            except ValueError as exc:
                raise ValueError("endpoint host contains an invalid IPv6 address") from exc
        return host


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
    alter_id: int | None = Field(default=None, ge=0, alias="alterId")


class RoutingConfig(FlexibleBaseModel):
    vless_route: int | str | None = None

    @field_validator("vless_route")
    @classmethod
    def validate_vless_route(cls, value: int | str | None) -> int | None:
        return parse_vless_route(value) if value is not None else None


class ServerConfig(FlexibleBaseModel):
    id: str
    enabled: bool
    protocol: ProtocolType
    name: str = Field(min_length=1)
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
        value = value.strip()
        if "/" in value or not value:
            raise ValueError("server id must be non-empty and may not contain '/'")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("server name must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_protocol_fields(self) -> ServerConfig:
        if self.protocol in {ProtocolType.VLESS, ProtocolType.VMESS}:
            if not self.auth.uuid:
                raise ValueError(f"{self.protocol.value} requires auth.uuid")
            try:
                uuidlib.UUID(self.auth.uuid)
            except ValueError as exc:
                raise ValueError(f"{self.protocol.value} requires a valid auth.uuid") from exc
            if self.protocol == ProtocolType.VMESS and self.tls and self.tls.mode == "reality":
                raise ValueError("the VMess base64 JSON format does not support reality TLS")
        elif self.protocol == ProtocolType.TROJAN and not self.auth.password:
            raise ValueError("trojan requires auth.password")
        elif self.protocol == ProtocolType.SHADOWSOCKS:
            if not self.auth.method or not self.auth.password:
                raise ValueError("shadowsocks requires auth.method and auth.password")

        if self.tls and self.tls.mode == "reality":
            if not self.tls.reality or not self.tls.reality.public_key:
                raise ValueError("reality TLS requires tls.reality.public_key")
            if not self.tls.fp:
                raise ValueError("reality TLS requires tls.fp")
        elif self.tls and self.tls.reality:
            raise ValueError("tls.reality requires tls.mode to be 'reality'")
        return self


class ServersFile(FlexibleBaseModel):
    servers: list[ServerConfig]
