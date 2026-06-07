#!/bin/bash
# Generates documentation summaries for YugabyteDB experiments.
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




################################################
################## YugaByteDB ##################
################################################


install_yugabytedb() {
  PERSISTENT=${1:-yes}

  if [[ "$PERSISTENT" == "yes" ]]; then
    EPHEMERAL=false
  else
    EPHEMERAL=true
  fi

  helm install bexhoma yugabytedb/yugabyte \
    --version 2025.2.1 \
    --set \
gflags.tserver.ysql_enable_packed_row=true,\
gflags.tserver.ysql_max_connections=1280,\
resource.master.limits.cpu=2,\
resource.master.limits.memory=16Gi,\
resource.master.requests.cpu=2,\
resource.master.requests.memory=16Gi,\
resource.tserver.limits.cpu=8,\
resource.tserver.limits.memory=16Gi,\
resource.tserver.requests.cpu=8,\
resource.tserver.requests.memory=16Gi,\
storage.master.size=100Gi,\
storage.master.storageClass=shared,\
storage.tserver.size=100Gi,\
storage.tserver.storageClass=shared,\
storage.ephemeral=$EPHEMERAL,\
tserver.livenessProbe.timeoutSeconds=10,\
master.livenessProbe.timeoutSeconds=10,\
enableLoadBalancer=true

  echo "Waiting 60s for pods to start..."
  sleep 60
}


remove_yugabytedb() {
  REMOVE_PVC=${1:-no}

  echo "Deleting Helm release bexhoma..."
  helm delete bexhoma

  if [[ "$REMOVE_PVC" == "yes" ]]; then
    echo "Removing PVCs for yb-tserver and yb-master..."
    kubectl delete pvc -l app=yb-tserver
    kubectl delete pvc -l app=yb-master
  else
    echo "Keeping PVCs (persistent storage not deleted)"
  fi

  echo "Waiting 60s for cleanup..."
  sleep 60
}


# install YugabyteDB
install_yugabytedb no

#### YCSB Ingestion (Example-YugaByteDB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  run &>$LOG_DIR/doc_ycsb_yugabytedb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB ingestion  sf=1  nbp=1"

#### YCSB Execution (Example-YugaByteDB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  -sl \
  run &>$LOG_DIR/doc_ycsb_yugabytedb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB execution skip-load  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30

kubectl delete pvc bexhoma-storage-yugabytedb-ycsb-1
sleep 30

#### YCSB Dummy Persistent Storage (Example-YugaByteDB.md)
bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
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
  -rst shared -rss 1Gi \
  run &>$LOG_DIR/doc_ycsb_yugabytedb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB dummy PVC  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Simple (Example-YugaByteDB.md)
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run &>$LOG_DIR/doc_benchbase_yugabytedb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB simple  sf=16  nbp=1,2"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase More Complex (Example-YugaByteDB.md)
bexhoma benchbase -ms 1 -tr \
  -sf 128 \
  -slg 30 \
  -sd 20 \
  -xkey \
  -dbms YugabyteDB \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -nbf 16 \
  -tb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc \
  run &>$LOG_DIR/doc_benchbase_yugabytedb_2.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB complex  sf=128  nbp=1,2,5,10"


# remove YugabyteDB installation
remove_yugabytedb no


################################################
######## YugaByteDB Application Metrics ########
################################################


# install YugabyteDB
install_yugabytedb no
sleep 30

bexhoma ycsb -ms 1 -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms YugabyteDB \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 4 \
  -nbp 1 \
  -nbt 64 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_ycsb_run_yugabytedb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB appmetrics  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no


# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Application Metrics (Example-YugaByteDB.md)
bexhoma benchbase -ms 1 -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_run_yugabytedb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB appmetrics  sf=16  nbp=1,2"


# remove YugabyteDB installation
remove_yugabytedb no


###########################################
############## Clean Folder ###############
###########################################


clean_logs
