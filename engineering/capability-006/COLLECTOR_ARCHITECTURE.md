# Collector Architecture

Status: Draft

## Purpose

This document explains the architecture of Capability-006: Collector/Ingestion Framework.

The Collector Framework exists to protect Horizon Core from external source details.

## Boundary

Collectors sit outside the memory path and feed it through canonical observations.

They do not know:

- Asset Domain.
- Observation Aggregate.
- Application use cases.
- Storage.
- Timeline.
- Current State.
- Experience.
- APIs.
- Hardware.
- Transport protocols.

## Pipeline

```text
Collector
  -> RawObservation
  -> ObservationMapper
  -> ObservationCatalog
  -> CanonicalObservation
  -> ObservationPublisher
```

## Transport Independence

The framework does not implement real external transports.

Future OBD, Bluetooth, CAN, MQTT, REST, CSV, Serial, TCP, UDP, and hardware adapters must be implemented behind Collector or CollectorAdapter contracts.

## Catalog First

External observation names are not official Horizon language.

The Observation Catalog remains the official vocabulary. The mapper translates external keys into catalog definitions before anything is published.

## Current Runtime Compatibility

The current Observation runtime supports numeric values only.

The Collector Framework therefore defaults to accepting only `number` definitions. It rejects unsupported value types instead of encoding them into numbers.

## Fake Collector

The Fake Collector is not a hardware simulation. It is a deterministic proof that the pipeline can ingest external-like data without a real integration.

It emits:

- `engine.rpm`
- `engine.coolant.temperature`
- `electrical.battery.voltage`
