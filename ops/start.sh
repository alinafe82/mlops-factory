#!/usr/bin/env bash
set -euo pipefail
export UVICORN_HOST="${UVICORN_HOST:-0.0.0.0}"
export UVICORN_PORT="${UVICORN_PORT:-8000}"
export SKIP_MODEL_LOAD="${SKIP_MODEL_LOAD:-0}"
exec uvicorn app.main:app --host "$UVICORN_HOST" --port "$UVICORN_PORT"
