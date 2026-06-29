"""Timeline replay service."""

from __future__ import annotations

from horizon_domain.timeline.entities import TimelineEntry


class ReplayEngine:
    """Replays Timeline entries in deterministic chronological order."""

    def replay(self, entries: tuple[TimelineEntry, ...]) -> tuple[TimelineEntry, ...]:
        """Return entries ordered for replay."""
        return tuple(sorted(entries, key=lambda entry: (entry.timestamp.value, entry.sequence)))
