"""Application commands for Observation use cases."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterObservationCommand:
    """Application command to register an Observation."""

    asset_id: str
    observation_type: str
    value: float
    unit: str
    source: str
    timestamp: str | None = None
    quality: str = "good"

    def validate(self) -> None:
        """Validate required command fields."""
        for field_name, value in {
            "asset_id": self.asset_id,
            "observation_type": self.observation_type,
            "unit": self.unit,
            "source": self.source,
        }.items():
            if not value.strip():
                raise ValueError(f"{field_name} is required.")
