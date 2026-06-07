#!/bin/bash
# Generates documentation summaries for TPC-H experiments.
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
################# TPC-H ###################
###########################################


#### TCP-H Compare (Example-TPC-H.md)
bexhoma tpch -ms 1 -dt -tr \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H compare  sf=1"


#### TCP-H Monitoring (Example-TPC-H.md)
bexhoma tpch -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H monitoring  sf=10"


#### TCP-H Throughput (Example-TPC-H.md)
bexhoma tpch -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_throughput.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-postgresql-tpch-1
sleep 30


#### TCP-H Persistent Storage (Example-TPC-H.md)
bexhoma tpch -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 30Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H storage  sf=1  nc=2"


#### TCP-H Fractional Scaling Factor (Example-TPC-H.md)
bexhoma tpch -ms 1 -dt -tr \
  -dbms PostgreSQL \
  -nlp 8 \
  -nlt 8 \
  -sf 0.1 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 5Gi -rsr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpch_testcase_fractional.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H fractional  sf=0.1  nc=2"


###########################################
############# TPC-H MonetDB ###############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpch-100
sleep 30


#### TCP-H Power 100 (Example-Result-TPC-H-MonetDB.md)
bexhoma tpch -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -rr 256Gi -lr 256Gi \
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB power  sf=100  nc=1  ne=1"


#### TCP-H Power 100 repeated (Example-Result-TPC-H-MonetDB.md)
bexhoma tpch -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -rr 256Gi -lr 256Gi \
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB power  sf=100  nc=2  ne=1,1"


#### TCP-H Throughput 100 (Example-Result-TPC-H-MonetDB.md)
bexhoma tpch -ms 1 \
  -m -mc \
  -sf 100 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -dbms MonetDB \
  -rr 256Gi -lr 256Gi \
  -t 3600 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpch_monetdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H MonetDB throughput  sf=100  ne=1,1,3"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
