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
# -dbms YugabyteDB              DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_yugabytedb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB ingestion  sf=1  nbp=1"

#### YCSB Execution (Example-YugaByteDB.md)
# -dbms YugabyteDB              DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -sl                           skip loading phase (reuse existing data)
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -sl \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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
# -dbms YugabyteDB              DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rss 1Gi                      size of the persistent volume claim
# -rst cephcsi                   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rss 1Gi \
  -rst cephcsi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_ycsb_yugabytedb_3.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB dummy PVC  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Simple (Example-YugaByteDB.md)
# -dbms YugabyteDB              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_yugabytedb_1.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB simple  sf=16  nbp=1,2"


# remove YugabyteDB installation
remove_yugabytedb no
sleep 30

# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase More Complex (Example-YugaByteDB.md)
# -dbms YugabyteDB              DBMS under test
# -sf 128                       scaling factor (controls database size)
# -xsd 20                       benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2,5,10                 benchmarking pod counts to sweep (comma-separated)
# -nbt 1280                     threads per benchmarking pod
# -xkey                         simulate user think time and keying delays
# -xli 30                       log status to stdout every x seconds
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 128 \
  -xsd 20 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2,5,10 \
  -nbt 1280 \
  -xkey \
  -xli 30 \
  -m \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
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

# -dbms YugabyteDB              DBMS under test
# -sf 1                         scaling factor (number of records x 1000)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 4                       loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
bexhoma ycsb \
  -dbms YugabyteDB \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 4 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 64 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_ycsb_run_yugabytedb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB YugabyteDB appmetrics  sf=1  nbp=1"


# remove YugabyteDB installation
remove_yugabytedb no


# install YugabyteDB
install_yugabytedb no
sleep 30


#### Benchbase Application Metrics (Example-YugaByteDB.md)
# -dbms YugabyteDB              DBMS under test
# -sf 16                        scaling factor (controls database size)
# -xsd 5                        benchmark duration in minutes
# -xtb 1024                     base ops/s used to compute the throughput target (2^10)
# -xnbf 16                      throughput target as a multiple of the base ops/s
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
bexhoma benchbase \
  -dbms YugabyteDB \
  -sf 16 \
  -xsd 5 \
  -xtb 1024 \
  -xnbf 16 \
  -nbp 1,2 \
  -nbt 16 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  run &>$LOG_DIR/doc_benchbase_run_yugabytedb_appmetrics.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase YugabyteDB appmetrics  sf=16  nbp=1,2"


# remove YugabyteDB installation
remove_yugabytedb no


###########################################
############## Clean Folder ###############
###########################################


clean_logs
