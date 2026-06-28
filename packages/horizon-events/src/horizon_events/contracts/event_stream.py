"""Event stream contract without implementation."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class EventStream(Protocol):
    """Ordered sequence of event envelopes."""

    @property
    def name(self) -> str:
        """Return the stream name."""

    def append(self, envelope: EventEnvelope) -> None:
        """Append an envelope to the stream."""

    def read(self) -> tuple[EventEnvelope, ...]:
        """Read all envelopes from the stream."""
