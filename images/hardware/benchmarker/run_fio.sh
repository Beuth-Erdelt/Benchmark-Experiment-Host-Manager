#!/bin/sh
set -e

SUT_HOST="${SUT_HOST:-sut-service}"
SUT_USER="${SUT_USER:-bench}"
KEY_PATH="${KEY_PATH:-/root/.ssh/id_ed25519}"
TEST_DIR="${TEST_DIR:-/tmp/fio-test}"
SIZE="${SIZE:-1G}"

SSH_OPTS="-i ${KEY_PATH} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

echo "=== fio Sequential Write ==="
ssh ${SSH_OPTS} "${SUT_USER}@${SUT_HOST}" \
  "fio --name=seqwrite --directory=${TEST_DIR} --rw=write --bs=1M --size=${SIZE} --numjobs=1 --runtime=30 --time_based --group_reporting"

echo "=== fio Random Read/Write (QD1) ==="
ssh ${SSH_OPTS} "${SUT_USER}@${SUT_HOST}" \
  "fio --name=randrw --directory=${TEST_DIR} --rw=randrw --bs=4k --iodepth=1 --size=${SIZE} --numjobs=1 --runtime=30 --time_based --group_reporting --fsync=1"
