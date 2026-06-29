"""Behavior tests for the Observation aggregate."""

from datetime import UTC, datetime, timedelta

import pytest

from horizon_domain import AssetId
from horizon_domain.observation import (
    Observation,
    ObservationQuality,
    ObservationRegistered,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
    RegisterObservation,
)
from horizon_kernel import DomainException, FrozenClock


def test_register_observation_creates_aggregate_and_event() -> None:
    command = _command()

    observation = Observation.register(command, _clock())

    assert observation.asset_id == command.asset_id
    assert observation.observation_type.value == "temperature"
    assert observation.value.value == 23.5
    assert len(observation.domain_events) == 1
    assert isinstance(observation.domain_events[0], ObservationRegistered)
    assert observation.domain_events[0].payload["type"] == "temperature"


def test_register_observation_rejects_future_timestamp() -> None:
    command = _command(
        timestamp=ObservationTimestamp(datetime(2026, 1, 1, tzinfo=UTC) + timedelta(seconds=1))
    )

    with pytest.raises(DomainException, match="timestamp cannot be in the future"):
        Observation.register(command, _clock())


def _command(timestamp: ObservationTimestamp | None = None) -> RegisterObservation:
    return RegisterObservation(
        asset_id=AssetId.new(),
        observation_type=ObservationType("temperature"),
        value=ObservationValue(23.5),
        unit=ObservationUnit("celsius"),
        source=ObservationSource("manual"),
        timestamp=timestamp or ObservationTimestamp(datetime(2026, 1, 1, tzinfo=UTC)),
        quality=ObservationQuality.GOOD,
    )


def _clock() -> FrozenClock:
    return FrozenClock(datetime(2026, 1, 1, tzinfo=UTC))
