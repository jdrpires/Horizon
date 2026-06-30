# Horizon Alpha 1.0

Status: Prepared for Chief Software Architect review

Date: 2026-06-30

## Objective

Horizon Alpha 1.0 records the completion of the first architectural generation of Horizon.

This release freezes the first coherent path from Asset identity to live physical observation, local ingestion, Timeline memory, Current State projection, and the first mobile client experience.

Alpha 1.0 is not the completion of the Living Digital Twin. It is the foundation on which the Living Digital Twin can be built without weakening memory, evidence, traceability, or domain sovereignty.

## Release Scope

Alpha 1.0 includes:

- Project foundation and governance.
- Horizon Kernel.
- Horizon Event Platform.
- Horizon Protocol.
- Asset Domain.
- Observation Domain.
- Application Layer.
- Horizon Lab.
- Temporal Timeline and Replay.
- Current State projection.
- Local JSON Storage.
- Experience Layer for Horizon Lab.
- Observation Catalog.
- Collector Framework.
- Android/ELM327 OBD Collector Spike.
- Android OBD Bridge.
- Milestone M1: First Live Observation.
- Horizon Live Ingestion Gateway.
- Horizon Mobile.

## Project State

Horizon is in Alpha.

The current system can:

- Register Assets.
- Register Observations.
- Persist factual runtime data locally.
- Rebuild Timeline from persisted Observations.
- Rebuild Current State from Timeline.
- Accept live Observation payloads through a local Gateway boundary.
- Preserve Bluetooth, OBD, and Android outside Horizon Core.
- Present Asset state through Horizon Mobile.

The system does not yet implement intelligence, knowledge, recommendations, autonomous diagnosis, or Living Digital Twin runtime behavior.

## Architectural Meaning

Alpha 1.0 establishes that Horizon is not a telemetry dashboard and not an OBD scanner.

The release proves the first memory path:

```text
Asset
  |
  v
Observation Catalog
  |
  v
Observation
  |
  v
Storage
  |
  v
Timeline
  |
  v
Current State
  |
  v
Gateway
  |
  v
Horizon Mobile
```

Physical integration remains outside the Core. The Core receives canonical Observations and preserves them as evidence.

## Release Rule

Alpha 1.0 freezes Generation 1 as the foundation for future capabilities.

Future generations must build on this memory-first architecture. They must not bypass Observation, Timeline, Current State, evidence, or explainability.
