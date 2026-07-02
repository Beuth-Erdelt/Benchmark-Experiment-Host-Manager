#!/bin/bash

######################## Show parameters ########################
echo "BEXHOMA_SUT_HOST:$BEXHOMA_SUT_HOST"
echo "BEXHOMA_SUT_USER:$BEXHOMA_SUT_USER"
echo "BEXHOMA_SUT_KEY:$BEXHOMA_SUT_KEY"
echo "HARDWARE_THREADS:$HARDWARE_THREADS"

######################## Set SSH options ########################
SSH_OPTS="-i ${BEXHOMA_SUT_KEY} -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

######################## Run sysbench CPU benchmark ########################
echo "=== sysbench CPU ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_SUT_HOST}" \
  "sysbench cpu --cpu-max-prime=20000 --threads=${HARDWARE_THREADS} run"

######################## Run sysbench memory benchmark ########################
echo "=== sysbench Memory ==="
ssh ${SSH_OPTS} "${BEXHOMA_SUT_USER}@${BEXHOMA_SUT_HOST}" \
  "sysbench memory --memory-block-size=1K --memory-total-size=10G --threads=${HARDWARE_THREADS} run"
