"""Validation helpers for Asset value objects."""

from horizon_kernel import DomainException, ValidationError


def ensure_not_blank(value: str, field: str) -> str:
    """Return a stripped string or raise a validation error."""
    stripped = value.strip()
    if not stripped:
        raise DomainException(ValidationError(f"asset.{field}", f"{field} cannot be blank."))
    return stripped
