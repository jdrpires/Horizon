"""Current State snapshot entity."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from horizon_domain.asset import AssetId
from horizon_domain.current_state.value_objects import CurrentStateValue


@dataclass(frozen=True, slots=True)
class CurrentStateSnapshot:
    """Immutable Current State snapshot."""

    asset_id: AssetId
    values: tuple[CurrentStateValue, ...]
    observation_count: int
    last_updated_at: datetime | None

    def value_for(self, observation_type: str) -> CurrentStateValue | None:
        """Return the latest value for a type."""
        for value in self.values:
            if value.observation_type.value == observation_type:
                return value
        return None

    def to_dict(self) -> dict[str, object]:
        """Serialize this snapshot."""
        return {
            "asset_id": self.asset_id.to_string(),
            "last_updated_at": None
            if self.last_updated_at is None
            else self.last_updated_at.isoformat(),
            "observation_count": self.observation_count,
            "values": [value.to_dict() for value in self.values],
        }
