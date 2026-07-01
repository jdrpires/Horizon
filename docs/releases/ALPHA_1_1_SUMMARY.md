# Alpha 1.1 Summary

Status: Prepared for Chief Software Architect review

## Purpose

Alpha 1.1 records the successful validation of live vehicle telemetry through Horizon.

It is not a new product generation. It is an institutional release marker showing that the Generation 1 architecture can carry real observations from physical hardware into Horizon memory.

## What Was Validated

- Citroën C3 Feel 1.6 AT live telemetry.
- Android Realme running Horizon Mobile.
- ELM327 Bluetooth collection.
- Bluetooth Session Engine.
- Mobile State Synchronization.
- Cloudflare Tunnel as field validation bridge.
- Horizon Gateway live ingestion.
- Collector Framework boundary.
- Application observation flow.
- Storage persistence.
- Timeline updates.
- Current State projection.

## Confirmed Runtime Behavior

During the field test:

- `GET /health` returned `200 OK`.
- `GET /assets` returned `200 OK`.
- `POST /observations` returned `202 Accepted`.
- `GET /current-state` returned `200 OK`.
- `GET /timeline` returned `200 OK`.

The mobile runtime no longer produced:

- `asset_id: null`
- `GET /assets/null`
- `422 Unprocessable Entity`

## What Is Not Part Of Alpha

Alpha 1.1 does not include:

- Memory Engine.
- Knowledge Engine.
- Living Digital Twin Runtime.
- AI Layer.
- Recommendation Engine.
- Conversation Engine.
- Production authentication.
- Multi-tenant runtime.
- Offline mobile queue.
- Background sync.

## Generation 2

Generation 2 should build intelligence from memory.

The next capabilities should focus on:

- Observation Value Model.
- Memory Engine.
- Knowledge Engine.
- Health Engine.
- Recommendation Engine.
- Conversation Engine.
- Living Digital Twin Runtime.

Generation 2 must preserve the Alpha lesson: the platform understands assets only through identity, observations, memory, Timeline, Current State, and explainable derivation.
