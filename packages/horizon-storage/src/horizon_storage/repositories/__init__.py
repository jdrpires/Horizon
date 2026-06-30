"""Storage repositories."""

from horizon_storage.repositories.json_repositories import (
    JsonAssetRepository,
    JsonObservationRepository,
)

__all__ = ["JsonAssetRepository", "JsonObservationRepository"]
