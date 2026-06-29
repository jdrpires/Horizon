"""Factory for Observation aggregates."""

from horizon_domain.observation.aggregates import Observation
from horizon_domain.observation.commands import RegisterObservation
from horizon_kernel import Clock


class ObservationFactory:
    """Factory wrapper for Observation registration."""

    @staticmethod
    def register(command: RegisterObservation, clock: Clock | None = None) -> Observation:
        """Create a registered Observation."""
        return Observation.register(command, clock)
