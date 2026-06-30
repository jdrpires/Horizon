# Document Hierarchy

Status: Draft

## Purpose

This document defines the official hierarchy of Horizon documentation.

Documents are not equal in authority. Higher documents define enduring meaning. Lower documents translate that meaning into decisions, specifications, and implementation.

## Official Hierarchy

```text
README
  |
  v
Constitution
  |
  v
Manifesto
  |
  v
Engineering Playbook
  |
  v
Governance
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
Implementation
```

## README

The README is the public entry point.

It explains what Horizon is, how to begin, and where authoritative documents live. It orients readers but does not replace deeper documents.

## Constitution

The Constitution defines the permanent essence of Horizon.

It answers what Horizon is. It remains valid even if the implementation is rewritten. No lower document may contradict it.

## Manifesto

The Manifesto defines the long-term Living Digital Twin direction.

It protects the product philosophy and prevents premature or accidental implementation of the Twin.

## Engineering Playbook

The Engineering Playbook defines engineering discipline, code culture, decision expectations, and delivery rules.

It governs how work should be performed.

## Governance

Governance documents define institutional process.

They explain lifecycle, authority, document hierarchy, decision process, capability model, and repository principles.

## RFC

RFCs define architectural intent, domain language, or capability boundaries.

They answer why a capability or boundary should exist before implementation begins.

## ADR

ADRs record accepted architectural decisions and their consequences.

They answer what decision was made and why future work must respect it.

## SPEC

SPECs define implementable behavior.

They translate accepted intent and decisions into testable expectations.

## Implementation

Implementation is the current executable expression of accepted documents.

It is important, but it is not the source of architectural truth. Code may reveal gaps, but it must not silently redefine Horizon.

## Precedence Rule

When documents conflict, the higher document prevails.

When implementation conflicts with accepted documents, implementation must be corrected or a new architectural decision must be approved.

## Historical Rule

Accepted documents are not erased to make the present look simpler.

Superseded, deprecated, rejected, and archived documents remain part of Horizon's memory.
