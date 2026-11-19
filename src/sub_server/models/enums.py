from enum import StrEnum


class ProtocolType(StrEnum):
    VLESS = "vless"
    VMESS = "vmess"
    TROJAN = "trojan"
    SHADOWSOCKS = "shadowsocks"
    HYSTERIA2 = "hysteria2"


class OutputFormat(StrEnum):
    BASE64 = "base64"
    RAW = "raw"
