# Horizon Alpha 1.0 Release Notes

Status: Prepared for Chief Software Architect review

Date: 2026-06-30

## Capability Timeline

### Capability-001: Foundation, Kernel, Events, and Protocol

Established the monorepo foundation, Horizon Kernel, Event Platform, and Horizon Protocol.

This capability created the first reusable language and technical boundary for commands, queries, events, identifiers, metadata, versioning, and platform conventions.

### Capability-002: Asset Domain

Introduced Asset as the root aggregate of Horizon.

The Asset Domain established identity, lifecycle, ownership, configuration, and invariants without reducing Horizon to vehicles or any other asset category.

### Capability-003: Application Layer and Horizon Lab

Created the first in-memory Application Layer and local interactive lab.

The Application Layer connected commands, handlers, use cases, in-memory repositories, event publication, and result mapping without infrastructure.

### Capability-004: Observation Domain

Introduced Observation as a factual measurement associated with an Asset.

Observation remained separate from knowledge, insights, telemetry consolidation, and Digital Twin behavior. The vertical slice enabled Assets and Observations to flow through the local lab.

### Capability-005: Temporal Memory and Current State Foundation

Established Timeline, Replay, Current State, and local persistence as the first memory foundation.

Timeline records chronological facts. Current State projects the latest known values from Timeline. Storage persists factual runtime data without becoming domain truth.

### Capability-006: Collector Framework

Created the generic Collector Framework for external Observation ingestion.

The framework receives external data, normalizes it through the Observation Catalog, produces Canonical Observations, and publishes them through an abstract boundary. It does not know Bluetooth, OBD, CAN, MQTT, REST, hardware, or manufacturers.

### Capability-007: Android/ELM327 OBD Collector Spike

Created an experimental OBD/ELM327 adapter package.

The spike validated ELM327 commands, OBD PID parsing, mock transport, Android Bluetooth boundary documentation, and mapping from OBD values into catalog-backed Observation definitions.

### Capability-008: Android OBD Bridge

Created the first Android bridge for collecting ELM327 readings from a physical vehicle.

The bridge lists paired Bluetooth devices, connects through RFCOMM, reads RPM, engine temperature, and control module voltage, and emits Horizon-compatible JSON payloads while keeping Android and Bluetooth outside Horizon Core.

### Capability-009: Live Ingestion Gateway

Created the Horizon Live Ingestion Gateway.

The Gateway accepts `POST /observations`, validates payloads, resolves Observation definitions through the catalog, maps entries through the Collector Framework, and forwards canonical Observations into the existing Application, Storage, Timeline, and Current State path.

### Capability-010: Horizon Mobile

Evolved the Android OBD Bridge into Horizon Mobile, the first official Horizon client.

Horizon Mobile continues collecting ELM327 readings, sends Observations to the Gateway, queries Assets, Current State, and Timeline, and presents the Asset as a stateful subject rather than a scanner output.

## Milestone

### M1: First Live Observation

The first physical observation was recorded from a Citroen C3 through an ELM327 Bluetooth adapter and Android/Realme device.

Observed values:

- RPM: `805 rpm`
- Engine temperature: `76 C`
- Voltage: `12.31 V`

This confirmed the boundary strategy: Bluetooth and OBD remain outside Horizon Core, while Horizon receives canonical Observations.

## Release Summary

Alpha 1.0 completes Generation 1: the evidence path from Asset identity to live ingestion and mobile presentation.

It does not implement the Memory Engine, Knowledge Engine, Health Engine, Recommendation Engine, Conversation Engine, Agent Framework, or Living Digital Twin runtime.
