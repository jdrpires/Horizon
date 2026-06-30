"""Value validation for catalog definitions."""

from __future__ import annotations

from datetime import datetime
from math import isfinite

from horizon_catalog.models import ObservationDefinition, ValueType


def validate_value(definition: ObservationDefinition, value: object) -> object:
    """Validate and normalize a value for an Observation definition."""
    if definition.value_type is ValueType.NUMBER:
        return _number(value)
    if definition.value_type is ValueType.TEXT:
        return _text(value)
    if definition.value_type is ValueType.BOOLEAN:
        return _boolean(value)
    if definition.value_type is ValueType.ENUM:
        return _enum(definition, value)
    if definition.value_type is ValueType.DATETIME:
        return _datetime(value)
    raise ValueError("Tipo de valor não suportado.")


def _number(value: object) -> float:
    """Validate a number value."""
    try:
        parsed = float(str(value).replace(",", "."))
    except ValueError as exc:
        raise ValueError("Valor precisa ser um número válido.") from exc
    if not isfinite(parsed):
        raise ValueError("Valor precisa ser um número válido.")
    return parsed


def _text(value: object) -> str:
    """Validate a text value."""
    parsed = str(value).strip()
    if not parsed:
        raise ValueError("Valor de texto não pode ficar em branco.")
    return parsed


def _boolean(value: object) -> bool:
    """Validate a boolean value."""
    if isinstance(value, bool):
        return value
    parsed = str(value).strip().lower()
    if parsed in {"true", "sim", "s", "1", "yes"}:
        return True
    if parsed in {"false", "nao", "não", "n", "0", "no"}:
        return False
    raise ValueError("Valor precisa ser verdadeiro ou falso.")


def _enum(definition: ObservationDefinition, value: object) -> str:
    """Validate an enum value."""
    parsed = str(value).strip()
    if parsed in definition.enum_values:
        return parsed
    raise ValueError("Valor precisa ser uma opção do catálogo.")


def _datetime(value: object) -> str:
    """Validate a datetime value."""
    parsed = str(value).strip()
    try:
        datetime.fromisoformat(parsed)
    except ValueError as exc:
        raise ValueError("Valor precisa ser uma data/hora ISO válida.") from exc
    return parsed
