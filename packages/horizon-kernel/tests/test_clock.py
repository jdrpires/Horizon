from datetime import UTC, datetime

import pytest

from horizon_kernel.utils import FrozenClock, SystemClock


def test_system_clock_returns_timezone_aware_datetime() -> None:
    now = SystemClock().now()

    assert now.tzinfo is not None


def test_frozen_clock_returns_configured_instant() -> None:
    instant = datetime(2026, 1, 1, tzinfo=UTC)

    assert FrozenClock(instant).now() == instant


def test_frozen_clock_rejects_naive_datetime() -> None:
    with pytest.raises(ValueError):
        FrozenClock(datetime(2026, 1, 1))
