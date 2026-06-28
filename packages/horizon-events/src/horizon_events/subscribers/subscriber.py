"""Event subscriber and subscription models."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from horizon_events.envelopes import EventEnvelope
from horizon_events.shared import EventId
from horizon_events.subscribers.filters import EventFilter

EventHandler = Callable[[EventEnvelope], None]


@dataclass(frozen=True, slots=True)
class Subscription:
    """Registered subscriber reference."""

    id: EventId
    subscriber_name: str

    @classmethod
    def create(cls, subscriber_name: str) -> Subscription:
        """Create a subscription identifier for a subscriber."""
        return cls(id=EventId.new(), subscriber_name=subscriber_name)


@dataclass(slots=True)
class EventSubscriber:
    """Event subscriber composed of a handler and optional filters."""

    name: str
    handler: EventHandler
    filters: tuple[EventFilter, ...] = field(default_factory=tuple)

    def handle(self, envelope: EventEnvelope) -> None:
        """Handle an accepted event envelope."""
        self.handler(envelope)

    def matches(self, envelope: EventEnvelope) -> bool:
        """Return whether all filters accept the envelope."""
        return all(event_filter.matches(envelope) for event_filter in self.filters)
