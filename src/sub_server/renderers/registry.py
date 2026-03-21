from __future__ import annotations

from sub_server.core.exceptions import UnsupportedProtocolError
from sub_server.renderers.shadowsocks import ShadowsocksRenderer
from sub_server.renderers.trojan import TrojanRenderer
from sub_server.renderers.vless import VlessRenderer
from sub_server.renderers.vmess import VmessRenderer


class RendererRegistry:
    def __init__(self) -> None:
        self._renderers = {
            "vless": VlessRenderer(),
            "vmess": VmessRenderer(),
            "trojan": TrojanRenderer(),
            "shadowsocks": ShadowsocksRenderer(),
        }

    def get(self, protocol: str):
        renderer = self._renderers.get(protocol)
        if renderer is None:
            raise UnsupportedProtocolError(protocol)
        return renderer

