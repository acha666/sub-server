from __future__ import annotations

from sub_server.config.resolver import ResolvedSubscription
from sub_server.models.enums import OutputFormat
from sub_server.renderers.registry import RendererRegistry
from sub_server.services.encoding import encode_subscription


class SubscriptionService:
    def __init__(self, registry: RendererRegistry | None = None) -> None:
        self.registry = registry or RendererRegistry()

    def render_lines(self, resolved: ResolvedSubscription) -> list[str]:
        lines = []
        include_key_in_name = resolved.key_rule.output.include_key_in_name
        for server in resolved.servers:
            renderer = self.registry.get(server.protocol.value)
            lines.append(
                renderer.render(server, include_key_in_name=include_key_in_name, key=resolved.key)
            )
        return lines

    def render_subscription(self, resolved: ResolvedSubscription, force_raw: bool = False) -> str:
        text = "\n".join(self.render_lines(resolved))
        output_format = OutputFormat.RAW if force_raw else resolved.key_rule.output.format
        return encode_subscription(text, output_format)

