"""Factory for creating Asset aggregates."""

from horizon_domain.asset.aggregates import Asset
from horizon_domain.asset.commands import RegisterAsset
from horizon_kernel import Clock


class AssetFactory:
    """Factory wrapper for Asset registration."""

    @staticmethod
    def register(command: RegisterAsset, clock: Clock | None = None) -> Asset:
        """Create a registered Asset."""
        return Asset.register(command, clock)
