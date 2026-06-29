"""Timeline DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_domain.timeline import TimelineEntry


@dataclass(frozen=True, slots=True)
class TimelineEntryDTO:
    """Serializable Timeline entry view."""

    asset_id: str
    observation_id: str
    observation_type: str
    value: float
    unit: str
    source: str
    timestamp: str
    quality: str
    sequence: int

    @classmethod
    def from_entry(cls, entry: TimelineEntry) -> TimelineEntryDTO:
        """Map a Timeline entry to a DTO."""
        return cls(
            asset_id=entry.asset_id.to_string(),
            observation_id=entry.observation_id.to_string(),
            observation_type=entry.observation_type.value,
            value=entry.value.value,
            unit=entry.unit.value,
            source=entry.source.value,
            timestamp=entry.timestamp.value.isoformat(),
            quality=entry.quality.value,
            sequence=entry.sequence,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize this DTO."""
        return {
            "asset_id": self.asset_id,
            "observation_id": self.observation_id,
            "type": self.observation_type,
            "value": self.value,
            "unit": self.unit,
            "source": self.source,
            "timestamp": self.timestamp,
            "quality": self.quality,
            "sequence": self.sequence,
        }


@dataclass(frozen=True, slots=True)
class TimelineResultDTO:
    """Timeline query result."""

    entries: tuple[TimelineEntryDTO, ...]

    def to_dict(self) -> dict[str, object]:
        """Serialize this result."""
        return {"entries": [entry.to_dict() for entry in self.entries]}


@dataclass(frozen=True, slots=True)
class ReplayTimelineResultDTO:
    """Timeline replay result."""

    entries: tuple[TimelineEntryDTO, ...]

    def to_dict(self) -> dict[str, object]:
        """Serialize this replay."""
        return {"entries": [entry.to_dict() for entry in self.entries]}
