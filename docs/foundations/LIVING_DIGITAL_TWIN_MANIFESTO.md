# Living Digital Twin Manifesto

Status: Accepted

## Purpose

The Living Digital Twin is Horizon's long-term product destination: a continuously evolving representation of an Asset built from facts, timelines, current state, and explainable knowledge.

This manifesto defines principles only. It does not authorize implementation of the Living Digital Twin before its own RFC, ADR, SPEC, and sprint.

## Principles

- The Twin is never mutated directly.
- The Twin evolves from facts and approved projections.
- Observations are factual measurements, not knowledge.
- Timeline is chronological memory, not the Twin.
- Current State is a present-state projection, not the Twin.
- Knowledge interprets evidence; it does not invent facts.
- AI may assist interpretation only through approved Knowledge boundaries.
- Every state must be explainable from source facts.
- Every recommendation must cite evidence.
- Infrastructure stores data, but it does not define domain truth.

## Boundaries

The Living Digital Twin does not read sensors directly. It does not bypass domain events, timelines, or approved projections.

The Living Digital Twin must not be introduced through incidental behavior in Observation, Timeline, Current State, Collector, API, or infrastructure modules.

## Evolution Path

Horizon evolves toward the Living Digital Twin through explicit layers:

1. Asset identity.
2. Observation facts.
3. Temporal Timeline.
4. Current State projection.
5. Knowledge interpretation.
6. Digital Twin behavior.
7. Recommendations and automation.

Each layer requires documentation, tests, and architectural approval before implementation.

## Non-Goals

This manifesto does not implement:

- Digital Twin state.
- Knowledge Engine.
- AI behavior.
- Recommendations.
- Collector behavior.
- Persistence.
- API endpoints.
- Infrastructure adapters.

## Governance

Any implementation claiming to affect the Living Digital Twin requires a dedicated RFC, ADR, SPEC, and review by the Chief Software Architect.
