from __future__ import annotations

from datetime import datetime

from sub_server.config.resolver import ResolvedSubscription
from sub_server.models.enums import OutputFormat
from sub_server.renderers.registry import RendererRegistry
from sub_server.services.encoding import encode_subscription
from sub_server.services.templates import render_template, template_variables
from sub_server.utils.url import encode_fragment

REMARK_NODE_PREFIX = (
    "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1?encryption=none&type=tcp#"
)


class SubscriptionService:
    def __init__(self, registry: RendererRegistry | None = None) -> None:
        self.registry = registry or RendererRegistry()

    def render_lines(
        self,
        resolved: ResolvedSubscription,
        *,
        now: datetime | None = None,
    ) -> list[str]:
        variables = template_variables(resolved.key, resolved.key_rule.name, now=now)
        lines = [
            f"{REMARK_NODE_PREFIX}{encode_fragment(render_template(line.strip(), variables))}"
            for line in resolved.key_rule.output.remark_nodes.splitlines()
            if line.strip()
        ]
        include_key_in_name = resolved.key_rule.output.include_key_in_name
        for server in resolved.servers:
            renderer = self.registry.get(server.protocol.value)
            rendered_server = server.model_copy(
                update={"name": render_template(server.name, variables)}
            )
            lines.append(
                renderer.render(
                    rendered_server,
                    include_key_in_name=include_key_in_name,
                    key=resolved.key,
                )
            )
        return lines

    def render_subscription(self, resolved: ResolvedSubscription, force_raw: bool = False) -> str:
        text = "\n".join(self.render_lines(resolved))
        output_format = OutputFormat.RAW if force_raw else resolved.key_rule.output.format
        return encode_subscription(text, output_format)
