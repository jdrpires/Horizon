"""Commands accepted by the Asset aggregate."""

from __future__ import annotations

from dataclasses import dataclass, field

from horizon_domain.asset.value_objects import (
    AssetClassification,
    AssetConfiguration,
    AssetId,
    AssetIdentity,
    Ownership,
)
from horizon_kernel import UniqueId


@dataclass(frozen=True, slots=True)
class AssetCommand:
    """Base command metadata for Asset operations."""

    correlation_id: UniqueId = field(default_factory=UniqueId.new)
    causation_id: UniqueId = field(default_factory=UniqueId.new)


@dataclass(frozen=True, slots=True)
class RegisterAsset(AssetCommand):
    """Register a new Asset."""

    identity: AssetIdentity = field(default_factory=lambda: AssetIdentity("Unnamed Asset"))
    classification: AssetClassification = field(
        default_factory=lambda: AssetClassification("generic.asset")
    )
    ownership: Ownership = field(default_factory=lambda: Ownership("unassigned"))
    configuration: AssetConfiguration = field(default_factory=AssetConfiguration)
    asset_id: AssetId = field(default_factory=AssetId.new)


@dataclass(frozen=True, slots=True)
class ActivateAsset(AssetCommand):
    """Activate an Asset."""

    asset_id: AssetId = field(default_factory=AssetId.new)


@dataclass(frozen=True, slots=True)
class DeactivateAsset(AssetCommand):
    """Deactivate an Asset."""

    asset_id: AssetId = field(default_factory=AssetId.new)
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class ArchiveAsset(AssetCommand):
    """Archive an Asset without deleting it."""

    asset_id: AssetId = field(default_factory=AssetId.new)
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class TransferOwnership(AssetCommand):
    """Transfer an Asset to new ownership."""

    asset_id: AssetId = field(default_factory=AssetId.new)
    ownership: Ownership = field(default_factory=lambda: Ownership("unassigned"))


@dataclass(frozen=True, slots=True)
class UpdateConfiguration(AssetCommand):
    """Update generic Asset configuration."""

    asset_id: AssetId = field(default_factory=AssetId.new)
    configuration: AssetConfiguration = field(default_factory=AssetConfiguration)
