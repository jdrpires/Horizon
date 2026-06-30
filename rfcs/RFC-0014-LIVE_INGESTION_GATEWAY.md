# RFC-0014: Live Ingestion Gateway

Status: Accepted

## Summary

Introduce `services/horizon-gateway` as the first official live ingestion boundary for Horizon observations produced by external collectors.

This Gateway is not a public API and not a business layer. It receives collector payloads, validates their shape, resolves Observation definitions through the Observation Catalog, maps them through the Collector Framework, and forwards Canonical Observations into the existing Horizon pipeline.

## Context

Milestone M1 proved that an Android OBD Bridge can observe a physical Asset through ELM327 Bluetooth while keeping Bluetooth outside Horizon Core.

The next boundary is live ingestion. Horizon needs a local endpoint that can receive the Android OBD Bridge payload and move it into Application, Storage, Timeline, and Current State without allowing HTTP concerns to shape Domain or Collector behavior.

## Goals

- Create a local FastAPI service under `services/horizon-gateway`.
- Expose `POST /observations`.
- Accept Horizon-compatible collector payloads.
- Validate source, Asset reference, Observation definitions, values, units, timestamps, and quality.
- Reject unknown Observation Catalog definitions.
- Reject unknown Asset references.
- Use the Collector Framework for Raw Observation to Canonical Observation mapping.
- Publish Canonical Observations into the existing Application Layer.
- Update JSON Storage through existing repositories.
- Rebuild Timeline and Current State through existing Application behavior.
- Enable the Android OBD Bridge to send payloads over HTTP.

## Non-Goals

- Build a public REST API.
- Create authentication, users, JWT, or authorization.
- Create a dashboard.
- Add SQL, ORM, MQTT, WebSocket, Redis, Docker, or external infrastructure.
- Implement Knowledge, AI, Twin Runtime, or Living Digital Twin behavior.
- Change Domain, Application, Storage, Timeline, Current State, Experience, Catalog, Collector Framework, or Android Bluetooth behavior.

## Payload

```json
{
  "source": "android-obd-elm327",
  "asset_id": "<uuid or external_reference>",
  "observations": [
    {
      "definition_id": "engine.rpm",
      "value": 805,
      "unit": "rpm",
      "timestamp": "2026-06-30T20:00:00Z",
      "quality": "good"
    }
  ]
}
```

## Boundary

The Gateway owns HTTP schema validation and forwarding only.

It must not infer domain meaning, create interpretations, or convert unsupported values into numeric observations.

An Asset reference must resolve to an existing Asset ID or existing Asset external reference. The Gateway does not invent Assets.

## Pipeline

```text
Gateway
  |
  v
Schema Validation
  |
  v
Observation Catalog
  |
  v
Collector Framework
  |
  v
Publisher
  |
  v
Application
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
```

## Compatibility

The current Observation runtime remains numeric-only.

Definitions whose `value_type` is not `number` are rejected until the future Observation Value Model expands Observation values.

The Gateway is additive and isolated. Horizon Core packages do not depend on the Gateway.

## Validation

The capability is valid when tests prove:

- A valid payload is accepted.
- Invalid schema is rejected.
- Unknown definitions are rejected.
- Unknown Asset references are rejected.
- Unit mismatches are rejected.
- Collector mapping is executed.
- Storage is updated.
- Timeline grows.
- Current State reflects the latest observations.

