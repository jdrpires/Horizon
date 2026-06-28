"""Base aggregate root model."""

from __future__ import annotations

from datetime import datetime

from horizon_kernel.contracts import EventPublisher
from horizon_kernel.entities import Entity
from horizon_kernel.events import DomainEvent
from horizon_kernel.ids import UniqueId
from horizon_kernel.utils import Clock


class AggregateRoot(Entity):
    """Entity that owns consistency boundaries and records domain events."""

    __slots__ = ("_domain_events",)

    def __init__(
        self,
        *,
        id: UniqueId | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        version: int = 1,
        metadata: dict[str, object] | None = None,
        clock: Clock | None = None,
    ) -> None:
        """Create an aggregate root."""
        super().__init__(
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            metadata=metadata,
            clock=clock,
        )
        self._domain_events: list[DomainEvent] = []

    @property
    def domain_events(self) -> tuple[DomainEvent, ...]:
        """Return pending domain events."""
        return tuple(self._domain_events)

    def record_event(self, event: DomainEvent) -> None:
        """Record a domain event raised by this aggregate."""
        self._domain_events.append(event)

    def pull_events(self) -> tuple[DomainEvent, ...]:
        """Return pending events and clear the aggregate event buffer."""
        events = self.domain_events
        self.clear_events()
        return events

    def clear_events(self) -> None:
        """Clear pending domain events."""
        self._domain_events.clear()

    def publish_events(self, publisher: EventPublisher) -> None:
        """Publish pending events using the supplied publisher."""
        publisher.publish_all(self.domain_events)
        self.clear_events()
