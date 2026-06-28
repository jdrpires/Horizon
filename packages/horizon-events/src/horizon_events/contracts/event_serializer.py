"""Serializer contract."""

from __future__ import annotations

from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class EventSerializer(Protocol):
    """Converts envelopes to and from primitive payloads."""

    def serialize(self, envelope: EventEnvelope) -> dict[str, object]:
        """Serialize an envelope to primitive values."""

    def deserialize(self, data: dict[str, object]) -> EventEnvelope:
        """Deserialize an envelope from primitive values."""
