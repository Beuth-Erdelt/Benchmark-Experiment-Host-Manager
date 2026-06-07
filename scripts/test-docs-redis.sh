#!/bin/bash
# Generates documentation summaries for Redis experiments.
#
# Runs a parameterised sequence of bexhoma experiments, waits for each to
# complete, writes logs, and extracts summaries into separate files.
#
# Author: Patrick K. Erdelt
# Copyright (C) 2020 Patrick K. Erdelt
# SPDX-License-Identifier: AGPL-3.0-or-later
# See LICENSE for details.


source ./scripts/testfunctions.sh




####################################################
#################### YCSB Redis ####################
####################################################


# Single host Redis
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Redis                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 12                       loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_redis_1.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis single  sf=1  nbp=1"


# Cluster of 3 Redis instances
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Redis                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 12                       loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_redis_2.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis cluster 3  sf=1  nbp=1"


# Cluster of 3 Redis instances and replication
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Redis                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 12                       loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 1                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  -nwr 1 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 1 \
  -m -mc \
  run &>$LOG_DIR/doc_ycsb_redis_3.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis cluster 3 replication  sf=1  nbp=1"


# Single host Redis with PVC
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Redis                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 12                       loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/doc_ycsb_redis_4.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis single PVC  sf=1  nbp=1  nc=2"


# Cluster of 3 Redis instances and PVC
# -tr                           verify result meets basic sanity requirements
# -sf 1                         scaling factor (number of records x 1000)
# -sfo 10                       number of operations for the benchmark phase (x 1000)
# -nw 3                         number of worker nodes in the cluster
# --workload a                  YCSB workload template (a = 50%% read / 50%% update)
# -dbms Redis                   DBMS under test
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# -tb 16384                     base ops/s used to compute throughput targets (2^14)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nlf 12                       loading throughput target as a multiple of the base ops/s
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nbf 4                        throughput target as a multiple of the base ops/s
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nc 2                         number of repeated runs per configuration
# -m                            collect SUT resource metrics
# -mc                           collect metrics for all cluster nodes
# -rst shared                   storage class for persistent volumes
# -rss 50Gi                     size of the persistent volume claim
# -rsr                          delete and recreate the PVC at experiment start
bexhoma ycsb -tr \
  -sf 1 \
  -sfo 10 \
  -nw 3 \
  --workload a \
  -dbms Redis \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  -tb 16384 \
  -nlp 8 \
  -nlt 64 \
  -nlf 12 \
  -nbp 1 \
  -nbt 128 \
  -nbf 4 \
  -ne 1 \
  -nc 2 \
  -m -mc \
  -rst shared -rss 50Gi -rsr \
  run &>$LOG_DIR/doc_ycsb_redis_5.log

wait_process "ycsb"
echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Redis cluster 3 PVC  sf=1  nbp=1  nc=2"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
