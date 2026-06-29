# ADR-0001: Monorepo Foundation

Status: Accepted

## Context

The Engineering Playbook requires Horizon to use a monorepo. No service should exist outside the repository. The project needs a professional foundation before product features are implemented.

## Decision

Use a monorepo with the following top-level areas:

- `apps/`
- `services/`
- `packages/`
- `docs/`
- `rfcs/`
- `adrs/`
- `infra/`
- `tools/`
- `tests/`
- `examples/`

The repository includes common development workflow files such as README, license, Docker Compose, Makefile, pyproject configuration, pre-commit configuration, GitHub templates, and CI.

## Consequences

- Shared libraries and services evolve in one repository.
- Architecture documentation, RFCs, and ADRs live beside the code.
- Local development and CI can enforce a consistent engineering baseline.
- Package ownership and release boundaries must be clarified as the platform grows.
