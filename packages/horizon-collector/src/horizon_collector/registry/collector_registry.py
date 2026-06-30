"""Collector registry."""

from __future__ import annotations

from horizon_collector.contracts import Collector
from horizon_collector.exceptions import CollectorAlreadyRegisteredError, CollectorNotFoundError


class CollectorRegistry:
    """Registry for available collectors."""

    def __init__(self) -> None:
        """Create an empty registry."""
        self._collectors: dict[str, Collector] = {}

    @property
    def names(self) -> tuple[str, ...]:
        """Return registered collector names."""
        return tuple(self._collectors)

    def register(self, collector: Collector) -> None:
        """Register a collector."""
        name = collector.name.strip()
        if not name:
            raise ValueError("collector name cannot be blank.")
        if name in self._collectors:
            raise CollectorAlreadyRegisteredError(name)
        self._collectors[name] = collector

    def get(self, name: str) -> Collector:
        """Return a registered collector."""
        try:
            return self._collectors[name.strip()]
        except KeyError as exc:
            raise CollectorNotFoundError(name) from exc
