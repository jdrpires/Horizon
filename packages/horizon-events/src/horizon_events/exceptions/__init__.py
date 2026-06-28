"""Exceptions raised by the Horizon Event Platform."""

from horizon_events.exceptions.errors import (
    EventBusError,
    EventPlatformError,
    EventSerializationError,
    EventValidationError,
    SubscriberError,
)

__all__ = [
    "EventBusError",
    "EventPlatformError",
    "EventSerializationError",
    "EventValidationError",
    "SubscriberError",
]
