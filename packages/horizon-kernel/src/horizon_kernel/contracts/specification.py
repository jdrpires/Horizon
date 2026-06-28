"""Specification interface for reusable domain predicates."""

from __future__ import annotations

from typing import Protocol, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class Specification(Protocol[T_contra]):
    """Predicate object that answers whether a candidate satisfies a rule."""

    def is_satisfied_by(self, candidate: T_contra) -> bool:
        """Return whether the candidate satisfies this specification."""
