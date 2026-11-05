#!/bin/bash
# Generates documentation summaries for Dragonfly experiments.
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
#### Main Example ##################################
####################################################


# Main example: single host Dragonfly, quick, without monitoring
# -dbms Dragonfly               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xop 1                        number of operations for the benchmark phase (in millions)
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 1 \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly single  sf=1  nbp=1"


####################################################
#### Monitoring ####################################
####################################################


# Monitoring: single host Dragonfly with application metrics, at least 1 minute of benchmarking
# -dbms Dragonfly               DBMS under test
# -sf 3                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 3 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_monitoring.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly single monitoring  sf=3  nbp=1"


####################################################
#### Persistent Storage ############################
####################################################


# Persistent storage: single host Dragonfly
# -dbms Dragonfly               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -ar                           run save-snapshot.sh (SAVE) before each benchmarking round
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly single PVC  sf=1  nbp=1  nc=2"


####################################################
#### Variants ######################################
####################################################


# Variant cluster: 3 Dragonfly instances
# -dbms Dragonfly               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nw 3                         number of worker nodes in the cluster
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -ar                           run save-snapshot.sh (SAVE) before each benchmarking round
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_cluster.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3  sf=1  nbp=1"


# Variant cluster: 3 Dragonfly instances on persistent storage
# -dbms Dragonfly               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 2                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nw 3                         number of worker nodes in the cluster
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -ar                           run save-snapshot.sh (SAVE) before each benchmarking round
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rsr                          delete and recreate the PVC at experiment start
# -rss 50Gi                     size of the persistent volume claim
# -rst $BEXHOMA_STORAGE_CLASS   storage class for persistent volumes
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 2 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rsr \
  -rss 50Gi \
  -rst $BEXHOMA_STORAGE_CLASS \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_cluster_storage.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3 PVC  sf=1  nbp=1  nc=2"


# Variant replication: 3 Dragonfly instances, 1 master and 2 replicas
# -dbms Dragonfly               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nw 3                         number of worker nodes in the cluster
# -nwr 1                        number of worker node replicas
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -tr                           verify result meets basic sanity requirements
# -ar                           run save-snapshot.sh (SAVE) before each benchmarking round
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 1 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -nwr 1 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -tr \
  -ar \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  run &>$LOG_DIR/docs_ycsb_dragonfly_replica.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3 replication  sf=1  nbp=1"


####################################################
#### Technical Details #############################
####################################################


# Technical details: cluster of 3 Dragonfly instances with a changed setting (--set)
# -dbms Dragonfly               DBMS under test
# -sf 1                         scaling factor (number of records in millions)
# -xwl a                        YCSB workload template (a = 50%% read / 50%% update)
# -xtb 16384                    base ops/s used to compute throughput targets (2^14)
# -xnbf 4                       throughput target as a multiple of the base ops/s
# -xnlf 12                      loading throughput target as a multiple of the base ops/s
# -nc 1                         number of repeated runs per configuration
# -ne 1                         parallel client counts to sweep (comma-separated)
# -nlp 8                        number of data loader pods
# -nlt 64                       threads per loader pod
# -nbp 1                        benchmarking pod counts to sweep (comma-separated)
# -nbt 128                      threads per benchmarking pod
# -nw 3                         number of worker nodes in the cluster
# -xop 10                       number of operations for the benchmark phase (in millions)
# -m                            collect SUT resource metrics
# -ma                           collect application-level metrics
# -mc                           collect metrics for all cluster nodes
# -ms $BEXHOMA_MS               max simultaneous DBMS configurations
# -tr                           verify result meets basic sanity requirements
# -ar                           run save-snapshot.sh (SAVE) before each benchmarking round
# -lr 64Gi                      RAM limit for the SUT container
# -rr 64Gi                      RAM requested for the SUT container
# -rss 50Gi                     size of the persistent volume claim
# -rnn $BEXHOMA_NODE_SUT        schedule SUT pod on this node
# -rnl $BEXHOMA_NODE_LOAD       schedule loader pods on this node
# -rnb $BEXHOMA_NODE_BENCHMARK  schedule benchmarker pods on this node
# --set ...                     8 io threads per worker instead of 16 (template), see "Settings of Dragonfly"
bexhoma ycsb \
  -dbms Dragonfly \
  -sf 10 \
  -xwl a \
  -xtb 16384 \
  -xnbf 4 \
  -xnlf 12 \
  -nc 1 \
  -ne 1 \
  -nlp 8 \
  -nlt 64 \
  -nbp 1 \
  -nbt 128 \
  -nw 3 \
  -xop 10 \
  -m \
  -ma \
  -mc \
  -ms $BEXHOMA_MS \
  -tr \
  -ar \
  -lr 64Gi \
  -rr 64Gi \
  -rss 50Gi \
  -rnn $BEXHOMA_NODE_SUT -rnl $BEXHOMA_NODE_LOAD -rnb $BEXHOMA_NODE_BENCHMARK \
  --set "statefulset[bexhoma-worker].container[dbms].env.DFLY_proactor_threads=8" \
  run &>$LOG_DIR/docs_ycsb_dragonfly_cluster_settings.log

echo "$(date '+%Y-%m-%d %H:%M:%S') [DONE] YCSB Dragonfly cluster 3 --set proactor_threads=8  sf=10  nbp=1"


###########################################
############## Clean Folder ###############
###########################################


clean_logs
