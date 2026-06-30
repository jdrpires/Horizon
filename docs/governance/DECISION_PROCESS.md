# Decision Process

Status: Draft

## Purpose

This document formalizes how Horizon makes significant decisions.

Horizon decisions must be traceable. A future engineer should be able to understand the problem, the alternatives, the decision, the evidence, and the validation path without relying on memory from a meeting or chat thread.

## Official Process

```text
Problem
  |
  v
Workshop
  |
  v
Alternatives
  |
  v
Decision
  |
  v
Record
  |
  v
Implementation
  |
  v
Validation
  |
  v
Demo
```

## Problem

Every significant decision begins with a named problem.

The problem must describe the tension being solved. It must not begin as a preferred implementation.

## Workshop

The Workshop explores context, constraints, risks, domain language, and future consequences.

The goal is to understand the decision space before narrowing it.

## Alternatives

Meaningful alternatives must be considered when the decision affects architecture, domain behavior, or long-term capability direction.

Alternatives may be rejected, but they should be rejected for explicit reasons.

## Decision

The decision selects a path.

It should be small enough to implement and strong enough to guide future work.

## Record

The decision must be recorded in the correct document type.

- RFC records intent and capability boundaries.
- ADR records architectural decisions and consequences.
- SPEC records implementable behavior.
- Sprint artifacts record delivery evidence.

## Implementation

Implementation begins only after the relevant documents exist or are explicitly authorized as part of the sprint.

Implementation must follow the accepted decision. It must not expand scope quietly.

## Validation

Validation proves that the implementation satisfies the decision.

Validation may include tests, manual flows, demo records, review notes, quality tool output, and consistency checks against accepted documents.

## Demo

The Demo shows the decision alive in the system.

It should make the capability understandable, not merely prove that commands run.

## Escalation Rule

If a new inconsistency appears during implementation, the process returns to Workshop or Decision. It does not continue by assumption.

## Decision Rule

The strongest decision is not the fastest one. It is the one future engineers can still explain.
