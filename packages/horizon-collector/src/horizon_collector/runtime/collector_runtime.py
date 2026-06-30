"""Collector runtime implementation."""

from __future__ import annotations

from horizon_collector.collector import CanonicalObservation
from horizon_collector.contracts import ObservationMapper, ObservationPublisher
from horizon_collector.registry import CollectorRegistry
from horizon_collector.runtime.session import CollectorSession


class InMemoryCollectorRuntime:
    """Execute collectors without transport or infrastructure dependencies."""

    def __init__(
        self,
        *,
        registry: CollectorRegistry,
        mapper: ObservationMapper,
        publisher: ObservationPublisher,
    ) -> None:
        """Create a runtime."""
        self._registry = registry
        self._mapper = mapper
        self._publisher = publisher
        self._sessions: list[CollectorSession] = []

    @property
    def sessions(self) -> tuple[CollectorSession, ...]:
        """Return runtime sessions."""
        return tuple(self._sessions)

    def run_once(self, collector_name: str) -> tuple[CanonicalObservation, ...]:
        """Execute one collector once and publish mapped observations."""
        collector = self._registry.get(collector_name)
        session = CollectorSession(collector_name=collector.name)
        self._sessions.append(session)
        session.start()
        try:
            raw_observations = collector.collect(session)
            canonical = self._mapper.map_many(raw_observations)
            self._publisher.publish_many(canonical)
            session.complete()
            return canonical
        except Exception:
            session.fail()
            raise
