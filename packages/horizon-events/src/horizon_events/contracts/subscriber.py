"""Subscriber contract."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class EventSubscriber(Protocol):
    """Receives event envelopes."""

    def handle(self, envelope: EventEnvelope) -> None:
        """Handle an event envelope."""

    def matches(self, envelope: EventEnvelope) -> bool:
        """Return whether this subscriber accepts an envelope."""
