"""Immutable domain event model."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType

from horizon_kernel.exceptions import DomainException, ValidationError
from horizon_kernel.ids import UniqueId


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Immutable event describing a domain occurrence."""

    event_id: UniqueId
    aggregate_id: UniqueId
    correlation_id: UniqueId
    causation_id: UniqueId
    occurred_at: datetime
    version: int
    metadata: Mapping[str, object] = field(default_factory=dict)
    payload: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate event invariants."""
        if self.occurred_at.tzinfo is None:
            raise DomainException(
                ValidationError("event.occurred_at_timezone", "occurred_at must be timezone-aware.")
            )
        if self.version < 1:
            raise DomainException(
                ValidationError("event.version", "version must be greater than zero.")
            )
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))

    @classmethod
    def create(
        cls,
        *,
        aggregate_id: UniqueId,
        correlation_id: UniqueId,
        causation_id: UniqueId,
        occurred_at: datetime,
        version: int,
        metadata: dict[str, object] | None = None,
        payload: dict[str, object] | None = None,
    ) -> DomainEvent:
        """Create a domain event with a generated event identifier."""
        return cls(
            event_id=UniqueId.new(),
            aggregate_id=aggregate_id,
            correlation_id=correlation_id,
            causation_id=causation_id,
            occurred_at=occurred_at,
            version=version,
            metadata={} if metadata is None else metadata,
            payload={} if payload is None else payload,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this event to primitive values."""
        return {
            "event_id": self.event_id.to_string(),
            "aggregate_id": self.aggregate_id.to_string(),
            "correlation_id": self.correlation_id.to_string(),
            "causation_id": self.causation_id.to_string(),
            "occurred_at": self.occurred_at.isoformat(),
            "version": self.version,
            "metadata": dict(self.metadata),
            "payload": dict(self.payload),
        }
