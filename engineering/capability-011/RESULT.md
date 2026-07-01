# Capability-011 Result

Status: Draft

## Summary

Created the official monorepo runtime path for Horizon development.

The runtime uses an editable install from the repository root so apps, services, and tools can import internal packages without `sys.path` mutation or manual `PYTHONPATH`.

## Cause

The Gateway was executed from `services/horizon-gateway`.

That working directory made the Gateway `app` package importable, but the internal packages such as `horizon_application` were not installed in the active Python environment.

The result was:

```text
ModuleNotFoundError: No module named 'horizon_application'
```

## Delivered

- Root workspace metadata in `pyproject.toml`.
- Gateway `app` package included in the root editable package configuration.
- `scripts/bootstrap-dev.sh`.
- `scripts/run-gateway.sh`.
- `docs/architecture/MONOREPO_RUNTIME.md`.
- Removal of local `sys.path` manipulation from:
  - `apps/horizon-lab/main.py`
  - `tools/android_obd_probe.py`
  - `services/horizon-gateway/tests/test_observation_ingestion.py`

## Bootstrap

```bash
scripts/bootstrap-dev.sh
```

If Python 3.12 or newer is not the default:

```bash
PYTHON_BIN=/path/to/python3.12 scripts/bootstrap-dev.sh
```

## Gateway Command

Official command after bootstrap:

```bash
source .venv/bin/activate
cd services/horizon-gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Shortcut:

```bash
scripts/run-gateway.sh
```

## Python Version Audit

Question: does Horizon currently depend on Python 3.13?

Answer: no.

The repository currently uses Python 3.12-era syntax and typing features, but no Python 3.13-exclusive feature was found.

Observed language features:

- `type | None` unions: supported before Python 3.12.
- `typing.Self`: supported in Python 3.11.
- Pattern-free dataclasses and protocols: supported before Python 3.12.
- Inline generic syntax such as `class Result[T]` and `def choose_from_list[T]`: requires Python 3.12, not Python 3.13.

The correct minimum supported runtime for the current codebase is Python 3.12.

## Validation

- Python version audit: passed. No Python 3.13-exclusive language feature was found.
- Python 3.12 syntax audit: passed. The repository compiles with Python 3.12.10.
- Python feature note: inline generic syntax such as `class Result[T]` and `def choose_from_list[T]` requires Python 3.12, not Python 3.13.
- Runtime configuration: updated to `>=3.12,<4.0`.
- Static import workaround search: passed for functional runtime code. Remaining `sys.path` and `PYTHONPATH` references are documentation statements only.
- Domain dependency direction: passed. No Domain package imports `apps`, `services`, Gateway, Horizon Lab, or Horizon Mobile.
- Script syntax: `bash -n scripts/bootstrap-dev.sh scripts/run-gateway.sh` passed.
- Script permissions: both scripts are executable.
- Compile validation: `python3 -m compileall packages services apps/horizon-lab tools tests` passed with Python 3.12.10.
- `git diff --check`: passed.
- Failure reproduction from `services/horizon-gateway`: `python3 -c "import horizon_application"` still fails before bootstrap, confirming the missing editable runtime cause.
- Bootstrap: `scripts/bootstrap-dev.sh` passed with Python 3.12.10 after network access was allowed for dependency installation.
- Editable runtime imports from `services/horizon-gateway`: passed for `horizon_application`, `horizon_domain`, `horizon_storage`, `horizon_catalog`, `horizon_collector`, and Gateway `app`.
- Gateway start: passed from `services/horizon-gateway` with `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`.
- `GET /health`: passed with `200 OK` and `{"status":"ok","service":"horizon-gateway"}`.
- `POST /observations`: passed with `202 Accepted`, `accepted=1`, `timeline_entries=1`, and `current_state_values=1`.
- Horizon Lab runtime: passed. It started without `sys.path` mutation, loaded 1 Asset and 1 Observation from temporary storage, and exited through the menu.
- Gateway tests: `.venv/bin/python -m pytest services/horizon-gateway/tests -q` passed, 7 tests.

## Scope Confirmation

No Domain rule was changed.

No Application behavior was changed.

No Storage behavior was changed.

No Android behavior was changed.

No Gateway endpoint behavior was changed.
