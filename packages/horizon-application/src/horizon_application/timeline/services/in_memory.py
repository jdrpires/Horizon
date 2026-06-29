"""In-memory Timeline repository."""

from __future__ import annotations

from horizon_domain import AssetId, Observation
from horizon_domain.observation import ObservationTimestamp, ObservationType
from horizon_domain.timeline import Timeline, TimelineEntry, TimelineQuery


class InMemoryTimelineRepository:
    """In-memory repository for Timeline memory."""

    def __init__(self) -> None:
        """Create an empty Timeline repository."""
        self._timelines: dict[str, Timeline] = {}
        self._sequence = 0

    def append_observation(self, observation: Observation) -> TimelineEntry:
        """Append an Observation to its Asset Timeline."""
        asset_key = observation.asset_id.to_string()
        timeline = self._timelines.get(asset_key)
        if timeline is None:
            timeline = Timeline(asset_id=observation.asset_id)
            self._timelines[asset_key] = timeline
        self._sequence += 1
        return timeline.add_observation(observation, self._sequence)

    def get_timeline(self, asset_id: AssetId) -> tuple[TimelineEntry, ...]:
        """Return Timeline entries for one Asset."""
        timeline = self._timelines.get(asset_id.to_string())
        return () if timeline is None else timeline.entries

    def query(self, query: TimelineQuery) -> tuple[TimelineEntry, ...]:
        """Return entries matching a Timeline query."""
        if query.asset_id is None:
            entries = tuple(
                entry for timeline in self._timelines.values() for entry in timeline.entries
            )
        else:
            entries = self.get_timeline(query.asset_id)
        return tuple(entry for entry in _chronological(entries) if _matches(entry, query))


def _chronological(entries: tuple[TimelineEntry, ...]) -> tuple[TimelineEntry, ...]:
    """Return deterministic chronological order."""
    return tuple(sorted(entries, key=lambda entry: (entry.timestamp.value, entry.sequence)))


def _matches(entry: TimelineEntry, query: TimelineQuery) -> bool:
    """Return whether an entry matches the query."""
    if query.observation_type is not None and entry.observation_type != query.observation_type:
        return False
    if query.start_at is not None and entry.timestamp.value < query.start_at.value:
        return False
    if query.end_at is not None and entry.timestamp.value > query.end_at.value:
        return False
    if query.cursor is not None:
        if query.cursor.include_position:
            if entry.timestamp.value < query.cursor.position:
                return False
        elif entry.timestamp.value <= query.cursor.position:
            return False
    return True
