"""Current State value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Self

from horizon_domain.asset import AssetId
from horizon_domain.observation import ObservationType
from horizon_kernel import ValueObject


@dataclass(frozen=True, slots=True)
class CurrentStateQuery(ValueObject):
    """Query for one Asset Current State."""

    asset_id: AssetId

    def to_dict(self) -> dict[str, object]:
        """Serialize this query."""
        return {"asset_id": self.asset_id.to_string()}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this query."""
        return cls(asset_id=AssetId.from_string(str(data["asset_id"])))


@dataclass(frozen=True, slots=True)
class CurrentStateValue(ValueObject):
    """Latest known value for one Observation type."""

    observation_type: ObservationType
    value: float
    unit: str
    source: str
    timestamp: datetime
    observation_id: str
    sequence: int

    def to_dict(self) -> dict[str, object]:
        """Serialize this value."""
        return {
            "type": self.observation_type.value,
            "value": self.value,
            "unit": self.unit,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "observation_id": self.observation_id,
            "sequence": self.sequence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value."""
        return cls(
            observation_type=ObservationType(str(data["type"])),
            value=float(data["value"]),
            unit=str(data["unit"]),
            source=str(data["source"]),
            timestamp=datetime.fromisoformat(str(data["timestamp"])),
            observation_id=str(data["observation_id"]),
            sequence=int(data["sequence"]),
        )
