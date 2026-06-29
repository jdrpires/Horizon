"""Timeline behavior tests."""

from datetime import UTC, datetime

from horizon_domain import AssetId
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
from horizon_domain.timeline import ReplayEngine, Timeline, TimelineCursor, TimelineQuery
from horizon_domain.timeline.specifications import is_chronological
from horizon_kernel import FrozenClock


def test_timeline_orders_entries_chronologically() -> None:
    asset_id = AssetId.new()
    timeline = Timeline(asset_id=asset_id)

    second = _observation(asset_id, "rpm", 2400, "rpm", datetime(2026, 1, 1, 8, 11, tzinfo=UTC))
    first = _observation(
        asset_id, "temperature", 23.5, "celsius", datetime(2026, 1, 1, 8, 10, tzinfo=UTC)
    )

    timeline.add_observation(second, sequence=1)
    timeline.add_observation(first, sequence=2)

    assert [entry.observation_type.value for entry in timeline.entries] == ["temperature", "rpm"]
    assert is_chronological(timeline.entries)


def test_replay_engine_is_deterministic_for_equal_timestamps() -> None:
    asset_id = AssetId.new()
    timestamp = datetime(2026, 1, 1, 8, 10, tzinfo=UTC)
    timeline = Timeline(asset_id=asset_id)
    first = timeline.add_observation(_observation(asset_id, "rpm", 900, "rpm", timestamp), 1)
    second = timeline.add_observation(_observation(asset_id, "voltage", 14.1, "volt", timestamp), 2)

    assert ReplayEngine().replay((second, first)) == (first, second)


def test_timeline_query_validates_period_and_cursor() -> None:
    asset_id = AssetId.new()
    query = TimelineQuery(
        asset_id=asset_id,
        observation_type=ObservationType("rpm"),
        start_at=ObservationTimestamp(datetime(2026, 1, 1, 8, 10, tzinfo=UTC)),
        end_at=ObservationTimestamp(datetime(2026, 1, 1, 8, 20, tzinfo=UTC)),
        cursor=TimelineCursor(datetime(2026, 1, 1, 8, 15, tzinfo=UTC)),
    )

    assert query.to_dict()["asset_id"] == asset_id.to_string()
    assert query.to_dict()["observation_type"] == "rpm"


def _observation(
    asset_id: AssetId,
    observation_type: str,
    value: float,
    unit: str,
    timestamp: datetime,
) -> Observation:
    command = RegisterObservation(
        asset_id=asset_id,
        observation_type=ObservationType(observation_type),
        value=ObservationValue(value),
        unit=ObservationUnit(unit),
        source=ObservationSource("manual"),
        timestamp=ObservationTimestamp(timestamp),
        quality=ObservationQuality.GOOD,
    )
    return Observation.register(command, FrozenClock(datetime(2026, 1, 1, 9, 0, tzinfo=UTC)))
