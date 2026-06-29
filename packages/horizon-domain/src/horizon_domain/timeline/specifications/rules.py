"""Timeline specifications."""

from __future__ import annotations

from horizon_domain.timeline.entities import TimelineEntry


def is_chronological(entries: tuple[TimelineEntry, ...]) -> bool:
    """Return whether entries are in deterministic chronological order."""
    ordered = tuple(sorted(entries, key=lambda entry: (entry.timestamp.value, entry.sequence)))
    return entries == ordered
