# Monorepo Runtime

Status: Draft

## Purpose

Horizon services, apps, and tools must run through the monorepo runtime instead of local path hacks.

The runtime exists to make internal packages importable from any entry point without `sys.path` mutation, ad hoc `PYTHONPATH`, or service-local workarounds.

## Problem

The M2 live ingestion test exposed:

```text
ModuleNotFoundError: No module named 'horizon_application'
```

The Gateway was started from:

```bash
cd services/horizon-gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

From that working directory, Python can resolve the Gateway `app` package, but it cannot resolve internal Horizon packages unless the monorepo is installed into the active environment.

The correct fix is not to append paths at runtime. The correct fix is to install the Horizon workspace as an editable package.

## Runtime Model

The repository root is the installable workspace.

The root `pyproject.toml` declares the internal Horizon packages and the Gateway `app` package. Development environments install the root project in editable mode.

```text
Repository root
  |
  v
Editable install
  |
  v
Active virtual environment
  |
  v
apps, services, tools
```

## Internal Packages

The editable runtime exposes:

- `horizon_kernel`
- `horizon_events`
- `horizon_protocol`
- `horizon_domain`
- `horizon_application`
- `horizon_storage`
- `horizon_experience`
- `horizon_catalog`
- `horizon_collector`
- `collector_obd`
- `app` for the local Horizon Gateway service package

## Bootstrap

Run from the repository root:

```bash
scripts/bootstrap-dev.sh
```

The script:

- requires Python 3.12 or newer;
- creates `.venv` if needed;
- installs the root project in editable mode;
- verifies imports for the core Horizon packages.

It does not set `PYTHONPATH`.

## Gateway Runtime

After bootstrap:

```bash
source .venv/bin/activate
cd services/horizon-gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Or use:

```bash
scripts/run-gateway.sh
```

## Rules

- Do not solve imports with `sys.path.append`.
- Do not require manual `PYTHONPATH`.
- Do not add Gateway-local import hacks.
- Do not make Domain depend on services or apps.
- Runtime configuration must stay outside business rules.

## Validation

A valid monorepo runtime must prove:

- internal package imports work from the active environment;
- Gateway starts from `services/horizon-gateway`;
- `GET /health` responds;
- `POST /observations` still uses the existing ingestion pipeline;
- Horizon Lab runs without local path manipulation;
- Domain packages do not import apps or services.
