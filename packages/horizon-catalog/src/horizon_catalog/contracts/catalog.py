"""Catalog contracts."""

from __future__ import annotations

from typing import Protocol

from horizon_catalog.models import ObservationDefinition


class ObservationCatalog(Protocol):
    """Contract for Observation catalogs."""

    @property
    def definitions(self) -> tuple[ObservationDefinition, ...]:
        """Return enabled definitions."""

    @property
    def categories(self) -> tuple[str, ...]:
        """Return enabled categories."""

    def get(self, definition_id: str) -> ObservationDefinition:
        """Return a definition by ID."""

    def find_by_alias(self, alias: str) -> ObservationDefinition:
        """Return a definition by alias."""

    def by_category(self, category: str) -> tuple[ObservationDefinition, ...]:
        """Return definitions for one category."""
