# Capability-011 Review

Status: Draft

## Review Scope

Review the monorepo runtime capability.

## Architectural Checks

- Runtime is solved through editable installation.
- Gateway does not mutate `sys.path`.
- Horizon Lab does not mutate `sys.path`.
- Tools do not mutate `sys.path`.
- Manual `PYTHONPATH` is not required.
- Domain does not depend on services.
- Domain does not depend on apps.
- Gateway behavior remains unchanged.
- Android remains unchanged.
- No business rule was changed.

## Review Notes

Pending Chief Software Architect review.
