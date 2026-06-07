#!/bin/bash
# Generates documentation summaries for multi-tenancy experiments.
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




####################################################
######### Benchbase TPC-H Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_schema.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_database.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma tpch -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 1 -nlt 1 -nbp 1 -nlt 64 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 5Gi -rsr \
  run &>$LOG_DIR/test_tpch_run_postgresql_tenants_container.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######### Benchbase TPC-C Multi-Tenant PVC #########
####################################################

BEXHOMA_NUM_TENANTS=2

bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_schema.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT schema  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_database.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_postgresql_tenants_container.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"




####################################################
######## Benchbase TPC-C Multi-Tenant MySQL ########
####################################################

BEXHOMA_NUM_TENANTS=2

bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne $BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_database.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT MySQL database  tenants=$BEXHOMA_NUM_TENANTS  sf=1"

bexhoma benchbase \
  -rr 64Gi -lr 64Gi \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -sf 1 -sd 5 -xkey \
  --dbms MySQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/test_benchbase_run_mysql_tenants_container.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase MT MySQL container  tenants=$BEXHOMA_NUM_TENANTS  sf=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
