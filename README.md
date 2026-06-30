# Horizon

Horizon is an operating system for Living Digital Twins.

Horizon is not a telemetry system.
It is not a dashboard.
It is not an OBD reader.
It is not automotive software.

Horizon exists to help connected assets become understandable over time.
It treats memory as the foundation of intelligence.
It treats observations as facts, not conclusions.
It treats state as projection, not truth.
It treats knowledge as something derived, revisable, and explainable.
It exists so an Asset can carry identity, history, context, and meaning through a Living Digital Twin.

## Read First

New developers should read these documents before reading the code:

1. [Horizon Constitution](docs/foundations/HORIZON_CONSTITUTION.md)
2. [Living Digital Twin Manifesto](docs/foundations/LIVING_DIGITAL_TWIN_MANIFESTO.md)
3. [Engineering Playbook](docs/ENGINEERING_PLAYBOOK.md)

Understanding these documents is more important than understanding the current implementation. The code will evolve. These documents define what must remain true when it does.

## Core Principles

- **Memory precedes Intelligence**: Horizon cannot understand what it cannot remember.
- **Knowledge is derived**: Knowledge is never stored as absolute truth; it is continuously derived from memory.
- **Timeline stores facts**: Timeline records what happened. It does not interpret.
- **Current State is a projection**: Current State is the latest known view derived from Timeline.
- **Every Twin has identity**: One Asset has one Living Digital Twin across its existence.
- **Every conclusion is explainable**: Conclusions, hypotheses, and recommendations must trace back to evidence.
- **The Domain is sovereign**: Technology must never shape the meaning of the domain.
- **Observation is not Knowledge**: An Observation is a fact observed at a moment, not an insight.
- **AI is not Memory**: AI may converse with the Twin, but it does not replace the Twin's history.
- **Catalogs protect language**: Observations should be born from shared vocabulary, not arbitrary names.

## Architecture Overview

Horizon evolves through a memory-first path:

```text
Asset
  ↓
Observation Catalog
  ↓
Observation
  ↓
Timeline
  ↓
Current State
  ↓
Memory Engine (future)
  ↓
Living Digital Twin (future)
  ↓
Knowledge Engine (future)
  ↓
Conversation Engine (future)
  ↓
LLM
```

The current system starts with Asset identity, factual Observations, a catalog for consistent Observation language, chronological Timeline memory, and Current State projection. Future capabilities will build memory, knowledge, conversation, and Living Digital Twin behavior on top of those foundations.

## Repository Structure

```text
apps/
  horizon-lab/                 Local interactive lab
packages/
  horizon-application/         In-memory orchestration and use cases
  horizon-catalog/             Official Observation Catalog
  horizon-collector/           Generic external Observation ingestion framework
  horizon-domain/              Asset, Observation, Timeline, Current State
  horizon-events/              Event envelopes and in-memory event movement
  horizon-experience/          User-facing terminal presentation helpers
  horizon-kernel/              Domain primitives
  horizon-protocol/            Platform language and contracts
  horizon-storage/             Local JSON fact storage adapter
  kernel/                      Earlier shared package boundary
  shared/                      Shared package boundary
services/
  api/                         API service boundary
docs/
  foundations/                 Constitution and permanent manifestos
  engineering/                 Governance documents
  specifications/              Implementable specifications
  architecture/                Architecture notes
rfcs/                          Architecture and capability proposals
adrs/                          Architecture decision records
infra/                         Infrastructure boundary
tools/                         Developer tooling
tests/                         Cross-project tests
examples/                      Example assets and usage
storage/                       Local runtime storage directory
```

## Getting Started

Install dependencies:

```bash
make install
```

Run Horizon Lab:

```bash
python apps/horizon-lab/main.py
```

Run tests:

```bash
make test
```

Run linting:

```bash
make lint
```

Run coverage:

```bash
make coverage
```

Run with Docker:

```bash
make docker
```

Horizon Lab is the main local entry point today. It lets you register Assets, select Observation definitions from the catalog, register numeric Observations, view Timeline, and view Current State using local runtime storage.

## Documentation

- **Constitution**: Permanent answer to "What is Horizon?"
  - [docs/foundations/HORIZON_CONSTITUTION.md](docs/foundations/HORIZON_CONSTITUTION.md)
- **Manifesto**: Long-term Living Digital Twin principles.
  - [docs/foundations/LIVING_DIGITAL_TWIN_MANIFESTO.md](docs/foundations/LIVING_DIGITAL_TWIN_MANIFESTO.md)
- **Engineering Playbook**: Engineering principles, workflow, and decision discipline.
  - [docs/ENGINEERING_PLAYBOOK.md](docs/ENGINEERING_PLAYBOOK.md)
- **RFCs**: Architectural intent, capability boundaries, and domain language before implementation.
  - [rfcs/README.md](rfcs/README.md)
- **ADRs**: Accepted architectural decisions and their consequences.
  - [adrs/README.md](adrs/README.md)
- **SPECs**: Implementable behavior for accepted capabilities.
  - [docs/specifications/](docs/specifications/)
- **Document Governance**: Rules for document states, numbering, review, and superseded records.
  - [docs/engineering/DOCUMENT_GOVERNANCE.md](docs/engineering/DOCUMENT_GOVERNANCE.md)

## Project Governance

Horizon evolves through institutional governance before implementation. Major work begins with vision and workshop, then moves through RFC, ADR, SPEC, Capability, Sprint, Demo, and Merge.

- [Project Lifecycle](docs/governance/PROJECT_LIFECYCLE.md): How Horizon moves from Foundation to Capabilities, Alpha, Beta, Release, and LTS.
- [Architecture Governance](docs/governance/ARCHITECTURE_GOVERNANCE.md): Who may change architecture and when RFCs, ADRs, SPECs, Capabilities, Sprints, and Merges are allowed.
- [Document Hierarchy](docs/governance/DOCUMENT_HIERARCHY.md): The official order of authority from README and Constitution down to implementation.
- [Decision Process](docs/governance/DECISION_PROCESS.md): The required path from problem to workshop, decision, record, validation, and demo.
- [Capability Model](docs/governance/CAPABILITY_MODEL.md): The difference between Epics, Capabilities, Sprints, Features, Tasks, Bugs, RFCs, ADRs, and SPECs.
- [Repository Principles](docs/governance/REPOSITORY_PRINCIPLES.md): The repository rules that protect Domain, memory, explainability, and traceability.

## Current Project Status

Horizon is in Alpha.

Implemented:

- Foundation
- Asset
- Observation
- Timeline
- Replay
- Current State
- Storage
- Experience Layer
- Observation Catalog
- Collector Framework

Still on the roadmap:

- Observation Value Model
- Memory Engine
- Living Digital Twin
- Knowledge Engine
- Conversation Engine
- Transport-specific Collectors
- API

## Contribution

Contributions must respect the [Engineering Playbook](docs/ENGINEERING_PLAYBOOK.md).

- Use Conventional Commits.
- Keep changes small, traceable, and reviewable.
- Do not introduce architectural changes without an RFC.
- Record accepted architectural decisions as ADRs.
- Align implementation with accepted SPECs.
- Preserve the sovereignty of the Domain.
- Keep facts, projections, knowledge, and presentation separate.
- Add tests for meaningful behavior.

Before proposing changes, read the Constitution, Manifesto, and Playbook. If a change weakens Horizon's memory, evidence, explainability, or Twin identity, it does not belong here.

## License

Project Horizon is licensed under the terms of the [MIT License](LICENSE).
