#!/bin/sh
set -e

SUT_HOST="${SUT_HOST:-sut-service}"
SUT_USER="${SUT_USER:-bench}"
KEY_PATH="${KEY_PATH:-/root/.ssh/id_ed25519}"
THREADS="${THREADS:-4}"

SSH_OPTS="-i ${KEY_PATH} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

echo "=== sysbench CPU ==="
ssh ${SSH_OPTS} "${SUT_USER}@${SUT_HOST}" \
  "sysbench cpu --cpu-max-prime=20000 --threads=${THREADS} run"

echo "=== sysbench Memory ==="
ssh ${SSH_OPTS} "${SUT_USER}@${SUT_HOST}" \
  "sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=${THREADS} run"
