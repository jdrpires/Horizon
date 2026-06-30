# ADR-0007: Current State Engine

Status: Accepted

## Context

Horizon can now register Observations and query/replay Timeline entries. The next layer needs to answer the present-state question for an Asset without introducing the Living Digital Twin.

The Living Digital Twin Manifesto states that Current State is a present-state projection, not the Twin.

## Decision

Implement `CurrentState` as an immutable projection built from Timeline replay.

For each Observation type, the projection keeps the latest Timeline entry according to timestamp and sequence ordering. The resulting `CurrentStateSnapshot` is immutable and contains the Asset ID, last update timestamp, Observation count, and latest Observation per type.

Current State reads Timeline only. It does not read Event Envelopes directly and does not mutate Timeline.

## Consequences

- Horizon can answer "How is this Asset now?" in memory.
- Digital Twin work remains explicitly unimplemented.
- Future Knowledge and Twin modules can consume Current State without changing Timeline.
- Deterministic replay remains the source of projection consistency.
