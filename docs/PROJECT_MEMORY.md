# Project Memory

This document preserves operational context that should not live only in chat history.

## Current State

Project Horizon is a Python monorepo for a connected-asset intelligence platform.

The repository currently contains:

- Professional project foundation and developer workflow.
- `horizon-kernel`, a pure domain primitives library.
- `horizon-events`, a pure event platform library.
- Initial API service shell without product endpoints.
- Docker and Compose foundation for future local development.
- GitHub templates, CI workflow, Makefile, linting, typing, testing, and pre-commit configuration.

## Source Of Truth

Before implementation, read:

- `docs/ENGINEERING_PLAYBOOK.md`
- RFCs in `rfcs/`
- ADRs in `adrs/`
- Architecture documents in `docs/architecture/`

When documentation and code conflict, documentation wins.

## Decisions Already Captured

- The repository is a monorepo.
- The domain must remain independent from frameworks and infrastructure.
- Events are treated as the source of truth; state is a projection.
- The Horizon Kernel is universal and contains no automotive concepts.
- The Horizon Event Platform defines event movement and structure, not persistence or broker infrastructure.
- Event Store, stream persistence, broker selection, schema registry storage, and snapshots remain future decisions.

## Explicitly Not Implemented Yet

- Digital Twin.
- Knowledge Engine.
- AI or LLM behavior.
- Collector behavior.
- OBD behavior.
- Product endpoints.
- Domain-specific business rules.
- Event Store implementation.
- Kafka, Redis Streams, RabbitMQ, Celery, PostgreSQL persistence, or any broker/storage adapter.

## Local Notes

The file `Sem Título 4ENGINEERING_PLAYBOOK.md.rtf` exists locally as the original source artifact used to create `docs/ENGINEERING_PLAYBOOK.md`. It is not versioned in Git.

## Validation History

The Kernel was validated with:

- Ruff.
- Black.
- MyPy.
- Pytest with coverage above 95%.

The Event Platform was validated with:

- Ruff.
- Black.
- MyPy.
- Pytest with coverage above 95%.

## Known Gaps

- `RFC-0001`, `RFC-0002`, `ADR-0001`, `ADR-0002`, and `ADR-0003` now capture current implementation intent after the fact. Future architecture should be documented before implementation.
- Product Principles, Domain Model, and Ubiquitous Language are still not defined.
- The repository does not yet include a generated `poetry.lock`.
- GitHub `CODEOWNERS` contains placeholder organization teams and should be updated to real GitHub handles or teams.

## Recommended Next Sprints

1. Define Product Principles, Domain Model, and Ubiquitous Language.
2. Define the Event Store through a dedicated RFC and ADR.
3. Define observability standards for correlation, tracing, metrics, and logs.
4. Define API boundary conventions before adding endpoints.
5. Define package versioning and release workflow for internal libraries.
