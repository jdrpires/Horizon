"""Identifier tests."""

from dataclasses import FrozenInstanceError
from uuid import UUID

import pytest

from horizon_protocol import (
    AssetId,
    CausationId,
    CorrelationId,
    EventId,
    InsightId,
    JourneyId,
    MaintenanceId,
    ModuleId,
    ObservationId,
    ProtocolIdentifier,
    RecommendationId,
    TenantId,
    UserId,
)
from horizon_protocol.validators import validate_identifier_format


@pytest.mark.parametrize(
    "identifier_type",
    [
        AssetId,
        JourneyId,
        InsightId,
        RecommendationId,
        ObservationId,
        MaintenanceId,
        EventId,
        CorrelationId,
        CausationId,
        UserId,
        TenantId,
        ModuleId,
    ],
)
def test_protocol_identifiers_are_uuid_backed_and_immutable(
    identifier_type: type[ProtocolIdentifier],
) -> None:
    identifier = identifier_type.new()

    assert UUID(identifier.to_string()) == identifier.value
    assert identifier_type.from_string(identifier.to_string()) == identifier
    with pytest.raises(FrozenInstanceError):
        setattr(identifier, "value", UUID(int=0))


def test_identifier_format_validator_accepts_uuid_and_rejects_other_values() -> None:
    identifier = AssetId.new().to_string()

    assert validate_identifier_format(identifier) == identifier
    with pytest.raises(ValueError, match="canonical UUID"):
        validate_identifier_format("asset-123")
