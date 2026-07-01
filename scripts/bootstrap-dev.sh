#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
VENV_DIR="${VENV_DIR:-"$ROOT_DIR/.venv"}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  cat >&2 <<EOF
Python runtime not found: $PYTHON_BIN

Horizon targets Python 3.12 or newer.
Install Python 3.12+ or run this script with:

  PYTHON_BIN=/path/to/python3.12 scripts/bootstrap-dev.sh
EOF
  exit 1
fi

"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' || {
  "$PYTHON_BIN" --version >&2
  echo "Horizon requires Python >= 3.12." >&2
  exit 1
}

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -e "$ROOT_DIR"
"$VENV_DIR/bin/python" -c 'import horizon_application, horizon_catalog, horizon_collector, horizon_domain, horizon_events, horizon_experience, horizon_kernel, horizon_protocol, horizon_storage; print("Horizon editable runtime ready.")'

cat <<EOF

Bootstrap complete.

Activate the environment:

  source "$VENV_DIR/bin/activate"

Run Gateway:

  cd "$ROOT_DIR/services/horizon-gateway"
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
EOF
