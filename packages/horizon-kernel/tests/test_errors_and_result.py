from collections.abc import MutableMapping
from typing import cast

import pytest

from horizon_kernel.exceptions import (
    BusinessError,
    DomainException,
    DomainRuleViolation,
    Error,
    InfrastructureError,
    UnexpectedError,
    ValidationError,
)
from horizon_kernel.shared import Result


def test_error_serializes_and_freezes_details() -> None:
    error = ValidationError("validation.invalid", "Invalid value.", {"field": "name"})

    assert error.to_dict() == {
        "code": "validation.invalid",
        "message": "Invalid value.",
        "details": {"field": "name"},
    }
    with pytest.raises(TypeError):
        cast(MutableMapping[str, object], error.details)["field"] = "other"


def test_domain_exception_exposes_structured_error() -> None:
    error = BusinessError("business.failed", "Operation failed.")
    exception = DomainException(error)

    assert exception.error == error
    assert str(exception) == "Operation failed."


def test_error_hierarchy_types() -> None:
    assert isinstance(DomainRuleViolation("rule.failed", "Rule failed."), BusinessError)
    assert isinstance(InfrastructureError("infra.failed", "Infra failed."), Error)
    assert isinstance(UnexpectedError("unexpected.failed", "Unexpected failed."), Error)


def test_result_ok_maps_binds_and_unwraps() -> None:
    result = Result.Ok(2)

    mapped = result.map(lambda value: value + 3)
    bound = mapped.bind(lambda value: Result.Ok(str(value)))

    assert result.is_ok
    assert not result.is_fail
    assert mapped.value == 5
    assert bound.unwrap() == "5"


def test_result_fail_preserves_error() -> None:
    error = ValidationError("validation.failed", "Invalid.")
    result: Result[int] = Result.Fail(error)

    assert result.is_fail
    assert result.error == error
    assert result.map(lambda value: value + 1).error == error
    assert result.bind(lambda value: Result.Ok(value + 1)).error == error


def test_result_rejects_invalid_state_and_failed_unwrap() -> None:
    error = ValidationError("validation.failed", "Invalid.")

    with pytest.raises(ValueError):
        Result[int]()

    with pytest.raises(ValueError):
        _ = Result.Ok(1).error

    with pytest.raises(ValueError, match=r"Invalid\."):
        Result.Fail(error).unwrap()
