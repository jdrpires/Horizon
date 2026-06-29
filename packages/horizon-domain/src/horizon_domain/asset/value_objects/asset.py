"""Value objects for the Asset domain."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Self

from horizon_domain.asset.validators import ensure_not_blank
from horizon_kernel import DomainException, UniqueId, ValidationError, ValueObject


@dataclass(frozen=True, slots=True)
class AssetId(ValueObject):
    """Immutable Asset identifier."""

    value: UniqueId

    def __init__(self, value: UniqueId | str | None = None) -> None:
        """Create an Asset ID from a UUID string, UniqueId, or generated value."""
        resolved = UniqueId.new() if value is None else value
        object.__setattr__(self, "value", resolved if isinstance(resolved, UniqueId) else UniqueId(resolved))

    @classmethod
    def new(cls) -> AssetId:
        """Create a new Asset ID."""
        return cls()

    @classmethod
    def from_string(cls, value: str) -> AssetId:
        """Create an Asset ID from a string."""
        return cls(value)

    def to_string(self) -> str:
        """Serialize this Asset ID as a string."""
        return self.value.to_string()

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"value": self.to_string()}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        return cls(str(data["value"]))

    def __str__(self) -> str:
        """Return the string representation."""
        return self.to_string()


class AssetStatus(StrEnum):
    """Allowed Asset lifecycle states."""

    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class AssetIdentity(ValueObject):
    """Human and external identity for an Asset."""

    name: str
    external_reference: str | None = None

    def __post_init__(self) -> None:
        """Validate Asset identity."""
        object.__setattr__(self, "name", ensure_not_blank(self.name, "identity.name"))
        if self.external_reference is not None:
            reference = ensure_not_blank(self.external_reference, "identity.external_reference")
            object.__setattr__(self, "external_reference", reference)

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"name": self.name, "external_reference": self.external_reference}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        external_reference = data.get("external_reference")
        return cls(
            name=str(data["name"]),
            external_reference=None if external_reference is None else str(external_reference),
        )


@dataclass(frozen=True, slots=True)
class AssetClassification(ValueObject):
    """Generic classification for an Asset."""

    category: str
    kind: str | None = None

    def __post_init__(self) -> None:
        """Validate Asset classification."""
        object.__setattr__(self, "category", ensure_not_blank(self.category, "classification.category"))
        if self.kind is not None:
            object.__setattr__(self, "kind", ensure_not_blank(self.kind, "classification.kind"))

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"category": self.category, "kind": self.kind}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        kind = data.get("kind")
        return cls(category=str(data["category"]), kind=None if kind is None else str(kind))


@dataclass(frozen=True, slots=True)
class Ownership(ValueObject):
    """Ownership reference for an Asset."""

    owner_id: str
    tenant_id: str | None = None

    def __post_init__(self) -> None:
        """Validate ownership."""
        object.__setattr__(self, "owner_id", ensure_not_blank(self.owner_id, "ownership.owner_id"))
        if self.tenant_id is not None:
            object.__setattr__(self, "tenant_id", ensure_not_blank(self.tenant_id, "ownership.tenant_id"))

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"owner_id": self.owner_id, "tenant_id": self.tenant_id}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        tenant_id = data.get("tenant_id")
        return cls(owner_id=str(data["owner_id"]), tenant_id=None if tenant_id is None else str(tenant_id))


@dataclass(frozen=True, slots=True)
class AssetConfiguration(ValueObject):
    """Generic Asset configuration that carries no infrastructure or telemetry behavior."""

    values: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze configuration values."""
        clean_values: dict[str, object] = {}
        for key, value in self.values.items():
            clean_key = ensure_not_blank(str(key), "configuration.key")
            if clean_key.lower() in _FORBIDDEN_CONFIGURATION_KEYS:
                raise DomainException(
                    ValidationError(
                        "asset.configuration.forbidden_key",
                        f"{clean_key} belongs to another domain.",
                    )
                )
            clean_values[clean_key] = value
        object.__setattr__(self, "values", MappingProxyType(clean_values))

    def to_dict(self) -> dict[str, object]:
        """Serialize this value object."""
        return {"values": dict(self.values)}

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object."""
        raw_values = data.get("values", {})
        if not isinstance(raw_values, Mapping):
            raise DomainException(
                ValidationError("asset.configuration.values", "configuration values must be a mapping.")
            )
        return cls(raw_values)


_FORBIDDEN_CONFIGURATION_KEYS = frozenset(
    {
        "temperature",
        "rpm",
        "fuel",
        "fuel_level",
        "telemetry",
        "engine",
        "tires",
        "gps",
        "latitude",
        "longitude",
        "sensor",
        "sensors",
    }
)
