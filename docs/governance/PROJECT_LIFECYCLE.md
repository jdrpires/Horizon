# Project Lifecycle

Status: Draft

## Purpose

This document defines how Horizon evolves as a long-lived platform.

Horizon does not grow by adding isolated functionality directly to the codebase. It evolves through disciplined institutional stages that protect memory, domain language, architectural traceability, and the Living Digital Twin vision.

## Lifecycle Stages

```text
Foundation
  |
  v
Capabilities
  |
  v
Alpha
  |
  v
Beta
  |
  v
Release
  |
  v
LTS
```

## Foundation

Foundation defines what must remain true even when implementations change.

It includes the Constitution, Manifesto, Engineering Playbook, document governance, domain language, protocol boundaries, and initial architectural decisions.

Foundation work is not feature work. It exists to protect the identity of the project.

## Capabilities

A Capability is a coherent platform ability that advances Horizon toward Living Digital Twins.

Capabilities must be grounded in accepted language and architectural review. They may span several sprints, but they must have a clear boundary, non-goals, and validation path.

Examples include Observation Catalog, Temporal Memory, Current State, Storage, Experience Layer, and future Memory Engine work.

## Alpha

Alpha is the stage where foundational capabilities become usable together.

Alpha may include incomplete experience, limited runtime support, and evolving operational practices, but it must preserve domain correctness, evidence, traceability, and architectural boundaries.

## Beta

Beta begins when the core memory path is coherent enough for broader usage.

Beta work focuses on hardening behavior, improving operational confidence, refining user experience, and validating capability interactions without weakening the Domain.

## Release

Release means Horizon has a stable product boundary, stable operating model, and accepted compatibility expectations.

A Release must preserve explainability, memory lineage, and domain sovereignty across supported workflows.

## LTS

LTS is the long-term support stage for stable Horizon behavior.

LTS prioritizes compatibility, migration discipline, documentation accuracy, and protection against architectural drift.

## Evolution Flow

Functional work must not begin as code. Every meaningful evolution follows this path:

```text
Vision
  |
  v
Workshop
  |
  v
RFC
  |
  v
ADR
  |
  v
SPEC
  |
  v
Capability
  |
  v
Sprint
  |
  v
Demo
  |
  v
Merge
```

## Practical Consequences

- A feature cannot bypass Vision, Workshop, RFC, ADR, or SPEC when it changes architecture, domain language, or capability boundaries.
- A Sprint is an execution vehicle, not an architectural approval mechanism.
- A Merge confirms implementation quality only after the documented intent has been satisfied.
- Demo evidence is part of the lifecycle because Horizon must remain understandable, not merely compiled.
- Capabilities must strengthen the memory-first path from Asset to Living Digital Twin.

## Lifecycle Rule

Horizon may move slowly when a decision is unclear. It must not move quickly by forgetting why it exists.
