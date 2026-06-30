# Horizon Alpha 1.0 Known Limitations

Status: Prepared for Chief Software Architect review

Alpha 1.0 is intentionally limited.

The release completes the first memory and ingestion foundation. It does not claim to complete Horizon's intelligence, Living Digital Twin runtime, operational platform, or product ecosystem.

## Not Implemented

### Artificial Intelligence

Horizon Alpha 1.0 does not implement AI behavior.

No model interprets Assets, Observations, Timeline, Current State, or user intent.

### Knowledge Engine

Knowledge is not implemented.

Observations remain facts. Timeline remains memory. Current State remains projection. No component derives explainable knowledge yet.

### Memory Engine

The future Memory Engine is not implemented.

Timeline exists, but contextual memory grouping, history construction, and narrative evidence organization remain Generation 2 work.

### Recommendation Engine

Recommendations are not implemented.

No component suggests action, maintenance, diagnosis, or operational changes.

### Health Engine

Health scoring is not implemented.

Alpha 1.0 does not classify Asset health or generate condition states beyond factual Current State projection.

### Dashboard Web

There is no web dashboard.

Horizon Lab is a local terminal laboratory. Horizon Mobile is the first mobile client.

### Authentication

Authentication is not implemented.

The Gateway is a local ingestion boundary, not a public API.

### Multi-Tenant Runtime

Multi-tenant behavior is not implemented.

Tenant identifiers exist in protocol language, but no operational tenant isolation exists in Alpha 1.0.

### Background Sync

Background synchronization is not implemented.

Horizon Mobile does not run a background service.

### Offline Queue

Offline queueing is not implemented.

The mobile client can emit payloads when configured and connected, but it does not guarantee delivery during offline operation.

### Twin Runtime

The Living Digital Twin runtime is not implemented.

Horizon has Asset identity, Observations, Timeline, Current State, and ingestion boundaries. It does not yet have a living runtime that builds long-term context and knowledge.

## Operational Limitations

- Local JSON storage is suitable for Alpha validation, not production durability.
- The Gateway has no authentication, authorization, rate limiting, or public deployment posture.
- Horizon Mobile uses a simple Android UI and direct Bluetooth collection flow.
- Real vehicle validation requires ELM327 hardware, Android/Realme execution, and local network access.
- Python quality tooling may be unavailable in local environments unless installed explicitly.

## Architectural Limitation

Alpha 1.0 proves the evidence path. It does not prove the intelligence path.

Generation 2 must build intelligence only from memory, evidence, explainability, and accepted architectural records.
