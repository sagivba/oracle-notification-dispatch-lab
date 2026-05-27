#!/usr/bin/env bash
# Purpose: Release packaging workflow entry point for Oracle Notification Dispatch Lab.
# It runs the repository-local Python packaging helper only; it does not connect
# to Oracle, run Docker, access organizational databases, or execute DDL/DML.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-}"

cd "$REPO_ROOT"

[[ -f "AGENTS.md" ]] || {
  printf 'ERROR: scripts/package-release.sh must run from oracle-dev-ai-lab.\n' >&2
  exit 1
}

if [[ -z "$PYTHON_BIN" ]]; then
  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
  elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    printf 'ERROR: python or python3 is required to run the packaging helper.\n' >&2
    exit 1
  fi
fi

"$PYTHON_BIN" tools/package_release.py "$@"
