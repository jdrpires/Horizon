"""Observation application flow tests."""

from horizon_application import (
    ApplicationService,
    RegisterAssetCommand,
    RegisterObservationCommand,
)
from horizon_events import EventEnvelope, EventSubscriber


def test_register_observation_requires_existing_asset_and_publishes_event() -> None:
    seen: list[EventEnvelope] = []
    service = ApplicationService.create_in_memory(
        event_subscribers=(EventSubscriber("test-console", seen.append),)
    )
    asset = service.register_asset(
        RegisterAssetCommand(name="Asset One", category="generic.asset", owner_id="tenant-a")
    ).asset

    result = service.register_observation(
        RegisterObservationCommand(
            asset_id=asset.asset_id,
            observation_type="temperature",
            value=23.5,
            unit="celsius",
            source="manual",
        )
    )

    assert result.observation.asset_id == asset.asset_id
    assert result.observation.observation_type == "temperature"
    assert result.events[0].event_name == "ObservationRegistered"
    assert seen[-1].event_name.value == "ObservationRegistered"
    assert service.list_observations()[0].observation_id == result.observation.observation_id


def test_register_observation_rejects_missing_asset() -> None:
    service = ApplicationService.create_in_memory()

    try:
        service.register_observation(
            RegisterObservationCommand(
                asset_id="00000000-0000-0000-0000-000000000000",
                observation_type="temperature",
                value=23.5,
                unit="celsius",
                source="manual",
            )
        )
    except ValueError as exc:
        assert "existing Asset" in str(exc)
    else:
        raise AssertionError("Observation without Asset was accepted")
