"""Observation domain commands."""

from __future__ import annotations

from dataclasses import dataclass, field

from horizon_domain.asset import AssetId
from horizon_domain.observation.value_objects import (
    ObservationId,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
)
from horizon_kernel import UniqueId


@dataclass(frozen=True, slots=True)
class RegisterObservation:
    """Register a new Observation."""

    asset_id: AssetId
    observation_type: ObservationType
    value: ObservationValue
    unit: ObservationUnit
    source: ObservationSource
    timestamp: ObservationTimestamp
    quality: ObservationQuality = ObservationQuality.GOOD
    observation_id: ObservationId = field(default_factory=ObservationId.new)
    correlation_id: UniqueId = field(default_factory=UniqueId.new)
    causation_id: UniqueId = field(default_factory=UniqueId.new)
