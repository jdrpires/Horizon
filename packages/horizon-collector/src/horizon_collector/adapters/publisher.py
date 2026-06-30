"""Observation publisher adapters."""

from __future__ import annotations

from horizon_collector.collector import CanonicalObservation


class InMemoryObservationPublisher:
    """Publisher that stores canonical observations in memory for tests and demos."""

    def __init__(self) -> None:
        """Create an empty publisher."""
        self._published: list[CanonicalObservation] = []

    @property
    def published(self) -> tuple[CanonicalObservation, ...]:
        """Return published observations."""
        return tuple(self._published)

    def publish(self, observation: CanonicalObservation) -> None:
        """Publish one canonical observation."""
        self._published.append(observation)

    def publish_many(self, observations: tuple[CanonicalObservation, ...]) -> None:
        """Publish many canonical observations."""
        self._published.extend(observations)
