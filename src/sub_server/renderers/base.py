from __future__ import annotations

from abc import ABC, abstractmethod

from sub_server.models.server import ServerConfig


class ShareLinkRenderer(ABC):
    protocol: str

    @abstractmethod
    def render(self, server: ServerConfig, include_key_in_name: bool = False, key: str = "") -> str:
        raise NotImplementedError

