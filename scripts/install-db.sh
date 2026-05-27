#!/usr/bin/env bash
# Purpose: Official shell entry point for the controlled local DB install.
# It targets only the local oracle-notification-dispatch-lab-db container and runs the managed
# SQL entry point db/install/install.sql. It does not contain inline DDL or DML.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

CONTAINER_NAME="oracle-notification-dispatch-lab-db"
ORACLE_PDB="${ORACLE_PDB:-FREEPDB1}"
DB_SOURCE_DIR="${REPO_ROOT}/db"
REMOTE_DB_DIR="/tmp/oracle-notification-dispatch-lab-db"

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

sqlplus_output_has_error() {
  local output="$1"

  [[ "$output" =~ (SP2-|ORA-|PLS-) ]]
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
      ORACLE_PWD|ORACLE_PDB|NOTIF_APP_OWNER_PWD|NOTIF_APP_RUNTIME_PWD|NOTIF_APP_READONLY_PWD|NOTIF_REVIEWER_PWD)
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

  [[ -n "$value" ]] || fail "Set ${name} in local .env or environment before running install-db.sh."
  [[ "$value" != "change_me_in_local_env" ]] || fail "Replace placeholder value for ${name} before running install-db.sh."
}

load_dotenv_if_present

require_secret_var "ORACLE_PWD"
require_secret_var "NOTIF_APP_OWNER_PWD"
require_secret_var "NOTIF_APP_RUNTIME_PWD"
require_secret_var "NOTIF_APP_READONLY_PWD"
require_secret_var "NOTIF_REVIEWER_PWD"

[[ "$CONTAINER_NAME" == "oracle-notification-dispatch-lab-db" ]] || fail "Install target must remain oracle-notification-dispatch-lab-db."
[[ -n "$ORACLE_PDB" ]] || fail "ORACLE_PDB must not be empty."
[[ -f "${DB_SOURCE_DIR}/install/install.sql" ]] || fail "Missing official SQL entry point: db/install/install.sql."

command -v docker >/dev/null 2>&1 || fail "docker command was not found."

if [[ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null || true)" != "true" ]]; then
  fail "Local lab container ${CONTAINER_NAME} is not running. Start it separately before installing."
fi

docker exec "$CONTAINER_NAME" mkdir -p "$REMOTE_DB_DIR"
docker cp "${DB_SOURCE_DIR}/." "${CONTAINER_NAME}:${REMOTE_DB_DIR}/"

set +e
install_output="$(docker exec -i "$CONTAINER_NAME" sqlplus -L -S \
  "sys/${ORACLE_PWD}@localhost:1521/${ORACLE_PDB} as sysdba" \
  @"${REMOTE_DB_DIR}/install/install.sql" \
  "$NOTIF_APP_OWNER_PWD" \
  "$NOTIF_APP_RUNTIME_PWD" \
  "$NOTIF_APP_READONLY_PWD" \
  "$NOTIF_REVIEWER_PWD" \
  "$REMOTE_DB_DIR" 2>&1)"
install_status=$?
set -e

printf '%s\n' "$install_output"

if [[ "$install_status" -ne 0 ]]; then
  fail "SQLPlus install failed with exit status ${install_status}."
fi

if sqlplus_output_has_error "$install_output"; then
  fail "SQLPlus install output contained SP2-, ORA-, or PLS- errors."
fi

printf 'Oracle Notification Dispatch Lab controlled install completed.\n'
