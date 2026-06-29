"""Asset application DTOs."""

from __future__ import annotations

from dataclasses import dataclass

from horizon_domain import Asset
from horizon_events import EventEnvelope


@dataclass(frozen=True, slots=True)
class AssetDTO:
    """Serializable view of an Asset aggregate."""

    asset_id: str
    name: str
    external_reference: str | None
    category: str
    kind: str | None
    owner_id: str
    tenant_id: str | None
    status: str
    configuration: dict[str, object]
    version: int

    @classmethod
    def from_asset(cls, asset: Asset) -> AssetDTO:
        """Map an Asset aggregate to a DTO."""
        return cls(
            asset_id=asset.asset_id.to_string(),
            name=asset.identity.name,
            external_reference=asset.identity.external_reference,
            category=asset.classification.category,
            kind=asset.classification.kind,
            owner_id=asset.ownership.owner_id,
            tenant_id=asset.ownership.tenant_id,
            status=asset.status.value,
            configuration=dict(asset.configuration.values),
            version=asset.version,
        )

    def to_dict(self) -> dict[str, object]:
        """Serialize the DTO."""
        return {
            "asset_id": self.asset_id,
            "name": self.name,
            "external_reference": self.external_reference,
            "category": self.category,
            "kind": self.kind,
            "owner_id": self.owner_id,
            "tenant_id": self.tenant_id,
            "status": self.status,
            "configuration": self.configuration,
            "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class EventEnvelopeDTO:
    """Serializable view of an Event Envelope."""

    event_name: str
    data: dict[str, object]

    @classmethod
    def from_envelope(cls, envelope: EventEnvelope) -> EventEnvelopeDTO:
        """Map an envelope to a DTO."""
        return cls(event_name=envelope.event_name.value, data=envelope.to_dict())


@dataclass(frozen=True, slots=True)
class RegisterAssetResultDTO:
    """Result returned by the Register Asset use case."""

    asset: AssetDTO
    events: tuple[EventEnvelopeDTO, ...]
