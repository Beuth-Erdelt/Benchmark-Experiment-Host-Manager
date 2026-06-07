#!/bin/bash
# Generates documentation summaries for TPC-DS experiments.
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
################# TPC-DS ##################
###########################################


#### TCP-DS Compare (Example-TPC-DS.md)
bexhoma tpcds -ms 1 -dt -tr \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_compare.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS compare  sf=1"


#### TCP-DS Monitoring (Example-TPC-DS.md)
bexhoma tpcds -ms 1 -dt -tr \
  -dbms MonetDB \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 3 \
  -t 1200 \
  -ii -ic -is \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS monitoring  sf=3"


#### TCP-DS Throughput (Example-TPC-DS.md)
bexhoma tpcds -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 1 \
  -ne 1,2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_throughput.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS throughput  sf=1  ne=1,2"


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-1
sleep 30


#### TCP-DS Persistent Storage (Example-TPC-DS.md)
bexhoma tpcds -ms 1 -dt -tr \
  -dbms MonetDB \
  -nlp 8 \
  -nlt 8 \
  -sf 1 \
  -t 1200 \
  -ii -ic -is \
  -nc 2 \
  -rst shared -rss 10Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_tpcds_testcase_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS storage  sf=1  nc=2"


###########################################
############# TPC-DS MonetDB ##############
###########################################


#### Remove persistent storage
kubectl delete pvc bexhoma-storage-monetdb-tpcds-30
sleep 30


#### TCP-DS Power 30 (Example-TPC-DS.md)
bexhoma tpcds -ms 1 \
  -m -mc \
  -sf 30 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1 \
  -dbms MonetDB \
  -rr 1024Gi -lr 1024Gi \
  -t 14400 -dt \
  -rst shared -rss 1000Gi -rsr \
  run &>$LOG_DIR/doc_tpcds_monetdb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power  sf=30  nc=1  ne=1"


#### TCP-DS Power 30 repeated (Example-TPC-DS.md)
bexhoma tpcds -ms 1 \
  -m -mc \
  -sf 30 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 2 -ne 1,1 \
  -dbms MonetDB \
  -rr 1024Gi -lr 1024Gi \
  -t 14400 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB power  sf=30  nc=2  ne=1,1"


#### TCP-DS Throughput 30 (Example-TPC-DS.md)
bexhoma tpcds -ms 1 \
  -m -mc \
  -sf 30 \
  -ii -ic -is \
  -nlp 8 -nlt 8 \
  -nc 1 -ne 1,1,3 \
  -dbms MonetDB \
  -rr 1024Gi -lr 1024Gi \
  -t 14400 -dt \
  -rst shared -rss 1000Gi \
  run &>$LOG_DIR/doc_tpcds_monetdb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS MonetDB throughput  sf=30  ne=1,1,3"


###########################################
############ Profiling MonetDB ############
###########################################


#### TCP-DS Profiling (Example-TPC-DS.md)
bexhoma tpcds -ms 1 -dt -tr \
  -dbms MonetDB \
  -rr 64Gi -lr 64Gi \
  -nlp 8 \
  -nlt 8 \
  -sf 10 \
  -ii -ic -is \
  -ne 1,1 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 50Gi \
  profiling &>$LOG_DIR/doc_tpcds_testcase_profiling.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-DS profiling  sf=10  ne=1,1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
