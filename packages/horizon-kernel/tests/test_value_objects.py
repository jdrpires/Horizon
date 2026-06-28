from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from horizon_kernel.exceptions import DomainException
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
    Voltage,
)


def assign_attribute(target: object, name: str, value: object) -> None:
    setattr(target, name, value)


def test_temperature_is_immutable_validated_and_serializable() -> None:
    temperature = Temperature("21.5")

    assert temperature == Temperature(Decimal("21.5"))
    assert Temperature.from_dict(temperature.to_dict()) == temperature
    with pytest.raises(FrozenInstanceError):
        assign_attribute(temperature, "celsius", Decimal("20"))
    with pytest.raises(DomainException):
        Temperature("-274")


def test_percentage_and_bounded_scores() -> None:
    percentage = Percentage("42")
    confidence = Confidence("0.8")
    health = HealthScore(99)
    level = FuelLevel(75)

    assert percentage.to_ratio() == Decimal("0.42")
    assert Confidence.from_dict(confidence.to_dict()) == confidence
    assert HealthScore.from_dict(health.to_dict()) == health
    assert FuelLevel.from_dict(level.to_dict()) == level
    with pytest.raises(DomainException):
        Percentage(101)
    with pytest.raises(DomainException):
        Confidence("1.1")


def test_measurements_reject_negative_values_and_roundtrip() -> None:
    values = [
        Voltage("12.4"),
        Distance(100),
        Duration(timedelta(seconds=30)),
        Speed("7.5"),
    ]

    assert Voltage.from_dict(values[0].to_dict()) == values[0]
    assert Distance.from_dict(values[1].to_dict()) == values[1]
    assert Duration.from_dict(values[2].to_dict()) == values[2]
    assert Speed.from_dict(values[3].to_dict()) == values[3]
    with pytest.raises(DomainException):
        Voltage(-1)
    with pytest.raises(DomainException):
        Distance(-1)
    with pytest.raises(DomainException):
        Duration(-1)
    with pytest.raises(DomainException):
        Speed(-1)


def test_timestamp_requires_timezone_and_normalizes_to_utc() -> None:
    timestamp = Timestamp(datetime(2026, 1, 1, 9, 0, tzinfo=UTC))

    assert Timestamp.from_dict(timestamp.to_dict()) == timestamp
    assert timestamp.value.tzinfo == UTC
    with pytest.raises(DomainException):
        Timestamp(datetime(2026, 1, 1, 9, 0))


def test_coordinates_money_and_rpm() -> None:
    latitude = Latitude("-23.5")
    longitude = Longitude("-46.6")
    money = Money("10.25", "usd")
    rpm = RPM(900)

    assert Latitude.from_dict(latitude.to_dict()) == latitude
    assert Longitude.from_dict(longitude.to_dict()) == longitude
    assert Money.from_dict(money.to_dict()) == money
    assert money.currency == "USD"
    assert RPM.from_dict(rpm.to_dict()) == rpm
    with pytest.raises(DomainException):
        Latitude("-91")
    with pytest.raises(DomainException):
        Longitude("181")
    with pytest.raises(DomainException):
        Money("-1", "USD")
    with pytest.raises(DomainException):
        Money("1", "US")
    with pytest.raises(DomainException):
        RPM(-1)
