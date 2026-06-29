"""Observation domain events."""

from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Self

from horizon_domain.observation.value_objects import ObservationId
from horizon_kernel import DomainEvent, UniqueId


class ObservationDomainEvent(DomainEvent):
    """Base class for Observation events."""

    event_name: ClassVar[str] = "ObservationDomainEvent"

    @classmethod
    def create(
        cls,
        *,
        observation_id: ObservationId,
        correlation_id: UniqueId,
        causation_id: UniqueId,
        occurred_at: datetime,
        version: int,
        payload: dict[str, object] | None = None,
    ) -> Self:
        """Create an Observation domain event."""
        return cls(
            event_id=UniqueId.new(),
            aggregate_id=observation_id.value,
            correlation_id=correlation_id,
            causation_id=causation_id,
            occurred_at=occurred_at,
            version=version,
            metadata={"event_name": cls.event_name},
            payload={} if payload is None else payload,
        )


class ObservationRegistered(ObservationDomainEvent):
    """Observation was registered."""

    event_name: ClassVar[str] = "ObservationRegistered"
