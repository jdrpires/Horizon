#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${VENV_DIR:-"$ROOT_DIR/.venv"}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  cat >&2 <<EOF
Horizon development environment was not found.

Run first:

  scripts/bootstrap-dev.sh
EOF
  exit 1
fi

cd "$ROOT_DIR/services/horizon-gateway"
exec "$VENV_DIR/bin/python" -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
