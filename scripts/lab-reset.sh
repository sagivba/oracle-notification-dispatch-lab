#!/usr/bin/env bash
# Purpose: Remove the disposable Oracle Docker lab container, volume, and network.
# Related decisions: DEC-004, DEC-005, DEC-006, DEC-007.
set -euo pipefail

CONTAINER_NAME="oracle-dev-ai-lab-db"
VOLUME_NAME="oracle-dev-ai-lab-u01"
NETWORK_NAME="oracle-dev-ai-lab-net"

confirm="${1:-}"

cat <<EOF
WARNING: This removes the disposable local Oracle lab runtime.

It will remove, if present:
  Container: ${CONTAINER_NAME}
  Volume:    ${VOLUME_NAME}
  Network:   ${NETWORK_NAME}

This deletes local database runtime state. Git repository files are not removed.
EOF

if [[ "${confirm}" != "--yes" ]]; then
  echo ""
  echo "Re-run with --yes to confirm."
  exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}"; then
  docker rm -f "${CONTAINER_NAME}" >/dev/null
  echo "Removed container: ${CONTAINER_NAME}"
else
  echo "Container not present: ${CONTAINER_NAME}"
fi

if docker volume ls --format '{{.Name}}' | grep -Fxq "${VOLUME_NAME}"; then
  docker volume rm "${VOLUME_NAME}" >/dev/null
  echo "Removed volume: ${VOLUME_NAME}"
else
  echo "Volume not present: ${VOLUME_NAME}"
fi

if docker network ls --format '{{.Name}}' | grep -Fxq "${NETWORK_NAME}"; then
  docker network rm "${NETWORK_NAME}" >/dev/null
  echo "Removed network: ${NETWORK_NAME}"
else
  echo "Network not present: ${NETWORK_NAME}"
fi
