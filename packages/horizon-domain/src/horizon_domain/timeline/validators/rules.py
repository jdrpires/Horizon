"""Timeline validation helpers."""

from __future__ import annotations

from datetime import datetime

from horizon_kernel import DomainException, ValidationError


def ensure_timezone_aware(value: datetime, field: str) -> datetime:
    """Validate a timezone-aware datetime."""
    if value.tzinfo is None:
        raise DomainException(
            ValidationError("timeline.timestamp.timezone", f"{field} must be timezone-aware.")
        )
    return value
