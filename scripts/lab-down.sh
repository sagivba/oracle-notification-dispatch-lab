#!/usr/bin/env bash
# Purpose: Stop the local Oracle AI Database 26ai Free Docker lab without deleting persisted data.
# Related decisions: DEC-004, DEC-005, DEC-006.
set -euo pipefail

CONTAINER_NAME="oracle-dev-ai-lab-db"

if docker ps -a --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}"; then
  echo "Stopping ${CONTAINER_NAME}. The Docker volume remains intact."
  docker stop "${CONTAINER_NAME}" >/dev/null
else
  echo "Container ${CONTAINER_NAME} does not exist. Nothing to stop."
fi
