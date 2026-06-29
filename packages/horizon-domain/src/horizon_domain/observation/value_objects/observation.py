"""Value objects for the Observation domain."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import isfinite
from typing import Self

from horizon_domain.asset.validators import ensure_not_blank
from horizon_kernel import DomainException, UniqueId, ValidationError, ValueObject


@dataclass(frozen=True, slots=True)
class ObservationId(ValueObject):
    """Immutable Observation identifier."""

    value: UniqueId

    def __init__(self, value: UniqueId | str | None = None) -> None:
        """Create an Observation ID."""
        resolved = UniqueId.new() if value is None else value
        object.__setattr__(self, "value", resolved if isinstance(resolved, UniqueId) else UniqueId(resolved))

    @classmethod
    def new(cls) -> ObservationId:
        """Create a new Observation ID."""
        return cls()

    @classmethod
    def from_string(cls, value: str) -> ObservationId:
        """Create an Observation ID from a string."""
        return cls(value)

    def to_string(self) -> str:
        """Serialize this Observation ID."""
        return self.value.to_string()

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.to_string()}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(str(data["value"]))

    def __str__(self) -> str:
        """Return this ID as a string."""
        return self.to_string()


class ObservationQuality(StrEnum):
    """Observation quality values."""

    GOOD = "good"
    SUSPECT = "suspect"
    BAD = "bad"


@dataclass(frozen=True, slots=True)
class ObservationType(ValueObject):
    """Known Observation type."""

    value: str

    def __post_init__(self) -> None:
        """Validate Observation type."""
        value = ensure_not_blank(self.value, "observation.type").lower()
        if value not in KNOWN_OBSERVATION_TYPES:
            raise DomainException(
                ValidationError("observation.type.unknown", f"{value} is not a known observation type.")
            )
        object.__setattr__(self, "value", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(str(data["value"]))


@dataclass(frozen=True, slots=True)
class ObservationValue(ValueObject):
    """Finite numeric Observation value."""

    value: float

    def __post_init__(self) -> None:
        """Validate Observation value."""
        numeric_value = float(self.value)
        if not isfinite(numeric_value):
            raise DomainException(
                ValidationError("observation.value.invalid", "Observation value must be finite.")
            )
        object.__setattr__(self, "value", numeric_value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(float(data["value"]))


@dataclass(frozen=True, slots=True)
class ObservationUnit(ValueObject):
    """Observation unit."""

    value: str

    def __post_init__(self) -> None:
        """Validate Observation unit."""
        object.__setattr__(self, "value", ensure_not_blank(self.value, "observation.unit"))

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(str(data["value"]))


@dataclass(frozen=True, slots=True)
class ObservationSource(ValueObject):
    """Observation source."""

    value: str

    def __post_init__(self) -> None:
        """Validate Observation source."""
        object.__setattr__(self, "value", ensure_not_blank(self.value, "observation.source"))

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(str(data["value"]))


@dataclass(frozen=True, slots=True)
class ObservationTimestamp(ValueObject):
    """Observation timestamp."""

    value: datetime

    def __post_init__(self) -> None:
        """Validate timestamp timezone."""
        if self.value.tzinfo is None:
            raise DomainException(
                ValidationError(
                    "observation.timestamp.timezone",
                    "Observation timestamp must be timezone-aware.",
                )
            )

    def ensure_not_future(self, now: datetime) -> None:
        """Reject timestamps after now."""
        if self.value > now:
            raise DomainException(
                ValidationError(
                    "observation.timestamp.future",
                    "Observation timestamp cannot be in the future.",
                )
            )

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.value.isoformat()}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(datetime.fromisoformat(str(data["value"])))


KNOWN_OBSERVATION_TYPES = frozenset(
    {
        "temperature",
        "rpm",
        "fuel_level",
        "voltage",
        "speed",
        "distance",
        "pressure",
        "humidity",
        "location",
        "generic",
    }
)
