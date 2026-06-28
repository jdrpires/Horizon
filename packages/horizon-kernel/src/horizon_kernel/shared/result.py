"""Rust-inspired result type for explicit success and failure handling."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar, cast

from horizon_kernel.exceptions import Error, UnexpectedError

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True, slots=True)
class Result[T]:
    """Container representing either a successful value or a structured error."""

    _value: T | None = None
    _error: Error | None = None

    def __post_init__(self) -> None:
        """Validate that a result contains exactly one outcome."""
        if (self._error is None) == (self._value is None):
            raise ValueError("Result must contain exactly one value or one error.")

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        """Create a successful result."""
        return cls(_value=value)

    @classmethod
    def fail(cls, error: Error) -> Result[T]:
        """Create a failed result."""
        return cls(_error=error)

    @classmethod
    def Ok(cls, value: T) -> Result[T]:
        """Create a successful result."""
        return cls.ok(value)

    @classmethod
    def Fail(cls, error: Error) -> Result[T]:
        """Create a failed result."""
        return cls.fail(error)

    @property
    def is_ok(self) -> bool:
        """Return whether this result is successful."""
        return self._error is None

    @property
    def is_fail(self) -> bool:
        """Return whether this result is failed."""
        return self._error is not None

    @property
    def value(self) -> T:
        """Return the success value or raise when failed."""
        return self.unwrap()

    @property
    def error(self) -> Error:
        """Return the error or raise when successful."""
        if self._error is None:
            raise ValueError("Cannot access error from successful Result.")
        return self._error

    def map(self, transform: Callable[[T], U]) -> Result[U]:
        """Transform the success value while preserving failures."""
        if self.is_fail:
            return Result.fail(self.error)
        return Result.ok(transform(cast(T, self._value)))

    def bind(self, transform: Callable[[T], Result[U]]) -> Result[U]:
        """Chain another operation returning a result."""
        if self.is_fail:
            return Result.fail(self.error)
        return transform(cast(T, self._value))

    def unwrap(self) -> T:
        """Return the success value or raise a ValueError for failures."""
        if self._error is not None:
            raise ValueError(self._error.message)
        if self._value is None:
            raise ValueError(UnexpectedError("result.empty", "Result has no value.").message)
        return self._value
