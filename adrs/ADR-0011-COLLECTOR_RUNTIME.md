# ADR-0011: Collector Runtime

Status: Accepted

## Context

Horizon needs a way to receive observations from future external sources without allowing transport or hardware concerns to enter Horizon Core.

Potential future collectors may use Bluetooth, OBD, CAN, MQTT, REST, CSV, Serial, TCP, UDP, or vendor-specific protocols. None of those concerns should shape Domain, Application, Storage, Timeline, Current State, Experience, Catalog, Events, or Protocol internals.

## Decision

Create `horizon-collector` as an isolated package for generic ingestion.

The package defines Collector contracts, a Collector Runtime, Collector Sessions, an Observation Mapper, a Collector Registry, an Observation Publisher boundary, validation, and a Fake Collector.

The Collector Runtime depends on the Observation Catalog for official definitions and produces Canonical Observations. It does not import Domain, Application, Storage, Timeline, Current State, or Experience packages.

Transport-specific collectors must be implemented later behind Collector or CollectorAdapter contracts.

## Consequences

- Future OBD, Bluetooth, CAN, MQTT, REST, CSV, Serial, TCP, UDP, and hardware integrations can be added without changing Horizon Core.
- External naming is normalized before entering Horizon.
- Observation Catalog remains the official vocabulary.
- Current runtime numeric-only compatibility is preserved.
- Non-numeric values are rejected instead of being artificially converted.
- The framework can be tested entirely in memory.
- The first Fake Collector proves the ingestion pipeline without real hardware.
