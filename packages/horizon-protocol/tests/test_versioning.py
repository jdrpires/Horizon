"""Versioning tests."""

import pytest

from horizon_protocol import Compatibility, ProtocolVersion, SchemaVersion


def test_protocol_version_compatibility_relationships() -> None:
    supported = ProtocolVersion(1, 2, 0)

    assert ProtocolVersion(1, 2, 0).compatibility_with(supported) is Compatibility.SAME
    assert (
        ProtocolVersion(1, 3, 0).compatibility_with(supported)
        is Compatibility.BACKWARD_COMPATIBLE
    )
    assert (
        ProtocolVersion(1, 1, 0).compatibility_with(supported)
        is Compatibility.FUTURE_COMPATIBLE
    )
    assert ProtocolVersion(2, 0, 0).compatibility_with(supported) is Compatibility.INCOMPATIBLE


def test_schema_version_boolean_helpers() -> None:
    supported = SchemaVersion(1, 1, 0)

    assert SchemaVersion(1, 2, 0).is_backward_compatible_with(supported)
    assert SchemaVersion(1, 0, 0).is_future_compatible_with(supported)
    assert not SchemaVersion(2, 0, 0).is_backward_compatible_with(supported)
    assert not SchemaVersion(2, 0, 0).is_future_compatible_with(supported)


def test_versions_reject_invalid_values() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        ProtocolVersion(0, 1, 0)
    with pytest.raises(ValueError, match="non-negative"):
        ProtocolVersion(1, -1, 0)
    with pytest.raises(ValueError, match="integers"):
        SchemaVersion.parse("1.two.0")
