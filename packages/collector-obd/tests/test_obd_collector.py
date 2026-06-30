"""Tests for the Android/ELM327 OBD collector spike."""

from __future__ import annotations

import unittest

from collector_obd import Elm327Adapter, MockObdTransport, ObdObservationMapper
from collector_obd.exceptions import AndroidBluetoothUnavailableError, ObdParseError, ObdTransportError
from collector_obd.pids import (
    CONTROL_MODULE_VOLTAGE_PID,
    COOLANT_TEMPERATURE_PID,
    RPM_PID,
    supported_pids,
)
from collector_obd.protocol.commands import RPM
from collector_obd.protocol.models import ObdResponse
from collector_obd.protocol.parser import parse_pid_response
from collector_obd.transport.android_bluetooth import AndroidBluetoothTransport
from horizon_catalog import load_vehicle_catalog
from horizon_collector.adapters import InMemoryObservationPublisher
from horizon_collector.registry import CollectorRegistry
from horizon_collector.runtime import CollectorSession, InMemoryCollectorRuntime


class ObdParserTests(unittest.TestCase):
    """OBD parser behavior."""

    def test_parse_supported_pid_responses(self) -> None:
        """Parser converts supported ELM327 responses into numeric values."""
        self.assertEqual(
            parse_pid_response(RPM_PID, ObdResponse(RPM_PID.command, "41 0C 0E 10\r>")),
            900.0,
        )
        self.assertEqual(
            parse_pid_response(
                COOLANT_TEMPERATURE_PID,
                ObdResponse(COOLANT_TEMPERATURE_PID.command, "41 05 83\r>"),
            ),
            91.0,
        )
        self.assertEqual(
            parse_pid_response(
                CONTROL_MODULE_VOLTAGE_PID,
                ObdResponse(CONTROL_MODULE_VOLTAGE_PID.command, "41 42 37 64\r>"),
            ),
            14.18,
        )

    def test_parser_rejects_unexpected_prefix(self) -> None:
        """Parser rejects mismatched PID responses."""
        with self.assertRaises(ObdParseError):
            parse_pid_response(RPM_PID, ObdResponse(RPM_PID.command, "41 05 5B\r>"))


class ObdTransportTests(unittest.TestCase):
    """OBD transport behavior."""

    def test_mock_transport_requires_connection(self) -> None:
        """Mock transport must be connected before sending commands."""
        transport = MockObdTransport()

        with self.assertRaises(ObdTransportError):
            transport.send(RPM)

    def test_mock_transport_returns_configured_responses(self) -> None:
        """Mock transport returns deterministic ELM327 responses."""
        transport = MockObdTransport()
        transport.connect()

        response = transport.send(RPM)

        self.assertEqual(response.raw, "41 0C 0E 10\r>")
        self.assertEqual(transport.sent_commands, ["010C"])

    def test_android_bluetooth_transport_is_placeholder(self) -> None:
        """Android Bluetooth transport fails explicitly until native runtime exists."""
        transport = AndroidBluetoothTransport(device_address="00:11:22:33:44:55")

        with self.assertRaises(AndroidBluetoothUnavailableError):
            transport.connect()


class Elm327AdapterTests(unittest.TestCase):
    """ELM327 adapter behavior."""

    def test_adapter_initializes_and_collects_raw_observations(self) -> None:
        """Adapter emits raw observations compatible with the Collector Framework."""
        transport = MockObdTransport()
        adapter = Elm327Adapter(transport)

        raw = adapter.collect(CollectorSession(collector_name=adapter.name))

        self.assertTrue(adapter.obd_session.initialized)
        self.assertEqual([item.key for item in raw], [pid.external_key for pid in supported_pids()])
        self.assertEqual([item.value for item in raw], [900.0, 91.0, 14.18])
        self.assertIn("ATZ", transport.sent_commands)
        self.assertIn("010C", transport.sent_commands)


class ObdMappingTests(unittest.TestCase):
    """OBD mapping behavior."""

    def test_mapper_converts_obd_raw_to_canonical_observations(self) -> None:
        """Mapper resolves OBD keys into Observation Catalog definitions."""
        adapter = Elm327Adapter(MockObdTransport())
        raw = adapter.collect(CollectorSession(collector_name=adapter.name))
        mapper = ObdObservationMapper(catalog=load_vehicle_catalog())

        canonical = mapper.map_many(raw)

        self.assertEqual(
            [item.definition.id for item in canonical],
            ["engine.rpm", "engine.temperature", "electrical.battery_voltage"],
        )
        self.assertEqual([item.value for item in canonical], [900.0, 91.0, 14.18])
        self.assertEqual([item.unit for item in canonical], ["rpm", "celsius", "volt"])


class ObdRuntimeTests(unittest.TestCase):
    """Collector Framework integration behavior."""

    def test_runtime_publishes_mock_obd_canonical_observations(self) -> None:
        """Mock OBD collector publishes through the Collector Framework."""
        adapter = Elm327Adapter(MockObdTransport())
        registry = CollectorRegistry()
        registry.register(adapter)
        publisher = InMemoryObservationPublisher()
        runtime = InMemoryCollectorRuntime(
            registry=registry,
            mapper=ObdObservationMapper(catalog=load_vehicle_catalog()),
            publisher=publisher,
        )

        observations = runtime.run_once(adapter.name)

        self.assertEqual(len(observations), 3)
        self.assertEqual(publisher.published, observations)
        self.assertEqual(observations[0].definition.id, "engine.rpm")
        self.assertEqual(observations[1].definition.id, "engine.temperature")
        self.assertEqual(observations[2].definition.id, "electrical.battery_voltage")


if __name__ == "__main__":
    unittest.main()
