#!/usr/bin/env bash
# Purpose: Official shell entry point for local Oracle SQL smoke tests.
# It runs only managed SQL files under db/tests/sql against the local
# oracle-dev-ai-lab-db container and does not contain inline DDL or DML.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONTAINER_NAME="oracle-dev-ai-lab-db"
ORACLE_PDB="${ORACLE_PDB:-FREEPDB1}"
SQL_TEST_DIR="${REPO_ROOT}/db/tests/sql"
REMOTE_SQL_TEST_DIR="/tmp/oracle-dev-ai-lab-sql-tests"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

load_dotenv_if_present() {
  local env_file="${REPO_ROOT}/.env"
  local line key value

  [[ -f "$env_file" ]] || return 0

  while IFS= read -r line || [[ -n "$line" ]]; do
    line="${line%$'\r'}"
    [[ -z "$line" || "$line" == \#* || "$line" != *=* ]] && continue

    key="${line%%=*}"
    value="${line#*=}"
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"

    case "$key" in
      ORACLE_PWD|ORACLE_PDB)
        if [[ -z "${!key:-}" ]]; then
          printf -v "$key" '%s' "$value"
          export "$key"
        fi
        ;;
    esac
  done <"$env_file"
}

require_secret_var() {
  local name="$1"
  local value="${!name:-}"

  [[ -n "$value" ]] || fail "Set ${name} in local .env or environment before running run-db-tests.sh."
  [[ "$value" != "change_me_in_local_env" ]] || fail "Replace placeholder value for ${name} before running run-db-tests.sh."
}

load_dotenv_if_present

require_secret_var "ORACLE_PWD"

[[ "$CONTAINER_NAME" == "oracle-dev-ai-lab-db" ]] || fail "DB test target must remain oracle-dev-ai-lab-db."
[[ -n "$ORACLE_PDB" ]] || fail "ORACLE_PDB must not be empty."
[[ -d "$SQL_TEST_DIR" ]] || fail "Missing SQL test directory: db/tests/sql."

command -v docker >/dev/null 2>&1 || fail "docker command was not found."

if [[ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null || true)" != "true" ]]; then
  fail "Local lab container ${CONTAINER_NAME} is not running. Start it separately before running DB smoke tests."
fi

mapfile -t sql_tests < <(find "$SQL_TEST_DIR" -maxdepth 1 -type f -name '*.sql' | sort)
[[ "${#sql_tests[@]}" -gt 0 ]] || fail "No managed SQL smoke tests found under db/tests/sql."

docker exec "$CONTAINER_NAME" mkdir -p "$REMOTE_SQL_TEST_DIR"
docker cp "${SQL_TEST_DIR}/." "${CONTAINER_NAME}:${REMOTE_SQL_TEST_DIR}/"

for sql_test in "${sql_tests[@]}"; do
  test_name="$(basename "$sql_test")"
  printf 'Running SQL smoke test: %s\n' "$test_name"
  docker exec -i "$CONTAINER_NAME" sqlplus -L -S \
    "sys/${ORACLE_PWD}@localhost:1521/${ORACLE_PDB} as sysdba" \
    @"${REMOTE_SQL_TEST_DIR}/${test_name}"
done
