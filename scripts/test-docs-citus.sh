#!/bin/bash
# Generates documentation summaries for Citus experiments.
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
#################### YCSB Citus ####################
####################################################


bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  --workload a \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_citus_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-ycsb-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-0
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-1
kubectl delete pvc bxw-bexhoma-worker-citus-ycsb-1-2
sleep 30


bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  --workload a \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run &>$LOG_DIR/doc_ycsb_citus_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Citus storage  sf=1  nbp=1  nc=2"


####################################################
################## Benchbase Citus #################
####################################################


bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_citus_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus  sf=16  nbp=1,2"

kubectl delete pvc bexhoma-storage-citus-benchbase-tpcc-128
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-benchbase-tpcc-128-3
sleep 30


bexhoma benchbase -ms 1 -tr \
  -sf 128 \
  -sd 20 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -nbp 1,2,4,8 \
  -nbt 64 \
  -nbf 16 \
  -tb 1024 \
  -m -mc \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run &>$LOG_DIR/doc_benchbase_citus_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus scale  sf=128  nbp=1,2,4,8"


bexhoma benchbase -ms 1 -tr \
  -sf 128 \
  -sd 20 \
  -slg 30 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -xkey \
  -dbms Citus \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 4 \
  -tb 1024 \
  -m -mc \
  -nc 2 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -rst shared -rss 100Gi \
  run &>$LOG_DIR/doc_benchbase_citus_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase Citus keytime  sf=128  nbp=1,2,5,10  nc=2"


####################################################
################## HammerDB Citus ##################
####################################################


bexhoma hammerdb -ms 1 -tr \
  -sf 16 \
  -xlat \
  -dbms Citus \
  -nw 3 \
  -nwr 1 \
  -nws 48 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlt 8 \
  -nbp 1 \
  -nbt 16 \
  -ne 1 \
  -nc 1 \
  run &>$LOG_DIR/doc_hammerdb_citus_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus  sf=16  nbp=1"

kubectl delete pvc bexhoma-storage-citus-hammerdb-128
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-128-3
sleep 30


bexhoma hammerdb -ms 1 -tr \
  -sf 128 \
  -sd 30 \
  -xlat \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 128 \
  -nbp 1,2,4,8 \
  -nbt 128 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  -rst shared -rss 50Gi \
  run &>$LOG_DIR/doc_hammerdb_citus_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus scale  sf=128  nbp=1,2,4,8"

kubectl delete pvc bexhoma-storage-citus-hammerdb-500
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-0
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-1
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-2
kubectl delete pvc bxw-bexhoma-worker-citus-hammerdb-500-3
sleep 30


bexhoma hammerdb -ms 1 -tr \
  -sf 500 \
  -sd 20 \
  -xlat \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -nlp 1 \
  -nlt 250 \
  -nbp 1,2,5,10 \
  -nbt 250 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 200Gi \
  run &>$LOG_DIR/doc_hammerdb_citus_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] HammerDB Citus large  sf=500  nbp=1,2,5,10  nc=2"


####################################################
#################### TPC-H Citus ###################
####################################################

bexhoma tpch -ms 1 -tr \
  -sf 1 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 1200 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1 \
  -nc 1 \
  run &>$LOG_DIR/test_tpch_testcase_citus_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus  sf=1  nbp=1"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
sleep 30


bexhoma tpch -ms 1 -tr \
  -sf 10 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 14400 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -ii -ic -is \
  -nlp 8 \
  -nbp 1 \
  -ne 1,1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run &>$LOG_DIR/test_tpch_testcase_citus_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus storage  sf=10  ne=1,1  nc=2"

kubectl delete pvc bexhoma-storage-citus-tpch-10
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-0
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-1
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-2
kubectl delete pvc bxw-bexhoma-worker-citus-tpch-10-3
sleep 30


bexhoma tpch -ms 1 -tr \
  -sf 10 \
  -nw 4 \
  -nwr 1 \
  -nws 48 \
  -dt \
  -t 14400 \
  -dbms Citus \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -icol \
  -nlp 8 \
  -nbp 1 \
  -ne 1,1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi \
  run &>$LOG_DIR/test_tpch_testcase_citus_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] TPC-H Citus columnar  sf=10  ne=1,1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
