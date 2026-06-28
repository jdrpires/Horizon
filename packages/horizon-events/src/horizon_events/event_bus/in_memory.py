"""In-memory event bus implementation."""

from __future__ import annotations

from horizon_events.dispatchers import InMemoryEventDispatcher
from horizon_events.envelopes import EventEnvelope
from horizon_events.subscribers import EventSubscriber, Subscription


class InMemoryEventBus:
    """Technology-agnostic in-process event bus."""

    def __init__(self, dispatcher: InMemoryEventDispatcher | None = None) -> None:
        """Create an event bus."""
        self._dispatcher = InMemoryEventDispatcher() if dispatcher is None else dispatcher
        self._subscribers: dict[str, tuple[Subscription, EventSubscriber]] = {}

    @property
    def subscriptions(self) -> tuple[Subscription, ...]:
        """Return current subscriptions."""
        return tuple(subscription for subscription, _subscriber in self._subscribers.values())

    def publish(self, envelope: EventEnvelope) -> None:
        """Publish a single envelope to matching subscribers."""
        self._dispatcher.dispatch(
            envelope,
            tuple(subscriber for _subscription, subscriber in self._subscribers.values()),
        )

    def publish_many(self, envelopes: tuple[EventEnvelope, ...]) -> None:
        """Publish multiple envelopes in order."""
        for envelope in envelopes:
            self.publish(envelope)

    def subscribe(self, subscriber: EventSubscriber) -> Subscription:
        """Subscribe a handler to this bus."""
        subscription = Subscription.create(subscriber.name)
        self._subscribers[subscription.id.to_string()] = (subscription, subscriber)
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """Remove one subscription."""
        self._subscribers.pop(subscription.id.to_string(), None)

    def clear(self) -> None:
        """Remove all subscribers."""
        self._subscribers.clear()
