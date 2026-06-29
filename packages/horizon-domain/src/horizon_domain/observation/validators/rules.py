"""Observation validation helpers."""

from horizon_domain.asset import AssetId
from horizon_kernel import DomainException, ValidationError


def ensure_asset_id(asset_id: AssetId | None) -> AssetId:
    """Ensure an Observation references an Asset."""
    if asset_id is None:
        raise DomainException(
            ValidationError("observation.asset_id.required", "Observation must reference an Asset.")
        )
    return asset_id
