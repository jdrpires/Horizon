"""Timeline repository contract."""

from __future__ import annotations

from typing import Protocol

from horizon_domain.asset import AssetId
from horizon_domain.observation import Observation
from horizon_domain.timeline.entities import TimelineEntry
from horizon_domain.timeline.value_objects import TimelineQuery


class TimelineRepository(Protocol):
    """Repository boundary for Timeline memory."""

    def append_observation(self, observation: Observation) -> TimelineEntry:
        """Append an Observation to the Timeline memory."""

    def get_timeline(self, asset_id: AssetId) -> tuple[TimelineEntry, ...]:
        """Return Timeline entries for an Asset."""

    def query(self, query: TimelineQuery) -> tuple[TimelineEntry, ...]:
        """Return entries matching a Timeline query."""
