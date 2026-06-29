"""Observation value object tests."""

from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from horizon_domain.observation import (
    ObservationId,
    ObservationQuality,
    ObservationSource,
    ObservationTimestamp,
    ObservationType,
    ObservationUnit,
    ObservationValue,
)
from horizon_domain.observation.specifications import is_known_observation_type
from horizon_kernel import DomainException


def test_observation_id_serializes_and_is_immutable() -> None:
    observation_id = ObservationId.new()

    assert ObservationId.from_string(observation_id.to_string()) == observation_id
    assert ObservationId.from_dict(observation_id.to_dict()) == observation_id
    with pytest.raises(FrozenInstanceError):
        setattr(observation_id, "value", ObservationId.new().value)


def test_observation_type_rejects_unknown_values() -> None:
    assert ObservationType("Temperature").value == "temperature"
    assert is_known_observation_type("rpm")
    with pytest.raises(DomainException, match="not a known observation type"):
        ObservationType("unknown")


def test_observation_value_rejects_invalid_numbers() -> None:
    assert ObservationValue(1).value == 1.0
    with pytest.raises(DomainException, match="must be finite"):
        ObservationValue(float("nan"))


def test_unit_source_and_timestamp_validate_required_shape() -> None:
    assert ObservationUnit("celsius").to_dict() == {"value": "celsius"}
    assert ObservationSource("manual").to_dict() == {"value": "manual"}
    assert ObservationQuality.GOOD.value == "good"

    with pytest.raises(DomainException, match="unit cannot be blank"):
        ObservationUnit(" ")
    with pytest.raises(DomainException, match="source cannot be blank"):
        ObservationSource(" ")
    with pytest.raises(DomainException, match="timezone-aware"):
        ObservationTimestamp(datetime(2026, 1, 1))
