# Project Timeline

Status: Living Historical Record

## Foundation 1.0

Horizon established its initial foundation: Kernel, Events, Protocol, domain language, architecture discipline, and the first memory-first principles.

## Foundation 2.0

The project governance model was established with permanent documentation, lifecycle rules, architecture governance, decision process, document hierarchy, repository principles, Constitution, and Living Digital Twin Manifesto.

## Asset And Observation Foundation

The Asset domain became the root of Horizon identity. Observation became the factual unit of memory, distinct from knowledge, insight, or interpretation.

## Timeline And Current State

Timeline established chronological memory. Current State became the latest projection from Timeline, explicitly not intelligence and not independent truth.

## Observation Catalog

The Observation Catalog introduced controlled vocabulary for observed facts, protecting Horizon from arbitrary names and inconsistent telemetry language.

## Collector Framework

The Collector Framework created the generic ingestion boundary for external observation sources without coupling Horizon Core to Bluetooth, OBD, CAN, MQTT, REST, CSV, hardware, or manufacturers.

## Android OBD Bridge

The Android OBD Bridge proved that Android could connect to ELM327 Bluetooth, parse basic OBD-II PIDs, and produce canonical observation payloads outside Horizon Core.

## Milestone M1: First Live Observation

Horizon recorded its first observation from a physical vehicle: a Citroën C3 through ELM327 Bluetooth and Android.

## Gateway And Live Ingestion

The Horizon Gateway introduced the live ingestion boundary with `POST /observations`, allowing external collectors to submit canonical observations.

## Horizon Mobile

The Android bridge evolved into Horizon Mobile, the first official client focused on the Asset state rather than scanner-style PID output.

## Capability-012: Bluetooth Session Engine

Horizon Mobile introduced a robust Bluetooth Session Engine for ELM327 RFCOMM communication, stable MAC binding, ELM327 initialization, PID polling, reconnection, and field diagnostics.

## Capability-013: Mobile State Synchronization

Horizon Mobile introduced a single mobile state model and reliable Asset binding, preventing null Asset identity in Gateway calls and live observation payloads.

## Milestone M2: First End-to-End Live Vehicle Telemetry

Horizon validated the full live telemetry path:

```text
Citroën C3
  ↓
ELM327 Bluetooth
  ↓
Android Realme
  ↓
Horizon Mobile
  ↓
Cloudflare Tunnel
  ↓
Horizon Gateway
  ↓
Collector Framework
  ↓
Application
  ↓
Storage
  ↓
Timeline
  ↓
Current State
```

## Alpha 1.1

Alpha 1.1 records that Generation 1 is not only architecturally coherent, but validated with real hardware and continuous live vehicle telemetry.
