# Alpha Certification

Status: Prepared for Chief Software Architect review

## Certification

Horizon Alpha 1.1 is certified as:

- Foundation Complete
- Live Vehicle Telemetry Validated
- Memory First Architecture Validated
- Collector Framework Validated
- Gateway Validated
- Android Client Validated
- Current State Validated
- Timeline Validated
- Observation Pipeline Validated

## Evidence Basis

Alpha 1.1 certification is based on Milestone M2: First End-to-End Live Vehicle Telemetry.

The validated field flow was:

```text
Citroën C3 Feel 1.6 AT
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

## Included In Alpha 1.1

- Foundation and governance.
- Asset identity.
- Observation domain.
- Observation Catalog.
- Collector Framework.
- Live Ingestion Gateway.
- Horizon Mobile.
- Bluetooth Session Engine.
- Mobile State Synchronization.
- Timeline.
- Current State.
- Local storage.
- First end-to-end live vehicle telemetry validation.

## Not Included In Alpha 1.1

- Memory Engine.
- Knowledge Engine.
- Twin Runtime.
- AI Layer.
- Recommendation Engine.
- Conversation Engine.
- Production authentication.
- Multi-tenant runtime.
- Offline queue.
- Background mobile sync.
- Production deployment hardening.

## Certification Rule

Alpha 1.1 certifies the live memory path. It does not certify intelligence.

Future intelligence must be derived from the memory path validated here: Asset, Observation, Storage, Timeline, Current State, and explainable derivation.
