#!/usr/bin/env bash
# Purpose: Static review workflow entry point for Oracle Notification Dispatch Lab DB code.
# It performs repository-only contract checks and validates the review report
# template without connecting to Docker, Oracle, or organizational databases.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPORT_PATH="${REPO_ROOT}/db/review/review-report.md"

failures=0

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  failures=$((failures + 1))
}

require_file() {
  local path="$1"
  [[ -f "${REPO_ROOT}/${path}" ]] || fail "Missing required file: ${path}"
}

require_report_text() {
  local text="$1"
  grep -Fq "$text" "$REPORT_PATH" || fail "Review report is missing: ${text}"
}

check_no_forbidden_targets() {
  local checked_files=(
    "scripts/review-db-code.sh"
    "docs/review-workflow.md"
    "db/review/review-report.md"
  )
  local connection_pattern='(HOST|host|CONNECT_STRING|DSN|dsn|SERVICE_NAME|jdbc:|//).*(production|prod[-]db|staging|shared[-]db|organizational)'

  for path in "${checked_files[@]}"; do
    # The docs must mention organizational DBs as forbidden targets, so this
    # check is intentionally limited to connection-style values.
    if grep -Eiv 'connection_pattern=' "${REPO_ROOT}/${path}" | grep -Eiq "$connection_pattern"; then
      fail "Possible forbidden DB target reference in ${path}"
    fi
  done
}

check_versioned_db_sources() {
  local invalid_paths

  invalid_paths="$(
    find "${REPO_ROOT}/db/src" -type f \
      ! -name '*.sql' \
      ! -name 'README.md' \
      -print
  )"

  if [[ -n "$invalid_paths" ]]; then
    printf '%s\n' "$invalid_paths" >&2
    fail "DB source files must be versioned SQL files or README placeholders."
  fi
}

main() {
  cd "$REPO_ROOT"

  require_file "AGENTS.md"
  require_file "docs/safety-rules.md"
  require_file "docs/decision-log.md"
  require_file "docs/spec-pipeline.md"
  require_file "docs/review-workflow.md"
  require_file "db/review/review-report.md"
  require_file "db/src/tables/lab_smoke_test.sql"
  require_file "db/install/install.sql"
  require_file "scripts/install-db.sh"
  require_file "scripts/run-db-tests.sh"

  require_report_text "## Spec coverage"
  require_report_text "## Infrastructure decisions coverage"
  require_report_text "## Object inventory"
  require_report_text "## Data model review"
  require_report_text "## PL/SQL review"
  require_report_text "## Security review"
  require_report_text "## Deployment review"
  require_report_text "## Risks"
  require_report_text "## Required fixes"
  require_report_text "## Optional improvements"
  require_report_text "## Approval status"
  require_report_text "BLOCKER"
  require_report_text "MAJOR"
  require_report_text "MINOR"
  require_report_text "QUESTION"
  require_report_text "A release package is not approved if any BLOCKER exists."

  check_versioned_db_sources
  check_no_forbidden_targets

  if [[ "$failures" -gt 0 ]]; then
    printf 'Review skeleton checks failed with %s issue(s).\n' "$failures" >&2
    return 1
  fi

  printf 'Review skeleton checks passed. Report template: %s\n' "$REPORT_PATH"
}

main "$@"
