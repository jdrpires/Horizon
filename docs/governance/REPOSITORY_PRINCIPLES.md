# Repository Principles

Status: Draft

## Purpose

This document defines the principles that govern work inside the Horizon repository.

The repository is not only a code container. It is the institutional memory of Horizon. It must preserve facts, decisions, intent, review, and implementation evidence.

## Never Break The Domain

The Domain is sovereign.

Implementation details, storage needs, presentation preferences, and external integrations must not corrupt domain language or domain invariants.

Consequences:

- Domain concepts must remain small and precise.
- Technical convenience must not rename business meaning.
- New domains must not duplicate existing domain concepts.

## Never Create Architectural Shortcuts

Shortcuts become future architecture when they are merged without record.

Consequences:

- New boundaries require documentation.
- Temporary decisions must be labeled as temporary.
- Hidden coupling must be rejected or recorded for removal.

## Intelligence Begins With Memory

Horizon cannot understand what it cannot remember.

Consequences:

- Memory must precede intelligence.
- Derived behavior must point back to evidence.
- Features that skip memory weaken the Living Digital Twin path.

## Memory Begins With Observations

Every memory trace begins as an observed fact.

Consequences:

- Observations must remain factual.
- Observations must not become knowledge.
- Catalog language must reduce ambiguity before facts accumulate.

## AI Never Replaces The Twin

AI may assist conversation, summarization, interpretation, and exploration.

It does not know the Asset. The Twin knows the Asset through identity, memory, context, and history.

Consequences:

- AI must not become source of truth.
- AI output must not bypass evidence.
- AI behavior requires explicit boundaries before implementation.

## No Decision Without Traceability

Every significant decision must leave a record.

Consequences:

- Architecture decisions belong in ADRs.
- Capability intent belongs in RFCs.
- Behavior expectations belong in SPECs.
- Sprint outcomes belong in engineering artifacts.

## No Implementation Without Documentation

Implementation follows accepted understanding.

Consequences:

- New Capabilities require documentation before code unless the sprint explicitly authorizes document creation first.
- Accepted documents must not be silently overwritten.
- Missing documentation is a blocker, not an implementation detail.

## Preserve Historical Memory

The repository must remember how Horizon changed.

Consequences:

- Superseded documents remain in place.
- Tags mark meaningful milestones.
- Changelogs and result artifacts record what was delivered.

## Keep Boundaries Visible

Boundaries protect meaning.

Consequences:

- Domain, Application, Storage, Experience, Protocol, Events, and Catalog responsibilities must remain distinct.
- Presentation must not alter business rules.
- Storage must not define domain truth.

## Prefer Explanation Over Mystery

Horizon must be explainable to users and engineers.

Consequences:

- Every projection must be reconstructable.
- Every conclusion must be explainable.
- Every recommendation must cite evidence when recommendations exist.

## Repository Rule

The repository must make it harder to forget than to remember.
