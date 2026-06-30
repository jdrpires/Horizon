# ADR-0009: Presentation Layer

Status: Accepted

## Context

Horizon Lab currently exposes implementation details such as aggregates, event envelopes, UUIDs, and technical field names. This is useful during early engineering sprints, but it is not appropriate for product-oriented usage.

The platform needs a first Experience Layer that improves interaction without changing business rules or architecture.

## Decision

Create `horizon-experience` as a presentation-only package.

The package provides plain terminal rendering, human-friendly formatters, safe prompts, validators, menus, and presenters. It does not import `horizon-domain` and does not contain business rules.

Horizon Lab will use this package to render user-oriented messages and prevent invalid input from terminating the application.

## Consequences

- Horizon Lab becomes more usable without changing Domain, Application, Storage, Timeline, Current State, Replay, Event Bus, or Protocol.
- Technical details remain available internally but hidden from normal user output.
- Future Developer Mode and Experience Profiles can be introduced explicitly in later sprints.
- The terminal experience remains dependency-free because Rich is not introduced in Sprint-011.
