"""Catalog-backed observation mapper."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from horizon_catalog import ObservationCatalogRegistry, validate_value

from horizon_collector.collector import CanonicalObservation, RawObservation
from horizon_collector.exceptions import ObservationMappingError
from horizon_collector.validation.observations import ensure_supported_for_current_runtime


@dataclass(frozen=True, slots=True)
class ObservationSourceMapping:
    """Map an external observation key to an official catalog definition."""

    external_key: str
    catalog_key: str

    def __post_init__(self) -> None:
        """Validate mapping."""
        if not self.external_key.strip():
            raise ValueError("external_key cannot be blank.")
        if not self.catalog_key.strip():
            raise ValueError("catalog_key cannot be blank.")


class CatalogObservationMapper:
    """Map raw collector data into catalog-backed observations."""

    def __init__(
        self,
        *,
        catalog: ObservationCatalogRegistry,
        source_mappings: tuple[ObservationSourceMapping, ...] = (),
        current_runtime_numeric_only: bool = True,
    ) -> None:
        """Create the mapper."""
        self._catalog = catalog
        self._source_mappings = {
            mapping.external_key.strip(): mapping.catalog_key.strip() for mapping in source_mappings
        }
        self._current_runtime_numeric_only = current_runtime_numeric_only

    def map(self, raw_observation: RawObservation) -> CanonicalObservation:
        """Map one raw external observation into an official canonical observation."""
        catalog_key = self._source_mappings.get(raw_observation.key, raw_observation.key)
        try:
            definition = self._catalog.find_by_alias(catalog_key)
            if self._current_runtime_numeric_only:
                ensure_supported_for_current_runtime(definition)
            value = validate_value(definition, raw_observation.value)
        except Exception as exc:
            raise ObservationMappingError(raw_observation.key, str(exc)) from exc
        observed_at = raw_observation.observed_at or datetime.now(UTC)
        return CanonicalObservation(
            definition=definition,
            value=value,
            observed_at=observed_at,
            source=raw_observation.source,
            metadata={
                "external_key": raw_observation.key,
                "catalog_key": definition.id,
                **dict(raw_observation.metadata),
            },
        )

    def map_many(
        self,
        raw_observations: tuple[RawObservation, ...],
    ) -> tuple[CanonicalObservation, ...]:
        """Map many raw external observations."""
        return tuple(self.map(raw_observation) for raw_observation in raw_observations)
