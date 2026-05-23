#!/usr/bin/env bash
# Purpose: Start the local Oracle AI Database 26ai Free Docker lab for oracle-dev-ai-lab.
# Related decisions: DEC-005, DEC-006, DEC-007, DEC-008, DEC-009.
set -euo pipefail

CONTAINER_NAME="oracle-dev-ai-lab-db"
READY_MESSAGE="DATABASE IS READY TO USE!"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

command -v docker >/dev/null 2>&1 || fail "docker command was not found."

if [[ ! -f ".env" ]]; then
  fail "Create a local .env from .env.example and set ORACLE_PWD before starting the lab."
fi

oracle_pwd="$(
  grep -E '^ORACLE_PWD=' .env 2>/dev/null | tail -n 1 | cut -d '=' -f 2- | tr -d '"'"'"
)"

if [[ -z "${oracle_pwd}" || "${oracle_pwd}" == "change_me_in_local_env" ]]; then
  fail "Set ORACLE_PWD to a local non-placeholder value in .env. Do not commit real passwords."
fi

echo "Starting Oracle AI Database 26ai Free lab container: ${CONTAINER_NAME}"
docker compose up -d db

cat <<EOF

Startup requested.

Readiness check:
  docker logs -f ${CONTAINER_NAME}
  docker logs ${CONTAINER_NAME} | grep '${READY_MESSAGE}'

The lab is ready only after the logs contain:
  ${READY_MESSAGE}

Connection baseline:
  Host: localhost
  Port: 1521
  Service/PDB: FREEPDB1
EOF
