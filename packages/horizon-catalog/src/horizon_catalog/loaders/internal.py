"""Internal catalog loaders."""

from __future__ import annotations

from horizon_catalog.profiles import create_vehicle_catalog
from horizon_catalog.registry import ObservationCatalogRegistry


def load_vehicle_catalog() -> ObservationCatalogRegistry:
    """Load the internal Vehicle catalog."""
    return create_vehicle_catalog()
