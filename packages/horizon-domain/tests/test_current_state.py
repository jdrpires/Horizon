"""Current State behavior tests."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from horizon_domain import AssetId
from horizon_domain.current_state import CurrentStateBuilder
from horizon_domain.current_state.specifications import is_snapshot_immutable
from horizon_domain.observation import (
    Observation,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
    RegisterObservation,
)
from horizon_domain.timeline import Timeline
from horizon_kernel import FrozenClock


def test_current_state_keeps_latest_value_by_type() -> None:
    asset_id = AssetId.new()
    timeline = Timeline(asset_id=asset_id)
    timeline.add_observation(_observation(asset_id, "rpm", 900, "rpm", 10), 1)
    timeline.add_observation(_observation(asset_id, "rpm", 2400, "rpm", 11), 2)
    timeline.add_observation(_observation(asset_id, "rpm", 1100, "rpm", 12), 3)
    timeline.add_observation(_observation(asset_id, "voltage", 14.18, "volt", 14), 4)

    snapshot = CurrentStateBuilder().build(asset_id=asset_id, entries=timeline.entries)

    assert snapshot.observation_count == 4
    assert snapshot.value_for("rpm") is not None
    assert snapshot.value_for("rpm").value == 1100.0  # type: ignore[union-attr]
    assert snapshot.value_for("voltage").value == 14.18  # type: ignore[union-attr]
    assert snapshot.last_updated_at == datetime(2026, 1, 1, 8, 14, tzinfo=UTC)


def test_current_state_snapshot_is_immutable() -> None:
    asset_id = AssetId.new()
    snapshot = CurrentStateBuilder().build(asset_id=asset_id, entries=())

    assert is_snapshot_immutable(snapshot)
    with pytest.raises(FrozenInstanceError):
        setattr(snapshot, "observation_count", 1)


def _observation(asset_id: AssetId, observation_type: str, value: float, unit: str, minute: int) -> Observation:
    command = RegisterObservation(
        asset_id=asset_id,
        observation_type=ObservationType(observation_type),
        value=ObservationValue(value),
        unit=ObservationUnit(unit),
        source=ObservationSource("manual"),
        timestamp=ObservationTimestamp(datetime(2026, 1, 1, 8, minute, tzinfo=UTC)),
        quality=ObservationQuality.GOOD,
    )
    return Observation.register(command, FrozenClock(datetime(2026, 1, 1, 9, 0, tzinfo=UTC)))
