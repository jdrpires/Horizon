"""Behavior tests for the Asset aggregate."""

from datetime import UTC, datetime

import pytest

from horizon_domain import (
    ActivateAsset,
    ArchiveAsset,
    Asset,
    AssetActivated,
    AssetArchived,
    AssetClassification,
    AssetConfiguration,
    AssetConfigurationChanged,
    AssetDeactivated,
    AssetId,
    AssetIdentity,
    AssetRegistered,
    AssetStatus,
    AssetTransferred,
    DeactivateAsset,
    Ownership,
    RegisterAsset,
    TransferOwnership,
    UpdateConfiguration,
)
from horizon_kernel import DomainException, FrozenClock


def test_register_asset_creates_registered_aggregate_and_event() -> None:
    asset_id = AssetId.new()
    command = RegisterAsset(
        asset_id=asset_id,
        identity=AssetIdentity("Warehouse Gateway", "asset-001"),
        classification=AssetClassification("infrastructure.gateway", "gateway"),
        ownership=Ownership("tenant-a", "tenant-a"),
        configuration=AssetConfiguration({"region": "south"}),
    )

    asset = Asset.register(command, _clock())

    assert asset.asset_id == asset_id
    assert asset.identity.name == "Warehouse Gateway"
    assert asset.status is AssetStatus.REGISTERED
    assert len(asset.domain_events) == 1
    assert isinstance(asset.domain_events[0], AssetRegistered)
    assert asset.domain_events[0].payload["status"] == "registered"


def test_activate_deactivate_and_archive_record_domain_events() -> None:
    asset = _registered_asset()

    asset.activate(ActivateAsset(asset_id=asset.asset_id), _clock())
    asset.deactivate(DeactivateAsset(asset_id=asset.asset_id, reason="paused"), _clock())
    asset.archive(ArchiveAsset(asset_id=asset.asset_id, reason="retired"), _clock())

    assert asset.status is AssetStatus.ARCHIVED
    assert [type(event) for event in asset.domain_events] == [
        AssetRegistered,
        AssetActivated,
        AssetDeactivated,
        AssetArchived,
    ]
    assert asset.domain_events[-1].payload["reason"] == "retired"


def test_archived_asset_cannot_be_activated_or_modified() -> None:
    asset = _registered_asset()
    asset.archive(ArchiveAsset(asset_id=asset.asset_id), _clock())

    with pytest.raises(DomainException, match="Archived Asset cannot be activated"):
        asset.activate(ActivateAsset(asset_id=asset.asset_id), _clock())
    with pytest.raises(DomainException, match="Archived Asset cannot transfer ownership"):
        asset.transfer_ownership(
            TransferOwnership(asset_id=asset.asset_id, ownership=Ownership("tenant-b")),
            _clock(),
        )
    with pytest.raises(DomainException, match="Archived Asset cannot change configuration"):
        asset.update_configuration(
            UpdateConfiguration(asset_id=asset.asset_id, configuration=AssetConfiguration({"x": "y"})),
            _clock(),
        )


def test_transfer_ownership_and_configuration_changes_emit_events() -> None:
    asset = _registered_asset()

    asset.transfer_ownership(
        TransferOwnership(asset_id=asset.asset_id, ownership=Ownership("tenant-b")),
        _clock(),
    )
    asset.update_configuration(
        UpdateConfiguration(asset_id=asset.asset_id, configuration=AssetConfiguration({"mode": "managed"})),
        _clock(),
    )

    assert asset.ownership.owner_id == "tenant-b"
    assert asset.configuration.values["mode"] == "managed"
    assert isinstance(asset.domain_events[-2], AssetTransferred)
    assert isinstance(asset.domain_events[-1], AssetConfigurationChanged)


def test_id_never_changes_and_commands_must_target_same_asset() -> None:
    asset = _registered_asset()
    original_id = asset.asset_id

    with pytest.raises(DomainException, match="different Asset"):
        asset.activate(ActivateAsset(asset_id=AssetId.new()), _clock())

    assert asset.asset_id == original_id


def test_idempotent_noop_commands_do_not_emit_extra_events() -> None:
    asset = _registered_asset()

    asset.activate(ActivateAsset(asset_id=asset.asset_id), _clock())
    asset.activate(ActivateAsset(asset_id=asset.asset_id), _clock())
    asset.transfer_ownership(
        TransferOwnership(asset_id=asset.asset_id, ownership=asset.ownership),
        _clock(),
    )
    asset.update_configuration(
        UpdateConfiguration(asset_id=asset.asset_id, configuration=asset.configuration),
        _clock(),
    )

    assert [type(event) for event in asset.domain_events] == [AssetRegistered, AssetActivated]


def _registered_asset() -> Asset:
    return Asset.register(
        RegisterAsset(
            identity=AssetIdentity("Asset One"),
            classification=AssetClassification("generic.asset"),
            ownership=Ownership("tenant-a"),
            configuration=AssetConfiguration({"timezone": "UTC"}),
        ),
        _clock(),
    )


def _clock() -> FrozenClock:
    return FrozenClock(datetime(2026, 1, 1, tzinfo=UTC))
