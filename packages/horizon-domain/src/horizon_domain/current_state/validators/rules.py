"""Current State validators."""

from __future__ import annotations

from horizon_domain.asset import AssetId


def ensure_asset_id(asset_id: AssetId) -> AssetId:
    """Return a validated Asset ID."""
    if not isinstance(asset_id, AssetId):
        raise TypeError("asset_id must be an AssetId.")
    return asset_id
