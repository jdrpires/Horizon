# Architecture Governance

Status: Draft

## Purpose

This document defines who may change Horizon architecture and when formal documents are required.

Architecture governance exists to prevent accidental platform drift. It protects the Domain, memory model, evidence chain, explainability, and the long-term Living Digital Twin direction.

## Architecture Authority

The Chief Software Architect owns architectural approval.

Principal Engineers may propose designs, identify inconsistencies, write RFCs, draft ADRs, create SPECs, and implement accepted work. They must escalate conflicts instead of resolving architectural contradictions alone.

Codex may assist with documentation, implementation, validation, and review. Codex does not define architecture independently.

## When An RFC Is Required

An RFC is required when a change:

- Introduces a new Capability.
- Changes domain language.
- Changes package or module boundaries.
- Introduces a new platform protocol or communication rule.
- Alters how facts, memory, projections, knowledge, or AI are understood.
- Creates or changes public contracts between layers.
- Changes compatibility expectations.

An RFC explains intent and boundaries before implementation.

## When An ADR Is Required

An ADR is required when a decision:

- Selects one architectural path among meaningful alternatives.
- Defines or changes a dependency direction.
- Changes persistence, projection, replay, event, or protocol strategy.
- Establishes a new permanent boundary.
- Replaces or supersedes an earlier decision.
- Has consequences future engineers must understand.

An ADR records the decision and its consequences. It must not rewrite history.

## When A SPEC Is Required

A SPEC is required when accepted intent must become implementable behavior.

It is required for:

- New domains.
- New application flows.
- New projections.
- New catalogs or controlled vocabularies.
- New user-facing interaction rules.
- Behavior that needs tests, validation, and acceptance criteria.

A SPEC defines what must happen without smuggling in unrelated architecture.

## When A Capability Must Be Created

A Capability is required when work represents a platform ability rather than a small local change.

Create a Capability when the work:

- Advances the Horizon memory path.
- Requires more than one implementation surface.
- Needs documentation, demo, validation, and review.
- May shape future sprints.
- Introduces vocabulary future engineers will reuse.

## When A Sprint Can Start

A Sprint can start only when:

- The branch is created from the correct base.
- The workspace is clean or known documentary work is explicitly carried.
- Required RFCs, ADRs, and SPECs exist or are part of the sprint opening instructions.
- Dependencies from previous sprints are present.
- Inconsistencies have been escalated and resolved.
- Non-goals are explicit.

No Sprint may start from an architectural guess.

## When A Merge Can Happen

A Merge can happen only when:

- The implementation matches accepted documents.
- Tests and required quality checks are executed or explicitly documented as unavailable.
- Documentation created by the sprint is complete.
- No accepted document was overwritten silently.
- No forbidden scope was introduced.
- CHANGELOG, roadmap, result, or review artifacts are updated when required by the sprint.
- The branch is ready to become part of the main development line.

## Conflict Rule

If implementation pressure conflicts with accepted architecture, architecture wins until the Chief Software Architect records a new decision.

## Governance Rule

No convenience may become architecture by accident.
