# ADR-0006: Temporal Timeline

Status: Accepted

## Context

Horizon needs a chronological memory of Asset Observations before a Digital Twin can be safely introduced. Observation records facts, but consumers need a stable way to query and replay those facts in time order.

The Engineering Playbook states that events represent truth and state is projection. Timeline is therefore modeled as an in-memory chronological projection over Observation facts, not as the Twin itself.

## Decision

Implement a Temporal Memory Engine centered on `Timeline`.

Timeline stores immutable `TimelineEntry` objects derived from registered Observations. It supports chronological ordering, filtering by Asset, Observation type, and period, timestamp cursor navigation, and deterministic replay.

The first implementation uses `InMemoryTimelineRepository` only. It does not select an Event Store, database, broker, API, or infrastructure adapter.

## Consequences

- Future Digital Twin work can consume a stable timeline instead of reading raw application state.
- Observation remains factual and does not gain interpretation behavior.
- Replay is available locally without infrastructure.
- Event Store and physical persistence remain future architectural decisions.
