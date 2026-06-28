"""Shared immutable event identifiers and names."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class EventId:
    """UUID-backed event identifier."""

    value: UUID

    def __init__(self, value: UUID | str | None = None) -> None:
        """Create an event identifier from a UUID, string, or generated value."""
        object.__setattr__(self, "value", uuid4() if value is None else UUID(str(value)))

    @classmethod
    def new(cls) -> EventId:
        """Create a new event identifier."""
        return cls()

    @classmethod
    def from_string(cls, value: str) -> EventId:
        """Create an event identifier from a string."""
        return cls(value)

    def to_string(self) -> str:
        """Serialize this identifier."""
        return str(self.value)

    def __str__(self) -> str:
        """Return this identifier as a string."""
        return self.to_string()


@dataclass(frozen=True, slots=True)
class EventName:
    """Stable event name used by the registry and bus."""

    value: str

    def __post_init__(self) -> None:
        """Validate event name shape."""
        if not self.value or not self.value.strip():
            raise ValueError("Event name cannot be empty.")

    def __str__(self) -> str:
        """Return the event name."""
        return self.value
