# Document Governance

Status: Accepted

## Purpose

Document governance defines how Horizon records architecture, product language, implementation specifications, and sprint evidence.

Documentation is part of the system. Accepted documents must not be silently rewritten, renumbered, or deleted.

## Document States

Official documents may use these states:

- `Draft`: proposed and not yet authoritative.
- `Accepted`: approved and authoritative.
- `Superseded`: replaced by a newer document while retained for history.
- `Deprecated`: discouraged for future work but not directly replaced.
- `Rejected`: evaluated and declined.
- `Archived`: retained as historical material with no current authority.

## RFC Policy

RFCs define architectural intent, domain language, or capability boundaries before implementation.

- A published RFC never changes number.
- A published RFC is never deleted.
- RFC numbering is monotonic within the RFC series.
- New major capabilities require an RFC before implementation.
- Accepted RFCs may be clarified, but architectural changes require a new RFC or an explicit superseding document.

## ADR Policy

ADRs record architectural decisions.

- ADRs are immutable decision records.
- ADR numbering is monotonic within the ADR series.
- A new decision must not rewrite an older decision.
- If a decision changes, create a new ADR and mark the older ADR as superseded or deprecated when appropriate.

## SPEC Policy

SPECs define implementable behavior for a domain, application layer, or capability.

- SPECs must align with accepted RFCs and ADRs.
- SPEC numbering is monotonic within the SPEC series.
- SPECs may be updated during the sprint that creates them.
- After acceptance, behavior-changing updates require review and must preserve historical context.

## Numbering Convention

Documents use four-digit numeric identifiers:

- `RFC-0001-NAME.md`
- `ADR-0001-NAME.md`
- `SPEC-0001-NAME.md`

Numbers are never reused, even if a document becomes rejected, deprecated, superseded, or archived.

## Relationship Between Documents

- RFCs explain why a capability or boundary should exist.
- ADRs explain which architectural decision was made.
- SPECs explain what behavior must be implemented.
- Sprint artifacts explain what was delivered, validated, and reviewed.

When documents conflict, the order of authority is:

1. Engineering Playbook and foundation documents.
2. Accepted ADRs.
3. Accepted RFCs.
4. Accepted SPECs.
5. Sprint artifacts.
6. Code.

## Superseded Policy

Superseded documents remain in the repository.

A superseded document must include:

- `Status: Superseded`
- `Superseded By: <document-id>`

The index should show both the historical document and the active replacement.

## Review Policy

Documents that define architecture, domain language, or product capability require review before implementation.

Reviews must check:

- Consistency with the Engineering Playbook.
- Consistency with existing accepted RFCs, ADRs, and SPECs.
- Clear scope and non-goals.
- No hidden infrastructure or domain leakage.
- No numbering conflicts.

## Responsibilities

- Chief Software Architect: approves architectural decisions and resolves conflicts.
- Principal Engineer: implements according to accepted documents and escalates inconsistencies.
- Codex: assists implementation and documentation, but does not define architecture.
- Reviewers: verify correctness, boundaries, tests, and traceability.
