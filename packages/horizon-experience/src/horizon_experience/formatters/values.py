"""Human-friendly value formatting."""

from __future__ import annotations

from datetime import datetime

OBSERVATION_LABELS = {
    "temperature": "Temperatura",
    "rpm": "RPM",
    "fuel_level": "Combustível",
    "voltage": "Bateria",
    "speed": "Velocidade",
    "distance": "Distância",
    "pressure": "Pressão",
    "humidity": "Umidade",
    "location": "Localização",
    "generic": "Observação",
}

UNIT_LABELS = {
    "celsius": "°C",
    "rpm": "rpm",
    "volt": "V",
    "volts": "V",
    "percent": "%",
}

SOURCE_LABELS = {
    "manual": "Manual",
}


def friendly_observation_type(value: str) -> str:
    """Return a user-facing Observation type label."""
    return OBSERVATION_LABELS.get(value, value.replace("_", " ").title())


def friendly_unit(value: str) -> str:
    """Return a user-facing unit label."""
    return UNIT_LABELS.get(value, value)


def friendly_source(value: str) -> str:
    """Return a user-facing source label."""
    return SOURCE_LABELS.get(value, value.title())


def friendly_value(value: float) -> str:
    """Return a compact numeric value."""
    if value.is_integer():
        return str(int(value))
    return str(value)


def friendly_time(value: str | None) -> str:
    """Return a compact local timestamp label."""
    if value is None:
        return "Sem atualização"
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return value
    return parsed.strftime("%d/%m/%Y %H:%M")
