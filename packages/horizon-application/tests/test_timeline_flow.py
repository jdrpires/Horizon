"""Timeline application flow tests."""

from horizon_application import (
    ApplicationService,
    GetTimelineQuery,
    RegisterAssetCommand,
    RegisterObservationCommand,
    ReplayTimelineQuery,
)


def test_register_observation_appends_to_timeline_and_replays_in_order() -> None:
    service = ApplicationService.create_in_memory()
    asset = service.register_asset(
        RegisterAssetCommand(name="Asset One", category="generic.asset", owner_id="tenant-a")
    ).asset

    service.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="rpm",
            value=2400,
            unit="rpm",
            source="manual",
            timestamp="2026-01-01T08:11:00+00:00",
        )
    )
    service.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="rpm",
            value=900,
            unit="rpm",
            source="manual",
            timestamp="2026-01-01T08:10:00+00:00",
        )
    )

    timeline = service.show_timeline(GetTimelineQuery(asset_id=asset.asset_id))
    replay = service.replay_timeline(ReplayTimelineQuery(asset_id=asset.asset_id))

    assert [entry.value for entry in timeline.entries] == [900.0, 2400.0]
    assert replay.entries == timeline.entries


def test_timeline_filters_by_type_period_and_cursor() -> None:
    service = ApplicationService.create_in_memory()
    asset = service.register_asset(
        RegisterAssetCommand(name="Asset One", category="generic.asset", owner_id="tenant-a")
    ).asset

    service.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="rpm",
            value=900,
            unit="rpm",
            source="manual",
            timestamp="2026-01-01T08:10:00+00:00",
        )
    )
    service.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="temperature",
            value=23.5,
            unit="celsius",
            source="manual",
            timestamp="2026-01-01T08:11:00+00:00",
        )
    )

    result = service.show_timeline(
        GetTimelineQuery(
            asset_id=asset.asset_id,
            observation_type="temperature",
            start_at="2026-01-01T08:10:30+00:00",
            end_at="2026-01-01T08:12:00+00:00",
            cursor_at="2026-01-01T08:11:00+00:00",
        )
    )

    assert len(result.entries) == 1
    assert result.entries[0].observation_type == "temperature"
