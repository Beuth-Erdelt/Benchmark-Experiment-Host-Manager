#!/bin/bash
# Generates documentation summaries for HammerDB experiments.
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
################ HammerDB #################
###########################################


#### HammerDB Scale (Example-HammerDB.md)
bexhoma hammerdb -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_scale.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB scale  sf=16  nbp=1,2"


#### HammerDB Monitoring (Example-HammerDB.md)
bexhoma hammerdb -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB monitoring  sf=16  nbp=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
sleep 30


#### HammerDB Persistent Storage (Example-HammerDB.md)
bexhoma hammerdb -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_hammerdb_testcase_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB storage  sf=16  nbp=1  nc=2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-hammerdb-16
sleep 30


#### HammerDB Keying and Thinking Time (Example-HammerDB.md)
bexhoma hammerdb -ms 1 -tr \
  -sf 16 \
  -sd 20 \
  -xlat \
  -xkey \
  -dbms PostgreSQL \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1,2 \
  -nbt 160 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 30Gi \
  run &>$LOG_DIR/doc_hammerdb_testcase_keytime.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB keytime  sf=16  nbp=1,2  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
