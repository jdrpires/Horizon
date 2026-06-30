"""Input validation helpers."""

from __future__ import annotations

from datetime import datetime


def validate_non_empty(value: str, field: str) -> str:
    """Validate non-empty text."""
    clean = value.strip()
    if not clean:
        raise ValueError(f"{field} não pode ficar em branco.")
    return clean


def parse_float(value: str, field: str) -> float:
    """Parse a finite decimal value."""
    clean = validate_non_empty(value, field)
    try:
        parsed = float(clean.replace(",", "."))
    except ValueError as exc:
        raise ValueError(f"{field} precisa ser um número válido.") from exc
    if parsed != parsed or parsed in (float("inf"), float("-inf")):
        raise ValueError(f"{field} precisa ser um número válido.")
    return parsed


def parse_optional_datetime(value: str) -> str | None:
    """Validate an optional ISO-like datetime without changing its value."""
    clean = value.strip()
    if not clean:
        return None
    try:
        datetime.fromisoformat(clean)
    except ValueError as exc:
        raise ValueError(
            "Data/Hora precisa estar em formato ISO. Ex: 2026-01-01T08:10:00+00:00"
        ) from exc
    return clean
