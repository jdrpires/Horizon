"""Event envelope mapping tests."""

from horizon_application.services import DomainEventEnvelopeMapper
from horizon_domain import Asset, AssetClassification, AssetConfiguration, AssetIdentity, Ownership
from horizon_domain import RegisterAsset as DomainRegisterAsset


def test_domain_event_mapper_preserves_event_identity_and_payload() -> None:
    asset = Asset.register(
        DomainRegisterAsset(
            identity=AssetIdentity("Asset One"),
            classification=AssetClassification("generic.asset"),
            ownership=Ownership("tenant-a"),
            configuration=AssetConfiguration(),
        )
    )
    event = asset.domain_events[0]

    envelope = DomainEventEnvelopeMapper(source="test").map(event)

    assert envelope.event_name.value == "AssetRegistered"
    assert envelope.event["aggregate_id"] == asset.asset_id.to_string()
    assert envelope.metadata.aggregate_id == asset.asset_id.to_string()
    assert envelope.headers["domain_event"] == "AssetRegistered"
