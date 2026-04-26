#!/bin/bash
# Generates documentation summaries for collector experiments.
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
BEXHOMA_NODE_SUT="cl-worker38"
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




###########################################
############# TPC-C Benchbase #############
###########################################




#### Benchbase Monitoring (Example-Benchbase.md)
nohup python benchbase.py -ms 1 -tr \
  -rr 64Gi -lr 64Gi \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 1,2 \
  -nbt 160 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_1.log &

wait_process "benchbase"

#### Benchbase Monitoring (Example-Benchbase.md)
nohup python benchbase.py -ms 1 -tr \
  -rr 64Gi -lr 64Gi \
  -sf 16 \
  -sd 5 \
  -dbms PostgreSQL \
  -nbp 4,8 \
  -nbt 160 \
  -nbf 20 \
  -tb 1024 \
  -m -mc -ma \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_2.log &


wait_process "benchbase"









###########################################
########### TPC-C Benchbase MT ############
###########################################



BEXHOMA_NUM_TENANTS=2

# ---------------- SCHEMA ----------------
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -rr 64Gi -lr 64Gi \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_schema.log &

wait_process "benchbase"

# ---------------- DATABASE ----------------
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -rr 64Gi -lr 64Gi \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 20Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_database.log &

wait_process "benchbase"

# ---------------- CONTAINER ----------------
nohup python benchbase.py \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -rr 64Gi -lr 64Gi \
  -sf 1 -sd 5 -xkey \
  --dbms PostgreSQL \
  -nlp 1 -nbp 1 -nbt 10 \
  -ne "1,1" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 10Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_benchbase_testcase_collector_tenants_container.log &

wait_process "benchbase"




###########################################
################## TPC-H ##################
###########################################


nohup python tpch.py -tr \
  -rr 64Gi -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 8 -nbp 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 30Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_1.log &

wait_process "tpch"

nohup python tpch.py -tr \
  -rr 64Gi -lr 64Gi \
  -sf 6 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 8 -nbp 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 30Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_2.log &

wait_process "tpch"




###########################################
################ TPC-H MT #################
###########################################

BEXHOMA_NUM_TENANTS=2

# ---------------- SCHEMA ----------------
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb schema \
  -rr 64Gi -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 30Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_tenants_schema.log &

wait_process "tpch"

# ---------------- DATABASE ----------------
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb database \
  -rr 64Gi -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp $BEXHOMA_NUM_TENANTS -nlt 1 -nbp 1 -nbt 64 \
  -ne "$BEXHOMA_NUM_TENANTS,$BEXHOMA_NUM_TENANTS" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 30Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_tenants_database.log &

wait_process "tpch"

# ---------------- CONTAINER ----------------
nohup python tpch.py -tr \
  -mtn $BEXHOMA_NUM_TENANTS -mtb container \
  -rr 64Gi -lr 64Gi \
  -sf 3 \
  --dbms PostgreSQL \
  -ii -ic -is \
  -nlp 1 -nlt 1 -nbp 1 -nbt 64 \
  -ne "1,1" \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 15Gi -rsr \
  -nc 2 \
  -m -mc -ma \
  run </dev/null &>$LOG_DIR/doc_tpch_testcase_collector_tenants_container.log &

wait_process "tpch"


###########################################
################## YCSB ###################
###########################################


#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 2 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 15Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_collector_1.log &

wait_process "ycsb"


#### YCSB Monitoring (Example-YCSB.md)
nohup python ycsb.py -ms 1 -tr \
  -sf 3 \
  --workload a \
  -dbms PostgreSQL \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1,8 \
  -nbt 64 \
  -nbf 3 \
  -ne 1 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 15Gi -rsr \
  run </dev/null &>$LOG_DIR/doc_ycsb_testcase_collector_2.log &

wait_process "ycsb"



###########################################
################ HammerDB #################
###########################################



#### HammerDB Monitoring (Example-HammerDB.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 16 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_collector_1.log &


wait_process "hammerdb"

#### HammerDB Monitoring (Example-HammerDB.md)
nohup python hammerdb.py -ms 1 -tr \
  -sf 16 \
  -xlat \
  -sd 5 \
  -dbms PostgreSQL \
  -nlt 16 \
  -nbp 1,2 \
  -nbt 32 \
  -nc 2 \
  -m -mc -ma \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run </dev/null &>$LOG_DIR/doc_hammerdb_testcase_collector_2.log &


wait_process "hammerdb"




#find /data/benchmarks/ -name "*.pickle" -type f -delete


###########################################
############## Clean Folder ###############
###########################################


clean_logs
