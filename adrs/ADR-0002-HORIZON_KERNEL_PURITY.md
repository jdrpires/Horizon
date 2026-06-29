# ADR-0002: Horizon Kernel Purity

Status: Accepted

## Context

The Engineering Playbook states that the domain is sovereign and no technology should influence it. The Kernel is expected to be reused by other Horizon modules and potentially by other Python projects.

## Decision

Implement `horizon-kernel` as a pure Python package with no infrastructure or framework dependency.

The Kernel contains universal domain primitives only:

- Entity and Aggregate Root foundations.
- Domain Event foundation.
- Value Object foundation and reusable Value Objects.
- Result and Error primitives.
- Unique identifiers.
- Clock abstraction.
- Repository, Specification, Domain Service, Event Dispatcher, and Event Publisher contracts.

No automotive, Digital Twin, AI, API, database, or infrastructure concept belongs in the Kernel.

## Consequences

- Domain primitives remain easy to test.
- Services can depend on the Kernel without pulling infrastructure.
- Product-specific domain modeling must happen in future packages after RFCs and ADRs define it.
- The Kernel should be versioned carefully because downstream packages will depend on it.
