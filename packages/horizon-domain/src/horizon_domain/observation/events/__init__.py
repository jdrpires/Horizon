"""Observation events."""

from horizon_domain.observation.events.observation import (
    ObservationDomainEvent,
    ObservationRegistered,
)

__all__ = ["ObservationDomainEvent", "ObservationRegistered"]
