"""Collector framework tests."""

from __future__ import annotations

import pytest

from horizon_catalog import load_vehicle_catalog
from horizon_collector import (
    CatalogObservationMapper,
    CollectorRegistry,
    FakeCollector,
    InMemoryCollectorRuntime,
    ObservationSourceMapping,
    RawObservation,
)
from horizon_collector.adapters import InMemoryObservationPublisher
from horizon_collector.collector import CollectorSessionState
from horizon_collector.exceptions import (
    CollectorAlreadyRegisteredError,
    CollectorNotFoundError,
    ObservationMappingError,
)
from horizon_collector.runtime import CollectorSession


def _mapper() -> CatalogObservationMapper:
    return CatalogObservationMapper(
        catalog=load_vehicle_catalog(),
        source_mappings=(
            ObservationSourceMapping(
                external_key="engine.coolant.temperature",
                catalog_key="engine.temperature",
            ),
            ObservationSourceMapping(
                external_key="electrical.battery.voltage",
                catalog_key="electrical.battery_voltage",
            ),
        ),
    )


def test_registry_registers_and_retrieves_collectors() -> None:
    registry = CollectorRegistry()
    collector = FakeCollector()

    registry.register(collector)

    assert registry.names == ("fake",)
    assert registry.get("fake") is collector


def test_registry_rejects_duplicates_and_unknown_collectors() -> None:
    registry = CollectorRegistry()
    registry.register(FakeCollector())

    with pytest.raises(CollectorAlreadyRegisteredError):
        registry.register(FakeCollector())

    with pytest.raises(CollectorNotFoundError):
        registry.get("missing")


def test_mapper_maps_external_keys_to_catalog_definitions() -> None:
    mapper = _mapper()

    canonical = mapper.map(RawObservation(key="engine.coolant.temperature", value="91"))

    assert canonical.definition.id == "engine.temperature"
    assert canonical.observation_type == "temperature"
    assert canonical.value == 91.0
    assert canonical.unit == "celsius"
    assert canonical.metadata["external_key"] == "engine.coolant.temperature"


def test_mapper_uses_direct_catalog_aliases() -> None:
    mapper = _mapper()

    canonical = mapper.map(RawObservation(key="engine.rpm", value=900))

    assert canonical.definition.id == "engine.rpm"
    assert canonical.observation_type == "rpm"
    assert canonical.value == 900.0


def test_mapper_rejects_unknown_or_unsupported_values() -> None:
    mapper = _mapper()

    with pytest.raises(ObservationMappingError):
        mapper.map(RawObservation(key="unknown.signal", value=1))

    with pytest.raises(ObservationMappingError):
        mapper.map(RawObservation(key="fuel.type", value="diesel"))

    with pytest.raises(ObservationMappingError):
        mapper.map(RawObservation(key="engine.rpm", value="not-a-number"))


def test_fake_collector_emits_required_raw_observations() -> None:
    registry = CollectorRegistry()
    collector = FakeCollector()
    registry.register(collector)
    session_name = registry.get("fake").name

    raw = collector.collect(session=CollectorSession(collector_name="fake"))

    assert session_name == "fake"
    assert [item.key for item in raw] == [
        "engine.rpm",
        "engine.coolant.temperature",
        "electrical.battery.voltage",
    ]


def test_runtime_executes_complete_pipeline_and_publishes() -> None:
    registry = CollectorRegistry()
    registry.register(FakeCollector())
    publisher = InMemoryObservationPublisher()
    runtime = InMemoryCollectorRuntime(
        registry=registry,
        mapper=_mapper(),
        publisher=publisher,
    )

    canonical = runtime.run_once("fake")

    assert [item.definition.id for item in canonical] == [
        "engine.rpm",
        "engine.temperature",
        "electrical.battery_voltage",
    ]
    assert publisher.published == canonical
    assert runtime.sessions[0].state is CollectorSessionState.COMPLETED


def test_runtime_marks_failed_session_when_collection_fails() -> None:
    class FailingCollector:
        name = "failing"

        def collect(self, session: CollectorSession) -> tuple[RawObservation, ...]:
            raise RuntimeError("boom")

    registry = CollectorRegistry()
    registry.register(FailingCollector())
    publisher = InMemoryObservationPublisher()
    runtime = InMemoryCollectorRuntime(
        registry=registry,
        mapper=_mapper(),
        publisher=publisher,
    )

    with pytest.raises(RuntimeError):
        runtime.run_once("failing")

    assert runtime.sessions[0].state is CollectorSessionState.FAILED
    assert publisher.published == ()
