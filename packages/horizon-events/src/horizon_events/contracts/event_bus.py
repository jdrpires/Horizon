"""Event bus contract."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope
from horizon_events.subscribers import EventSubscriber, Subscription


class EventBus(Protocol):
    """In-process event bus contract."""

    def publish(self, envelope: EventEnvelope) -> None:
        """Publish a single envelope."""

    def publish_many(self, envelopes: tuple[EventEnvelope, ...]) -> None:
        """Publish multiple envelopes."""

    def subscribe(self, subscriber: EventSubscriber) -> Subscription:
        """Subscribe an event subscriber."""

    def unsubscribe(self, subscription: Subscription) -> None:
        """Remove a subscription."""

    def clear(self) -> None:
        """Remove all subscriptions."""
