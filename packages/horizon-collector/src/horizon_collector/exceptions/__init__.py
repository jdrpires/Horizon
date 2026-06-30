"""Collector exceptions."""

from horizon_collector.exceptions.errors import (
    CollectorAlreadyRegisteredError,
    CollectorError,
    CollectorNotFoundError,
    ObservationMappingError,
    UnsupportedObservationValueTypeError,
)

__all__ = [
    "CollectorAlreadyRegisteredError",
    "CollectorError",
    "CollectorNotFoundError",
    "ObservationMappingError",
    "UnsupportedObservationValueTypeError",
]
