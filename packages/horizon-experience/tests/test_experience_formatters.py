"""Experience formatter tests."""

from horizon_experience.formatters import friendly_observation_type, friendly_time, friendly_unit
from horizon_experience.validators import parse_float, parse_optional_datetime, validate_non_empty


def test_friendly_labels_hide_technical_observation_names() -> None:
    assert friendly_observation_type("temperature") == "Temperatura"
    assert friendly_unit("volt") == "V"


def test_friendly_time_formats_iso_datetime() -> None:
    assert friendly_time("2026-01-01T08:10:00+00:00") == "01/01/2026 08:10"


def test_input_validators_reject_invalid_values() -> None:
    assert validate_non_empty(" Asset ", "Nome") == "Asset"
    assert parse_float("23,5", "Valor") == 23.5
    assert parse_optional_datetime("") is None
