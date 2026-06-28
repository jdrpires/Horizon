"""Horizon Kernel public package."""

from horizon_kernel.aggregates import AggregateRoot
from horizon_kernel.entities import Entity
from horizon_kernel.events import DomainEvent
from horizon_kernel.exceptions import (
    BusinessError,
    DomainException,
    DomainRuleViolation,
    Error,
    InfrastructureError,
    UnexpectedError,
    ValidationError,
)
from horizon_kernel.ids import UniqueId
from horizon_kernel.shared import Result
from horizon_kernel.utils import Clock, FrozenClock, SystemClock
from horizon_kernel.value_objects import (
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
    ValueObject,
    Voltage,
)

__all__ = [
    "RPM",
    "AggregateRoot",
    "BusinessError",
    "Clock",
    "Confidence",
    "Distance",
    "DomainEvent",
    "DomainException",
    "DomainRuleViolation",
    "Duration",
    "Entity",
    "Error",
    "FrozenClock",
    "FuelLevel",
    "HealthScore",
    "InfrastructureError",
    "Latitude",
    "Longitude",
    "Money",
    "Percentage",
    "Result",
    "Speed",
    "SystemClock",
    "Temperature",
    "Timestamp",
    "UnexpectedError",
    "UniqueId",
    "ValidationError",
    "ValueObject",
    "Voltage",
]
