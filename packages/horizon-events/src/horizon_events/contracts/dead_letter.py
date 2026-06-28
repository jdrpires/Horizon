"""Dead-letter contracts without persistence implementation."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class DeadLetterPublisher(Protocol):
    """Publishes failed envelopes to a dead-letter boundary."""

    def publish_failed(self, envelope: EventEnvelope, reason: str) -> None:
        """Publish a failed envelope and reason."""


class DeadLetterStore(Protocol):
    """Stores failed envelopes for later inspection or replay."""

    def append_failed(self, envelope: EventEnvelope, reason: str) -> None:
        """Append a failed envelope and reason."""
