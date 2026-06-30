"""Catalog package exports."""

from horizon_catalog.profiles import create_vehicle_catalog
from horizon_catalog.registry import ObservationCatalogRegistry

__all__ = ["ObservationCatalogRegistry", "create_vehicle_catalog"]
