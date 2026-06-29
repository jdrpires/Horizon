"""UUID-backed immutable identifiers used by the Horizon Protocol."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class ProtocolIdentifier:
    """Immutable UUID-backed protocol identifier."""

    value: UUID

    def __init__(self, value: UUID | str | None = None) -> None:
        """Create an identifier from a UUID, UUID string, or generated value."""
        resolved = uuid4() if value is None else UUID(str(value))
        object.__setattr__(self, "value", resolved)

    @classmethod
    def new(cls) -> Self:
        """Create a new identifier."""
        return cls()

    @classmethod
    def from_string(cls, value: str) -> Self:
        """Create an identifier from a string."""
        return cls(value)

    def to_string(self) -> str:
        """Serialize this identifier."""
        return str(self.value)

    def __str__(self) -> str:
        """Return this identifier as a string."""
        return self.to_string()


class AssetId(ProtocolIdentifier):
    """Asset identifier."""


class JourneyId(ProtocolIdentifier):
    """Journey identifier."""


class InsightId(ProtocolIdentifier):
    """Insight identifier."""


class RecommendationId(ProtocolIdentifier):
    """Recommendation identifier."""


class ObservationId(ProtocolIdentifier):
    """Observation identifier."""


class MaintenanceId(ProtocolIdentifier):
    """Maintenance identifier."""


class EventId(ProtocolIdentifier):
    """Event identifier."""


class CorrelationId(ProtocolIdentifier):
    """Correlation identifier."""


class CausationId(ProtocolIdentifier):
    """Causation identifier."""


class UserId(ProtocolIdentifier):
    """User identifier."""


class TenantId(ProtocolIdentifier):
    """Tenant identifier."""


class ModuleId(ProtocolIdentifier):
    """Module identifier."""
