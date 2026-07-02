#!/bin/bash

######################## Show parameters ########################
echo "BEXHOMA_SUT_HOST:$BEXHOMA_SUT_HOST"
echo "BEXHOMA_SUT_USER:$BEXHOMA_SUT_USER"
echo "BEXHOMA_SUT_KEY:$BEXHOMA_SUT_KEY"
echo "HARDWARE_TEST_DIR:$HARDWARE_TEST_DIR"
echo "HARDWARE_SIZE:$HARDWARE_SIZE"

######################## Set SSH options ########################
SSH_OPTS="-i ${BEXHOMA_SUT_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

######################## Create test directory on SUT ########################
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_SUT_HOST}" "mkdir -p ${HARDWARE_TEST_DIR}"

######################## Run fio sequential write benchmark ########################
echo "=== fio Sequential Write ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_SUT_HOST}" \
  "fio --name=seqwrite --directory=${HARDWARE_TEST_DIR} --rw=write --bs=1M --size=${HARDWARE_SIZE} --numjobs=1 --runtime=30 --time_based --group_reporting"

######################## Run fio random read/write benchmark ########################
echo "=== fio Random Read/Write (QD1) ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_SUT_HOST}" \
  "fio --name=randrw --directory=${HARDWARE_TEST_DIR} --rw=randrw --bs=4k --iodepth=1 --size=${HARDWARE_SIZE} --numjobs=1 --runtime=30 --time_based --group_reporting --fsync=1"
