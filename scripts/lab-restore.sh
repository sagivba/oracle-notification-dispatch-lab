#!/usr/bin/env bash
# Purpose: Restore local Oracle Docker lab volume data from a lab-backup directory.
# Related decisions: DEC-003, DEC-004, DEC-005, DEC-006, DEC-007, DEC-009.
set -euo pipefail

CONTAINER_NAME="oracle-notification-dispatch-lab-db"
VOLUME_NAME="oracle-notification-dispatch-lab-u01"
BACKUP_DIR="${1:-}"
CONFIRM="${2:-}"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

usage() {
  cat <<EOF
Usage:
  scripts/lab-restore.sh <backup_directory> [--replace]

Use --replace to remove an existing ${CONTAINER_NAME} container and ${VOLUME_NAME} volume first.
EOF
}

command -v docker >/dev/null 2>&1 || fail "docker command was not found."

if [[ -z "${BACKUP_DIR}" ]]; then
  usage
  exit 1
fi

[[ -f "${BACKUP_DIR}/oradata.tar.gz" ]] || fail "Backup archive not found: ${BACKUP_DIR}/oradata.tar.gz"

if docker ps -a --format '{{.Names}}' | grep -Fxq "${CONTAINER_NAME}"; then
  if [[ "${CONFIRM}" != "--replace" ]]; then
    fail "Container ${CONTAINER_NAME} already exists. Re-run with --replace to remove it."
  fi
  docker rm -f "${CONTAINER_NAME}" >/dev/null
fi

if docker volume ls --format '{{.Name}}' | grep -Fxq "${VOLUME_NAME}"; then
  if [[ "${CONFIRM}" != "--replace" ]]; then
    fail "Volume ${VOLUME_NAME} already exists. Re-run with --replace to remove it."
  fi
  docker volume rm "${VOLUME_NAME}" >/dev/null
fi

docker volume create "${VOLUME_NAME}" >/dev/null
docker run --rm \
  -v "${VOLUME_NAME}":/volume \
  -v "$(pwd)/${BACKUP_DIR}":/backup \
  alpine sh -c 'cd /volume && tar xzf /backup/oradata.tar.gz'

restore_image="container-registry.oracle.com/database/free:latest"
if [[ -f "${BACKUP_DIR}/image_name.txt" ]]; then
  restore_image="$(cat "${BACKUP_DIR}/image_name.txt")"
fi

if [[ ! -f ".env" ]]; then
  fail "Create local .env from .env.example and set ORACLE_PWD before starting restored container."
fi

echo "Starting restored lab container with image: ${restore_image}"
ORACLE_IMAGE="${restore_image}" docker compose up -d db

cat <<EOF

Restore completed.

Readiness check:
  docker logs -f ${CONTAINER_NAME}
  docker logs ${CONTAINER_NAME} | grep 'DATABASE IS READY TO USE!'
EOF
