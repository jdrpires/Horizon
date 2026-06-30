"""Collector framework protocols."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from horizon_collector.collector import CanonicalObservation, RawObservation

if TYPE_CHECKING:
    from horizon_collector.runtime.session import CollectorSession


class Collector(Protocol):
    """External source collector independent from transport details."""

    @property
    def name(self) -> str:
        """Return the collector name."""
        ...

    def collect(self, session: CollectorSession) -> tuple[RawObservation, ...]:
        """Collect raw observations for one session."""
        ...


class CollectorAdapter(Protocol):
    """Transport adapter boundary hidden behind collectors."""

    def read(self) -> tuple[RawObservation, ...]:
        """Read raw observations from an external source."""
        ...


class ObservationMapper(Protocol):
    """Map raw external observations to catalog-backed observations."""

    def map(self, raw_observation: RawObservation) -> CanonicalObservation:
        """Map one raw observation."""
        ...

    def map_many(
        self,
        raw_observations: tuple[RawObservation, ...],
    ) -> tuple[CanonicalObservation, ...]:
        """Map many raw observations."""
        ...


class ObservationPublisher(Protocol):
    """Publish canonical observations into Horizon through an outer boundary."""

    def publish(self, observation: CanonicalObservation) -> None:
        """Publish one canonical observation."""
        ...

    def publish_many(self, observations: tuple[CanonicalObservation, ...]) -> None:
        """Publish many canonical observations."""
        ...


class CollectorRuntime(Protocol):
    """Runtime capable of executing registered collectors."""

    def run_once(self, collector_name: str) -> tuple[CanonicalObservation, ...]:
        """Execute one collector once and publish mapped observations."""
        ...
