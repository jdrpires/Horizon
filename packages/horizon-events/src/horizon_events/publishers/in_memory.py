"""In-memory publisher implementation."""

from horizon_events.envelopes import EventEnvelope
from horizon_events.event_bus import InMemoryEventBus


class InMemoryEventPublisher:
    """Publisher that delegates to an in-memory event bus."""

    def __init__(self, event_bus: InMemoryEventBus) -> None:
        """Create a publisher for an event bus."""
        self._event_bus = event_bus

    def publish(self, envelope: EventEnvelope) -> None:
        """Publish one envelope."""
        self._event_bus.publish(envelope)

    def publish_many(self, envelopes: tuple[EventEnvelope, ...]) -> None:
        """Publish many envelopes."""
        self._event_bus.publish_many(envelopes)
