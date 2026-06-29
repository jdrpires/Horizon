"""Shared protocol types."""

from enum import StrEnum


class MessageKind(StrEnum):
    """Supported Horizon message kinds."""

    COMMAND = "command"
    QUERY = "query"
    EVENT = "event"
