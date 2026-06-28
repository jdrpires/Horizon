"""Subscriber filters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from horizon_events.envelopes import EventEnvelope


class EventFilter(Protocol):
    """Predicate used to decide whether a subscriber receives an envelope."""

    def matches(self, envelope: EventEnvelope) -> bool:
        """Return whether this filter accepts an envelope."""


@dataclass(frozen=True, slots=True)
class EventNameFilter:
    """Filter envelopes by event name."""

    event_name: str

    def matches(self, envelope: EventEnvelope) -> bool:
        """Return whether the envelope has the configured event name."""
        return envelope.event_name.value == self.event_name


@dataclass(frozen=True, slots=True)
class TenantFilter:
    """Filter envelopes by tenant."""

    tenant: str

    def matches(self, envelope: EventEnvelope) -> bool:
        """Return whether the envelope belongs to the configured tenant."""
        return envelope.tenant == self.tenant


@dataclass(frozen=True, slots=True)
class CategoryFilter:
    """Filter envelopes by category header."""

    category: str

    def matches(self, envelope: EventEnvelope) -> bool:
        """Return whether the envelope carries the configured category."""
        return envelope.headers.get("category") == self.category
