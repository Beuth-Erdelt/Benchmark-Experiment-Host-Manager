#!/bin/bash
# Test runs for PostgreSQL 18 configurations and features.
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

# Wait for all previous jobs to complete
wait_process "tpch"
wait_process "tpcds"
wait_process "hammerdb"
wait_process "benchbase"
wait_process "ycsb"















####################################################
################ YCSB IO Subsystem #################
####################################################



nohup python ycsb.py -tr \
  -sf 100 \
  -sfo 5 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 16 \
  -nlt 128 \
  -nlf 4 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -rr 64Gi -lr 64Gi \
  -rst shared -rss 500Gi -rsr \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=16GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=32MB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=8GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].min_wal_size=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_timeout=20min \
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=worker \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_io_worker.log &


wait_process "ycsb"


nohup python ycsb.py -tr \
  -sf 100 \
  -sfo 5 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 16 \
  -nlt 128 \
  -nlf 4 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -rr 64Gi -lr 64Gi \
  -rst shared -rss 500Gi \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=16GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=32MB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=8GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].min_wal_size=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_timeout=20min \
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=worker \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_io_uring.log &


wait_process "ycsb"


nohup python ycsb.py -tr \
  -sf 100 \
  -sfo 5 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 16 \
  -nlt 128 \
  -nlf 4 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -rr 64Gi -lr 64Gi \
  -rst shared -rss 500Gi \
  --set deployment[bexhoma-deployment-postgres].container[dbms].shared_buffers=16GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_cache_size=48GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].work_mem=32MB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].maintenance_work_mem=2GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].max_wal_size=8GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].min_wal_size=1GB \
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_timeout=20min \
  --set deployment[bexhoma-deployment-postgres].container[dbms].checkpoint_completion_target=0.9 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].autovacuum=on \
  --set deployment[bexhoma-deployment-postgres].container[dbms].effective_io_concurrency=64 \
  --set deployment[bexhoma-deployment-postgres].container[dbms].io_method=worker \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_io_sync.log &


wait_process "ycsb"



###########################################
############## Clean Folder ###############
###########################################


clean_logs
