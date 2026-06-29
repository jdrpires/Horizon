"""Register Asset vertical slice tests."""

from horizon_application import ApplicationService, RegisterAssetCommand
from horizon_events import EventEnvelope, EventSubscriber


def test_register_asset_flow_persists_asset_and_publishes_envelope() -> None:
    seen: list[EventEnvelope] = []
    service = ApplicationService.create_in_memory(
        event_subscribers=(EventSubscriber("test-console", seen.append),)
    )

    result = service.register_asset(
        RegisterAssetCommand(name="Asset One", category="generic.asset", owner_id="tenant-a")
    )

    assert result.asset.name == "Asset One"
    assert result.asset.status == "registered"
    assert len(result.events) == 1
    assert result.events[0].event_name == "AssetRegistered"
    assert len(seen) == 1
    assert seen[0].event_name.value == "AssetRegistered"
    assert service.unit_of_work.committed
    assert service.list_assets()[0].asset_id == result.asset.asset_id


def test_application_service_rolls_back_invalid_register_asset() -> None:
    service = ApplicationService.create_in_memory()

    try:
        service.register_asset(RegisterAssetCommand(name="", category="generic.asset", owner_id="owner"))
    except ValueError:
        pass
    else:
        raise AssertionError("invalid command was accepted")

    assert service.unit_of_work.rolled_back is False
    assert service.list_assets() == ()
