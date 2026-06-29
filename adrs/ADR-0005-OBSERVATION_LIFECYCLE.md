# ADR-0005: Observation Lifecycle

Status: Accepted

## Context

Horizon needs to record factual measurements about Assets without introducing Knowledge, Insights, Digital Twin behavior, Collector behavior, or infrastructure.

The Engineering Playbook states that events represent truth and state is a projection. Observation therefore records the observed fact and emits a domain event.

## Decision

Model `Observation` as an append-only aggregate created through `RegisterObservation`.

An Observation references an existing Asset by `AssetId`. It records type, value, unit, timestamp, source, and quality. The current lifecycle has one domain transition: registration.

Observation does not mutate Asset, does not infer meaning, does not classify health, and does not create recommendations.

## Consequences

- Observation remains a factual domain boundary.
- Future Knowledge, Insight, Digital Twin, and Collector modules can consume Observation events later.
- In-memory application flows can register Observations without persistence.
- Event Store and replay remain future architectural decisions.
