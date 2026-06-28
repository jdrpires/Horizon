"""Strongly typed unique identifiers."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UniqueId:
    """Immutable UUID-backed identity value."""

    value: UUID

    def __init__(self, value: UUID | str | None = None) -> None:
        """Create an identifier from a UUID, UUID string, or a generated value."""
        resolved = uuid4() if value is None else UUID(str(value))
        object.__setattr__(self, "value", resolved)

    @classmethod
    def new(cls) -> UniqueId:
        """Create a new unique identifier."""
        return cls()

    @classmethod
    def from_string(cls, value: str) -> UniqueId:
        """Create an identifier from a UUID string."""
        return cls(value)

    def to_string(self) -> str:
        """Serialize this identifier as a UUID string."""
        return str(self.value)

    def __str__(self) -> str:
        """Return the canonical UUID string."""
        return self.to_string()
