# ADR-0003: Horizon Event Platform Boundary

Status: Accepted

## Context

Horizon needs events to move through the platform consistently. The Engineering Playbook states that events represent truth, but infrastructure decisions should not be made without architecture approval.

## Decision

Implement `horizon-events` as a pure, technology-agnostic event platform.

The Event Platform defines:

- Event envelopes.
- Event metadata.
- Correlation and causation propagation.
- In-memory publication and dispatch.
- Subscribers and filters.
- Serialization contract and dictionary serializer.
- Event registry.
- Event and schema versioning primitives.
- Middleware pipeline.
- Contracts for future Event Store, streams, snapshots, and dead-letter behavior.

The Event Platform does not implement persistence, brokers, queues, databases, or external infrastructure.

## Consequences

- Horizon can standardize event shape and flow before choosing infrastructure.
- Event Store and broker decisions remain open and must be captured by future RFCs and ADRs.
- Tests can validate event behavior without external services.
- Future adapters can implement contracts without changing the core event model.
