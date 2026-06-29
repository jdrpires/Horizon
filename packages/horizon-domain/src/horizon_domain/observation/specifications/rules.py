"""Observation specification helpers."""

from horizon_domain.observation.value_objects.observation import KNOWN_OBSERVATION_TYPES


def is_known_observation_type(value: str) -> bool:
    """Return whether an observation type is known."""
    return value.strip().lower() in KNOWN_OBSERVATION_TYPES
