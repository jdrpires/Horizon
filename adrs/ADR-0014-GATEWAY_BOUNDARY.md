# ADR-0014: Gateway Boundary

Status: Accepted

## Context

Horizon has external collectors and an Android OBD Bridge capable of producing observation payloads from a real Asset.

The platform now needs a local ingestion endpoint, but HTTP must not become part of Domain, Application, Storage, Timeline, Current State, Catalog, or Collector Framework design.

## Decision

Create `services/horizon-gateway` as an outer boundary service.

The Gateway uses FastAPI and Pydantic for local HTTP schema validation. It resolves Observation definitions through the Observation Catalog, maps incoming payload entries through the Collector Framework, and publishes Canonical Observations into the existing Application Layer.

The Gateway may depend on Horizon packages because it is an outer composition boundary. Horizon Core packages must not depend on the Gateway.

The Gateway rejects unknown Asset references. It does not create Assets automatically.

## Consequences

- Android OBD Bridge payloads can enter Horizon locally through `POST /observations`.
- Bluetooth remains outside Horizon Core.
- HTTP remains outside Horizon Core.
- Observation language continues to be protected by the Observation Catalog.
- Existing Application, Storage, Timeline, and Current State behavior is reused.
- The Gateway can be replaced later without rewriting Domain or Application.
- Operators must register or otherwise provide an existing Asset reference before live ingestion.

