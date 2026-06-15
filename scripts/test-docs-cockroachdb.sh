#!/bin/bash
# Generates documentation summaries for CockroachDB experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




#################################################
################## CockroachDB ##################
#################################################


#### YCSB Ingestion (Example-CockroachDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms CockroachDB             DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  -xop 10 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB ingestion  sf=1  nbp=1"


#### YCSB PVC (Example-CockroachDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -xop 1                        number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms CockroachDB             DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 1 \
  -xop 1 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_2.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB storage  sf=1  nbp=1  nc=2"


#### YCSB Scale (Example-CockroachDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 10                        scaling factor (number of records x 1000)
# -xop 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms CockroachDB             DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -xtb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -xnlf 4                        loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 64                       threads per benchmarking pod
# -xnbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -ms $BEXHOMA_MS -tr \
  -sf 10 \
  -xop 10 \
  -nw 3 \
  -nwr 3 \
  --workload a \
  -dbms CockroachDB \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -xtb 16384 \
  -nlp 8 \
  -nlt 64 \
  -xnlf 4 \
  -nbp 1 \
  -nbt 64 \
  -xnbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_cockroachdb_3.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB CockroachDB scale  sf=10  nbp=1"


#### Benchbase Simple (Example-CockroachDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 16                        scaling factor (controls database size)
# -xsd 5                         benchmark duration in minutes
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -dbms CockroachDB             DBMS under test
# -nbp 1,2                      benchmarking pod counts to sweep (comma-separated)
# -nbt 16                       threads per benchmarking pod
# -xnbf 16                       throughput target as a multiple of the base ops/s
# -xtb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 16 \
  -xsd 5 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2 \
  -nbt 16 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_1.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB simple  sf=16  nbp=1,2"


#### Benchbase Complex (Example-CockroachDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 128                       scaling factor (controls database size)
# -xsd 10                        benchmark duration in minutes
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -dbms CockroachDB             DBMS under test
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 1280                     threads per benchmarking pod
# -xnbf 16                       throughput target as a multiple of the base ops/s
# -xtb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 128 \
  -xsd 10 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc -ma \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_2.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB complex  sf=128  nbp=1,2,4,8"


#### Benchbase Complex with PVC (Example-CockroachDB.md)
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -sf 128                       scaling factor (controls database size)
# -xsd 10                        benchmark duration in minutes
# -nw 3                         number of worker nodes in the cluster
# -nwr 3                        number of worker node replicas
# -dbms CockroachDB             DBMS under test
# -nbp 1,2,4,8                  benchmarking pod counts to sweep (comma-separated)
# -nbt 1280                     threads per benchmarking pod
# -xnbf 16                       throughput target as a multiple of the base ops/s
# -xtb 1024                      base ops/s used to compute the throughput target (2^10)
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -ma                           collect application-level metrics
# -rst shared                   storage class for persistent volumes
# -rss 100Gi                    size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma benchbase -ms $BEXHOMA_MS -tr \
  -sf 128 \
  -xsd 10 \
  -nw 3 \
  -nwr 3 \
  -dbms CockroachDB \
  -nbp 1,2,4,8 \
  -nbt 1280 \
  -xnbf 16 \
  -xtb 1024 \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -m -mc -ma \
  -rst shared -rss 100Gi -rsr \
  run &>$LOG_DIR/doc_benchbase_cockroachdb_3.log

wait_process "benchbase"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] Benchbase CockroachDB storage  sf=128  nbp=1,2,4,8"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
