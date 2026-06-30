"""Current State application flow tests."""

from horizon_application import (
    ApplicationService,
    GetCurrentStateQuery,
    RegisterAssetCommand,
    RegisterObservationCommand,
)


def test_current_state_is_built_from_timeline_replay() -> None:
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
            observation_type="voltage",
            value=14.18,
            unit="volt",
            source="manual",
            timestamp="2026-01-01T08:12:00+00:00",
        )
    )

    snapshot = service.get_current_state(GetCurrentStateQuery(asset_id=asset.asset_id))

    assert snapshot.observation_count == 3
    assert snapshot.last_updated_at == "2026-01-01T08:12:00+00:00"
    assert {value.observation_type: value.value for value in snapshot.values} == {
        "rpm": 2400.0,
        "voltage": 14.18,
    }
