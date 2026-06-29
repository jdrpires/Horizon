"""Timeline aggregate."""

from __future__ import annotations

from datetime import datetime

from horizon_domain.asset import AssetId
from horizon_domain.observation import Observation
from horizon_domain.timeline.entities import TimelineEntry
from horizon_kernel import AggregateRoot, Clock


class Timeline(AggregateRoot):
    """Chronological memory for one Asset."""

    __slots__ = ("_asset_id", "_entries")

    def __init__(
        self,
        *,
        asset_id: AssetId,
        entries: tuple[TimelineEntry, ...] = (),
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        version: int = 1,
        clock: Clock | None = None,
    ) -> None:
        """Create a Timeline."""
        super().__init__(
            id=asset_id.value,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
            clock=clock,
        )
        self._asset_id = asset_id
        self._entries = _chronological(entries)

    @property
    def asset_id(self) -> AssetId:
        """Return the Timeline Asset ID."""
        return self._asset_id

    @property
    def entries(self) -> tuple[TimelineEntry, ...]:
        """Return Timeline entries in chronological order."""
        return self._entries

    def add_observation(self, observation: Observation, sequence: int) -> TimelineEntry:
        """Add an Observation-derived entry and keep chronological order."""
        if observation.asset_id != self.asset_id:
            raise ValueError("Observation asset_id does not match Timeline asset_id.")
        entry = TimelineEntry.from_observation(observation, sequence)
        self._entries = _chronological((*self._entries, entry))
        self.increment_version()
        return entry

    def to_dict(self) -> dict[str, object]:
        """Serialize this Timeline."""
        return {
            "asset_id": self.asset_id.to_string(),
            "version": self.version,
            "entries": [entry.to_dict() for entry in self.entries],
        }


def _chronological(entries: tuple[TimelineEntry, ...]) -> tuple[TimelineEntry, ...]:
    """Return entries in deterministic chronological order."""
    return tuple(sorted(entries, key=lambda entry: (entry.timestamp.value, entry.sequence)))
