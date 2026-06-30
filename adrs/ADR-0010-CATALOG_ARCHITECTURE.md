# ADR-0010: Catalog Architecture

Status: Accepted

## Context

Horizon Lab currently asks users to type Observation types freely. That creates inconsistent names and makes future API, Collector, Mobile, Twin, and AI consumers harder to align.

The current Observation runtime accepts numeric values only and must not be changed in Sprint-012.

## Decision

Create `horizon-catalog` as an independent catalog package.

The package contains Observation definitions, profile definitions, registry lookup, internal loaders, validation, contracts, and catalog exceptions. It does not import Domain, Application, Storage, Timeline, Current State, Event Bus, Protocol, or Experience.

Horizon Lab may consume the catalog to remove free typing from the user flow. In this sprint, it registers only definitions whose value type is `number`.

## Consequences

- Observation naming becomes catalog-driven.
- Non-numeric definitions can be modeled before runtime support exists.
- No artificial value conversion is introduced.
- Future `Observation Value Model` work has a clean boundary.
