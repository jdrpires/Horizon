"""Publisher contract."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class EventPublisher(Protocol):
    """Boundary for publishing event envelopes."""

    def publish(self, envelope: EventEnvelope) -> None:
        """Publish one event envelope."""

    def publish_many(self, envelopes: tuple[EventEnvelope, ...]) -> None:
        """Publish many event envelopes."""
