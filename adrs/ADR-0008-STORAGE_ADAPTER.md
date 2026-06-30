# ADR-0008: Storage Adapter

Status: Accepted

## Context

Sprint-010 requires persistence across Horizon Lab restarts while preserving the established architecture: the domain is sovereign, Timeline is chronological memory, and Current State is a projection.

Persisting projections would blur the boundary between facts and derived state.

## Decision

Implement `horizon-storage` as a JSON adapter package.

The adapter persists only Asset and Observation facts. It provides JSON repositories, serializers, storage contracts, and bootstrap support. Domain packages do not import or know `horizon-storage`.

Horizon Lab composes the storage repositories with the application service and rebuilds Timeline by replaying loaded Observations into the in-memory Timeline repository. Current State remains derived from Timeline.

## Consequences

- Restarting Horizon Lab preserves Assets and Observations.
- Timeline and Current State remain deterministic projections.
- JSON storage is inspectable and versionable.
- Future storage engines can implement the same repository contracts without changing domain behavior.
- Corrupt JSON is reported as storage corruption instead of silently mutating facts.
