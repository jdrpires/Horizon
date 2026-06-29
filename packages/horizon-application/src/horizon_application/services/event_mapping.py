"""Domain Event to Event Envelope mapping."""

from __future__ import annotations

from horizon_events import EventEnvelope, EventMetadata
from horizon_kernel import DomainEvent


class DomainEventEnvelopeMapper:
    """Maps Kernel Domain Events to Horizon Event Platform envelopes."""

    def __init__(
        self,
        *,
        producer: str = "horizon-application",
        source: str = "application-layer",
        environment: str = "local",
    ) -> None:
        """Create a mapper."""
        self._producer = producer
        self._source = source
        self._environment = environment

    def map(self, event: DomainEvent) -> EventEnvelope:
        """Map one Domain Event to an Event Envelope."""
        event_name = str(event.metadata.get("event_name", type(event).__name__))
        metadata = EventMetadata.create(
            aggregate_id=event.aggregate_id.to_string(),
            producer=self._producer,
            source=self._source,
            environment=self._environment,
            correlation_id=event.correlation_id.to_string(),
            causation_id=event.causation_id.to_string(),
            occurred_at=event.occurred_at,
            tags={"domain": _domain_tag(event_name)},
        )
        return EventEnvelope.create(
            event_name=event_name,
            event=event.to_dict(),
            metadata=metadata,
            headers={"domain_event": type(event).__name__},
            version=event.version,
            schema_version=1,
        )

    def map_all(self, events: tuple[DomainEvent, ...]) -> tuple[EventEnvelope, ...]:
        """Map many Domain Events to Event Envelopes."""
        return tuple(self.map(event) for event in events)


def _domain_tag(event_name: str) -> str:
    """Return a domain tag from the event name."""
    if event_name.startswith("Observation"):
        return "observation"
    if event_name.startswith("Asset"):
        return "asset"
    return "unknown"
