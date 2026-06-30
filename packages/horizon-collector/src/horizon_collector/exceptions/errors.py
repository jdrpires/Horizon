"""Collector framework errors."""

from __future__ import annotations


class CollectorError(Exception):
    """Base error for collector framework failures."""


class CollectorAlreadyRegisteredError(CollectorError):
    """Raised when registering a duplicate collector."""

    def __init__(self, name: str) -> None:
        """Create the error."""
        super().__init__(f"collector already registered: {name}")


class CollectorNotFoundError(CollectorError):
    """Raised when a collector is not registered."""

    def __init__(self, name: str) -> None:
        """Create the error."""
        super().__init__(f"collector not found: {name}")


class ObservationMappingError(CollectorError):
    """Raised when raw data cannot become a canonical observation."""

    def __init__(self, key: str, reason: str) -> None:
        """Create the error."""
        super().__init__(f"could not map observation '{key}': {reason}")


class UnsupportedObservationValueTypeError(CollectorError):
    """Raised when current runtime cannot accept the catalog value type."""

    def __init__(self, definition_id: str, value_type: str) -> None:
        """Create the error."""
        super().__init__(
            f"observation definition '{definition_id}' has unsupported value_type '{value_type}' "
            "for the current runtime."
        )
