# RFC-0001: Horizon Kernel

Status: Accepted

## Summary

Create `horizon-kernel` as a reusable, pure Python domain primitives library for Project Horizon.

## Context

The Engineering Playbook states that the domain is sovereign and must not be influenced by frameworks or infrastructure. The platform needs shared domain primitives before product-specific models are introduced.

## Goals

- Provide reusable base classes and primitives for domain modeling.
- Keep the Kernel independent from FastAPI, databases, Redis, Docker, HTTP, JSON responses, and LLMs.
- Support testable domain code through deterministic primitives such as `Clock`.
- Avoid automotive or product-specific concepts.

## Non-Goals

- Implement Digital Twin behavior.
- Implement Knowledge Engine behavior.
- Implement business rules.
- Implement persistence.
- Implement API endpoints.

## Design

`horizon-kernel` contains:

- `Entity`
- `AggregateRoot`
- `ValueObject`
- `DomainEvent`
- `DomainException`
- `Result`
- `Error`
- `UniqueId`
- `Clock`
- `Specification`
- `DomainService`
- `Repository`
- `EventDispatcher`
- `EventPublisher`

Value Objects are immutable, validated, serializable, and compared by value.

Entities are compared by identity and carry lifecycle metadata.

Aggregate Roots own pending domain events and expose methods to record, publish, retrieve, and clear events.

## Constraints

- Python 3.13.
- Standard library only for Kernel internals.
- Full typing.
- No infrastructure dependencies.
- No product-specific domain concepts.

## Validation

The Kernel must maintain at least 95% test coverage and pass Ruff, Black, and MyPy.
