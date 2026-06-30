"""Current State DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_domain.current_state import CurrentStateSnapshot, CurrentStateValue


@dataclass(frozen=True, slots=True)
class CurrentStateValueDTO:
    """Serializable latest value."""

    observation_type: str
    value: float
    unit: str
    source: str
    timestamp: str
    observation_id: str
    sequence: int

    @classmethod
    def from_value(cls, value: CurrentStateValue) -> CurrentStateValueDTO:
        """Map a domain value."""
        return cls(
            observation_type=value.observation_type.value,
            value=value.value,
            unit=value.unit,
            source=value.source,
            timestamp=value.timestamp.isoformat(),
            observation_id=value.observation_id,
            sequence=value.sequence,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this DTO."""
        return {
            "type": self.observation_type,
            "value": self.value,
            "unit": self.unit,
            "source": self.source,
            "timestamp": self.timestamp,
            "observation_id": self.observation_id,
            "sequence": self.sequence,
        }


@dataclass(frozen=True, slots=True)
class CurrentStateSnapshotDTO:
    """Serializable Current State snapshot."""

    asset_id: str
    values: tuple[CurrentStateValueDTO, ...]
    observation_count: int
    last_updated_at: str | None

    @classmethod
    def from_snapshot(cls, snapshot: CurrentStateSnapshot) -> CurrentStateSnapshotDTO:
        """Map a domain snapshot."""
        return cls(
            asset_id=snapshot.asset_id.to_string(),
            values=tuple(CurrentStateValueDTO.from_value(value) for value in snapshot.values),
            observation_count=snapshot.observation_count,
            last_updated_at=None
            if snapshot.last_updated_at is None
            else snapshot.last_updated_at.isoformat(),
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this DTO."""
        return {
            "asset_id": self.asset_id,
            "last_updated_at": self.last_updated_at,
            "observation_count": self.observation_count,
            "values": [value.to_dict() for value in self.values],
        }
