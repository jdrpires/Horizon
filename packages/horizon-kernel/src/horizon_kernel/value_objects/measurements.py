"""General-purpose value objects for common measurements and bounded values."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Self

from horizon_kernel.exceptions import DomainException, ValidationError
from horizon_kernel.value_objects.base import ValueObject


def _decimal(value: Decimal | int | float | str, field: str) -> Decimal:
    """Convert numeric input to Decimal."""
    try:
        return Decimal(str(value))
    except InvalidOperation as exc:
        raise DomainException(
            ValidationError("validation.decimal", f"{field} must be a valid decimal.")
        ) from exc


def _require_number(data: dict[str, object], field: str) -> Decimal:
    """Read a numeric field from serialized data."""
    value = data.get(field)
    if not isinstance(value, int | float | str | Decimal):
        raise DomainException(ValidationError("validation.required", f"{field} is required."))
    return _decimal(value, field)


@dataclass(frozen=True, slots=True)
class Temperature(ValueObject):
    """Temperature measured in Celsius."""

    celsius: Decimal

    def __init__(self, celsius: Decimal | int | float | str) -> None:
        """Create a temperature in Celsius."""
        value = _decimal(celsius, "celsius")
        if value < Decimal("-273.15"):
            raise DomainException(
                ValidationError(
                    "temperature.absolute_zero", "Temperature cannot be below absolute zero."
                )
            )
        object.__setattr__(self, "celsius", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this temperature."""
        return {"celsius": str(self.celsius)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a temperature."""
        return cls(_require_number(data, "celsius"))


@dataclass(frozen=True, slots=True)
class Percentage(ValueObject):
    """Percentage value constrained between 0 and 100."""

    value: Decimal

    def __init__(self, value: Decimal | int | float | str) -> None:
        """Create a percentage."""
        resolved = _decimal(value, "value")
        if resolved < Decimal("0") or resolved > Decimal("100"):
            raise DomainException(
                ValidationError("percentage.range", "Percentage must be between 0 and 100.")
            )
        object.__setattr__(self, "value", resolved)

    def to_ratio(self) -> Decimal:
        """Return this percentage as a ratio between 0 and 1."""
        return self.value / Decimal("100")

    def to_dict(self) -> dict[str, object]:
        """Serialize this percentage."""
        return {"value": str(self.value)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a percentage."""
        return cls(_require_number(data, "value"))


@dataclass(frozen=True, slots=True)
class Voltage(ValueObject):
    """Electrical potential measured in volts."""

    volts: Decimal

    def __init__(self, volts: Decimal | int | float | str) -> None:
        """Create a voltage."""
        value = _decimal(volts, "volts")
        if value < Decimal("0"):
            raise DomainException(
                ValidationError("voltage.negative", "Voltage cannot be negative.")
            )
        object.__setattr__(self, "volts", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this voltage."""
        return {"volts": str(self.volts)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a voltage."""
        return cls(_require_number(data, "volts"))


@dataclass(frozen=True, slots=True)
class Distance(ValueObject):
    """Distance measured in meters."""

    meters: Decimal

    def __init__(self, meters: Decimal | int | float | str) -> None:
        """Create a distance."""
        value = _decimal(meters, "meters")
        if value < Decimal("0"):
            raise DomainException(
                ValidationError("distance.negative", "Distance cannot be negative.")
            )
        object.__setattr__(self, "meters", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this distance."""
        return {"meters": str(self.meters)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a distance."""
        return cls(_require_number(data, "meters"))


@dataclass(frozen=True, slots=True)
class Duration(ValueObject):
    """Duration measured in seconds."""

    seconds: Decimal

    def __init__(self, seconds: Decimal | int | float | str | timedelta) -> None:
        """Create a duration from seconds or a timedelta."""
        raw_value = seconds.total_seconds() if isinstance(seconds, timedelta) else seconds
        value = _decimal(raw_value, "seconds")
        if value < Decimal("0"):
            raise DomainException(
                ValidationError("duration.negative", "Duration cannot be negative.")
            )
        object.__setattr__(self, "seconds", value)

    def to_timedelta(self) -> timedelta:
        """Return this duration as a timedelta."""
        return timedelta(seconds=float(self.seconds))

    def to_dict(self) -> dict[str, object]:
        """Serialize this duration."""
        return {"seconds": str(self.seconds)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a duration."""
        return cls(_require_number(data, "seconds"))


@dataclass(frozen=True, slots=True)
class Timestamp(ValueObject):
    """Timezone-aware timestamp normalized to UTC."""

    value: datetime

    def __init__(self, value: datetime | str) -> None:
        """Create a timestamp from a datetime or ISO-8601 string."""
        instant = datetime.fromisoformat(value) if isinstance(value, str) else value
        if instant.tzinfo is None:
            raise DomainException(
                ValidationError("timestamp.timezone", "Timestamp must be timezone-aware.")
            )
        object.__setattr__(self, "value", instant.astimezone(UTC))

    def to_dict(self) -> dict[str, object]:
        """Serialize this timestamp."""
        return {"value": self.value.isoformat()}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a timestamp."""
        value = data.get("value")
        if not isinstance(value, str):
            raise DomainException(ValidationError("timestamp.required", "value is required."))
        return cls(value)


@dataclass(frozen=True, slots=True)
class Confidence(ValueObject):
    """Confidence score constrained between 0 and 1."""

    value: Decimal

    def __init__(self, value: Decimal | int | float | str) -> None:
        """Create a confidence score."""
        resolved = _decimal(value, "value")
        if resolved < Decimal("0") or resolved > Decimal("1"):
            raise DomainException(
                ValidationError("confidence.range", "Confidence must be between 0 and 1.")
            )
        object.__setattr__(self, "value", resolved)

    def to_dict(self) -> dict[str, object]:
        """Serialize this confidence score."""
        return {"value": str(self.value)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a confidence score."""
        return cls(_require_number(data, "value"))


@dataclass(frozen=True, slots=True)
class Latitude(ValueObject):
    """Geographic latitude in decimal degrees."""

    degrees: Decimal

    def __init__(self, degrees: Decimal | int | float | str) -> None:
        """Create a latitude."""
        value = _decimal(degrees, "degrees")
        if value < Decimal("-90") or value > Decimal("90"):
            raise DomainException(
                ValidationError("latitude.range", "Latitude must be between -90 and 90 degrees.")
            )
        object.__setattr__(self, "degrees", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this latitude."""
        return {"degrees": str(self.degrees)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a latitude."""
        return cls(_require_number(data, "degrees"))


@dataclass(frozen=True, slots=True)
class Longitude(ValueObject):
    """Geographic longitude in decimal degrees."""

    degrees: Decimal

    def __init__(self, degrees: Decimal | int | float | str) -> None:
        """Create a longitude."""
        value = _decimal(degrees, "degrees")
        if value < Decimal("-180") or value > Decimal("180"):
            raise DomainException(
                ValidationError(
                    "longitude.range", "Longitude must be between -180 and 180 degrees."
                )
            )
        object.__setattr__(self, "degrees", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this longitude."""
        return {"degrees": str(self.degrees)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a longitude."""
        return cls(_require_number(data, "degrees"))


@dataclass(frozen=True, slots=True)
class Money(ValueObject):
    """Monetary amount with ISO-style currency code."""

    amount: Decimal
    currency: str

    def __init__(self, amount: Decimal | int | float | str, currency: str) -> None:
        """Create a monetary amount."""
        resolved_amount = _decimal(amount, "amount")
        resolved_currency = currency.upper()
        if resolved_amount < Decimal("0"):
            raise DomainException(ValidationError("money.negative", "Money cannot be negative."))
        if len(resolved_currency) != 3 or not resolved_currency.isalpha():
            raise DomainException(
                ValidationError(
                    "money.currency", "Currency must be a three-letter alphabetic code."
                )
            )
        object.__setattr__(self, "amount", resolved_amount)
        object.__setattr__(self, "currency", resolved_currency)

    def to_dict(self) -> dict[str, object]:
        """Serialize this monetary amount."""
        return {"amount": str(self.amount), "currency": self.currency}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a monetary amount."""
        currency = data.get("currency")
        if not isinstance(currency, str):
            raise DomainException(
                ValidationError("money.currency_required", "currency is required.")
            )
        return cls(_require_number(data, "amount"), currency)


@dataclass(frozen=True, slots=True)
class FuelLevel(ValueObject):
    """Resource fill level constrained between 0 and 100 percent."""

    percentage: Percentage

    def __init__(self, percentage: Percentage | Decimal | int | float | str) -> None:
        """Create a fill level percentage."""
        value = percentage if isinstance(percentage, Percentage) else Percentage(percentage)
        object.__setattr__(self, "percentage", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this fill level."""
        return {"percentage": str(self.percentage.value)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a fill level."""
        return cls(_require_number(data, "percentage"))


@dataclass(frozen=True, slots=True)
class RPM(ValueObject):
    """Rotational speed measured in revolutions per minute."""

    value: int

    def __init__(self, value: int) -> None:
        """Create a rotational speed value."""
        if value < 0:
            raise DomainException(ValidationError("rpm.negative", "RPM cannot be negative."))
        object.__setattr__(self, "value", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this rotational speed."""
        return {"value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a rotational speed."""
        value = data.get("value")
        if not isinstance(value, int):
            raise DomainException(ValidationError("rpm.required", "value is required."))
        return cls(value)


@dataclass(frozen=True, slots=True)
class HealthScore(ValueObject):
    """Health score constrained between 0 and 100."""

    value: Percentage

    def __init__(self, value: Percentage | Decimal | int | float | str) -> None:
        """Create a health score."""
        resolved = value if isinstance(value, Percentage) else Percentage(value)
        object.__setattr__(self, "value", resolved)

    def to_dict(self) -> dict[str, object]:
        """Serialize this health score."""
        return {"value": str(self.value.value)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a health score."""
        return cls(_require_number(data, "value"))


@dataclass(frozen=True, slots=True)
class Speed(ValueObject):
    """Speed measured in meters per second."""

    meters_per_second: Decimal

    def __init__(self, meters_per_second: Decimal | int | float | str) -> None:
        """Create a speed."""
        value = _decimal(meters_per_second, "meters_per_second")
        if value < Decimal("0"):
            raise DomainException(ValidationError("speed.negative", "Speed cannot be negative."))
        object.__setattr__(self, "meters_per_second", value)

    def to_dict(self) -> dict[str, object]:
        """Serialize this speed."""
        return {"meters_per_second": str(self.meters_per_second)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize a speed."""
        return cls(_require_number(data, "meters_per_second"))
