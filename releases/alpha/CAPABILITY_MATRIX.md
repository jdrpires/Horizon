# Horizon Alpha 1.0 Capability Matrix

Status: Prepared for Chief Software Architect review

| Capability | Status | Demo | Release | Documentation |
| --- | --- | --- | --- | --- |
| Capability-001: Foundation, Kernel, Events, Protocol | Released | Local compile and protocol tests | Genesis / Alpha 1.0 | RFC-0001, RFC-0002, RFC-0003, ADR-0001, ADR-0002, ADR-0003 |
| Capability-002: Asset Domain | Released | Asset registration through Horizon Lab | Alpha 1.0 | RFC-0004, ADR-0004, SPEC-0001 |
| Capability-003: Application Layer and Horizon Lab | Released | In-memory Register Asset flow | Alpha 1.0 | SPEC-0002 |
| Capability-004: Observation Domain | Released | Register Asset and Observation in memory | Alpha 1.0 | RFC-0005, ADR-0005, SPEC-0003, engineering/sprint-007 |
| Capability-005: Temporal Memory, Current State, Storage, Experience, Catalog | Released | Timeline, Replay, Current State, persisted Horizon Lab, catalog-driven input | Alpha 1.0 | RFC-0006 to RFC-0010, ADR-0006 to ADR-0010, SPEC-0004 to SPEC-0008 |
| Capability-006: Collector Framework | Released | Fake Collector pipeline | Alpha 1.0 | RFC-0011, ADR-0011, SPEC-0009, engineering/capability-006 |
| Capability-007: Android/ELM327 OBD Collector Spike | Released | Mock OBD probe | Alpha 1.0 | RFC-0012, ADR-0012, SPEC-0010, engineering/capability-007 |
| Capability-008: Android OBD Bridge | Released | Android bridge build and field test path | Alpha 1.0 | RFC-0013, ADR-0013, SPEC-0011, engineering/capability-008 |
| Capability-009: Live Ingestion Gateway | Released | Local Gateway ingestion smoke test | Alpha 1.0 | RFC-0014, ADR-0014, SPEC-0012, engineering/capability-009 |
| Capability-010: Horizon Mobile | Implemented | Android build, unit tests, Gateway query smoke test | Alpha 1.0 | RFC-0015, ADR-0015, SPEC-0013, engineering/capability-010 |

## Notes

- Capability-005 groups the memory-facing sprints that completed the Alpha 1.0 local runtime foundation.
- Capability-010 is included in the Alpha 1.0 release documentation as the first official mobile client and is awaiting Chief Software Architect review in the current branch.
- All listed capabilities are documented through accepted or draft-review artifacts already present in the repository.
