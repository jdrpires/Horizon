"""Map OBD observations through the Horizon Collector Framework."""

from __future__ import annotations

from horizon_catalog import ObservationCatalogRegistry
from horizon_collector.mapping import CatalogObservationMapper, ObservationSourceMapping

from collector_obd.pids import supported_pids


class ObdObservationMapper(CatalogObservationMapper):
    """Catalog-backed mapper for supported OBD PIDs."""

    def __init__(self, *, catalog: ObservationCatalogRegistry) -> None:
        """Create the mapper with OBD PID to catalog mappings."""
        super().__init__(
            catalog=catalog,
            source_mappings=tuple(
                ObservationSourceMapping(
                    external_key=pid.external_key,
                    catalog_key=pid.catalog_key,
                )
                for pid in supported_pids()
            ),
        )
