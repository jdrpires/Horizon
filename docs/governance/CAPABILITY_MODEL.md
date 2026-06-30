# Capability Model

Status: Draft

## Purpose

This document defines Horizon's planning vocabulary.

The vocabulary exists to prevent work from being mislabeled. A Sprint is not a Capability. A Capability is not an Epic. A SPEC is not an ADR. Clear names protect clear decisions.

## Epic

An Epic is a large strategic theme.

It may span many Capabilities and many Sprints. It expresses a broad direction, such as a phase of Horizon's evolution toward Living Digital Twins.

An Epic does not authorize implementation by itself.

## Capability

A Capability is a coherent platform ability.

It has a clear boundary, purpose, non-goals, validation path, and relationship to Horizon's memory-first architecture.

A Capability usually requires an RFC, ADR, SPEC, implementation sprint, demo, and review.

## Sprint

A Sprint is a bounded execution period for delivering part or all of a Capability.

It should begin from the correct branch, respect prior work, avoid reimplementation, and close with validation and merge discipline.

A Sprint is not a place to invent architecture without approval.

## Feature

A Feature is a user-visible or system-visible behavior inside a Capability.

It is smaller than a Capability and should remain aligned with the Capability's accepted scope.

## Task

A Task is a specific unit of work.

It may create a file, add a test, update documentation, validate a flow, or implement a narrow behavior. Tasks do not define architectural meaning.

## Bug

A Bug is a correction to behavior that contradicts accepted expectations.

Fixing a bug should preserve architecture. If the bug reveals an architectural contradiction, the decision process must be reopened.

## RFC

An RFC defines why a capability, domain language, or architectural boundary should exist.

It describes goals, non-goals, context, compatibility, and scope before implementation.

## ADR

An ADR records a decision that has architectural consequences.

It preserves the reason a path was chosen and the tradeoffs future engineers must respect.

## SPEC

A SPEC defines testable behavior.

It translates accepted RFCs and ADRs into implementation expectations, examples, flows, invariants, and acceptance criteria.

## Relationship

```text
Epic
  |
  v
Capability
  |
  v
Sprint
  |
  v
Feature
  |
  v
Task
```

Supporting records:

```text
RFC -> ADR -> SPEC -> Implementation -> Review
```

## Naming Rule

Work must be named at the right altitude.

Calling a Capability a Feature makes architecture invisible. Calling a Task a Sprint makes delivery look larger than it is. Horizon requires precise names because memory begins with accurate records.
