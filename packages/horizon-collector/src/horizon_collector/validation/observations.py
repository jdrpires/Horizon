"""Observation validation for collector ingestion."""

from __future__ import annotations

from horizon_catalog import ObservationDefinition, ValueType

from horizon_collector.exceptions import UnsupportedObservationValueTypeError


def ensure_supported_for_current_runtime(definition: ObservationDefinition) -> None:
    """Ensure the current Observation runtime can receive the definition."""
    if definition.value_type is not ValueType.NUMBER:
        raise UnsupportedObservationValueTypeError(definition.id, definition.value_type.value)
