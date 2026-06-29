"""Asset domain error helpers."""

from horizon_kernel import DomainException, DomainRuleViolation


def asset_rule_violation(code: str, message: str) -> DomainException:
    """Create an Asset domain rule violation."""
    return DomainException(DomainRuleViolation(code=f"asset.{code}", message=message))
