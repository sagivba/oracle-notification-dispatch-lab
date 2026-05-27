#!/usr/bin/env bash
# Purpose: Back up local Oracle Docker lab metadata and persisted volume data.
# Related decisions: DEC-003, DEC-004, DEC-006, DEC-019.
set -euo pipefail

CONTAINER_NAME="oracle-notification-dispatch-lab-db"
VOLUME_NAME="oracle-notification-dispatch-lab-u01"
BACKUP_ROOT="${BACKUP_ROOT:-backups/oracle-notification-dispatch-lab}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="${BACKUP_ROOT}/${TIMESTAMP}"
WAS_RUNNING="false"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

command -v docker >/dev/null 2>&1 || fail "docker command was not found."
docker ps -a --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}" || fail "Container not found: ${CONTAINER_NAME}"
docker volume ls --format '{{.Name}}' | grep -Fxq "${VOLUME_NAME}" || fail "Volume not found: ${VOLUME_NAME}"

mkdir -p "${BACKUP_DIR}"

docker inspect "${CONTAINER_NAME}" > "${BACKUP_DIR}/container_inspect.json"
docker volume inspect "${VOLUME_NAME}" > "${BACKUP_DIR}/volume_inspect.json"
docker inspect --format '{{.Config.Image}}' "${CONTAINER_NAME}" > "${BACKUP_DIR}/image_name.txt"

cat > "${BACKUP_DIR}/runtime.txt" <<EOF
container=${CONTAINER_NAME}
volume=${VOLUME_NAME}
network=oracle-notification-dispatch-lab-net
oradata_mount=/opt/oracle/oradata
listener_port=1521
pdb=FREEPDB1
created_at=${TIMESTAMP}
EOF

if docker ps --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}"; then
  WAS_RUNNING="true"
  echo "Stopping ${CONTAINER_NAME} before backing up volume data."
  docker stop "${CONTAINER_NAME}" >/dev/null
fi

restart_if_needed() {
  if [[ "${WAS_RUNNING}" == "true" ]]; then
    docker start "${CONTAINER_NAME}" >/dev/null || true
  fi
}
trap restart_if_needed EXIT

docker run --rm \
  -v "${VOLUME_NAME}":/volume \
  -v "$(pwd)/${BACKUP_DIR}":/backup \
  alpine sh -c 'tar czf /backup/oradata.tar.gz -C /volume .'

echo "Backup completed: ${BACKUP_DIR}"
