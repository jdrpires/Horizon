# Project Horizon

Project Horizon is a monorepo for a connected-asset intelligence platform built around explicit domain boundaries, immutable events, and long-term operational clarity.

The project is in its foundation phase. The repository intentionally contains infrastructure, tooling, documentation entry points, and package boundaries only. Business rules, Digital Twin behavior, collectors, OBD flows, and AI capabilities are not implemented in this phase.

## Vision

Horizon is designed to support connected assets for years, with engineering practices that favor correctness, traceability, and explainability over short-term shortcuts.

The platform follows the principles documented in the Engineering Playbook:

- The domain is sovereign.
- Events represent truth; state is a projection.
- Services communicate through contracts, not implementation details.
- Architecture decisions belong in the repository.
- AI proposes and assists, but does not define architecture.

## Architecture

Horizon uses a monorepo organized around applications, services, packages, infrastructure, tools, tests, and documentation.

The foundation is prepared for:

- Python 3.13 services with FastAPI and Pydantic v2.
- Clean Architecture and DDD boundaries.
- Event Sourcing as a platform principle.
- PostgreSQL, TimescaleDB, pgvector, and Redis infrastructure.
- Docker Compose for local development.
- GitHub Actions for continuous integration.
- Poetry, Ruff, Black, MyPy, Pytest, Coverage, and Pre-commit.

Architectural details must be defined through RFCs and ADRs before implementation.

## How To Run

Install dependencies:

```bash
make install
```

Run quality checks:

```bash
make lint
make test
```

Run the API service locally:

```bash
make run
```

Run the local infrastructure and API container:

```bash
make docker
```

## Structure

```text
apps/
  collector-android/
  web-console/
services/
  api/
packages/
  kernel/
    domain/
      aggregates/
      contracts/
      errors/
      events/
      ids/
      value_objects/
  shared/
docs/
rfcs/
adrs/
infra/
tools/
tests/
examples/
```

## Contribution

Contributions must follow the Engineering Playbook.

- Use Conventional Commits.
- Open RFCs for major functionality.
- Record architectural decisions as ADRs.
- Keep domain logic independent from frameworks and infrastructure.
- Add tests for meaningful behavior.
- Keep pull requests small, reviewable, and linked to the relevant RFC or ADR when applicable.

Before opening a pull request, run:

```bash
make lint
make test
make coverage
```

## Roadmap

- Establish repository foundation and engineering workflow.
- Formalize the initial platform RFCs and ADRs.
- Define service boundaries and contracts.
- Introduce the first domain model through approved RFCs.
- Add infrastructure observability standards.
- Implement product capabilities only after the architecture is approved.

## Documentation

- [Engineering Playbook](docs/ENGINEERING_PLAYBOOK.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Product Vision](docs/PRODUCT_VISION.md)
- [RFC Index](rfcs/README.md)
- [ADR Index](adrs/README.md)

## License

Project Horizon is licensed under the terms of the [MIT License](LICENSE).
