"""Observation catalog registry."""

from __future__ import annotations

from collections import defaultdict

from horizon_catalog.exceptions import DefinitionNotFoundError
from horizon_catalog.models import ObservationDefinition


class ObservationCatalogRegistry:
    """Registry for official Observation definitions."""

    def __init__(self, definitions: tuple[ObservationDefinition, ...]) -> None:
        """Create the registry."""
        self._definitions = tuple(sorted(definitions, key=lambda item: item.display_order))
        self._by_id = {definition.id: definition for definition in self._definitions}
        self._by_alias: dict[str, ObservationDefinition] = {}
        self._by_category: dict[str, list[ObservationDefinition]] = defaultdict(list)
        for definition in self._definitions:
            self._by_category[definition.category].append(definition)
            for alias in definition.aliases:
                self._by_alias[alias.lower()] = definition

    @property
    def definitions(self) -> tuple[ObservationDefinition, ...]:
        """Return enabled definitions in display order."""
        return tuple(definition for definition in self._definitions if definition.enabled)

    @property
    def categories(self) -> tuple[str, ...]:
        """Return categories in display order."""
        seen: list[str] = []
        for definition in self.definitions:
            if definition.category not in seen:
                seen.append(definition.category)
        return tuple(seen)

    def get(self, definition_id: str) -> ObservationDefinition:
        """Return a definition by ID."""
        try:
            definition = self._by_id[definition_id]
        except KeyError as exc:
            raise DefinitionNotFoundError(definition_id) from exc
        if not definition.enabled:
            raise DefinitionNotFoundError(definition_id)
        return definition

    def find_by_alias(self, alias: str) -> ObservationDefinition:
        """Return a definition by alias."""
        clean = alias.strip().lower()
        if clean in self._by_id and self._by_id[clean].enabled:
            return self._by_id[clean]
        try:
            definition = self._by_alias[clean]
        except KeyError as exc:
            raise DefinitionNotFoundError(alias) from exc
        if not definition.enabled:
            raise DefinitionNotFoundError(alias)
        return definition

    def by_category(self, category: str) -> tuple[ObservationDefinition, ...]:
        """Return definitions for one category."""
        return tuple(definition for definition in self._by_category[category] if definition.enabled)
