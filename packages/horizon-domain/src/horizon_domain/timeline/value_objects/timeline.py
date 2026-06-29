"""Timeline value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Self, cast

from horizon_domain.asset import AssetId
from horizon_domain.observation import ObservationTimestamp, ObservationType
from horizon_kernel import DomainException, ValidationError, ValueObject


@dataclass(frozen=True, slots=True)
class TimelineCursor(ValueObject):
    """Timestamp cursor for Timeline navigation."""

    position: datetime
    include_position: bool = True

    def __post_init__(self) -> None:
        """Validate cursor timestamp."""
        if self.position.tzinfo is None:
            raise DomainException(
                ValidationError(
                    "timeline.cursor.timezone",
                    "Timeline cursor position must be timezone-aware.",
                )
            )

    def to_dict(self) -> dict[str, object]:
        """Serialize this cursor."""
        return {
            "position": self.position.isoformat(),
            "include_position": self.include_position,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this cursor."""
        return cls(
            position=datetime.fromisoformat(str(data["position"])),
            include_position=bool(data.get("include_position", True)),
        )


@dataclass(frozen=True, slots=True)
class TimelineQuery(ValueObject):
    """Timeline filtering query."""

    asset_id: AssetId | None = None
    observation_type: ObservationType | None = None
    start_at: ObservationTimestamp | None = None
    end_at: ObservationTimestamp | None = None
    cursor: TimelineCursor | None = None

    def __post_init__(self) -> None:
        """Validate the query period."""
        if self.start_at is not None and self.end_at is not None:
            if self.start_at.value > self.end_at.value:
                raise DomainException(
                    ValidationError(
                        "timeline.query.period",
                        "Timeline query start_at cannot be after end_at.",
                    )
                )

    def to_dict(self) -> dict[str, object]:
        """Serialize this query."""
        return {
            "asset_id": None if self.asset_id is None else self.asset_id.to_string(),
            "observation_type": None
            if self.observation_type is None
            else self.observation_type.value,
            "start_at": None if self.start_at is None else self.start_at.value.isoformat(),
            "end_at": None if self.end_at is None else self.end_at.value.isoformat(),
            "cursor": None if self.cursor is None else self.cursor.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this query."""
        asset_id = data.get("asset_id")
        observation_type = data.get("observation_type")
        start_at = data.get("start_at")
        end_at = data.get("end_at")
        cursor = data.get("cursor")
        cursor_data = None if cursor is None else cast(dict[str, object], cursor)
        return cls(
            asset_id=None if asset_id is None else AssetId.from_string(str(asset_id)),
            observation_type=None
            if observation_type is None
            else ObservationType(str(observation_type)),
            start_at=None
            if start_at is None
            else ObservationTimestamp(datetime.fromisoformat(str(start_at))),
            end_at=None
            if end_at is None
            else ObservationTimestamp(datetime.fromisoformat(str(end_at))),
            cursor=None if cursor_data is None else TimelineCursor.from_dict(cursor_data),
        )
