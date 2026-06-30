"""Asset JSON serializer."""

from __future__ import annotations

from datetime import datetime

from horizon_domain import (
    Asset,
    AssetClassification,
    AssetConfiguration,
    AssetId,
    AssetIdentity,
    AssetStatus,
    Ownership,
)


class AssetSerializer:
    """Serialize and deserialize Asset facts."""

    def serialize(self, value: Asset) -> dict[str, object]:
        """Serialize an Asset aggregate."""
        return {
            "asset_id": value.asset_id.to_string(),
            "identity": value.identity.to_dict(),
            "classification": value.classification.to_dict(),
            "ownership": value.ownership.to_dict(),
            "configuration": value.configuration.to_dict(),
            "status": value.status.value,
            "version": value.version,
            "created_at": value.created_at.isoformat(),
            "updated_at": value.updated_at.isoformat(),
        }

    def deserialize(self, payload: dict[str, object]) -> Asset:
        """Deserialize an Asset aggregate without producing domain events."""
        return Asset(
            asset_id=AssetId.from_string(str(payload["asset_id"])),
            identity=AssetIdentity.from_dict(_object(payload["identity"])),
            classification=AssetClassification.from_dict(_object(payload["classification"])),
            ownership=Ownership.from_dict(_object(payload["ownership"])),
            configuration=AssetConfiguration.from_dict(_object(payload["configuration"])),
            status=AssetStatus(str(payload["status"])),
            created_at=datetime.fromisoformat(str(payload["created_at"])),
            updated_at=datetime.fromisoformat(str(payload["updated_at"])),
            version=int(payload["version"]),
        )


def _object(value: object) -> dict[str, object]:
    """Return a dictionary payload."""
    if not isinstance(value, dict):
        raise ValueError("Expected an object payload.")
    return value
