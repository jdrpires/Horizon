# RFC-0011: Collector Framework

Status: Accepted

## Summary

Introduce `horizon-collector` as the generic ingestion framework for observations coming from external sources.

The Collector Framework receives external data, normalizes it through the Observation Catalog, creates Canonical Observations, and publishes them through a Horizon boundary. It does not implement Bluetooth, OBD, CAN, MQTT, REST, CSV, Serial, TCP, UDP, hardware, manufacturers, dashboards, or APIs.

## Context

Horizon's memory begins with observations. External sources will eventually produce those observations, but Horizon Core must remain independent from transport protocols, hardware details, vendor formats, and integration-specific vocabulary.

Without a Collector boundary, each future integration would be tempted to know Domain, Application, Storage, Timeline, Current State, or Experience internals. That would weaken the platform's memory model and make transport details look like architecture.

## Goals

- Define a reusable Collector Framework.
- Receive raw external observations from any source.
- Normalize external keys through the Observation Catalog.
- Validate values according to catalog definitions and current runtime compatibility.
- Produce Canonical Observations.
- Publish Canonical Observations through an abstract publisher.
- Provide a Fake Collector that proves ingestion without real hardware.

## Non-Goals

- Implement OBD.
- Implement Bluetooth.
- Implement CAN.
- Implement MQTT.
- Implement REST.
- Implement CSV ingestion.
- Implement Serial, TCP, or UDP transport.
- Implement hardware support.
- Implement dashboards.
- Change Domain, Application, Storage, Timeline, Current State, Experience, or Observation runtime behavior.
- Change `Observation.value`.
- Implement Living Digital Twin behavior, Knowledge, AI, or recommendations.

## Architecture Boundary

The Collector Framework owns ingestion mechanics only.

```text
External Source
  |
  v
Collector
  |
  v
Raw Observation
  |
  v
Observation Mapper
  |
  v
Observation Catalog
  |
  v
Canonical Observation
  |
  v
Observation Publisher
  |
  v
Horizon Boundary
```

## Contracts

- `Collector`: emits raw observations.
- `CollectorAdapter`: hides transport-specific reading behind a contract.
- `CollectorSession`: represents one collector execution.
- `CollectorRuntime`: executes collectors and coordinates mapping and publishing.
- `ObservationMapper`: maps raw observations to catalog-backed canonical observations.
- `CollectorRegistry`: stores available collectors.
- `ObservationPublisher`: publishes Canonical Observations into Horizon through an outer boundary.

## Catalog Mapping

Collectors must not invent Observation names.

External keys are mapped to official Observation Catalog definitions. When an external source uses a transport-specific or vendor-specific name, the mapper translates that name into the catalog language before publication.

The initial Fake Collector emits:

- `engine.rpm`
- `engine.coolant.temperature`
- `electrical.battery.voltage`

The mapper resolves those values to official catalog definitions without modifying the catalog.

## Runtime Compatibility

The current Observation runtime accepts numeric values only. Therefore, the Collector Framework defaults to publishing only catalog definitions whose `value_type` is `number`.

The framework must not convert text, boolean, enum, or datetime values into numbers. The future Observation Value Model will expand runtime support.

## Compatibility

This RFC does not change existing Domain, Application, Storage, Timeline, Current State, Experience, Event Bus, Protocol, or Catalog contracts.

The Collector Framework is additive and isolated.

## Validation

The Capability is valid when tests cover:

- Collector Runtime.
- Collector Registry.
- Observation Mapper.
- Observation Publisher.
- Fake Collector.
- End-to-end ingestion pipeline.
