"""Current State projection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from horizon_domain.asset import AssetId
from horizon_domain.current_state.entities import CurrentStateSnapshot
from horizon_domain.current_state.value_objects import CurrentStateValue
from horizon_domain.timeline import TimelineEntry


@dataclass(frozen=True, slots=True)
class CurrentStateProjection:
    """Latest values by Observation type."""

    asset_id: AssetId
    values_by_type: dict[str, CurrentStateValue]
    observation_count: int
    last_updated_at: datetime | None

    def snapshot(self) -> CurrentStateSnapshot:
        """Create an immutable snapshot."""
        values = tuple(
            self.values_by_type[key]
            for key in sorted(
                self.values_by_type,
                key=lambda item: (
                    self.values_by_type[item].timestamp,
                    self.values_by_type[item].sequence,
                    item,
                ),
            )
        )
        return CurrentStateSnapshot(
            asset_id=self.asset_id,
            values=values,
            observation_count=self.observation_count,
            last_updated_at=self.last_updated_at,
        )

    @classmethod
    def empty(cls, asset_id: AssetId) -> CurrentStateProjection:
        """Create an empty projection."""
        return cls(asset_id=asset_id, values_by_type={}, observation_count=0, last_updated_at=None)

    def apply(self, entry: TimelineEntry) -> CurrentStateProjection:
        """Apply one Timeline entry."""
        if entry.asset_id != self.asset_id:
            raise ValueError("Timeline entry asset_id does not match Current State asset_id.")
        next_values = dict(self.values_by_type)
        next_values[entry.observation_type.value] = CurrentStateValue(
            observation_type=entry.observation_type,
            value=entry.value.value,
            unit=entry.unit.value,
            source=entry.source.value,
            timestamp=entry.timestamp.value,
            observation_id=entry.observation_id.to_string(),
            sequence=entry.sequence,
        )
        return CurrentStateProjection(
            asset_id=self.asset_id,
            values_by_type=next_values,
            observation_count=self.observation_count + 1,
            last_updated_at=entry.timestamp.value,
        )
