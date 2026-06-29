# RFC-0002: Horizon Event Platform

Status: Accepted

## Summary

Create `horizon-events` as a reusable, technology-agnostic event platform library.

## Context

The Engineering Playbook states that events represent truth and that important behavior must be traceable. Horizon needs a common way to represent and move events without choosing infrastructure too early.

## Goals

- Represent events, envelopes, metadata, correlation, causation, publication, subscription, serialization, and versioning.
- Provide an in-memory event bus for local, dependency-free dispatch.
- Provide contracts for future infrastructure integration.
- Keep the platform independent from brokers, databases, web frameworks, and storage decisions.

## Non-Goals

- Implement an Event Store.
- Implement Kafka, Redis, RabbitMQ, Celery, PostgreSQL, or any broker adapter.
- Implement persistence.
- Implement product-specific events.
- Implement domain business rules.

## Design

`horizon-events` contains:

- `EventEnvelope`
- `EventMetadata`
- `CorrelationContext`
- `InMemoryEventBus`
- `InMemoryEventDispatcher`
- `InMemoryEventPublisher`
- Subscribers, handlers, subscriptions, and filters.
- Event registry.
- `DictionarySerializer`.
- Event and schema versioning primitives.
- Middleware contracts and pure middleware implementations.
- Contracts for Event Store, Event Stream, Snapshot Store, and dead-letter boundaries.

Correlation uses `ContextVars`, not global mutable state.

Serialization is dictionary-based and does not depend on JSON directly.

## Constraints

- Python 3.13.
- Standard library only.
- Full typing.
- No infrastructure decisions.
- No automotive or product-specific concepts.

## Validation

The Event Platform must maintain at least 95% test coverage and pass Ruff, Black, and MyPy.
