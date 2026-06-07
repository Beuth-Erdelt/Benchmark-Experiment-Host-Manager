#!/bin/bash
# Generates documentation summaries for Benchbase experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


# Import functions from testfunctions.sh
source ./scripts/testfunctions.sh

# Config nodes and paths
BEXHOMA_NODE_SUT="cl-worker14"
BEXHOMA_NODE_LOAD="cl-worker19"
BEXHOMA_NODE_BENCHMARK="cl-worker19"
LOG_DIR="./logs_tests"

# Check for file
if [[ ! -f "cluster.config" ]]; then
    echo "Error: cluster.config not found."
    exit 1
fi
echo "Passed: ./cluster.config found."

# Check for directories
for dir in "experiments" "k8s"; do
    if [[ ! -d "$dir" ]]; then
        echo "Error: Directory '$dir' missing."
        exit 1
    fi
done
echo "Passed: ./experiments/ found."
echo "Passed: ./k8s/ found."


if ! prepare_logs; then
    echo "Error: prepare_logs failed with code $?"
    exit 1
fi
echo "Passed: $LOG_DIR/ found."

echo "Checks passed. Proceeding..."




###########################################
############### Benchbase #################
###########################################


#### Benchbase Scale (Example-Benchbase.md)
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase scale  sf=16  nbp=1,2"


#### Benchbase Monitoring (Example-Benchbase.md)
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase monitoring  sf=16  nbp=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-16
sleep 30


#### Benchbase Persistent Storage (Example-Benchbase.md)
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_testcase_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase storage  sf=16  nbp=1  nc=2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-benchbase-tpcc-160
sleep 30


#### Benchbase Keying and Thinking Time (Example-Benchbase.md)
bexhoma benchbase -ms 1 -tr \
  -rr 128Gi -lr 128Gi \
  -sf 160 \
  -sd 30 \
  -xkey \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms PostgreSQL \
  -tb 1024 \
  -nbp 1,2,5,10 \
  -nbt 1600 \
  -nbf 1 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 100Gi \
  run &>$LOG_DIR/doc_benchbase_testcase_keytime.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase keytime  sf=160  nbp=1,2,5,10"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
