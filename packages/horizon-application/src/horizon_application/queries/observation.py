"""Application queries for Observations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ListObservationsQuery:
    """List registered Observations."""
