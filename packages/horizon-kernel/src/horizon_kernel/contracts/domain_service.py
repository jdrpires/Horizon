"""Domain service interface."""

from typing import Protocol


class DomainService(Protocol):
    """Marker protocol for stateless domain services."""
