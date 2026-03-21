from sub_server.models.enums import OutputFormat
from sub_server.utils.url import b64encode_text


def encode_subscription(text: str, output_format: OutputFormat) -> str:
    if output_format == OutputFormat.RAW:
        return text
    if output_format == OutputFormat.BASE64:
        return b64encode_text(text)
    raise ValueError(f"unsupported output format: {output_format}")

