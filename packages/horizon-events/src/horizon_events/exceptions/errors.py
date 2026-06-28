"""Exception hierarchy for event platform failures."""


class EventPlatformError(Exception):
    """Base exception for exceptional event platform failures."""


class EventValidationError(EventPlatformError):
    """Raised when an event structure is invalid."""


class EventSerializationError(EventPlatformError):
    """Raised when serialization or deserialization fails."""


class EventBusError(EventPlatformError):
    """Raised when event bus operations fail."""


class SubscriberError(EventPlatformError):
    """Raised when subscriber registration or execution fails."""
