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


source ./scripts/testfunctions.sh




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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms YugabyteDB              DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB ingestion  sf=1  nbp=1"

#### YCSB Execution (Example-YugaByteDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms YugabyteDB              DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -sl                           skip loading phase (reuse existing data)
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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

wait_process "ycsb"
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
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms YugabyteDB              DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 1Gi                      size of the persistent volume claim
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB dummy PVC  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Simple (Example-YugaByteDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms YugabyteDB              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma benchbase -ms $BEXHOMA_MS -tr \
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

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB simple  sf=16  nbp=1,2"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase More Complex (Example-YugaByteDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 128                       scaling factor (controls database size)
# -slg 30                       log status to stdout every x seconds
# -sd 20                        benchmark duration in minutes
# -xkey                         simulate user think time and keying delays
# -dbms YugabyteDB              DBMS under test
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1280                     threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma benchbase -ms $BEXHOMA_MS -tr \
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

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB complex  sf=128  nbp=1,2,5,10"


# remove YugabyteDB installation
remove_yugabytedb no


################################################
######## YugaByteDB Application Metrics ########
################################################


# install YugabyteDB
install_yugabytedb no
sleep 30

# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms YugabyteDB              DBMS under test
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma ycsb -ms $BEXHOMA_MS -tr \
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

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB appmetrics  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no


# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Application Metrics (Example-YugaByteDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -sd 5                         benchmark duration in minutes
# -dbms YugabyteDB              DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -nbf 16                       throughput target as a multiple of the base ops/s
# -tb 1024                      base ops/s used to compute the throughput target (2^10)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -sd 5 \
  -dbms YugabyteDB \
  -nbp 1,2 \
  -nbt 16 \
  -nbf 16 \
  -tb 1024 \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_run_yugabytedb_appmetrics.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB appmetrics  sf=16  nbp=1,2"


# remove YugabyteDB installation
remove_yugabytedb no


###########################################
############## Clean Folder ###############
###########################################


clean_logs
