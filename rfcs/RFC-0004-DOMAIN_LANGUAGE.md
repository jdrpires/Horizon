# RFC-0004: Domain Language

Status: Accepted

## Summary

Consolidate the official domain language after Genesis and the first vertical slices.

This RFC preserves the accepted intent of `RFC-0003-DOMAIN_LANGUAGE.md` and makes `RFC-0004` the consolidated numbering reference for future domain-language work.

## Official Terms

- `Asset`: the root aggregate for any connected or managed thing.
- `Observation`: a factual measurement made about an Asset at a specific instant.
- `Domain Event`: immutable record of an important domain occurrence.
- `Application Layer`: in-memory orchestration layer that coordinates use cases, handlers, pipelines, repositories, and event publication.

## Non-Terms

The following are not part of the current domain implementation:

- Digital Twin.
- Knowledge.
- Insight.
- Recommendation.
- Collector.
- Journey.
- Persistence.
- Infrastructure.

## Boundary

Domain language belongs in the repository and evolves through RFCs, ADRs, and SPECs before implementation. Future modules must reuse the existing language instead of introducing parallel terms.

## Relationship To Earlier RFCs

`RFC-0003-DOMAIN_LANGUAGE.md` remains accepted historical context. `RFC-0004-DOMAIN_LANGUAGE.md` is the consolidated official reference after the Git Flow reorganization.
