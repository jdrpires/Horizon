"""Dispatcher contract."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope
from horizon_events.subscribers import EventSubscriber


class EventDispatcher(Protocol):
    """Dispatches envelopes to subscribers."""

    def dispatch(self, envelope: EventEnvelope, subscribers: tuple[EventSubscriber, ...]) -> None:
        """Dispatch an envelope to subscribers."""
