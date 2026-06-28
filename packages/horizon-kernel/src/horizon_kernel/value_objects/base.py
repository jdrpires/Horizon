"""Base value object contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self


class ValueObject(ABC):
    """Base class for immutable objects compared by their values."""

    @abstractmethod
    def to_dict(self) -> dict[str, object]:
        """Serialize this value object to primitive values."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, object]) -> Self:
        """Deserialize this value object from primitive values."""
