from enum import StrEnum


class ProtocolType(StrEnum):
    VLESS = "vless"
    VMESS = "vmess"
    TROJAN = "trojan"
    SHADOWSOCKS = "shadowsocks"


class OutputFormat(StrEnum):
    BASE64 = "base64"
    RAW = "raw"

