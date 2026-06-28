"""Event store contract without implementation."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class EventStore(Protocol):
    """Persistence boundary for appending and reading event envelopes."""

    def append(self, envelope: EventEnvelope) -> None:
        """Append an envelope."""

    def append_many(self, envelopes: tuple[EventEnvelope, ...]) -> None:
        """Append many envelopes."""

    def read(self, stream_name: str) -> tuple[EventEnvelope, ...]:
        """Read envelopes from a stream."""
