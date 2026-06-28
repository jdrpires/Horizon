"""Reusable immutable value objects."""

from horizon_kernel.value_objects.base import ValueObject
from horizon_kernel.value_objects.measurements import (
    RPM,
    Confidence,
    Distance,
    Duration,
    FuelLevel,
    HealthScore,
    Latitude,
    Longitude,
    Money,
    Percentage,
    Speed,
    Temperature,
    Timestamp,
    Voltage,
)

__all__ = [
    "RPM",
    "Confidence",
    "Distance",
    "Duration",
    "FuelLevel",
    "HealthScore",
    "Latitude",
    "Longitude",
    "Money",
    "Percentage",
    "Speed",
    "Temperature",
    "Timestamp",
    "ValueObject",
    "Voltage",
]
