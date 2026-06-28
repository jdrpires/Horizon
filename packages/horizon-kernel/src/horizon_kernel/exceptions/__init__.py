"""Domain exception and error primitives."""

from horizon_kernel.exceptions.domain_exception import DomainException
from horizon_kernel.exceptions.errors import (
    BusinessError,
    DomainRuleViolation,
    Error,
    InfrastructureError,
    UnexpectedError,
    ValidationError,
)

__all__ = [
    "BusinessError",
    "DomainException",
    "DomainRuleViolation",
    "Error",
    "InfrastructureError",
    "UnexpectedError",
    "ValidationError",
]
