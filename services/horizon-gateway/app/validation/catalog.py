"""Observation Catalog validation for gateway payloads."""

from __future__ import annotations

from horizon_catalog import ObservationCatalogRegistry, ValueType, validate_value
from horizon_catalog.exceptions import DefinitionNotFoundError

from app.schemas import ObservationItem


def validate_catalog_item(
    *,
    catalog: ObservationCatalogRegistry,
    item: ObservationItem,
) -> object:
    """Validate one gateway item against the official Observation Catalog."""
    try:
        definition = catalog.get(item.definition_id)
    except DefinitionNotFoundError as exc:
        raise ValueError(f"definition_id not found: {item.definition_id}") from exc
    if definition.value_type is not ValueType.NUMBER:
        raise ValueError(
            "definition_id exists but is not supported by the current numeric runtime: "
            f"{item.definition_id}"
        )
    if item.unit != definition.unit:
        raise ValueError(
            f"unit mismatch for {item.definition_id}: expected {definition.unit}, got {item.unit}"
        )
    return validate_value(definition, item.value)

