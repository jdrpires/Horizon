"""Asset lifecycle specifications."""

from horizon_domain.asset.value_objects import AssetStatus


def can_activate(status: AssetStatus) -> bool:
    """Return whether an Asset in the supplied status can be activated."""
    return status in {AssetStatus.REGISTERED, AssetStatus.INACTIVE}
