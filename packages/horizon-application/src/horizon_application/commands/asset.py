"""Application commands for Asset use cases."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class RegisterAssetCommand:
    """Application command to register an Asset."""

    name: str
    category: str
    owner_id: str
    external_reference: str | None = None
    kind: str | None = None
    tenant_id: str | None = None
    configuration: dict[str, object] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate required command fields."""
        for field_name, value in {
            "name": self.name,
            "category": self.category,
            "owner_id": self.owner_id,
        }.items():
            if not value.strip():
                raise ValueError(f"{field_name} is required.")
