class ConfigError(Exception):
    """Raised for invalid configuration."""


class SubscriptionKeyNotFoundError(Exception):
    """Raised when a subscription key does not exist."""


class UnsupportedProtocolError(Exception):
    """Raised when no renderer exists for a protocol."""

